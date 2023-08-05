use anyhow::Result;
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{
    py_types::Tensor,
    rearrange_spec::OpShape,
    symbolic_size::{SymbolicSizeConstraint, SymbolicSizeProduct},
    tensor_util::{Shape, TorchDeviceDtype},
};

use crate::{
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeComputeInfoImpl, CircuitNodeHashItems},
    circuit_utils::{child_name_with_maybe_paren, OperatorPriority},
    new_rc_unwrap, CachedCircuitInfo, CircuitNode, CircuitNodeAutoName, CircuitRc, PyCircuitBase,
    TensorEvalError,
};

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct SetSymbolicShape {
    #[pyo3(get)]
    pub node: CircuitRc,
    info: CachedCircuitInfo,
    #[pyo3(get)]
    name: Option<String>,
}

impl SetSymbolicShape {
    #[apply(new_rc_unwrap)]
    pub fn try_new(node: CircuitRc, shape: Shape, name: Option<String>) -> Result<Self> {
        let mut out = Self {
            node,
            info: Default::default(),
            name: Default::default(),
        };
        out.name = out.auto_name(name);
        out.info.shape = shape;
        out.init_info()
    }

    pub fn some_set_neq(
        node: CircuitRc,
        shape: OpShape,
        name: Option<String>,
    ) -> Result<CircuitRc> {
        assert_eq!(node.ndim(), shape.len());
        if shape
            .iter()
            .zip(node.shape())
            .all(|(&x, &s)| x.is_none() || x.unwrap() as usize == s)
        {
            return Ok(node);
        }
        let shape = shape
            .into_iter()
            .zip(node.shape())
            .map(|(x, s)| Option::from(x).unwrap_or(*s))
            .collect();
        Self::try_new(node, shape, name).map(|x| x.rc())
    }

    pub fn some_set_and_symbolic_neq(
        node: CircuitRc,
        shape: OpShape,
        name: Option<String>,
    ) -> Result<CircuitRc> {
        let shape = shape
            .into_iter()
            .zip(node.shape())
            .map(|(x, &n_s)| {
                SymbolicSizeProduct::has_symbolic(n_s)
                    .then(|| Option::from(x))
                    .flatten()
                    .into()
            })
            .collect();
        Self::some_set_neq(node, shape, name)
    }
}

circuit_node_extra_impl!(SetSymbolicShape, self_hash_default);

impl CircuitNodeComputeInfoImpl for SetSymbolicShape {
    fn compute_shape(&self) -> Shape {
        self.info().shape.clone()
    }

    fn symbolic_size_constraints_extra(&self) -> Result<Vec<SymbolicSizeConstraint>> {
        let out = self
            .node
            .shape()
            .iter()
            .zip(self.shape())
            .map(|(&in_size, &set_to)| SymbolicSizeConstraint::get_new_from(in_size, set_to))
            .collect::<Result<Vec<_>>>()?
            .into_iter()
            .filter_map(|x| x)
            .collect();
        Ok(out)
    }

    fn compute_is_explicitly_computable(&self) -> bool {
        false
    }
}

impl CircuitNodeHashItems for SetSymbolicShape {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        for i in &self.info().shape {
            hasher.update(&i.to_le_bytes());
        }
    }
}

impl CircuitNode for SetSymbolicShape {
    circuit_node_auto_impl!("25332a58-39d6-443d-b225-65c810a09aa4");

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![(0..self.rank()).map(Some).collect()]
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.node.clone())?,
            self.info().shape.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(
        &self,
        _tensors: &[Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<Tensor> {
        Err(TensorEvalError::NotExplicitlyComputableInternal {
            circuit: self.crc(),
        }
        .into())
    }
}

impl CircuitNodeAutoName for SetSymbolicShape {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            child_name_with_maybe_paren(&Self::PRIORITY, self.node.clone())
                .map(|n| n + " set_shape")
        })
    }
}

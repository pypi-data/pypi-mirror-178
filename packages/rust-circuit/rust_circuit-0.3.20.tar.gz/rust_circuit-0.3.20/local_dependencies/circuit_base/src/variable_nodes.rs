use std::collections::BTreeMap;

use anyhow::{bail, Result};
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{
    py_types::Tensor,
    sv,
    tensor_util::{Shape, TorchDeviceDtype},
};
use uuid::Uuid;

use crate::{
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeComputeInfoImpl, CircuitNodeHashItems},
    circuit_utils::{child_name_with_maybe_paren, OperatorPriority},
    new_rc, new_rc_unwrap, CachedCircuitInfo, CircuitNode, CircuitNodeAutoName, CircuitRc,
    ConstructError, PyCircuitBase, Scalar, TensorEvalError,
};

/// Tags a Circuit with a UUID. Use this to make two otherwise equal nodes distinct.
/// This is used to make two independent samplings of the random variable, whereas without making them distinct,
/// they would be references to the same samplings
///
/// - *Why is this useful?* The `probs_and_group` attribute of random variables
///   groups RVs that have the "same randomness" somehow. Usually used as the
///   `.probs_and_group` attribute of `DiscreteVar`, to prevent several uniform
///   `DiscreteVar`s with the same number of samples, from being sampled all
///   together.
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Tag {
    #[pyo3(get)]
    pub node: CircuitRc,
    #[pyo3(get)]
    pub uuid: Uuid,
    name: Option<String>,
    info: CachedCircuitInfo,
}

impl Tag {
    #[apply(new_rc)]
    pub fn new(node: CircuitRc, uuid: Uuid, name: Option<String>) -> (Self) {
        let mut out = Self {
            node,
            uuid,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info().unwrap()
    }
}

impl CircuitNodeAutoName for Tag {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            child_name_with_maybe_paren(&Self::PRIORITY, self.node.clone()).map(|n| n + " tag")
        })
    }
}

circuit_node_extra_impl!(Tag, self_hash_default);

impl CircuitNodeComputeInfoImpl for Tag {
    fn compute_shape(&self) -> Shape {
        self.node.shape().clone()
    }
}

impl CircuitNodeHashItems for Tag {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(self.uuid.as_bytes());
    }
}

impl CircuitNode for Tag {
    circuit_node_auto_impl!("63fdc4ce-2f1b-40b3-b8b6-13991b54cbd7");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![(0..self.node.info().rank()).map(Some).collect()]
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Ok(Self::new(
            f(0, self.node.clone())?,
            self.uuid,
            self.name.clone(),
        ))
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        assert_eq!(tensors.len(), 1);
        Ok(tensors[0].clone())
    }
}

#[pymethods]
impl Tag {
    #[new]
    fn py_new(
        node: CircuitRc,
        uuid: Uuid,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Tag>> {
        let out = Self::new(node, uuid, name);
        Ok(out.into_init())
    }

    /// Creates a new Tag with a random UUID.
    #[staticmethod]
    pub fn new_with_random_uuid(node: CircuitRc, name: Option<String>) -> Self {
        Self::new(node, Uuid::new_v4(), name)
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct DiscreteVar {
    #[pyo3(get)]
    pub values: CircuitRc,
    #[pyo3(get)]
    pub probs_and_group: CircuitRc,
    name: Option<String>,
    info: CachedCircuitInfo,
}

impl DiscreteVar {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        values: CircuitRc,
        probs_and_group: CircuitRc,
        name: Option<String>,
    ) -> Result<Self> {
        if probs_and_group.info().rank() != 1 {
            bail!(ConstructError::DiscreteVarProbsMustBe1d {
                shape: probs_and_group.info().shape.clone(),
            });
        }
        if values.info().rank() < 1 {
            bail!(ConstructError::DiscreteVarNoSamplesDim {});
        }
        if values.info().shape[0] != probs_and_group.info().shape[0] {
            bail!(ConstructError::DiscreteVarWrongSamplesDim {
                node: values.info().shape[0],
                probs: probs_and_group.info().shape[0],
            });
        }
        let mut out = Self {
            values,
            probs_and_group,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }

    pub fn new_for_py(
        values: CircuitRc,
        probs_and_group: Option<CircuitRc>,
        name: Option<String>,
    ) -> Result<Self> {
        if values.info().rank() < 1 {
            bail!(ConstructError::DiscreteVarNoSamplesDim {});
        }
        let probs_and_group = probs_and_group
            .unwrap_or_else(|| Self::uniform_probs_and_group(values.info().shape[0], None).rc()); // TODO: name
        Self::try_new(values, probs_and_group, name)
    }
}

impl CircuitNodeAutoName for DiscreteVar {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        // Ignores probs and groups because we almost never care about the probs and groups name
        name.or_else(|| {
            child_name_with_maybe_paren(&Self::PRIORITY, self.values.clone()).map(|n| n + " var")
        })
    }
}

circuit_node_extra_impl!(DiscreteVar, self_hash_default);

impl CircuitNodeComputeInfoImpl for DiscreteVar {
    fn compute_shape(&self) -> Shape {
        self.values.info().shape[1..].iter().cloned().collect()
    }

    fn compute_can_be_sampled(&self) -> bool {
        true
    }
    fn compute_is_constant(&self) -> bool {
        false
    }
    fn compute_is_explicitly_computable(&self) -> bool {
        false
    }
}

impl CircuitNodeHashItems for DiscreteVar {}

impl CircuitNode for DiscreteVar {
    circuit_node_auto_impl!("1bd791cd-8460-496d-8cf5-303baa3cd226");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![
            std::iter::once(None)
                .chain((0..self.info().rank()).map(Some))
                .collect(),
            vec![None],
        ]
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new([self.values.clone(), self.probs_and_group.clone()].into_iter())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.values.clone())?,
            f(1, self.probs_and_group.clone())?,
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

#[pymethods]
impl DiscreteVar {
    #[new]
    fn py_new(
        values: CircuitRc,
        probs_and_group: Option<CircuitRc>,
        name: Option<String>,
    ) -> Result<PyClassInitializer<DiscreteVar>> {
        let out = Self::new_for_py(values, probs_and_group, name)?;
        Ok(out.into_init())
    }
    #[staticmethod]
    pub fn new_uniform(values: CircuitRc, name: Option<String>) -> Result<Self> {
        Self::new_for_py(values, None, name)
    }
    #[staticmethod]
    pub fn uniform_probs_and_group(size: usize, name: Option<String>) -> Tag {
        // TODO: naming
        Tag::new_with_random_uuid(Scalar::nrc(1.0 / (size as f64), sv![size], None), name)
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct StoredCumulantVar {
    #[pyo3(get)]
    pub cumulants: BTreeMap<usize, CircuitRc>, // using btreemap so it always iterates in order
    #[pyo3(get)]
    pub uuid: Uuid,
    name: Option<String>,
    info: CachedCircuitInfo,
}

impl StoredCumulantVar {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Uuid,
        name: Option<String>,
    ) -> Result<Self> {
        if !cumulants.contains_key(&1) || !cumulants.contains_key(&2) {
            bail!(ConstructError::StoredCumulantVarNeedsMeanVariance {});
        }
        if cumulants.contains_key(&0) {
            bail!(ConstructError::StoredCumulantVarInvalidCumulantNumber { number: 0 },);
        }
        let shape = &cumulants[&1].info().shape;
        for (k, v) in cumulants.iter() {
            let shape_here: Shape = shape
                .iter()
                .cycle()
                .take(k * shape.len())
                .copied()
                .collect();
            if shape_here != v.info().shape {
                bail!(ConstructError::StoredCumulantVarCumulantWrongShape {
                    cumulant_shape: v.info().shape.clone(),
                    cumulant_number: *k,
                    base_shape: shape.clone(),
                },);
            }
        }
        let mut out = Self {
            cumulants,
            uuid,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }

    pub fn new_mv(
        mean: CircuitRc,
        variance: CircuitRc,
        higher_cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Option<Uuid>,
        name: Option<String>,
    ) -> Result<Self> {
        let mut higher_cumulants = higher_cumulants;
        higher_cumulants.insert(1, mean);
        higher_cumulants.insert(2, variance);
        Self::try_new(
            higher_cumulants,
            uuid.unwrap_or_else(|| Uuid::new_v4()),
            name,
        )
    }
}

impl CircuitNodeAutoName for StoredCumulantVar {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.cumulants.values().any(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    "StoredCumulantVar(".to_owned()
                        + &self
                            .cumulants
                            .iter()
                            .map(|(r, x)| {
                                format!("{r}: {}", Self::shorten_child_name(x.name().unwrap()))
                            })
                            .collect::<Vec<String>>()
                            .join(", ")
                        + ")",
                )
            }
        })
    }
}

circuit_node_extra_impl!(StoredCumulantVar, self_hash_default);

impl CircuitNodeComputeInfoImpl for StoredCumulantVar {
    fn compute_shape(&self) -> Shape {
        self.cumulants[&1].info().shape.clone()
    }

    fn compute_can_be_sampled(&self) -> bool {
        self.cumulants.keys().max().unwrap() <= &2
    }
    fn compute_is_constant(&self) -> bool {
        false
    }
    fn compute_is_explicitly_computable(&self) -> bool {
        false
    }
}

impl CircuitNodeHashItems for StoredCumulantVar {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        for k in self.cumulants.keys() {
            hasher.update(&k.to_le_bytes());
        }
        hasher.update(self.uuid.as_bytes());
    }
}

impl CircuitNode for StoredCumulantVar {
    circuit_node_auto_impl!("f36da959-d160-484d-b6b8-7685ef7521c0");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.cumulants
            .values()
            .map(|x| vec![None; x.info().rank()])
            .collect()
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.cumulants.values().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.cumulants
                .iter()
                .enumerate()
                .map(|(i, (k, v))| f(i, v.clone()).map(|z| (*k, z)))
                .collect::<Result<BTreeMap<_, _>, _>>()?,
            self.uuid,
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

#[pymethods]
impl StoredCumulantVar {
    #[new]
    fn py_new(
        cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Option<Uuid>,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<StoredCumulantVar>> {
        let uuid = uuid.unwrap_or_else(|| Uuid::new_v4());
        let out = Self::try_new(cumulants, uuid, name)?;
        Ok(out.into_init())
    }

    #[staticmethod]
    #[pyo3(name = "new_mv")]
    #[args(higher_cumulants = "Default::default()", uuid = "None", name = "None")]
    pub fn new_mv_py(
        mean: CircuitRc,
        variance: CircuitRc,
        higher_cumulants: BTreeMap<usize, CircuitRc>,
        uuid: Option<Uuid>,
        name: Option<String>,
    ) -> Result<Self> {
        Self::new_mv(mean, variance, higher_cumulants, uuid, name)
    }
}

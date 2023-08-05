use std::{cmp::Ordering, iter::zip};

use anyhow::{anyhow, bail, Context, Result};
use itertools::Itertools;
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use pyo3::{prelude::*, types::PyTuple};
use rr_util::{
    atr,
    rearrange_spec::RInnerInts,
    tensor_util::{IndexError, IndexTensor, TensorIndexSync},
    util::EinsumAxes,
};
use rr_util::{
    opt_einsum::EinsumSpec,
    py_types::{
        einops_repeat, einsum_py, make_diagonal_py, scalar_to_tensor, scalar_to_tensor_py,
        ExtraPySelfOps, PyEinsumAxes, Tensor, PY_CIRCUIT_ITEMS, PY_UTILS,
    },
    pycall,
    rearrange_spec::{OpSize, RearrangeSpec}, // TODO: use new rearrange spec
    sv,
    tensor_util::{
        broadcast_shapes, Slice, TensorAxisIndex, TensorIndex, TorchDeviceDtype, TorchDeviceDtypeOp,
    },
    util::{
        cumsum, dict_to_list, {hashmap_collect_except_duplicates, AxisInt},
    },
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use uuid::uuid;

use crate::{
    check_canon_axes, circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{
        CircuitNodeComputeInfoImpl, CircuitNodeHashItems, CircuitNodeHashWithChildren,
    },
    circuit_utils::{
        child_name_with_maybe_paren, children_names_with_maybe_paren, OperatorPriority,
    },
    new_rc_unwrap,
    prelude::*,
    CachedCircuitInfo, CircuitNodeSelfOnlyHash, ConstructError, PyCircuitBase, Scalar, Shape,
};

/// our Einsum supports diag output
/// this means `a->aa` is valid and produces a tensor with the input on the diagonal
/// also `aa->aa` only copies the diagonal, and ignores the rest
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Einsum {
    pub args: EinsumArgs,
    pub out_axes: EinsumAxes,
    info: CachedCircuitInfo,
    name: Option<String>,
}

circuit_node_extra_impl!(Einsum);

impl CircuitNodeComputeInfoImpl for Einsum {
    fn compute_shape(&self) -> Shape {
        let map = self.shape_map().unwrap();
        self.out_axes.iter().map(|a| *map.get(a).unwrap()).collect()
    }
}
impl CircuitNodeHashWithChildren for Einsum {
    fn compute_hash_non_name(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.out_axes);
        for (c, axes) in &self.args {
            // no need to delimit because we have hash each loop
            hasher.update(&c.info().hash);
            hasher.update(axes);
        }
    }
}
impl CircuitNodeSelfOnlyHash for Einsum {
    fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.out_axes);
        for (_c, axes) in &self.args {
            hasher.update(uuid!("3749ab7f-4f4c-4fdb-a268-af9c084e70ef").as_bytes());
            hasher.update(axes);
        }
    }
}

impl CircuitNode for Einsum {
    circuit_node_auto_impl!("ed15422c-7c02-40c2-a3c2-e9224514d063");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let out_inv: HashMap<AxisInt, usize> = hashmap_collect_except_duplicates(
            self.out_axes.iter().enumerate().map(|(i, x)| (*x, i)),
        );
        self.input_axes()
            .map(|ints| {
                ints.iter()
                    .map(|i| {
                        if ints.iter().filter(|z| *z == i).count() > 1 {
                            return None;
                        }
                        out_inv.get(i).cloned()
                    })
                    .collect()
            })
            .collect()
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.args.iter().map(|a| a.0.clone()))
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.args
                .iter()
                .enumerate()
                .map(move |(i, (circ, axes))| -> Result<_> {
                    Ok((f(i, circ.clone())?, axes.clone()))
                })
                .collect::<Result<_, _>>()?,
            self.out_axes.clone(),
            self.name.clone(),
        )
    }

    fn self_flops(&self) -> BigUint {
        self.get_spec().flops()
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            if self.args.is_empty() {
                return Ok(scalar_to_tensor_py(py, 1., sv![], device_dtype.clone())?);
            }
            let out_axes_deduped: EinsumAxes = self.out_axes.iter().unique().cloned().collect();
            let result_non_diag: Tensor = einsum_py(
                py,
                zip(tensors.iter().cloned(), self.input_axes().cloned()).collect(),
                out_axes_deduped.clone(),
            )?;

            if out_axes_deduped.len() != self.out_axes.len() {
                Ok(make_diagonal_py(
                    py,
                    &result_non_diag,
                    out_axes_deduped,
                    self.out_axes.clone(),
                )?)
            } else {
                Ok(result_non_diag)
            }
        })
    }
}

pub type EinsumArgs = Vec<(CircuitRc, EinsumAxes)>;
impl Einsum {
    pub fn input_circuits(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.args.iter().map(|(circ, _)| circ.clone()))
    }

    pub fn input_axes(&self) -> Box<dyn Iterator<Item = &EinsumAxes> + '_> {
        Box::new(self.args.iter().map(|(_, axes)| axes))
    }

    pub fn shape_map(&self) -> Result<HashMap<AxisInt, usize>> {
        let mut out = HashMap::default();
        for (circ, axes) in &self.args {
            if circ.info().rank() != axes.len() {
                bail!(ConstructError::EinsumLenShapeDifferentFromAxes {
                    len_axes: axes.len(),
                    child_len_shape: circ.info().rank(),
                    einsum_name: self.name_cloned(),
                    child_circuit: circ.clone(),
                });
            }
            for (&circuit_size, axis) in circ.info().shape.iter().zip(axes) {
                let existing_size = *out.entry(*axis).or_insert(circuit_size);
                if existing_size != circuit_size {
                    bail!(ConstructError::EinsumAxisSizeDifferent {
                        new_size: circuit_size.into(),
                        existing_size: existing_size.into(),
                        axis: *axis as usize,
                        einsum_name: self.name_cloned(),
                        child_circuit: circ.clone(),
                    });
                }
            }
        }

        Ok(out)
    }

    #[apply(new_rc_unwrap)]
    pub fn try_new(args: EinsumArgs, out_axes: EinsumAxes, name: Option<String>) -> Result<Self> {
        // TODO: reduce axes nums!
        let mut out = Self {
            args,
            out_axes,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);

        let map = out.shape_map()?; // catch errors

        for a in &out.out_axes {
            if !map.contains_key(a) {
                return Err(ConstructError::EinsumOutputNotSubset {
                    circuit_name: out.name.clone(),
                    all_input_axes: map.into_keys().collect(),
                    output_axes: out.out_axes.clone(),
                }
                .into());
            }
        }

        // could reuse hashmap if helped with perf
        out.init_info()
    }

    pub fn try_from_spec(
        spec: &EinsumSpec,
        circuits: &[CircuitRc],
        name: Option<String>,
    ) -> Result<Self> {
        // TODO: maybe check int sizes!
        assert_eq!(spec.input_ints.len(), circuits.len());
        let to_idx =
            |vals: &[usize]| -> EinsumAxes { vals.iter().map(|&x| x as AxisInt).collect() };
        Self::try_new(
            circuits
                .iter()
                .zip(&spec.input_ints)
                .map(|(c, vals)| (c.clone(), to_idx(vals)))
                .collect(),
            to_idx(&spec.output_ints),
            name,
        )
    }

    pub fn axes_in_input(&self) -> HashSet<AxisInt> {
        // could be 256 bit bitmask
        self.input_axes().flatten().copied().collect()
    }
}

impl CircuitNodeAutoName for Einsum {
    const PRIORITY: OperatorPriority = OperatorPriority::Infix { priority: 1 };

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            children_names_with_maybe_paren(&Self::PRIORITY, self.children().collect()).map(
                |names| {
                    names
                        .iter()
                        .map(|name| Self::shorten_child_name(name))
                        .collect::<Vec<String>>()
                        .join(" * ")
                },
            )
        })
    }
}

pub struct PyEinsumArgs(EinsumArgs);
impl<'source> FromPyObject<'source> for PyEinsumArgs {
    fn extract(args_obj: &'source PyAny) -> PyResult<Self> {
        let args: Vec<(CircuitRc, EinsumAxes)> = args_obj.extract()?;

        Ok(PyEinsumArgs(args.into_iter().collect()))
    }
}
impl IntoPy<PyObject> for PyEinsumArgs {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0
            .into_iter()
            .map(|(c, axes)| (c, PyEinsumAxes(axes)))
            .collect::<Vec<_>>()
            .into_py(py)
    }
}
#[pymethods]
impl Einsum {
    #[new]
    #[args(args = "*", out_axes, name)]
    fn new_py(
        args: Vec<(CircuitRc, EinsumAxes)>,
        out_axes: EinsumAxes,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Self>> {
        let out = Self::try_new(args, out_axes, name)?;

        Ok(out.into_init())
    }

    #[getter]
    fn args(&self) -> PyEinsumArgs {
        PyEinsumArgs(self.args.clone())
    }

    #[getter]
    fn out_axes(&self) -> PyEinsumAxes {
        PyEinsumAxes(self.out_axes.clone())
    }

    fn all_input_circuits(&self) -> Vec<CircuitRc> {
        self.input_circuits().collect()
    }

    fn all_input_axes(&self) -> Vec<PyEinsumAxes> {
        self.input_axes().cloned().map(PyEinsumAxes).collect()
    }

    #[staticmethod]
    pub fn from_nodes_ints(
        nodes: Vec<CircuitRc>,
        input_ints: Vec<EinsumAxes>,
        output_ints: EinsumAxes,
        name: Option<String>,
    ) -> Result<Self> {
        if nodes.len() != input_ints.len() {
            bail!(ConstructError::EinsumWrongNumChildren {
                actual_num_children: nodes.len(),
                expected_num_children_based_on_axes: input_ints.len(),
                einsum_name: name
            })
        }
        Self::try_new(zip(nodes, input_ints).collect(), output_ints, name)
    }

    #[staticmethod]
    #[args(nodes = "*", name)]
    pub fn from_einsum_string(
        string: &str,
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> Result<Self> {
        let (mut input_ints, output_ints) = EinsumSpec::string_to_ints(string.to_owned())?;
        if input_ints.len() == 1 && input_ints[0].is_empty() && nodes.len() == 0 {
            input_ints.clear()
        }
        Self::from_nodes_ints(nodes, input_ints, output_ints, name)
    }

    #[staticmethod]
    #[args(nodes = "*", name)]
    pub fn from_fancy_string(
        string: &str,
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> Result<Self> {
        let (mut input_ints, output_ints) = EinsumSpec::fancy_string_to_ints(string.to_owned())?;
        if input_ints.len() == 1 && input_ints[0].is_empty() && nodes.len() == 0 {
            input_ints.clear()
        }
        Self::from_nodes_ints(nodes, input_ints, output_ints, name)
    }

    #[staticmethod]
    #[args(nodes = "*", name)]
    pub fn from_spec_py(
        spec: EinsumSpec,
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> Result<Self> {
        Self::try_from_spec(&spec, &nodes, name)
    }

    #[staticmethod]
    pub fn new_diag(node: CircuitRc, ints: EinsumAxes, name: Option<String>) -> Self {
        let deduped = ints.iter().unique().cloned().collect();
        Einsum::try_new(vec![(node, deduped)], ints, name).unwrap()
    }

    #[staticmethod]
    pub fn new_trace(node: CircuitRc, ints: EinsumAxes, name: Option<String>) -> Self {
        let deduped = ints.iter().unique().cloned().collect();
        Einsum::try_new(vec![(node, ints)], deduped, name).unwrap()
    }

    #[staticmethod]
    pub fn scalar_mul(
        node: CircuitRc,
        scalar: f64,
        name: Option<String>,
        scalar_name: Option<String>,
    ) -> Self {
        let axes: EinsumAxes = (0..node.info().rank()).map(|x| x as u8).collect();
        Einsum::try_new(
            vec![
                (node, axes.clone()),
                (Scalar::new(scalar, sv![], scalar_name).rc(), sv![]),
            ],
            axes,
            name,
        )
        .unwrap()
    }
    #[staticmethod]
    #[args(nodes = "*")]
    pub fn elementwise_broadcasted(nodes: Vec<CircuitRc>, name: Option<String>) -> Result<Einsum> {
        let out_shape = broadcast_shapes(&nodes.iter().map(|x| x.info().shape.clone()).collect())
            .context("failed to broadcast for einsum mul")?;
        let mut prev_one_shape = out_shape.len().saturating_sub(1) as u8;
        Einsum::try_new(
            nodes
                .iter()
                .map(|node| {
                    let rank_difference = out_shape.len() - node.info().rank();
                    (
                        node.clone(),
                        node.info()
                            .shape
                            .iter()
                            .enumerate()
                            .map(|(i, l)| {
                                if *l != out_shape[i + rank_difference] {
                                    prev_one_shape += 1;
                                    prev_one_shape
                                } else {
                                    (i + rank_difference) as u8
                                }
                            })
                            .collect(),
                    )
                })
                .collect(),
            (0u8..out_shape.len() as u8).collect(),
            name,
        )
    }
    #[staticmethod]
    pub fn empty(name: Option<String>) -> Self {
        Einsum::try_new(vec![], sv![], name).unwrap()
    }

    #[staticmethod]
    pub fn identity(node: CircuitRc, name: Option<String>) -> Self {
        let axes: EinsumAxes = (0..node.info().rank()).map(|x| x as u8).collect();
        Einsum::try_new(vec![(node, axes.clone())], axes, name).unwrap()
    }

    #[staticmethod]
    pub fn new_outer_product(
        nodes: Vec<CircuitRc>,
        name: Option<String>,
        out_axes_permutation: Option<Vec<usize>>,
    ) -> Self {
        let sections: Vec<_> = nodes.iter().map(|n| n.info().rank()).collect();
        let starts = cumsum(&sections);
        let mut out_axes: EinsumAxes = nodes
            .iter()
            .enumerate()
            .flat_map(|(i, _n)| (starts[i] as u8..(starts[i] + sections[i]) as u8))
            .collect();
        if let Some(permutation) = out_axes_permutation {
            let new_out_axes = permutation.iter().map(|i| out_axes[*i]).collect();
            out_axes = new_out_axes;
        }
        Einsum::try_new(
            nodes
                .iter()
                .enumerate()
                .map(|(i, n)| {
                    (
                        n.clone(),
                        (starts[i] as u8..(starts[i] + sections[i]) as u8).collect(),
                    )
                })
                .collect(),
            out_axes,
            name,
        )
        .unwrap()
    }

    pub fn evolve(&self, args: Option<EinsumArgs>, out_axes: Option<EinsumAxes>) -> Einsum {
        Einsum::try_new(
            args.unwrap_or_else(|| self.args.clone()),
            out_axes.unwrap_or_else(|| self.out_axes.clone()),
            self.name.clone(),
        )
        .unwrap()
    }

    pub fn reduced_axes(&self) -> HashSet<u8> {
        self.input_axes()
            .flatten()
            .filter(|i| !self.out_axes.contains(i))
            .copied()
            .collect()
    }

    pub fn next_axis(&self) -> u8 {
        self.input_axes()
            .flatten()
            .max()
            .map(|x| x + 1)
            .unwrap_or(0)
    }

    pub fn get_spec(&self) -> EinsumSpec {
        let to_usize = |vals: &[u8]| -> Vec<usize> { vals.iter().map(|&x| x as usize).collect() };
        EinsumSpec {
            input_ints: self.input_axes().map(|x| to_usize(x)).collect(),
            output_ints: to_usize(&self.out_axes),
            int_sizes: dict_to_list(
                &self
                    .shape_map()
                    .unwrap()
                    .iter()
                    .map(|(key, val)| (*key as usize, *val))
                    .collect(),
                None,
            ),
        }
    }

    pub fn normalize_ints(&self) -> Einsum {
        let spec = self.get_spec();
        let spec_normalized = spec.normalize();
        Einsum::try_from_spec(
            &spec_normalized,
            &self.input_circuits().collect::<Vec<CircuitRc>>(),
            self.name_cloned(),
        )
        .unwrap()
    }
}

/// Add supports broadcasting
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Add {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Add {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, name: Option<String>) -> Result<Self> {
        // TODO: reduce axes nums!
        let mut out = Self {
            nodes,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name.clone());
        out.compute_shape_maybe()
            .with_context(|| format!("Sum isn't broadcastable name={:?}", name))?;
        out.init_info()
    }

    pub fn try_from_counts(
        nodes: &HashMap<CircuitRc, usize>,
        name: Option<String>,
    ) -> Result<Self> {
        Self::try_new(
            nodes
                .iter()
                .flat_map(|(circ, &count)| vec![circ.clone(); count])
                .collect(),
            name,
        )
    }

    fn compute_shape_maybe(&self) -> Result<Shape> {
        broadcast_shapes(&self.nodes.iter().map(|x| x.info().shape.clone()).collect())
    }
}

#[pymethods]
impl Add {
    #[new]
    #[args(nodes = "*", name = "None")]
    fn new_py(nodes: Vec<CircuitRc>, name: Option<String>) -> PyResult<PyClassInitializer<Self>> {
        let out = Self::try_new(nodes, name)?;

        Ok(out.into_init())
    }

    pub fn has_broadcast(&self) -> bool {
        !self
            .nodes
            .iter()
            .all(|node| node.info().shape == self.info().shape)
    }

    pub fn nodes_and_rank_differences(&self) -> Vec<(CircuitRc, usize)> {
        self.nodes
            .iter()
            .map(|node| (node.clone(), self.info().rank() - node.info().rank()))
            .collect()
    }

    pub fn to_counts(&self) -> HashMap<CircuitRc, usize> {
        let mut counts = HashMap::default();
        for item in &self.nodes {
            *counts.entry(item.clone()).or_insert(0) += 1;
        }

        counts
    }

    #[staticmethod]
    #[args(nodes_and_weights = "*", use_1_weights = "false", name = "None")]
    pub fn from_weighted_nodes(
        nodes_and_weights: Vec<(CircuitRc, f64)>,
        use_1_weights: bool,
        name: Option<String>,
    ) -> Result<Self> {
        let children = nodes_and_weights
            .iter()
            .map(|(node, weight)| {
                if use_1_weights || *weight != 1. {
                    Einsum::scalar_mul(node.to_owned(), *weight, None, None).rc()
                } else {
                    node.to_owned()
                }
            })
            .collect();
        Self::try_new(children, name)
    }

    #[staticmethod]
    pub fn minus(positive: CircuitRc, negative: CircuitRc, name: Option<String>) -> Result<Self> {
        positive.sub(negative, name)
    }
}

circuit_node_extra_impl!(Add, self_hash_default);

impl CircuitNodeComputeInfoImpl for Add {
    fn compute_shape(&self) -> Shape {
        self.compute_shape_maybe().unwrap() // assuming error was caught on creation, panicking now
    }
}

impl CircuitNodeHashItems for Add {}

impl CircuitNode for Add {
    circuit_node_auto_impl!("88fb29e5-c81e-47fe-ae4c-678b22994670");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.nodes_and_rank_differences()
            .iter()
            .map(|(node, rank_difference)| {
                node.info()
                    .shape
                    .iter()
                    .enumerate()
                    .map(|(i, _x)| {
                        if self.info().shape[i + rank_difference] == node.info().shape[i] {
                            Some(i + rank_difference)
                        } else {
                            None
                        }
                    })
                    .collect()
            })
            .collect()
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.name.clone(),
        )
    }

    fn self_flops(&self) -> BigUint {
        self.info.numel() * self.nodes.len()
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        if tensors.is_empty() {
            return Ok(scalar_to_tensor(0.0, sv!(), device_dtype.clone())?);
        }
        let mut out = tensors[0].clone();
        Python::with_gil(|py| {
            for tensor in tensors[1..].iter() {
                out = tensor.clone().py_add(py, out.clone()).unwrap();
            }
        });
        Ok(out)
    }
}

impl CircuitNodeAutoName for Add {
    const PRIORITY: OperatorPriority = OperatorPriority::Infix { priority: 0 };

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            children_names_with_maybe_paren(&Self::PRIORITY, self.children().collect()).map(
                |names| {
                    names
                        .iter()
                        .map(|name| Self::shorten_child_name(name))
                        .collect::<Vec<String>>()
                        .join(" + ")
                },
            )
        })
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Rearrange {
    #[pyo3(get)]
    pub node: CircuitRc,
    #[pyo3(get)]
    pub spec: RearrangeSpec,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Rearrange {
    #[apply(new_rc_unwrap)]
    pub fn try_new(node: CircuitRc, spec: RearrangeSpec, name: Option<String>) -> Result<Self> {
        // spec must be valid because we enforce that on construction!
        // TODO: reduce axes nums!
        let mut out = Self {
            node: node.clone(),
            spec,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name.clone());

        // Check that RearrangeSpec is valid for input, prevent panic on rearrange.info().shape
        out.spec
            .conform_to_input_shape(&node.info().shape)
            .with_context(|| {
                format!(
                    "{}\nname={:?}, child={:?}",
                    "rearrange spec conform_to_input_shape failed in construct rearrange",
                    name,
                    node
                )
            })?;

        // check that known sizes of each axis divide the operand shape
        let input_sizes: Vec<usize> = out
            .spec
            .input_ints
            .iter()
            .map(|x| {
                x.iter()
                    .map(|y| {
                        let s = out.spec.int_sizes[*y as usize];
                        if s.is_none() {
                            1
                        } else {
                            s.unwrap()
                        }
                    })
                    .product()
            })
            .collect();
        let any_sizes_dont_divide = node.info().shape.iter().enumerate().any(|(i, l)| {
            if input_sizes[i] == 0 {
                *l == 0
            } else {
                *l % input_sizes[i] != 0
            }
        });

        if input_sizes.len() != node.info().rank() || any_sizes_dont_divide {
            return Err(ConstructError::RearrangeWrongInputShape {
                spec: out.spec,
                shape: node.info().shape.clone(),
            }
            .into());
        }
        out.init_info()
    }

    pub fn evolve(&self, node: Option<CircuitRc>, spec: Option<RearrangeSpec>) -> Rearrange {
        Rearrange::try_new(
            node.unwrap_or_else(|| self.node.clone()),
            spec.unwrap_or_else(|| self.spec.clone()),
            self.name.clone(),
        )
        .unwrap()
    }

    pub fn nrc_elim_identity(
        node: CircuitRc,
        spec: RearrangeSpec,
        name: Option<String>,
    ) -> CircuitRc {
        if spec.is_identity() {
            node
        } else {
            Rearrange::nrc(node, spec, name)
        }
    }

    pub fn unflatten(node: CircuitRc, shape: Shape, name: Option<String>) -> Result<Self> {
        if node.ndim() != 1 {
            bail!(ConstructError::UnflattenButNDimNot1 { ndim: node.ndim() })
        }
        Ok(Rearrange::new(node, RearrangeSpec::unflatten(shape)?, name))
    }
}

circuit_node_extra_impl!(Rearrange, self_hash_default);

impl CircuitNodeComputeInfoImpl for Rearrange {
    fn compute_shape(&self) -> Shape {
        self.conform_to_input_shape_spec().shapes().unwrap().1
    }
}

impl CircuitNodeHashItems for Rearrange {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.spec.compute_hash());
    }
}

impl CircuitNode for Rearrange {
    circuit_node_auto_impl!("13204d30-2f12-4edd-8765-34bc8b458ef2");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![self
            .spec
            .input_ints
            .iter()
            .map(|ints| {
                if ints.len() != 1 {
                    return None;
                }
                self.spec.output_ints.iter().position(|z| z == ints)
            })
            .collect()]
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.node.clone())?,
            self.spec.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        // avoid using self.spec.apply so we get shape errors correctly
        let (string, letter_sizes) = self
            .conform_to_input_shape_spec()
            .to_einops_string_and_letter_sizes();
        einops_repeat(&tensors[0], string, letter_sizes)
    }

    fn intermediate_cost_bound(&self) -> usize {
        // Most rearranges are free, but some involve a copy
        //
        // Cases include:
        // 1. Flattening axes out of order: a b -> (b a) is a copy unless either dimension is a singleton
        // 2. Flattening a repeat: a -> (a 2) is a copy
        // 3. Flattening a view with an offset/repeat:
        //    * If x = ones(4,4) and y = x[:, 1:] and z = repeat(y, 'a b -> (a b)'), z is a copy
        //    * If x = ones(4) and y = repeat(x, 'a -> 2 a') and z = repeat(y, 'a b -> (a b)'), z is a copy
        //
        // Because of the third case, we cannot confirm that a rearrange returns a view
        // and has cost 0 unless we have the stride and offset of the child nodes
        //
        // Thus, for now, we always return the upper bound cost of numel. We'll explicitly
        // track and propagate strides alongside shapes later to optimize this
        if self.spec.output_ints.iter().any(|x| x.len() > 1) {
            self.info().numel_usize()
        } else {
            // some flattens / repeats dont need copy, but we'd need stride to know that
            0
        }
    }
}

impl CircuitNodeAutoName for Rearrange {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            child_name_with_maybe_paren(&Self::PRIORITY, self.node.clone())
                .map(|n| n + " rearrange")
        })
    }
}

#[pymethods]
impl Rearrange {
    #[new]
    fn new_py(
        node: CircuitRc,
        spec: RearrangeSpec,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Self>> {
        let out = Rearrange::try_new(node, spec, name)?;

        Ok(out.into_init())
    }

    #[staticmethod]
    pub fn from_string(node: CircuitRc, string: &str, name: Option<String>) -> Result<Self> {
        Rearrange::try_new(
            node,
            string
                .parse()
                .context("failed to construct spec for Rearrange::new_string")?,
            name,
        )
    }

    #[staticmethod]
    fn reshape(node: CircuitRc, shape: Shape) -> Result<Self> {
        let rank: u8 = node.info().rank().try_into().unwrap();
        let flat_rs = RearrangeSpec::flatten(rank);
        let unflat_rs = RearrangeSpec::unflatten(shape)?;

        Rearrange::try_new(
            Rearrange::try_new(node, flat_rs, None)?.rc(),
            unflat_rs,
            None,
        )
    }

    pub fn conform_to_input_shape_spec(&self) -> RearrangeSpec {
        self.spec.conform_to_input_shape(self.node.shape()).unwrap()
    }

    pub fn conform_to_input_shape(&self) -> Self {
        Rearrange::try_new(self.node.clone(), self.conform_to_input_shape_spec(), None).unwrap()
    }
}

/// Index indexes a node dimwise.
/// each axis can be Int, Slice, or 1-d tensor
/// and each 1-d tensor is iterated independently, unlike torch or numpy
/// tensor indices which are iterated together.

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Index {
    #[pyo3(get)]
    pub node: CircuitRc,
    #[pyo3(get, name = "idx")]
    pub index: TensorIndex,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Index {
    #[apply(new_rc_unwrap)]
    pub fn try_new(node: CircuitRc, index: TensorIndex, name: Option<String>) -> Result<Self> {
        let mut index = index;
        let node_rank = node.info().rank();
        match index.0.len().cmp(&node_rank) {
            Ordering::Greater => {
                bail!(IndexError::IndexRankTooHigh {
                    index_rank: index.0.len(),
                    node_rank,
                });
            }
            Ordering::Less => index.0.extend(vec![
                TensorAxisIndex::Slice(Slice {
                    start: None,
                    stop: None
                });
                node_rank - index.0.len()
            ]),
            _ => {}
        }

        let index = TensorIndex(
            index
                .0
                .into_iter()
                .map(|x| match x {
                    TensorAxisIndex::Tensor(tensor) => {
                        TensorAxisIndex::Tensor(tensor.hashed().try_into().unwrap())
                    }
                    _ => x,
                })
                .collect(),
        );

        index.validate(&node.info().shape)?;

        let mut out = Self {
            node,
            index,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }
}

circuit_node_extra_impl!(Index, self_hash_default);

impl CircuitNodeComputeInfoImpl for Index {
    fn compute_shape(&self) -> Shape {
        self.index.apply_to_shape(&self.node.info().shape)
    }

    fn device_dtype_extra(&self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + '_> {
        Box::new(self.index.0.iter().filter_map(|x| match x {
            TensorAxisIndex::Tensor(tensor) if !tensor.shape().is_empty() => {
                let mut out: TorchDeviceDtypeOp = TorchDeviceDtype::from_tensor(tensor).into();
                out.dtype = None;
                Some(out)
            }
            _ => None,
        }))
    }
}

impl CircuitNodeHashItems for Index {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.index.compute_hash());
    }
}

impl CircuitNode for Index {
    circuit_node_auto_impl!("3c655670-b352-4a5f-891c-0d7160609341");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut cur: i32 = -1;
        let result = vec![zip(&self.node.info().shape, &self.index.0)
            .map(|(l, idx)| {
                if !matches!(idx, TensorAxisIndex::Single(_)) {
                    cur += 1;
                }
                if idx.is_identity(*l) {
                    Some(cur as usize)
                } else {
                    None
                }
            })
            .collect()];
        result
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.node.clone())?,
            self.index.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        assert_eq!(tensors.len(), 1);
        Python::with_gil(|py| {
            PY_CIRCUIT_ITEMS
                .circ_compiler_util
                .getattr(py, "IndexUtil")
                .unwrap()
                .getattr(py, "apply_dimwise")
                .unwrap()
                .call(py, (tensors[0].clone(), self.index.clone()), None)
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        })
    }

    fn intermediate_cost_bound(&self) -> usize {
        // Index returns a view if all of the axis indices are not int tensors
        let has_tensor = self
            .index
            .0
            .iter()
            .any(|x| matches!(x, TensorAxisIndex::Tensor(_)));

        if has_tensor {
            // It might still return a view with int tensors in some cases, but we don't handle this
            self.info().numel_usize()
        } else {
            0
        }
    }
}

impl CircuitNodeAutoName for Index {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            child_name_with_maybe_paren(&Self::PRIORITY, self.node.clone()).map(|n| n + " idx")
        })
    }
}

#[pymethods]
impl Index {
    #[new]
    fn new_py(
        node: CircuitRc,
        index: TensorIndex,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Index>> {
        let out = Index::try_new(node, index, name)?;

        Ok(out.into_init())
    }

    // TODO: add support for synchronized index construction like python
    pub fn slice_edges_to_none(&self) -> Self {
        Index::try_new(
            self.node.clone(),
            TensorIndex(
                zip(&self.index.0, &self.node.info().shape)
                    .map(|(ax, l)| match ax {
                        TensorAxisIndex::Slice(slice) => TensorAxisIndex::Slice(Slice {
                            start: if slice.start_u(*l) == 0 {
                                None
                            } else {
                                slice.start
                            },
                            stop: if slice.stop_u(*l) == *l {
                                None
                            } else {
                                slice.stop
                            },
                        }),
                        _ => ax.clone(),
                    })
                    .collect(),
            ),
            self.name_cloned(),
        )
        .unwrap()
    }
    #[staticmethod]
    pub fn new_synchronized_to_start(
        node: CircuitRc,
        index: TensorIndexSync, // tensor index
        name: Option<String>,
    ) -> Result<Self> {
        let index: TensorIndex = index.0;
        // let broadcast_shape = broadc
        let (tensor_part_is, nontensor_part_is) = (
            (0..index.0.len() as u8)
                .filter(|i| matches!(&index.0[*i as usize], &TensorAxisIndex::Tensor(_)))
                .collect::<RInnerInts>(),
            (0..index.0.len() as u8)
                .filter(|i| !matches!(&index.0[*i as usize], &TensorAxisIndex::Tensor(_)))
                .collect::<RInnerInts>(),
        );
        if tensor_part_is.is_empty() {
            bail!(anyhow!(
                "index synchronized_to_start needs to have at least one tensor axis"
            ))
        }
        let rearranged_tensors_idxs_first = Rearrange::try_new(
            node.clone(),
            RearrangeSpec {
                input_ints: (0..index.0.len() as u8).map(|x| sv![x]).collect(),
                output_ints: std::iter::once(tensor_part_is.clone())
                    .chain(nontensor_part_is.iter().map(|x| sv![*x]))
                    .collect(),
                int_sizes: sv![OpSize::NONE;index.0.len()],
            },
            name.as_ref().map(|x| format!("{}_pre_idx_flat", x)),
        )?
        .rc();
        let tensors_index = TensorIndex(
            tensor_part_is
                .iter()
                .map(|x| index.0[*x as usize].clone())
                .collect(),
        );
        let broadcasted_tensor: IndexTensor = pycall!(
            atr!(
                pycall!(
                    atr!(
                        atr!(PY_CIRCUIT_ITEMS.circ_compiler_util, IndexUtil, raw),
                        just_join_indices_sync,
                        raw
                    ),
                    (
                        tensors_index.clone(),
                        Python::with_gil(|py| PyObject::from(PyTuple::new(
                            py,
                            tensor_part_is
                                .iter()
                                .map(|x| node.info().shape[*x as usize])
                                .collect::<Vec<_>>()
                        ))),
                        match &tensors_index.0[0] {
                            TensorAxisIndex::Tensor(t) => {
                                TorchDeviceDtype::from_tensor(t).device
                            }
                            _ => panic!(),
                        }
                    ),
                    raw
                ),
                flatten,
                raw
            ),
            ()
        );
        let indexed = Index::try_new(
            rearranged_tensors_idxs_first,
            TensorIndex(vec![TensorAxisIndex::Tensor(broadcasted_tensor)]),
            name.as_ref().map(|x| format!("{}_t_idx", x)),
        )?
        .rc();
        let broadcasted_shape = broadcast_shapes(
            &tensors_index
                .0
                .iter()
                .map(|x| match x {
                    TensorAxisIndex::Tensor(t) => t.shape().clone(),
                    _ => panic!(),
                })
                .collect(),
        )?;
        let rearranged_back = Rearrange::try_new(
            indexed,
            RearrangeSpec {
                input_ints: std::iter::once((0..broadcasted_shape.len() as u8).collect())
                    .chain(
                        (broadcasted_shape.len() as u8
                            ..broadcasted_shape.len() as u8 + nontensor_part_is.len() as u8)
                            .map(|x| sv![x]),
                    )
                    .collect(),
                output_ints: (0..broadcasted_shape.len() as u8 + nontensor_part_is.len() as u8)
                    .map(|x| sv![x])
                    .collect(),
                int_sizes: broadcasted_shape
                    .iter()
                    .map(|z| OpSize::from(Some(*z)))
                    .chain(nontensor_part_is.iter().map(|_| OpSize::NONE))
                    .collect(),
            },
            name.as_ref().map(|x| format!("{}_post_t_shape", x)),
        )?
        .rc();
        let nontensor_index: Vec<TensorAxisIndex> = nontensor_part_is
            .iter()
            .map(|i| index.0[*i as usize].clone())
            .collect();
        Index::try_new(
            rearranged_back,
            TensorIndex(
                vec![TensorAxisIndex::IDENT; broadcasted_shape.len()]
                    .into_iter()
                    .chain(nontensor_index)
                    .collect(),
            ),
            name,
        )
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Concat {
    pub nodes: Vec<CircuitRc>,
    pub axis: usize,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Concat {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, axis: usize, name: Option<String>) -> Result<Self> {
        if nodes.is_empty() {
            return Err(ConstructError::ConcatZeroNodes {}.into());
        }
        let node_shape = &nodes[0].info().shape;
        for node in nodes.iter() {
            if node.ndim() != nodes[0].ndim() {
                return Err(ConstructError::ConcatShapeDifferent {
                    shapes: nodes.iter().map(|x| x.info().shape.clone()).collect(),
                }
                .into());
            }
            for (i, s) in node.info().shape.iter().enumerate() {
                if i != axis && *s != node_shape[i] {
                    return Err(ConstructError::ConcatShapeDifferent {
                        shapes: nodes.iter().map(|x| x.info().shape.clone()).collect(),
                    }
                    .into());
                }
            }
        }

        let mut out = Self {
            nodes,
            axis,
            info: Default::default(),
            name: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }

    fn convert_axis(nodes: &[CircuitRc], axis: i64, is_stack: bool) -> Result<usize> {
        if nodes.is_empty() {
            bail!(ConstructError::ConcatZeroNodes {})
        }
        let extra = if is_stack { 1 } else { 0 };
        Ok(check_canon_axes(nodes[0].info().rank() + extra, &[axis])?[0])
    }
}

circuit_node_extra_impl!(Concat, self_hash_default);

impl CircuitNodeComputeInfoImpl for Concat {
    fn compute_shape(&self) -> Shape {
        let mut shape = self.nodes[0].info().shape.clone();
        shape[self.axis] = self.nodes.iter().map(|n| n.info().shape[self.axis]).sum();
        shape
    }
}

impl CircuitNodeHashItems for Concat {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.axis.to_le_bytes());
    }
}

impl CircuitNode for Concat {
    circuit_node_auto_impl!("f2684583-c215-4f67-825e-6e4e51091ca7");

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.axis,
            self.name.clone(),
        )
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![
            (0..self.info().rank())
                .map(|i| match i == self.axis {
                    true => None,
                    false => Some(i),
                })
                .collect();
            self.nodes.len()
        ]
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            PY_UTILS
                .torch
                .getattr(py, "cat")
                .unwrap()
                .call(py, (tensors.to_vec(), self.axis), None)
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        })
    }
}

impl CircuitNodeAutoName for Concat {
    const PRIORITY: OperatorPriority = OperatorPriority::InfixAmbiguous {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            children_names_with_maybe_paren(&Self::PRIORITY, self.children().collect()).map(
                |names| {
                    names
                        .iter()
                        .map(|name| Self::shorten_child_name(name))
                        .collect::<Vec<String>>()
                        .join(" ++ ")
                },
            )
        })
    }
}

#[pymethods]
impl Concat {
    #[new]
    #[args(nodes = "*", axis, name = "None")]
    fn new_py(
        nodes: Vec<CircuitRc>,
        axis: i64,
        name: Option<&str>,
    ) -> Result<PyClassInitializer<Concat>> {
        let axis = Self::convert_axis(&nodes, axis, false)?;
        let out = Self::try_new(nodes, axis, name.map(str::to_owned))?;
        Ok(out.into_init())
    }

    #[getter]
    fn nodes(&self) -> Vec<CircuitRc> {
        self.nodes.to_vec()
    }

    #[getter]
    fn axis(&self) -> usize {
        self.axis
    }

    pub fn get_sizes_at_axis(&self) -> Vec<usize> {
        self.nodes
            .iter()
            .map(|x| x.info().shape[self.axis])
            .collect()
    }

    #[staticmethod]
    #[args(nodes = "*", axis, name = "None")]
    pub fn stack(nodes: Vec<CircuitRc>, axis: i64, name: Option<String>) -> Result<Self> {
        let axis = Self::convert_axis(&nodes, axis, true)?;
        let to_cat = nodes
            .into_iter()
            .map(|c| {
                c.unsqueeze(
                    vec![axis],
                    c.name().map(|s| format!("{}_unsqueeze_stack", s)),
                )
                .map(|x| x.rc())
            })
            .collect::<Result<_>>()
            .context("failed to unsqueeze for stack (axis invalid?)")?;
        Self::try_new(to_cat, axis, name).context("failed to concat for stack after unsqueeze")
    }
}

/// Scatter is equivelent to:
/// result = torch.zeros(shape)
/// result[index] = node.evaluate()
/// but index is considered dimwise
///
/// right now rewrites only work with slices, maybe will support others later
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Scatter {
    #[pyo3(get)]
    pub node: CircuitRc,
    #[pyo3(get, name = "idx")]
    pub index: TensorIndex,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Scatter {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        node: CircuitRc,
        index: TensorIndex,
        shape: Shape,
        name: Option<String>,
    ) -> Result<Self> {
        let index_shape = index.apply_to_shape(&shape);
        if index.all_uslices().is_none() {
            return Err(ConstructError::ScatterIndexTypeUnimplemented { index }.into());
        }
        if index_shape[..] != node.info().shape[..] {
            return Err(ConstructError::ScatterShapeWrong {
                shape,
                index,
                index_shape,
            }
            .into());
        }

        let mut out = Self {
            node,
            index,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.info.shape = shape;
        // todo check not too many axes / oob
        out.init_info()
    }
}

circuit_node_extra_impl!(Scatter, self_hash_default);

impl CircuitNodeComputeInfoImpl for Scatter {
    fn compute_shape(&self) -> Shape {
        self.info().shape.clone()
    }
}

impl CircuitNodeHashItems for Scatter {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.index.compute_hash());
        for i in &self.info().shape {
            hasher.update(&i.to_le_bytes());
        }
    }
}

impl CircuitNode for Scatter {
    circuit_node_auto_impl!("50cce6d3-457c-4f52-9a23-1903bdc76533");

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut cur: i32 = -1;
        vec![zip(&self.info().shape, &self.index.0)
            .enumerate()
            .map(|(i, (l, idx))| {
                if !matches!(idx, TensorAxisIndex::Single(_)) {
                    cur += 1;
                }
                if idx.is_identity(*l) {
                    Some(i as usize)
                } else {
                    None
                }
            })
            .collect()]
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.node.clone())?,
            self.index.clone(),
            self.info().shape.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            PY_CIRCUIT_ITEMS
                .circ_compiler_util
                .getattr(py, "ScatterFn")
                .unwrap()
                .call(py, (self.index.clone(), self.info().shape.clone()), None)
                .unwrap()
                .call(py, (tensors[0].clone(),), None)
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        })
    }

    fn intermediate_cost_bound(&self) -> usize {
        self.info().numel_usize()
    }
}

impl CircuitNodeAutoName for Scatter {
    const PRIORITY: OperatorPriority = OperatorPriority::PostFix {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            child_name_with_maybe_paren(&Self::PRIORITY, self.node.clone()).map(|n| n + " scatter")
        })
    }
}

#[pymethods]
impl Scatter {
    #[new]
    fn new_py(
        node: CircuitRc,
        index: TensorIndex,
        shape: Shape,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Scatter>> {
        let out = Scatter::try_new(node, index, shape, name)?;

        Ok(out.into_init())
    }

    pub fn is_identity(&self) -> bool {
        self.info().shape[..] == self.node.info().shape[..] && self.index.all_uslices().is_some()
    }
}

#[pyfunction]
pub fn flat_concat(circuits: Vec<CircuitRc>) -> Result<Concat> {
    let flatteneds = circuits
        .iter()
        .map(|x| -> Result<_> {
            Ok(Rearrange::try_new(
                x.clone(),
                RearrangeSpec::flatten_usize(x.info().rank())?,
                Some("flatten".to_owned()),
            )
            .unwrap()
            .rc())
        })
        .collect::<Result<_>>()?;
    Ok(Concat::try_new(flatteneds, 0, Some("flat_concat".to_owned())).unwrap())
}

#[pyfunction]
pub fn flat_concat_back(circuits: Vec<CircuitRc>) -> Result<(Concat, Vec<CircuitRc>)> {
    let flat = flat_concat(circuits.clone())?;
    let sections = flat.get_sizes_at_axis();
    let starts = cumsum(&sections);
    let out = (
        flat.clone(),
        zip(circuits, zip(starts, sections))
            .map(|(c, (start, sec))| {
                Ok(Rearrange::nrc(
                    Index::nrc(
                        flat.crc(),
                        TensorIndex(vec![TensorAxisIndex::new_plain_slice(start, start + sec)]),
                        None,
                    ),
                    RearrangeSpec::unflatten(c.info().shape.clone())?,
                    None,
                ))
            })
            .collect::<Result<_>>()?,
    );
    Ok(out)
}

/// input is shape (batch_dims..batch_dims, conv_dims..conv_dims, in_channels)
/// filter is shape (batch_dims_broadcastable_with_input..b,out_channels, conv_dims..conv_dims, in_channels)
/// some features this API can represent aren't actually supported yet bc pytorch
/// doesn't expose all options
/// Batch dims on filter aren't supported yet
/// different padding before and after not supported yet
#[pyclass(unsendable, extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Conv {
    #[pyo3(get)]
    pub input: CircuitRc,
    #[pyo3(get)]
    pub filter: CircuitRc,
    #[pyo3(get)]
    pub stride: Vec<usize>,
    #[pyo3(get)]
    pub padding: Vec<(usize, usize)>,

    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Conv {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        input: CircuitRc,
        filter: CircuitRc,
        stride: Vec<usize>,
        padding: Vec<(usize, usize)>,
        name: Option<String>,
    ) -> Result<Self> {
        let dims = stride.len();
        if stride.len() != padding.len() {
            bail!(ConstructError::ConvStridePaddingNotFull {
                stride: stride.len(),
                padding: padding.len(),
            });
        }
        if dims > 3 {
            bail!(ConstructError::NotSupportedYet {
                string: "Conv over more than 3 dims not supported".to_owned(),
            });
        }

        let mut out = Self {
            input,
            filter,
            stride,
            padding,
            name: Default::default(),
            info: Default::default(),
        };
        out.info.shape = out.try_compute_shape()?;
        out.name = out.auto_name(name);
        // todo check not too many axes / oob
        out.init_info()
    }

    pub fn try_compute_shape(&self) -> Result<Shape> {
        let dims = self.dims();
        let input_batch_shape =
            if let Some(input_batch_rank) = self.input.info().rank().checked_sub(dims + 1) {
                Ok::<Shape, ConstructError>(
                    self.input.info().shape[..input_batch_rank]
                        .iter()
                        .cloned()
                        .collect(),
                )
            } else {
                bail!(ConstructError::ConvInputWrongShape {});
            }?;

        let filter_batch_shape =
            if let Some(filter_batch_rank) = self.filter.info().rank().checked_sub(dims + 2) {
                Ok::<Shape, ConstructError>(
                    self.input.info().shape[..filter_batch_rank]
                        .iter()
                        .cloned()
                        .collect(),
                )
            } else {
                bail!(ConstructError::ConvFilterWrongShape {});
            }?;
        let output_batch_shape =
            broadcast_shapes(&vec![input_batch_shape.clone(), filter_batch_shape.clone()])
                .context("input and filter shapes dont broadcast")?;

        if !filter_batch_shape.is_empty() {
            bail!(ConstructError::NotSupportedYet {
                string: format!(
                    "Batch dims on filter aren't supported yet, found {:?}",
                    filter_batch_shape
                ),
            });
        }
        let out_channels = self.filter.info().shape[filter_batch_shape.len()];
        let in_channels = self.filter.info().shape[self.filter.info().rank() - 1];
        if in_channels != self.input.info().shape[self.input.info().rank() - 1] {
            bail!(ConstructError::ConvInputFilterDifferentNumInputChannels {
                filter: in_channels,
                input: self.input.info().shape[self.input.info().rank() - 1],
            });
        }
        let input_conv_shape =
            &self.input.info().shape[input_batch_shape.len()..input_batch_shape.len() + dims];
        let filter_kernel_shape = &self.filter.info().shape
            [self.filter.info().rank() - dims - 1..self.filter.info().rank() - 1];
        let input_conv_shape_padded_minus_edges: Shape =
            zip(input_conv_shape, zip(&self.padding, filter_kernel_shape))
                .map(|(input_l, (padding, kernel_l))| {
                    input_l - (kernel_l - 1) + padding.0 + padding.1
                })
                .collect();
        let new_conv_shape: Shape = zip(&input_conv_shape_padded_minus_edges, &self.stride)
            .map(|(i, s)| {
                if i % s != 0 {
                    Err(ConstructError::ConvStrideMustDivide {
                        shape: input_conv_shape_padded_minus_edges
                            .iter()
                            .cloned()
                            .collect(),
                        stride: self.stride.clone(),
                    })
                    .context("hi")
                } else {
                    Ok(i / s)
                }
            })
            .collect::<Result<Shape>>()?;

        Ok(output_batch_shape
            .into_iter()
            .chain(new_conv_shape)
            .chain(std::iter::once(out_channels))
            .collect())
    }
}

circuit_node_extra_impl!(Conv, self_hash_default);

impl CircuitNodeComputeInfoImpl for Conv {
    fn compute_shape(&self) -> Shape {
        self.info().shape.clone()
    }
}
impl CircuitNodeHashItems for Conv {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        // this is ok because all looped over items are fixed len and we follow this with uuid (from children hash)
        for (i, (j, k)) in zip(&self.stride, &self.padding) {
            hasher.update(&i.to_le_bytes());
            hasher.update(&j.to_le_bytes());
            hasher.update(&k.to_le_bytes());
        }
    }
}

impl CircuitNode for Conv {
    circuit_node_auto_impl!("a329465f-a18f-4313-a2a6-51d8ebad7dd6");

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new([self.input.clone(), self.filter.clone()].into_iter())
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        // todo: this doesn't state all available axis linkings
        vec![
            (0..self.input_batch_shape().len())
                .map(Some)
                .chain(vec![
                    None;
                    self.input.info().rank()
                        - self.input_batch_shape().len()
                ])
                .collect(),
            vec![None; self.filter.info().rank()],
        ]
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.input.clone())?,
            f(1, self.filter.clone())?,
            self.stride.clone(),
            self.padding.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        pycall!(
            PY_UTILS.conv,
            (
                self.dims(),
                tensors[0].clone(),
                tensors[1].clone(),
                self.stride.clone(),
                self.padding.clone(),
            ),
            anyhow
        )
    }

    fn intermediate_cost_bound(&self) -> usize {
        self.info().numel_usize()
    }
}

impl CircuitNodeAutoName for Conv {
    const PRIORITY: OperatorPriority = OperatorPriority::Function {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            let input_name = self.input.name()?;
            let filter_name = self.filter.name()?;
            Some(format!("Conv({input_name}, {filter_name})"))
        })
    }
}

#[derive(FromPyObject)]
pub enum ConvPaddingShorthand {
    Single(usize),
    Symmetric(Vec<usize>),
    Full(Vec<(usize, usize)>),
}

impl ConvPaddingShorthand {
    pub fn expand(self, l: usize) -> Vec<(usize, usize)> {
        match self {
            ConvPaddingShorthand::Single(single) => vec![(single, single); l],
            ConvPaddingShorthand::Symmetric(sym) => sym.into_iter().map(|s| (s, s)).collect(),
            ConvPaddingShorthand::Full(full) => full,
        }
    }
}

#[pymethods]
impl Conv {
    #[new]
    #[args(groups = "1", padding = "ConvPaddingShorthand::Single(0)")]
    fn new_py(
        input: CircuitRc,
        filter: CircuitRc,
        stride: Vec<usize>,
        padding: ConvPaddingShorthand,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Conv>> {
        let padding = padding.expand(stride.len());
        let out = Conv::try_new(input, filter, stride, padding, name)?;

        Ok(out.into_init())
    }
    pub fn dims(&self) -> usize {
        self.stride.len()
    }
    pub fn input_batch_shape(&self) -> Shape {
        self.input.info().shape[..self.info().rank() - 1 - self.dims()]
            .iter()
            .cloned()
            .collect()
    }
}

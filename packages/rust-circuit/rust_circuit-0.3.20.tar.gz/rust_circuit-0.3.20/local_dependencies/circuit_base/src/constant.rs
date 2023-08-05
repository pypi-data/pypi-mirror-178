use anyhow::Result;
use base16::encode_lower;
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use pyo3::{
    prelude::*,
    types::{IntoPyDict, PyTuple},
};
use rr_util::{
    lru_cache::TensorCacheRrfs,
    py_types::{scalar_to_tensor, Tensor, PY_UTILS},
    sv,
    tensor_db::{get_tensor_prefix, save_tensor},
    tensor_util::{TorchDeviceDtype, TorchDeviceDtypeOp},
};
use rustc_hash::FxHashMap as HashMap;
use uuid::Uuid;

use crate::{
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeComputeInfoImpl, CircuitNodeHashItems},
    named_axes::set_named_axes,
    new_rc,
    prelude::*,
    CachedCircuitInfo, NamedAxes, PyCircuitBase, Shape, TensorEvalError,
};

macro_rules! compute_info_auto_leaf_impl {
    () => {
        fn compute_max_non_leaf_size(&self) -> BigUint {
            BigUint::from(0usize)
        }
    };
}

macro_rules! circuit_node_auto_leaf_impl {
    ($uuid:literal) => {
        circuit_node_auto_impl!($uuid);

        fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
            Box::new([].into_iter())
        }

        fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
            vec![]
        }

        fn map_children_enumerate<F>(&self, _f: F) -> Result<Self>
        where
            F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
        {
            Ok(self.clone())
        }
    };
}

#[pyclass(extends=PyCircuitBase, unsendable)]
#[derive(Clone)]
pub struct Array {
    #[pyo3(get)]
    pub value: Tensor,
    info: CachedCircuitInfo,
    name: Option<String>,
}

circuit_node_extra_impl!(Array, self_hash_default);

impl CircuitNodeComputeInfoImpl for Array {
    fn compute_shape(&self) -> Shape {
        self.value.shape().clone()
    }
    fn device_dtype_extra(&self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + '_> {
        Box::new(std::iter::once(
            TorchDeviceDtype::from_tensor(&self.value).into(),
        ))
    }
    compute_info_auto_leaf_impl!();
}

impl CircuitNodeHashItems for Array {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(self.value.hash().unwrap());
    }
}

impl CircuitNode for Array {
    circuit_node_auto_leaf_impl!("b2aac9d5-1bfa-4c2a-9684-e3f9ecbc1b94");

    fn eval_tensors(
        &self,
        _tensors: &[Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<Tensor> {
        Ok(self.value.clone())
    }

    fn intermediate_cost_bound(&self) -> usize {
        // Array constants are already allocated, and the compiler's caller keeps a reference to them
        // in Python, so we can't deallocate them. Thus there's no scheduling optimization we can do
        // for them.
        0
    }
}

impl Array {
    #[apply(new_rc)]
    pub fn new(value: Tensor, name: Option<String>) -> (Self) {
        let value = value.hashed();
        Self {
            value,
            name,
            info: Default::default(),
        }
        .init_info()
        .unwrap()
    }
    pub fn from_hash_prefix(
        name: Option<String>,
        hash_base16: &str,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<Self> {
        if let Some(tc) = tensor_cache {
            return tc
                .get_tensor(hash_base16.to_owned())
                .map(|value| Array::new(value, name));
        }
        get_tensor_prefix(hash_base16).map(|value| Array::new(value, name))
    }

    pub fn randn(shape: Shape) -> Self {
        Self::randn_full(shape, None, Default::default(), None)
    }

    pub fn randn_named(
        shape: Shape,
        name: Option<String>,
        device_dtype: TorchDeviceDtypeOp,
    ) -> Self {
        Self::randn_full(shape, name, device_dtype, None)
    }
}

#[pymethods]
impl Array {
    #[new]
    fn py_new(value: Tensor, name: Option<String>) -> PyClassInitializer<Self> {
        Array::new(value, name).into_init()
    }

    #[staticmethod]
    pub fn new_named_axes(value: Tensor, name: Option<String>, named_axes: NamedAxes) -> Self {
        let result = Self::new(value, name);
        set_named_axes(result, named_axes)
    }

    #[staticmethod]
    #[pyo3(name = "randn")]
    #[args(
        shape = "*",
        name = "None",
        device_dtype = "Default::default()",
        seed = "None"
    )]
    pub fn randn_full(
        shape: Shape,
        name: Option<String>,
        device_dtype: TorchDeviceDtypeOp,
        seed: Option<usize>,
    ) -> Self {
        Python::with_gil(|py| {
            if let Some(seed) = seed {
                PY_UTILS
                    .torch
                    .getattr(py, "manual_seed")
                    .unwrap()
                    .call(py, (seed,), None)
                    .unwrap();
            }

            let mut kwargs = HashMap::default();
            if let Some(dtype) = device_dtype.dtype {
                let dtype: &str = &dtype;
                kwargs.insert("dtype", PY_UTILS.torch.getattr(py, dtype).unwrap());
            }
            if let Some(device) = device_dtype.device {
                kwargs.insert("device", device.into_py(py));
            }
            Array::new(
                PY_UTILS
                    .torch
                    .getattr(py, "randn")
                    .unwrap()
                    .call(
                        py,
                        (PyTuple::new(py, shape),),
                        Some(kwargs.into_py_dict(py)),
                    )
                    .unwrap()
                    .extract(py)
                    .unwrap(),
                name,
            )
        })
    }

    pub fn save_rrfs(&self) -> Result<String> {
        save_tensor(self.value.clone(), false).map(|_| self.tensor_hash_base16())
    }

    pub fn tensor_hash_base16(&self) -> String {
        encode_lower(&self.value.hash().unwrap())
    }

    #[staticmethod]
    pub fn from_hash(name: Option<String>, hash_base16: &str) -> Result<Self> {
        get_tensor_prefix(hash_base16).map(|value| Array::new(value, name))
    }

    #[staticmethod]
    #[pyo3(name = "from_hash_prefix")]
    pub fn from_hash_prefix_py(
        name: Option<String>,
        hash_base16: &str,
        tensor_cache: Option<TensorCacheRrfs>,
    ) -> Result<Self> {
        let mut tensor_cache = tensor_cache;
        Array::from_hash_prefix(name, hash_base16, &mut tensor_cache)
    }
}

#[pyclass(extends=PyCircuitBase, unsendable)]
#[derive(Clone)]
pub struct Symbol {
    #[pyo3(get)]
    pub uuid: Uuid,
    info: CachedCircuitInfo,
    name: Option<String>,
}

circuit_node_extra_impl!(Symbol, self_hash_default);

impl CircuitNodeComputeInfoImpl for Symbol {
    fn compute_shape(&self) -> Shape {
        self.info.shape.clone() // note: assumes shape has already been initted!
    }
    fn compute_is_explicitly_computable(&self) -> bool {
        false
    }
    compute_info_auto_leaf_impl!();
}

impl CircuitNodeHashItems for Symbol {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(self.uuid.as_bytes());
        for l in &self.info.shape {
            hasher.update(&l.to_le_bytes());
        }
    }
}

impl CircuitNode for Symbol {
    circuit_node_auto_leaf_impl!("13c3ee63-76e9-4afb-8057-40309d17b458");

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

    fn intermediate_cost_bound(&self) -> usize {
        0
    }
}

impl Symbol {
    #[apply(new_rc)]
    pub fn new(shape: Shape, uuid: Uuid, name: Option<String>) -> (Self) {
        let mut out = Self {
            uuid,
            name,
            info: Default::default(),
        };
        out.info.shape = shape;
        out.init_info().unwrap()
    }
}

#[pymethods]
impl Symbol {
    #[new]
    fn py_new(shape: Shape, uuid: Uuid, name: Option<String>) -> PyClassInitializer<Self> {
        Symbol::new(shape, uuid, name).into_init()
    }

    #[staticmethod]
    pub fn new_with_random_uuid(shape: Shape, name: Option<String>) -> Self {
        Self::new(shape, Uuid::new_v4(), name)
    }
    #[staticmethod]
    pub fn new_with_none_uuid(shape: Shape, name: Option<String>) -> Self {
        Self::new(shape, Uuid::nil(), name)
    }
}

#[pyclass(extends=PyCircuitBase, unsendable)]
#[derive(Clone)]
pub struct Scalar {
    #[pyo3(get)]
    pub value: f64,
    info: CachedCircuitInfo,
    name: Option<String>,
}

circuit_node_extra_impl!(Scalar, self_hash_default);

impl CircuitNodeComputeInfoImpl for Scalar {
    fn compute_shape(&self) -> Shape {
        self.info().shape.clone() // note: assumes shape has already been initted!
    }
    compute_info_auto_leaf_impl!();
}

impl CircuitNodeHashItems for Scalar {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.value.to_le_bytes());
        for l in &self.info.shape {
            hasher.update(&l.to_le_bytes());
        }
    }
}

impl CircuitNode for Scalar {
    circuit_node_auto_leaf_impl!("78a77905-8b3f-4471-bb77-255673941fef");

    fn eval_tensors(&self, _tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Ok(scalar_to_tensor(
            self.value,
            self.info().shape.clone(),
            device_dtype.clone(),
        )?)
    }

    fn intermediate_cost_bound(&self) -> usize {
        // scalar_to_tensor builds a 1 element tensor with a stride 0 view
        1
    }
}

impl Scalar {
    #[apply(new_rc)]
    pub fn new(value: f64, shape: Shape, name: Option<String>) -> (Self) {
        let mut out = Self {
            value,
            name,
            info: Default::default(),
        };
        out.info.shape = shape;

        out.init_info().unwrap()
    }
}

#[pymethods]
impl Scalar {
    #[new]
    #[args(shape = "sv![]")]
    fn py_new(value: f64, shape: Shape, name: Option<String>) -> PyClassInitializer<Self> {
        Self::new(value, shape, name).into_init()
    }

    pub fn is_zero(&self) -> bool {
        self.value == 0.
    }

    pub fn is_one(&self) -> bool {
        self.value == 1.
    }

    pub fn evolve_shape(&self, shape: Shape) -> Self {
        Self::new(self.value, shape, self.name.clone())
    }
}

#[test]
fn test_nrc() {
    pyo3::prepare_freethreaded_python();
    let ex = Scalar::nrc(0.0, sv![1, 2], None);
    ex.print().unwrap();
}

use std::{collections::BTreeMap, fs::File, io::Write};

use itertools::Itertools;
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use smallvec::{Array, SmallVec as Sv};
use uuid::Uuid;

use crate::{
    opt_einsum::EinsumSpec,
    rearrange_spec::{OpSize, RearrangeSpec},
    tensor_db::save_tensor,
    tensor_util::{Shape, TensorAxisIndex, TensorIndex, TorchDeviceDtypeOp},
};

pub trait RustRepr {
    /// Serialize objects to Rust expression source code
    fn repr(&self) -> String;
}

impl RustRepr for bool {
    fn repr(&self) -> String {
        if *self {
            "true".to_owned()
        } else {
            "false".to_owned()
        }
    }
}
impl RustRepr for u8 {
    fn repr(&self) -> String {
        format!("{}", self)
    }
}
impl RustRepr for usize {
    fn repr(&self) -> String {
        format!("{}", self)
    }
}
impl RustRepr for i64 {
    fn repr(&self) -> String {
        format!("{}", self)
    }
}
impl RustRepr for f64 {
    fn repr(&self) -> String {
        format!("{}_f64", self)
    }
}
impl RustRepr for OpSize {
    fn repr(&self) -> String {
        format!("OpSize::from({})", Option::<usize>::from(*self).repr())
    }
}
impl RustRepr for String {
    fn repr(&self) -> String {
        format!("\"{}\".to_owned()", self)
    }
}
impl RustRepr for &str {
    fn repr(&self) -> String {
        format!("\"{}\"", self)
    }
}
impl RustRepr for Uuid {
    fn repr(&self) -> String {
        if self.is_nil() {
            "Uuid::nil()".to_owned()
        } else {
            format!("uuid!(\"{}\")", self)
        }
    }
}
impl<T: RustRepr> RustRepr for Option<T> {
    fn repr(&self) -> String {
        match self {
            Some(x) => format!("Some({})", x.repr()),
            None => "None".to_owned(),
        }
    }
}
impl<A: RustRepr, B: RustRepr> RustRepr for (A, B) {
    fn repr(&self) -> String {
        format!("({},{})", self.0.repr(), self.1.repr())
    }
}

pub fn repr_op_string(ss: &Option<String>) -> String {
    match ss {
        None => "None".to_owned(),
        Some(s) => format!("ss!(\"{}\")", s),
    }
}

impl<T: RustRepr> RustRepr for Vec<T> {
    fn repr(&self) -> String {
        let strings: Vec<String> = self.iter().map(|s| s.repr()).collect();
        format!("vec![{}]", strings.join(","))
    }
}
impl<T: Array> RustRepr for Sv<T>
where
    T::Item: RustRepr,
{
    fn repr(&self) -> String {
        let strings: Vec<String> = self.iter().map(|s| s.repr()).collect();
        format!("sv![{}]", strings.join(","))
    }
}

impl<K: RustRepr, V: RustRepr> RustRepr for HashMap<K, V> {
    fn repr(&self) -> String {
        let strings: Vec<String> = self
            .iter()
            .map(|(k, v)| format!("({},{})", k.repr(), v.repr()))
            .collect();
        format!("HashMap::from([{}])", strings.join(","))
    }
}
impl<V: RustRepr> RustRepr for HashSet<V> {
    fn repr(&self) -> String {
        format!(
            "HashSet::from([{}])",
            self.iter().map(|x| x.repr()).collect::<Vec<_>>().join(",")
        )
    }
}
impl<K: RustRepr, V: RustRepr> RustRepr for BTreeMap<K, V> {
    fn repr(&self) -> String {
        let strings: Vec<String> = self
            .iter()
            .map(|(k, v)| format!("({},{})", k.repr(), v.repr()))
            .collect();
        format!("BTreeMap::from([{}])", strings.join(","))
    }
}

impl RustRepr for RearrangeSpec {
    fn repr(&self) -> String {
        format!(
            "RearrangeSpec::new({}, {}, {})",
            self.input_ints.repr(),
            self.output_ints.repr(),
            self.int_sizes.repr()
        )
    }
}

impl RustRepr for EinsumSpec {
    fn repr(&self) -> String {
        format!(
            "EinsumSpec{{input_ints:{}, output_ints:{}, int_sizes:{}}}",
            self.input_ints.repr(),
            self.output_ints.repr(),
            self.int_sizes.repr()
        )
    }
}

impl RustRepr for TorchDeviceDtypeOp {
    fn repr(&self) -> String {
        if let (None, None) = (&self.device, &self.dtype) {
            "TorchDeviceDtypeOp::default()".to_owned()
        } else {
            format!(
                "TorchDeviceDtypeOp {{ device: {}, dtype: {} }}",
                self.device.repr(),
                self.dtype.repr(),
            )
        }
    }
}

pub struct ReprWrapper(pub String);

impl RustRepr for ReprWrapper {
    fn repr(&self) -> String {
        self.0.clone()
    }
}

impl TensorAxisIndex {
    pub fn repr(
        &self,
        bound: usize,
        device_dtype: &TorchDeviceDtypeOp,
        tensors_as_randn: bool,
    ) -> String {
        match self {
            TensorAxisIndex::Single(i) => format!("TensorAxisIndex::Single({})", i),
            TensorAxisIndex::Tensor(t) => {
                if tensors_as_randn {
                    format!(
                        "TensorAxisIndex::new_tensor_randint_seeded({}, {}, {}, {})",
                        t.shape()[0].repr(),
                        bound.repr(),
                        device_dtype.repr(),
                        t.hash_usize().unwrap(),
                    )
                } else {
                    save_tensor((**t).clone(), false).unwrap();
                    let hash_base16: &str = &t.hashed().hash_base16().unwrap();
                    format!(
                        "TensorAxisIndex::Tensor(tensor_from_hash({}).unwrap())",
                        hash_base16.repr()
                    )
                }
            }
            TensorAxisIndex::Slice(s) => format!(
                "TensorAxisIndex::Slice(Slice {{ start:{}, stop:{} }})",
                s.start.repr(),
                s.stop.repr()
            ),
        }
    }
}

impl TensorIndex {
    pub fn repr(
        &self,
        shape: Shape,
        device_dtype: &TorchDeviceDtypeOp,
        tensors_as_randn: bool,
    ) -> String {
        // shape: shape of the tensor we're indexing into
        format!(
            "TensorIndex ( vec![{}] )",
            self.0
                .iter()
                .enumerate()
                .map(|(i, tensor_axis_index)| tensor_axis_index.repr(
                    shape[i],
                    device_dtype,
                    tensors_as_randn
                ))
                .collect::<Vec<String>>()
                .join(", ")
        )
    }
}

#[allow(unused)]
pub fn rustfmt_string(string: &str) -> String {
    // writing file bc dumb
    let templated = format!("fn main(){{\n{}\n}}", string);
    let tempfilename = "/tmp/rustfmt_string_temp";
    let mut tempfile = File::create(tempfilename).unwrap();
    tempfile.write(templated.as_bytes()).unwrap();
    let tempfile = File::open(tempfilename).unwrap();
    String::from_utf8(
        std::process::Command::new("rustfmt")
            .args(["--config", "max_width=130"])
            .stdin(tempfile)
            .output()
            .unwrap()
            .stdout,
    )
    .unwrap()
    .lines()
    .dropping(1)
    .dropping_back(1)
    .map(|x| x.strip_prefix("    ").unwrap())
    .join("\n")
}

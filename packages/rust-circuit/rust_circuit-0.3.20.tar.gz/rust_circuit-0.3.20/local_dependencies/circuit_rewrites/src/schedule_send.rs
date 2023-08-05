// temporary schedule sending setup
use anyhow::Result;
use circuit_base::{parsing::Parser, print::PrintOptions, CircuitNode, IrreducibleNode, Scalar};
use miniserde::{json, Deserialize, Serialize};
use pyo3::{prelude::*, types::PyByteArray};
use rr_util::{
    lru_cache::TensorCacheRrfs,
    py_types::{un_flat_concat, Tensor, PY_UTILS},
    pycall, sv,
    tensor_util::{Shape, TorchDeviceDtype},
};
use rustc_hash::FxHashMap as HashMap;

use crate::scheduled_execution::{get_children_keys, Instruction, Schedule};

#[pyclass]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct InstructionToSend {
    variant: String,
    key: usize,
    info: String,
    children: Vec<usize>,
}

#[pyclass]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ScheduleToSend {
    pub instructions: Vec<InstructionToSend>,
    pub constants: ::std::collections::HashMap<usize, String>,
    pub scalars: ::std::collections::HashMap<usize, String>,
    pub dtype: String,
    pub output_circuit: (usize, Vec<usize>),
    pub split_shapes: Option<Vec<Vec<usize>>>,
    pub old_constant_hashes: Vec<(Vec<u8>, usize)>,
}

#[pymethods]
impl ScheduleToSend {
    pub fn evaluate_remote(&self, remote_url: String, device: String) -> Option<Tensor> {
        let self_string = json::to_string(&self);
        let response = ureq::post(&remote_url).send_string(&self_string).unwrap();
        let mut body: Vec<u8> = vec![];
        // dbg!(&response);
        response.into_reader().read_to_end(&mut body).unwrap();
        let body_pybytes: PyObject =
            Python::with_gil(|py| PyByteArray::new(py, &body).clone().into());
        let out_shape = self.output_circuit.1.clone();
        let count: usize = out_shape.iter().product();
        pycall!(
            PY_UTILS.tensor_from_bytes,
            (
                TorchDeviceDtype {
                    dtype: self.dtype.clone(),
                    device
                },
                out_shape,
                body_pybytes,
                count,
            )
        )
    }
    pub fn evaluate_remote_many(&self, remote_url: String, device: String) -> Option<Vec<Tensor>> {
        self.evaluate_remote(remote_url, device).map(|tensor| {
            un_flat_concat(
                &tensor,
                self.split_shapes
                    .clone()
                    .unwrap()
                    .iter()
                    .map(|y| y.iter().cloned().collect())
                    .collect(),
            )
            .unwrap()
        })
    }
}

impl ScheduleToSend {
    pub fn load(self, device: String, cache: &mut Option<TensorCacheRrfs>) -> Result<Schedule> {
        let mut result = Schedule {
            instructions: vec![],
            constants: Default::default(),
            scalars: Default::default(),
            device_dtype: TorchDeviceDtype {
                device,
                dtype: self.dtype,
            },
            output_circuit: Some((self.output_circuit.0, Scalar::nrc(0.0, sv![], None))),
            split_shapes: self
                .split_shapes
                .map(|z| z.iter().map(|z| z.iter().cloned().collect()).collect()),
            old_constant_hashes: self
                .old_constant_hashes
                .iter()
                .map(|(b, i)| {
                    (
                        b.iter().cloned().collect::<Vec<_>>().try_into().unwrap(),
                        *i,
                    )
                })
                .collect(),
        };

        let parser = Parser::default();
        let mut shapes: HashMap<usize, Shape> = <HashMap<usize, Shape> as Default>::default();
        result.constants = self
            .constants
            .iter()
            .map(|(k, v)| {
                let parsed = parser.parse_circuit(&v, cache)?;
                shapes.insert(*k, parsed.info().shape.clone());
                let irreducible: Option<IrreducibleNode> = (**parsed).clone().into();
                Ok((*k, irreducible.unwrap()))
            })
            .collect::<Result<_>>()?;
        result.scalars = self
            .scalars
            .iter()
            .map(|(k, v)| {
                Ok((*k, {
                    let resulty = parser
                        .parse_circuit(&v, cache)?
                        .as_scalar()
                        .unwrap()
                        .clone();
                    shapes.insert(*k, resulty.info().shape.clone());
                    resulty
                }))
            })
            .collect::<Result<_>>()?;
        result.instructions = self
            .instructions
            .iter()
            .map(|ins| {
                let v: &str = &ins.variant;
                match v {
                    "Drop" => Ok(Instruction::Drop(ins.key)),
                    "Compute" => Ok(Instruction::Compute(ins.key, {
                        let result = parser.parse_circuit(&ins.info, cache)?;
                        shapes.insert(ins.key, result.info().shape.clone());
                        result
                    })),
                    _ => {
                        panic!()
                    }
                }
            })
            .collect::<Result<Vec<Instruction>>>()?;
        Ok(result)
    }
}

impl TryFrom<&Schedule> for ScheduleToSend {
    type Error = anyhow::Error;

    fn try_from(x: &Schedule) -> Result<Self, Self::Error> {
        fn options() -> PrintOptions {
            PrintOptions {
                shape_only_when_necessary: false,
                ..PrintOptions::default()
            }
            .validate_ret()
            .unwrap()
        }

        fn map_to_str<N: CircuitNode + Clone>(
            map: &HashMap<usize, N>,
        ) -> Result<std::collections::HashMap<usize, String>> {
            let options = options();
            map.iter()
                .map(|(k, v)| Ok((*k, options.repr(v.crc())?)))
                .collect::<Result<_>>()
        }

        let options = options();

        let out = Self {
            instructions: x
                .instructions
                .iter()
                .map(|i| {
                    let out = match i {
                        Instruction::Compute(key, circ) => InstructionToSend {
                            key: *key,
                            variant: "Compute".to_owned(),
                            info: options.repr(circ.clone())?,
                            children: get_children_keys(circ.clone()),
                        },
                        Instruction::Drop(key) => InstructionToSend {
                            key: *key,
                            variant: "Drop".to_owned(),
                            info: "".to_owned(),
                            children: vec![],
                        },
                    };
                    Ok(out)
                })
                .collect::<Result<_>>()?,
            constants: map_to_str(&x.constants)?,
            scalars: map_to_str(&x.scalars)?,
            dtype: x.device_dtype.dtype.clone(),
            output_circuit: (
                x.output_circuit.clone().unwrap().0,
                x.output_circuit
                    .clone()
                    .unwrap()
                    .1
                    .info()
                    .shape
                    .iter()
                    .cloned()
                    .collect(),
            ),
            split_shapes: x
                .split_shapes
                .clone()
                .map(|z| z.iter().map(|y| y.iter().cloned().collect()).collect()),
            old_constant_hashes: x
                .old_constant_hashes
                .iter()
                .map(|(b, i)| (b.iter().cloned().collect::<Vec<_>>(), *i))
                .collect(),
        };
        Ok(out)
    }
}

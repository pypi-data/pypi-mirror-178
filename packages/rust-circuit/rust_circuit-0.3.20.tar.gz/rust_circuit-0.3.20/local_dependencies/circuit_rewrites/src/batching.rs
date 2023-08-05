use std::collections::BTreeMap;

use anyhow::{bail, Result};
use circuit_base::{
    deep_map_op, deep_map_unwrap,
    named_axes::{axis_of_name, get_axis_leaves, set_named_axes},
    prelude::*,
    visit_circuit_unwrap, visit_circuit_with_parents, Concat, Einsum, Index, Module, ModuleArgSpec,
    ModuleSpec, Symbol,
};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*};
use rr_util::{
    python_error_exception,
    set_cover::set_cover,
    tensor_util::{TensorAxisIndex, TensorIndex},
    util::EinsumAxes,
};
use thiserror::Error;

use crate::{
    algebraic_rewrite::einsum_nest_optimize,
    circuit_optimizer::{OptimizationContext, OptimizationSettings},
};

#[pyfunction]
pub fn batch_to_concat(circuit: CircuitRc, axis: usize, num_batches: usize) -> Result<CircuitRc> {
    let l = circuit.info().shape[axis];
    if l % num_batches != 0 {
        bail!(BatchError::NumberDoesntDivide { l, num_batches });
    }
    let batch_size = l / num_batches;
    let circuit = deep_map_unwrap(circuit, |x| {
        x.as_index()
            .map(|x| Index::slice_edges_to_none(x).rc())
            .unwrap_or(x.clone())
    });

    let (name, circuit, leaves_axis, leaves_non_axis) = get_axis_leaves(circuit, axis, true)?;
    // println!("leaves axis");
    // for (k, v) in &leaves_axis {
    //     println!("{}", v);
    //     k.print();
    // }
    // println!("leaves non axis");
    // for k in &leaves_non_axis {
    //     k.print();
    // }
    let input_specs_axis: Vec<(CircuitRc, ModuleArgSpec)> = leaves_axis
        .iter()
        .map(|(sub, i)| {
            (
                sub.clone(),
                ModuleArgSpec {
                    symbol: set_named_axes(
                        Symbol::new_with_random_uuid(sub.info().shape.clone(), None),
                        BTreeMap::from([(*i as u8, name.clone())]),
                    ),
                    ban_non_symbolic_size_expand: false, // I think this needs to be false?
                    ..Default::default()
                },
            )
        })
        .collect();
    let input_specs: Vec<(CircuitRc, ModuleArgSpec)> = input_specs_axis
        .iter()
        .cloned()
        .chain(leaves_non_axis.iter().map(|sub| {
            (
                sub.clone(),
                ModuleArgSpec {
                    symbol: Symbol::new_with_random_uuid(sub.info().shape.clone(), None),
                    ban_non_symbolic_size_expand: false, // I think this needs to be false?
                    ..Default::default()
                },
            )
        }))
        .collect();
    // println!("input_specs");
    // for is in &input_specs {
    //     is.0.print();
    // }
    if input_specs.is_empty() {
        bail!(BatchError::AxisOriginatesTooHigh {});
    }
    let check_all_args_present = false; // this really should be true - get_axis_leaves doesn't get leaves!
    let module_spec = ModuleSpec::new_extract(
        circuit.clone(),
        input_specs.clone(),
        check_all_args_present,
        false,
    )
    .unwrap();
    // println!("module spec");
    // module_spec.spec_circuit.print();
    let module_spec = module_spec.resize(
        module_spec
            .arg_specs
            .iter()
            .map(|inp_spec| {
                if let Some((c, _is)) = input_specs_axis
                    .iter()
                    .find(|(_c, spec)| spec.symbol.uuid == inp_spec.symbol.uuid)
                {
                    let mut result = c.info().shape.clone();
                    result[leaves_axis[c]] = batch_size;
                    return result;
                }
                inp_spec.symbol.info().shape.clone()
            })
            .collect(),
    )?;
    // println!("module spec after resize");
    // module_spec.spec_circuit.print();
    let concattands: Vec<CircuitRc> = (0..num_batches)
        .map(|i| {
            let new_nodes: Vec<CircuitRc> = module_spec
                .arg_specs
                .iter()
                .map(|inp_spec| {
                    if let Some((c, _is)) = input_specs_axis
                        .iter()
                        .find(|z| z.1.symbol.uuid == inp_spec.symbol.uuid)
                    {
                        return Index::nrc(
                            c.clone(),
                            TensorIndex::new_single(
                                TensorAxisIndex::new_plain_slice(
                                    i * batch_size,
                                    (i + 1) * batch_size,
                                ),
                                leaves_axis[c],
                                c.info().rank(),
                            ),
                            None,
                        );
                    }
                    input_specs
                        .iter()
                        .find(|(_c, s)| s.symbol.uuid == inp_spec.symbol.uuid)
                        .unwrap()
                        .0
                        .clone()
                })
                .collect();

            // println!("module args");
            // for c in new_nodes.iter() {
            //     c.print();
            // }
            Module::nrc(new_nodes, module_spec.clone(), None)
        })
        .collect();
    let result = Concat::nrc(concattands, axis, None);
    if result.info().shape != circuit.info().shape {
        println!(
            "shapes not equal {:?} {:?}",
            result.info().shape,
            circuit.info().shape
        );
        println!("old");
        circuit.printu();
        println!("new");
        result.printu();
        panic!();
    }
    Ok(result)
}

#[apply(python_error_exception)]
#[base_error_name(Batch)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum BatchError {
    #[error("num_batches {num_batches} doesn't divide length {l} ({e_name})")]
    NumberDoesntDivide { l: usize, num_batches: usize },

    #[error("Would need to batch multiple axes, only supports one ({e_name})")]
    RequiresMultipleAxes {},

    #[error("Batching axis originates too high ({e_name})")]
    AxisOriginatesTooHigh {},
}

#[pyfunction]
#[pyo3(name = "batch_einsum")]
pub fn batch_einsum_py(einsum: Einsum, settings: OptimizationSettings) -> Result<CircuitRc> {
    batch_einsum(
        &einsum,
        &mut OptimizationContext::new_settings_circuit(settings, einsum.crc()),
    )
}

pub fn batch_einsum(einsum: &Einsum, context: &mut OptimizationContext) -> Result<CircuitRc> {
    let max_single_mem = context.cache.max_single_tensor_numel;
    assert!(einsum.info().numel_usize() <= max_single_mem);

    let mut no_memory_limit_context: OptimizationContext = Default::default();
    no_memory_limit_context.cache.max_single_tensor_numel = usize::MAX;
    // use named axes to record the ints used in intermediate einsums
    let einsum_args_named_axes: Vec<(CircuitRc, EinsumAxes)> = einsum
        .args
        .iter()
        .enumerate()
        .map(|(i, (c, ints))| {
            (
                set_named_axes(
                    Symbol::new_with_random_uuid(c.info().shape.clone(), Some(i.to_string())),
                    ints.iter()
                        .enumerate()
                        .map(|(i, int)| (i as u8, int.to_string()))
                        .collect(),
                )
                .rc(),
                ints.clone(),
            )
        })
        .collect();
    let einsum_named_axes = Einsum::try_new(
        einsum_args_named_axes.clone(),
        einsum.out_axes.clone(),
        einsum.name_cloned(),
    )
    .unwrap();
    let nested_big =
        einsum_nest_optimize(&einsum_named_axes, &mut no_memory_limit_context).unwrap();

    let mut intermediates_above_mem = vec![];
    visit_circuit_unwrap(nested_big.crc(), |c| {
        if c.info().numel_usize() > max_single_mem {
            intermediates_above_mem.push(c);
        }
    });
    assert!(!intermediates_above_mem.is_empty());
    // get the set cover of axes to batch
    let mut covers: Vec<u128> = vec![0; 64];
    for (i, intermediate) in intermediates_above_mem.iter().enumerate() {
        for (_, v) in &intermediate.info().named_axes {
            let int = v.parse::<usize>().unwrap();
            let v = covers[int] | 1 << i;
            covers[int] = v
        }
    }
    let ints_needed = set_cover(&covers);
    if ints_needed.len() != 1 {
        bail!(BatchError::RequiresMultipleAxes {});
    }

    let batch_int = ints_needed[0];
    let batch_str = batch_int.to_string();

    let batch_int_len = einsum.shape_map().unwrap()[&(batch_int as u8)];
    let max_interm_mem = intermediates_above_mem
        .iter()
        .map(|x| x.info().numel_usize())
        .max()
        .unwrap();
    let mut num_batches = ((max_interm_mem as f64) / (max_single_mem as f64)) as usize;
    while batch_int_len % num_batches != 0 {
        num_batches += 1;
    }

    let mut batchheads: Vec<CircuitRc> = vec![];
    visit_circuit_with_parents(nested_big.crc(), |x, parents| {
        if x.info().named_axes.values().any(|n| n == &batch_str)
            && !parents
                .iter()
                .any(|p| p.info().named_axes.values().any(|n| n == &batch_str))
        {
            batchheads.push(x);
        }
    });
    let batchheads_from: Vec<CircuitRc> = batchheads
        .iter()
        .map(|c| {
            batch_to_concat(c.clone(), axis_of_name(c, &batch_str).unwrap(), num_batches).unwrap()
        })
        .collect();
    let out_still_symbols = deep_map_op(nested_big.crc(), |c| {
        if let Some(p) = batchheads
            .iter()
            .position(|bh| c.info().hash == bh.info().hash)
        {
            return Some(batchheads_from[p].clone());
        }
        None
    })
    .unwrap();
    let out = deep_map_op(out_still_symbols, |c| {
        if let Some(sym) = c.as_symbol() && let Some(p) = einsum_args_named_axes
            .iter()
            .position(|(s, _ints)| sym.uuid==s.as_symbol().unwrap().uuid)
        {
            return Some(einsum.args[p].0.clone());
        }
        None
    })
    .unwrap();
    Ok(out)
}

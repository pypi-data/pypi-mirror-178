use std::collections::HashMap;

use circuit_base::{deep_map_op, deep_map_op_context, prelude::*, Add, Einsum, Index, Rearrange};
use pyo3::prelude::*;

use crate::circuit_optimizer::OptimizationContext;

/// takes circuitrc bc convenient
pub fn numel_sort_key(node: &CircuitRc) -> Vec<u8> {
    (usize::MAX - node.info().numel().to_u64_digits()[0] as usize)
        .to_be_bytes()
        .iter()
        .copied()
        .chain(node.variant_string().bytes())
        .chain(node.info().hash)
        .collect::<Vec<u8>>()
}

#[pyfunction]
#[pyo3(name = "canonicalize_node")]
pub fn canonicalize_node_py(circuit: CircuitRc) -> CircuitRc {
    canonicalize_node_op(circuit.clone()).unwrap_or(circuit)
}

pub fn canonicalize_node_op(circuit: CircuitRc) -> Option<CircuitRc> {
    match &**circuit {
        Circuit::Rearrange(rearrange) => Some(Rearrange::nrc(
            rearrange.node.clone(),
            rearrange
                .spec
                .conform_to_input_shape(&rearrange.node.info().shape)
                .unwrap()
                .canonicalize(true),
            circuit.name_cloned(),
        )),
        Circuit::Index(index) => Some(Index::nrc(
            index.node.clone(),
            index.index.canonicalize(&index.node.info().shape),
            index.name_cloned(),
        )),
        Circuit::Add(add) => {
            let mut nodes_sorted = add.nodes.clone();
            nodes_sorted.sort_by_key(numel_sort_key);
            Some(Add::nrc(nodes_sorted, add.name_cloned()))
        }
        Circuit::Einsum(einsum) => {
            let mut args_sorted = einsum.args.clone();
            args_sorted.sort_by_key(|(node, _ints)| numel_sort_key(node));
            Some(
                Einsum::try_new(args_sorted, einsum.out_axes.clone(), einsum.name_cloned())
                    .unwrap()
                    .normalize_ints()
                    .rc(),
            )
        }
        _ => None,
    }
}

#[pyfunction]
#[pyo3(name = "deep_canonicalize")]
pub fn deep_canonicalize_py(circuit: CircuitRc) -> CircuitRc {
    deep_canonicalize(circuit, &mut Default::default())
}

pub fn deep_canonicalize(circuit: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        circuit.clone(),
        &|x, _c: &mut HashMap<(), ()>| canonicalize_node_op(x),
        &mut HashMap::<(), ()>::new(),
        &mut context.cache.canonicalized,
    )
    .unwrap_or(circuit)
}

#[pyfunction]
#[pyo3(name = "canonicalize_node")]
pub fn normalize_node_py(circuit: CircuitRc) -> CircuitRc {
    normalize_node_op(circuit.clone()).unwrap_or(circuit)
}

pub fn normalize_node_op(circuit: CircuitRc) -> Option<CircuitRc> {
    match &**circuit {
        Circuit::Rearrange(rearrange) => Some(Rearrange::nrc(
            rearrange.node.clone(),
            rearrange.spec.canonicalize(false),
            circuit.name_cloned(),
        )),
        Circuit::Einsum(einsum) => Some(einsum.normalize_ints().rc()),
        _ => None,
    }
}

#[pyfunction]
pub fn deep_normalize(circuit: CircuitRc) -> CircuitRc {
    deep_map_op(circuit.clone(), normalize_node_op).unwrap_or(circuit)
}

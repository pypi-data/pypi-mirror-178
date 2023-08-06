use anyhow::{Context, Result};
use circuit_base::{CircuitNode, CircuitRc, Module, ModuleArgSpec, ModuleSpec};
use circuit_rewrites::module_rewrite::extract_rewrite_raw;
use get_update_node::IterativeMatcherRc;
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyRuntimeError, prelude::*, PyObject};
use rr_util::{pycall, python_error_exception};
use thiserror::Error;

#[pyfunction(
    prefix_to_strip = "None",
    module_name = "None",
    check_all_args_present = "true",
    check_unique_arg_names = "true",
    circuit_to_arg_spec = "None"
)]
pub fn extract_rewrite(
    circuit: CircuitRc,
    matcher: IterativeMatcherRc,
    prefix_to_strip: Option<String>,
    module_name: Option<String>,
    check_all_args_present: bool,
    check_unique_arg_names: bool,
    circuit_to_arg_spec: Option<PyObject>,
) -> Result<Module> {
    let edges: Vec<CircuitRc> = matcher.get(circuit.clone(), false)?.into_iter().collect();
    let mut specs: Vec<(CircuitRc, ModuleArgSpec)> = edges
        .into_iter()
        .map(|n| {
            if let Some(cts) = &circuit_to_arg_spec {
                pycall!(cts, (n.clone(),), anyhow)
            } else {
                Ok(ModuleArgSpec::just_name_shape(n.clone(), true, true, false))
            }
            .map(|z| (n, z))
        })
        .collect::<Result<Vec<_>>>()?;
    specs.sort_by_key(|x| x.1.symbol.name_cloned());
    extract_rewrite_raw(
        circuit,
        specs,
        prefix_to_strip,
        module_name,
        check_all_args_present,
        check_unique_arg_names,
    )
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct BindItem {
    #[pyo3(get, set)]
    pub matcher: IterativeMatcherRc,
    #[pyo3(get, set)]
    pub input_circuit: CircuitRc,
    #[pyo3(get, set)]
    pub batchable: bool,
    #[pyo3(get, set)]
    pub expandable: bool,
    #[pyo3(get, set)]
    pub ban_non_symbolic_size_expand: bool,
}

#[pymethods]
impl BindItem {
    #[new]
    #[args(
        batchable = "ModuleArgSpec::default().batchable",
        expandable = "ModuleArgSpec::default().expandable",
        ban_non_symbolic_size_expand = "ModuleArgSpec::default().ban_non_symbolic_size_expand"
    )]
    fn new(
        matcher: IterativeMatcherRc,
        input_circuit: CircuitRc,
        batchable: bool,
        expandable: bool,
        ban_non_symbolic_size_expand: bool,
    ) -> Self {
        Self {
            matcher,
            input_circuit,
            batchable,
            expandable,
            ban_non_symbolic_size_expand,
        }
    }
}

impl Binder {
    fn into_item(self) -> BindItem {
        match self {
            Self::Tup(matcher, input_circuit) => BindItem {
                matcher,
                input_circuit,
                batchable: ModuleArgSpec::default().batchable,
                expandable: ModuleArgSpec::default().expandable,
                ban_non_symbolic_size_expand: ModuleArgSpec::default().ban_non_symbolic_size_expand,
            },
            Self::Item(item) => item,
        }
    }
}

#[derive(Debug, FromPyObject)]
pub enum Binder {
    Tup(IterativeMatcherRc, CircuitRc),
    Item(BindItem),
}

#[pyfunction(binders = "*", check_unique_arg_names = "true", name = "None")]
pub fn module_new_bind(
    spec_circuit: CircuitRc,
    binders: Vec<Binder>,
    check_unique_arg_names: bool,
    name: Option<String>,
) -> Result<Module> {
    let (nodes, arg_specs) = binders
        .into_iter()
        .map(|binder| {
            let BindItem {
                matcher,
                input_circuit,
                batchable,
                expandable,
                ban_non_symbolic_size_expand,
            } = binder.into_item();
            let matched_circuit =
                matcher
                    .get_unique(spec_circuit.clone(), false)
                    .context(format!(
                        "failed to get unique for matcher={} in bind",
                        *matcher
                    ))?;

            let symbol = matched_circuit.as_symbol().cloned().ok_or_else(|| {
                ModuleBindError::ExpectedSymbol {
                    matched_circuit,
                    matcher,
                    spec_circuit: spec_circuit.clone(),
                }
            })?;

            Ok((
                input_circuit,
                ModuleArgSpec {
                    symbol,
                    batchable,
                    expandable,
                    ban_non_symbolic_size_expand,
                },
            ))
        })
        .collect::<Result<Vec<_>>>()?
        .into_iter()
        .unzip();

    Module::try_new(
        nodes,
        ModuleSpec::new(spec_circuit, arg_specs, true, check_unique_arg_names)?,
        name,
    )
}

#[apply(python_error_exception)]
#[base_error_name(ModuleBind)]
#[base_exception(PyRuntimeError)]
#[derive(Error, Debug, Clone)]
pub enum ModuleBindError {
    #[error("expected to match symbol, matched_circuit={matched_circuit:?}\nfor matcher={matcher:?}\nspec_circuit={spec_circuit:?}\n({e_name})")]
    ExpectedSymbol {
        matched_circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        spec_circuit: CircuitRc,
    },
}

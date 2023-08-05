use std::io::prelude::*;

use anyhow::{bail, Context, Result};
use circuit_base::{
    flat_concat, get_compatible_dtype, module::conform_all_modules, print::PrintOptions,
    CircuitNode, CircuitRc, ModuleSpec,
};
use num_bigint::BigUint;
use pyo3::prelude::*;
use rr_util::{
    opt_einsum::EinsumSpec,
    py_types::Tensor,
    python_println,
    repr::RustRepr,
    tensor_util::Shape,
    timed,
    util::{apply_fn_until_same, HashBytes},
};
use rustc_hash::FxHashMap as HashMap;

use crate::{
    canonicalize::deep_canonicalize,
    compiler_heuristics::deep_maybe_distribute,
    compiler_strip::{remove_autotags, strip_names},
    deep_rewrite::{
        compiler_simp, deep_heuristic_nest_adds, deep_optimize_einsums, deep_push_down_index_raw,
    },
    scheduled_execution::{
        circuit_to_schedule, circuit_to_schedule_naive_toposort, Schedule, SchedulingError,
    },
};

// a lot of the function boundries in this are there because it would be too hard to optimize things jointly
// not because we don't need to optimize things jointly
// like scheduling does impact whether you should distribute, but using that info would be
// difficult

#[pyclass]
#[derive(Debug, Clone, Copy)]
pub struct OptimizationSettings {
    #[pyo3(get, set)]
    pub verbose: usize,
    #[pyo3(get, set)]
    pub max_memory: usize,
    #[pyo3(get, set)]
    pub max_single_tensor_memory: usize,
    #[pyo3(get, set)]
    pub max_memory_fallback: Option<usize>,
    #[pyo3(get, set)]
    pub scheduling_num_mem_chunks: usize,
    #[pyo3(get, set)]
    pub distribute_min_size: Option<usize>,
    #[pyo3(get, set)]
    pub scheduling_naive: bool,
    #[pyo3(get, set)]
    pub scheduling_simplify: bool,
    #[pyo3(get, set)]
    pub scheduling_timeout: usize,
    #[pyo3(get, set)]
    pub scheduling_simplify_lossy: bool,
    #[pyo3(get, set)]
    pub adjust_numerical_scale: bool,
    #[pyo3(get, set)]
    pub numerical_scale_min: f64,
    #[pyo3(get, set)]
    pub numerical_scale_max: f64,
    #[pyo3(get, set)]
    pub capture_and_print: bool,
    #[pyo3(get, set)]
    pub create_tests: bool,
    #[pyo3(get, set)]
    pub log_simplifications: bool,
    #[pyo3(get, set)]
    pub log_slow_einsums: bool,
    #[pyo3(get, set)]
    pub save_circ: bool,
}

impl Default for OptimizationSettings {
    fn default() -> Self {
        Self {
            verbose: 0,
            max_memory: 9_000_000_000,
            max_single_tensor_memory: 9_000_000_000,
            max_memory_fallback: None,
            scheduling_num_mem_chunks: 200,
            distribute_min_size: None,
            scheduling_naive: false,
            scheduling_timeout: 5_000,
            scheduling_simplify: true,
            scheduling_simplify_lossy: false,
            adjust_numerical_scale: false,
            numerical_scale_min: 1e-8,
            numerical_scale_max: 1e8,
            capture_and_print: false,
            create_tests: false,
            log_simplifications: false,
            log_slow_einsums: false,
            save_circ: false,
        }
    }
}

#[pymethods]
impl OptimizationSettings {
    #[new]
    #[args(
        verbose = "OptimizationSettings::default().verbose",
        max_memory = "OptimizationSettings::default().max_memory",
        max_single_tensor_memory = "OptimizationSettings::default().max_single_tensor_memory",
        max_memory_fallback = "None",
        scheduling_num_mem_chunks = "OptimizationSettings::default().scheduling_num_mem_chunks",
        distribute_min_size = "None",
        scheduling_naive = "OptimizationSettings::default().scheduling_naive",
        scheduling_timeout = "OptimizationSettings::default().scheduling_timeout",
        scheduling_simplify = "OptimizationSettings::default().scheduling_simplify",
        scheduling_simplify_lossy = "OptimizationSettings::default().scheduling_simplify_lossy",
        adjust_numerical_scale = "OptimizationSettings::default().adjust_numerical_scale",
        numerical_scale_min = "OptimizationSettings::default().numerical_scale_min",
        numerical_scale_max = "OptimizationSettings::default().numerical_scale_max",
        capture_and_print = "OptimizationSettings::default().capture_and_print",
        create_tests = "OptimizationSettings::default().create_tests",
        log_simplifications = "OptimizationSettings::default().log_simplifications",
        log_slow_einsums = "OptimizationSettings::default().log_slow_einsums",
        save_circ = "OptimizationSettings::default().save_circ"
    )]
    fn new(
        verbose: usize,
        max_memory: usize,
        max_single_tensor_memory: usize,
        max_memory_fallback: Option<usize>,
        scheduling_num_mem_chunks: usize,
        distribute_min_size: Option<usize>,
        scheduling_naive: bool,
        scheduling_timeout: usize,
        scheduling_simplify: bool,
        scheduling_simplify_lossy: bool,
        adjust_numerical_scale: bool,
        numerical_scale_min: f64,
        numerical_scale_max: f64,
        capture_and_print: bool,
        create_tests: bool,
        log_simplifications: bool,
        log_slow_einsums: bool,
        save_circ: bool,
    ) -> Self {
        Self {
            verbose,
            max_memory,
            max_single_tensor_memory,
            max_memory_fallback,
            scheduling_num_mem_chunks,
            distribute_min_size,
            scheduling_naive,
            scheduling_timeout,
            scheduling_simplify,
            scheduling_simplify_lossy,
            adjust_numerical_scale,
            numerical_scale_min,
            numerical_scale_max,
            capture_and_print,
            create_tests,
            log_simplifications,
            log_slow_einsums,
            save_circ,
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct OptimizationCache {
    pub simplified: HashMap<HashBytes, CircuitRc>,
    pub distributed: HashMap<HashBytes, Option<CircuitRc>>,
    pub flops: HashMap<HashBytes, BigUint>,
    pub sum_of_node_sizes: HashMap<HashBytes, BigUint>,
    pub canonicalized: HashMap<HashBytes, Option<CircuitRc>>,
    pub module_specs_scheduled_same_settings: HashMap<ModuleSpec, Schedule>,
    pub module_specs_expanded_shape: HashMap<(ModuleSpec, Vec<Shape>), CircuitRc>,
    pub module_specs_expanded: HashMap<(ModuleSpec, Vec<HashBytes>), CircuitRc>,
    pub stripped_names: HashMap<HashBytes, Option<CircuitRc>>,
    pub times_distributed: usize,
    pub simplification_log: Vec<&'static str>,
    pub max_tensor_elements: usize,
    pub max_single_tensor_numel: usize,
    pub fallback_total_numel: usize,
    pub slow_einsum_log: Vec<EinsumSpec>,
}

/// Note: you can't change the settings once anything's been cached
/// bc cache assumes same settings on everything
#[pyclass]
#[derive(Debug, Clone, Default)]
pub struct OptimizationContext {
    pub cache: OptimizationCache,
    pub settings: OptimizationSettings,
}
#[pymethods]
impl OptimizationContext {
    #[staticmethod]
    pub fn new_settings(settings: OptimizationSettings) -> Self {
        Self {
            cache: Default::default(),
            settings,
        }
    }
    #[staticmethod]
    pub fn new_settings_circuit(settings: OptimizationSettings, circuit: CircuitRc) -> Self {
        let mut result = Self {
            cache: Default::default(),
            settings,
        };
        let dtype = get_compatible_dtype(&circuit);
        result.cache.max_tensor_elements = settings.max_memory / dtype.size();
        result.cache.max_single_tensor_numel = settings.max_single_tensor_memory / dtype.size();
        result.cache.fallback_total_numel =
            settings.max_memory_fallback.unwrap_or(settings.max_memory) / dtype.size();
        result
    }

    pub fn stringify_logs(&self) -> String {
        format!(
            "let slow_einsums = {}; let simplifications= {};",
            self.cache.slow_einsum_log.repr(),
            self.cache.simplification_log.repr()
        )
    }
}

#[pyfunction]
#[pyo3(name = "optimize_circuit")]
pub fn optimize_circuit_py(circuit: CircuitRc, settings: OptimizationSettings) -> CircuitRc {
    let mut context = OptimizationContext {
        settings,
        ..Default::default()
    };
    optimize_circuit(circuit, &mut context)
}

pub fn optimize_circuit(circuit: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    let print_timings = context.settings.verbose >= 2;
    let circuit = timed!(strip_names(circuit, context), 10, print_timings);
    let circuit = remove_autotags(circuit);
    let circuit = conform_all_modules(circuit);
    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 4 {
        python_println!("Original Circuit");
        circuit.printu();
    }
    if context.settings.save_circ {
        let s = circuit.repru();
        let f_name = format!("cached_circ_{}.circ", circuit.info().hash_usize());
        python_println!("Save circ to {}", f_name);

        let mut file = std::fs::File::create(f_name).unwrap();
        file.write_all(s.as_bytes()).unwrap();
    }
    let circuit = timed!(compiler_simp(circuit, context), 10, print_timings);
    // originally tried push_down_index in compiler_simp, but that produced worse circuits
    // for unknown reasons, maybe i'll investigate
    let circuit = timed!(
        apply_fn_until_same(&circuit, |x| deep_push_down_index_raw(
            compiler_simp(x.clone(), context),
            None
        )),
        10,
        print_timings
    );
    let circuit = timed!(compiler_simp(circuit, context), 10, print_timings);
    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 3 {
        python_println!("Simplified Circuit");
        PrintOptions::compiler_default()
            .print(circuit.clone())
            .unwrap();
    }
    let circuit = timed!(
        apply_fn_until_same(&circuit, |x| {
            let distributed = deep_maybe_distribute(x.clone(), context);
            compiler_simp(distributed, context)
        }),
        10,
        print_timings
    );

    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 3 {
        python_println!("Distributed Circuit");
        PrintOptions::compiler_default()
            .print(circuit.clone())
            .unwrap();
    }
    let circuit = timed!(deep_heuristic_nest_adds(circuit), 10, print_timings);
    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);

    let circuit = timed!(deep_optimize_einsums(circuit, context), 10, print_timings);

    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 3 {
        python_println!("Final Circuit");
        PrintOptions::compiler_default()
            .print(circuit.clone())
            .unwrap();
    }
    circuit
}

#[pyfunction]
pub fn optimize_to_schedule(
    circuit: CircuitRc,
    settings: OptimizationSettings,
) -> Result<Schedule> {
    let context = &mut OptimizationContext::new_settings_circuit(settings, circuit.clone());
    let verbose = settings.verbose;
    if verbose > 0 {
        python_println!("Optimizing verbose {}", verbose)
    }
    if settings.capture_and_print {
        PrintOptions::compiler_default()
            .print(circuit.clone())
            .context("capture print fail!")?;
    }
    let optimized_circuit = timed!(optimize_circuit(circuit, context), 10, verbose >= 1);
    // return evaluate_fn(&*optimized_circuit).unwrap();
    let schedule = if settings.scheduling_naive {
        circuit_to_schedule_naive_toposort(optimized_circuit)
    } else {
        timed!(
            circuit_to_schedule(optimized_circuit, context),
            10,
            verbose >= 1
        )?
    };
    if verbose > 1 {
        python_println!("{}", schedule.get_stats());
    }
    Ok(schedule)
}

#[pyfunction]
pub fn optimize_and_evaluate(circuit: CircuitRc, settings: OptimizationSettings) -> Result<Tensor> {
    if !circuit.info().is_explicitly_computable {
        bail!(SchedulingError::NotExplicitlyComputable { circuit });
    }
    let schedule = optimize_to_schedule(circuit, settings)?;

    Ok(schedule.evaluate(settings))
}

/// in python, lots of functions take in collections of circuits and operate on them at once
/// with node caching for just that batch
/// because functions that take one circuit already cache nodes, it's convenient to compute multiple nodes
/// by flat-concatting and then passing around as one circuit
/// flat concatting then splitting is an extra copy on all return data,
/// which we could get rid of by removing flat-concat after rewrites (which would only work with a black box flat_concat node bc simplification isn't guaranteed to preserve concat at at end)
#[pyfunction]
pub fn optimize_and_evaluate_many(
    circuits: Vec<CircuitRc>,
    settings: OptimizationSettings,
) -> Result<Vec<Tensor>> {
    let schedule = optimize_to_schedule_many(circuits, settings)?;
    Ok(schedule.evaluate_many(settings))
}

#[pyfunction]
pub fn optimize_to_schedule_many(
    circuits: Vec<CircuitRc>,
    settings: OptimizationSettings,
) -> Result<Schedule> {
    let flat_concatted = flat_concat(circuits.clone())?.rc();
    let mut schedule = optimize_to_schedule(flat_concatted, settings)?;
    schedule.split_shapes = Some(
        circuits
            .iter()
            .map(|x| x.info().shape.clone())
            .collect::<Vec<Shape>>(),
    );
    Ok(schedule)
}

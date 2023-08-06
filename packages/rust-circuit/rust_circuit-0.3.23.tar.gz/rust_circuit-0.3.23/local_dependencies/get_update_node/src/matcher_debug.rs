use std::{
    collections::BTreeSet,
    fmt::{Display, Write},
    iter::{once, zip},
};

use anyhow::Result;
use circuit_base::{
    clicolor,
    print::{color, last_child_arrows, CliColor, PrintOptions},
    CircuitNode, CircuitNodeUnion, CircuitRc,
};
use itertools::Itertools;
use pyo3::prelude::*;
use rr_util::python_println;
use rustc_hash::FxHashSet as HashSet;

use crate::{
    iterative_matcher::{per_child, ChainItem, IterativeMatcher},
    matcher::{Matcher, MatcherData},
    IterateMatchResults, IterativeMatcherData, IterativeMatcherRc,
};

impl Display for IterativeMatcher {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let s = match self.data() {
            IterativeMatcherData::Match(matcher) => format!("{}", matcher),
            IterativeMatcherData::Term(term) => {
                if *term {
                    "Term".to_owned()
                } else {
                    "term next".to_owned()
                }
            }
            IterativeMatcherData::Filter(filter) => format!(
                "Filter{{ depth_range {}:{}, matcher {}, term_at {}, term_if_matches {}, depth {} }}",
                op_debug(&filter.start_depth),
                op_debug(&filter.end_depth),
                &filter.iterative_matcher.0,
                &filter.term_early_at.0,
                filter.term_if_matches,
                filter.depth
            ),
            IterativeMatcherData::Children(childmatcher) => format!(
                "Children({}, {})",
                &childmatcher.iterative_matcher.0,
                childmatcher
                    .child_numbers
                    .iter()
                    .map(|x| x.to_string())
                    .join(","),
            ),
            IterativeMatcherData::SpecCircuit(matcher) => format!("SpecCircuit({})", &matcher.0),
            IterativeMatcherData::NoModuleSpec(matcher) => format!("NoModuleSpec({})", &matcher.0),
            IterativeMatcherData::Chains(chains) => {
                if chains.len() == 1 {
                    repr_chain_item(chains.iter().next().unwrap())
                } else {
                    format!("Any({})", chains.iter().map(repr_chain_item).join(", "))
                }
            }
            IterativeMatcherData::All(matchers) => {
                format!("All({})", matchers.iter().map(|x| x.to_string()).join(", "))
            }
            IterativeMatcherData::PyFunc(pyobject) => format!("PyIterativeMatcher {}", pyobject),
            IterativeMatcherData::Raw(_) => "".to_owned(),
        };
        f.write_str(&s)
    }
}

#[pymethods]
impl IterativeMatcher {
    fn __repr__(&self) -> String {
        format!("{}", &self)
    }
}

fn repr_chain_item(chain_item: &ChainItem) -> String {
    once(chain_item.first.clone())
        .chain(chain_item.rest.iter().cloned())
        .map(|x| format!("{}", &x.0))
        .join(" -> ")
}

fn op_debug<T: std::fmt::Debug>(x: &Option<T>) -> String {
    match x {
        None => "".to_owned(),
        Some(s) => format!("{:?}", s),
    }
}

fn repr_single_many<T, F>(x: &BTreeSet<T>, f: F) -> String
where
    F: Fn(&T) -> String,
{
    if x.len() == 1 {
        return f(x.iter().next().unwrap());
    }
    format!("{{{}}}", x.iter().map(f).join(", "))
}

pub fn circuit_short_print(circuit: &CircuitRc) -> String {
    format!(
        "{} {} {}",
        match circuit.name() {
            None => "None".to_owned(),
            Some(s) => format!("'{}'", s),
        },
        circuit.variant_string(),
        &circuit.hash_base16()[..6],
    )
}

impl Display for Matcher {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            match self.data() {
                MatcherData::Always(bool) =>
                    if *bool {
                        "Always".to_owned()
                    } else {
                        "Never".to_owned()
                    },
                MatcherData::Name(names) => repr_single_many(names, |x| format!("\"{}\"", x)),
                MatcherData::Type(types) => repr_single_many(types, |x| format!("{}", x)),
                MatcherData::Regex(regex) => format!(
                    "re{}'{}'",
                    if regex.escape_dot() { "-escdot" } else { "" },
                    regex.pattern()
                ),
                MatcherData::EqM(circuits) => repr_single_many(circuits, circuit_short_print),
                MatcherData::PyFunc(pyobject) => format!("{}", pyobject),
                MatcherData::Not(matcher) => format!("Not {}", &matcher.0),
                MatcherData::Any(any) => format!(
                    "Any({})",
                    any.iter().map(|x| format!("{}", &x.0)).join(", ")
                ),
                MatcherData::All(all) => format!(
                    "All({})",
                    all.iter().map(|x| format!("{}", &x.0)).join(", ")
                ),
                // MatcherData::Raw(RawMatcher),
                _ => "".to_owned(),
            }
        )
    }
}

#[pymethods]
impl Matcher {
    fn __repr__(&self) -> String {
        format!("{}", &self)
    }
}

#[pyfunction(print_options = "Default::default()")]
pub fn repr_matcher_debug(
    circuit: CircuitRc,
    matcher: IterativeMatcherRc,
    print_options: PrintOptions,
) -> Result<String> {
    let mut result = "".to_owned();
    let mut seen: HashSet<(CircuitRc, IterativeMatcherRc)> = Default::default();
    fn recurse(
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        last_child_stack: Vec<bool>,
        print_options: &PrintOptions,
        result: &mut String,
        seen: &mut HashSet<(CircuitRc, IterativeMatcherRc)>,
    ) -> Result<()> {
        let key = (circuit.clone(), matcher.clone());
        if !seen.insert(key) {
            write!(
                result,
                "{}'{}'...\n",
                last_child_arrows(&last_child_stack, true, print_options.arrows),
                circuit.name_cloned().unwrap_or("".to_owned())
            )
            .unwrap();
            return Ok(());
        }
        let matched: IterateMatchResults = matcher.match_iterate(circuit.clone())?;
        let line_repr: String = format!(
            "{}{}{}{}\n",
            last_child_arrows(&last_child_stack, true, print_options.arrows),
            print_options.repr_line_info(circuit.clone())?,
            if matched.found {
                color(&" # Found", clicolor!(Green))
            } else {
                "".to_owned()
            },
            color(
                &format!(" # {}", &matcher.0),
                CliColor::new(matcher.__hash__() as usize)
            ),
        );
        result.push_str(&line_repr);

        let child_matchers =
            per_child(matched.updated, matcher.clone(), circuit.children().count());
        for (i, (child, child_matcher)) in zip(circuit.children(), child_matchers).enumerate() {
            if let Some(child_matcher) = child_matcher {
                let new_last_child_stack = last_child_stack
                    .iter()
                    .cloned()
                    .chain(once(i == circuit.children().count() - 1))
                    .collect();
                recurse(
                    child,
                    child_matcher,
                    new_last_child_stack,
                    print_options,
                    result,
                    seen,
                )?;
            } else {
                // reuslt.push_str("")
            }
        }
        Ok(())
    }
    recurse(
        circuit,
        matcher,
        vec![],
        &print_options,
        &mut result,
        &mut seen,
    )?;
    Ok(result)
}

#[pyfunction]
pub fn print_matcher_debug(
    circuit: CircuitRc,
    matcher: IterativeMatcherRc,
    print_options: PrintOptions,
) -> Result<()> {
    python_println!("{}", repr_matcher_debug(circuit, matcher, print_options)?);
    Ok(())
}

#[pyfunction(discard_old_name = "false")]
pub fn append_matchers_to_names(
    circuit: CircuitRc,
    matcher: IterativeMatcherRc,
    discard_old_name: bool,
) -> Result<CircuitRc> {
    fn recurse(
        circuit: CircuitRc,
        matcher: Option<IterativeMatcherRc>,
        discard_old_name: bool,
    ) -> Result<CircuitRc> {
        if matcher.is_none() {
            return Ok(circuit);
        }
        let matcher = matcher.unwrap();
        let matched = matcher.match_iterate(circuit.clone())?;
        let child_matchers =
            per_child(matched.updated, matcher.clone(), circuit.children().count());
        let new_children: Vec<CircuitRc> = zip(circuit.children(), child_matchers)
            .map(|(a, b)| recurse(a, b, discard_old_name))
            .collect::<Result<Vec<CircuitRc>>>()?;
        let result = circuit.map_children_unwrap_idxs(|i| new_children[i].clone());
        if discard_old_name {
            return Ok(result.rename(Some(format!("{}", &matcher.0))));
        }
        Ok(result.rename(
            circuit
                .name()
                .map(|n| format!("{} Matcher {}", n, &matcher.0)),
        ))
    }
    recurse(circuit, Some(matcher), discard_old_name)
}

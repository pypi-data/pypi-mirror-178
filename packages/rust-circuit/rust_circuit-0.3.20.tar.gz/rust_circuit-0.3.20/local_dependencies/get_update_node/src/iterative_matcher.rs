use std::{
    collections::BTreeSet,
    fmt::{self, Debug},
    ops,
    sync::Arc,
    vec,
};

use anyhow::{bail, Result};
use circuit_base::{
    opaque_iterative_matcher::{
        Update as BaseUpdate, UpdatedIterativeMatcher as BaseUpdatedIterativeMatcher,
    },
    CircuitNode, CircuitRc,
};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*, AsPyPointer};
use rr_util::{
    eq_by_big_hash::EqByBigHash,
    impl_both_by_big_hash, python_error_exception, setup_callable, simple_default, simple_from,
    tensor_util::Slice,
    util::{
        arc_ref_clone, arc_unwrap_or_clone, as_sorted, flip_op_result, split_first_take,
        EmptySingleMany as ESM, HashBytes,
    },
};
use thiserror::Error;
use uuid::uuid;

use crate::{
    library::{apply_in_traversal, replace_outside_traversal_symbols},
    AnyFound, BoundAnyFound, BoundGetter, BoundUpdater, Getter, Matcher, MatcherData,
    MatcherFromPyBase, MatcherRc, TransformRc, Updater,
};

#[derive(Clone, FromPyObject)]
pub enum IterativeMatcherFromPy {
    BaseMatch(MatcherFromPyBase),
    // Finished(Finished),
    IterativeMatcher(IterativeMatcher),
    #[pyo3(transparent)]
    PyFunc(PyObject),
}

#[derive(Clone, Debug)]
pub enum IterativeMatcherData {
    Match(Matcher),
    Term(bool),
    Filter(FilterIterativeMatcher),
    Children(ChildrenMatcher),
    SpecCircuit(IterativeMatcherRc),
    NoModuleSpec(IterativeMatcherRc),
    Chains(BTreeSet<ChainItem>),
    Raw(RawIterativeMatcher),
    PyFunc(PyObject),
}

setup_callable!(IterativeMatcher, IterativeMatcherData, IterativeMatcherFromPy, match_iterate(circuit : CircuitRc) -> IterateMatchResults);

simple_from!(|x: Matcher| -> IterativeMatcher { IterativeMatcherData::Match(x).into() });
simple_from!(|x: MatcherData| -> IterativeMatcher { Matcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcher { Matcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcherFromPy {
    IterativeMatcherFromPy::BaseMatch(x.into())
});
simple_from!(|x: Matcher| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_from!(|x: MatcherData| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_default!(IterativeMatcherFromPy {
    MatcherFromPyBase::default().into()
});
simple_default!(IterativeMatcher {
    Matcher::default().into()
});
simple_default!(IterativeMatcherRc {
    IterativeMatcher::default().into()
});

impl From<IterativeMatcherFromPy> for IterativeMatcher {
    fn from(m: IterativeMatcherFromPy) -> Self {
        match m {
            IterativeMatcherFromPy::BaseMatch(x) => x.into(),

            // TODO: maybe Finished should be convertible to Term
            // IterativeMatcherFromPy::Finished(_) => IterativeMatcherData::Term.into(),
            IterativeMatcherFromPy::IterativeMatcher(x) => x.into(),
            // we intentionally do a matcher here as the default - if users want
            // a IterativeMatcher pyfunc, they can explicitly use IterativeMatcher
            // factory.
            IterativeMatcherFromPy::PyFunc(x) => MatcherData::PyFunc(x).into(),
        }
    }
}

#[derive(Clone)]
pub struct ChainItem {
    pub first: IterativeMatcherRc,
    pub rest: Vec<IterativeMatcherRc>,
    hash: HashBytes,
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub enum ChainItemPerChild {
    Many(Vec<Option<ChainItem>>),
    Single(ChainItem),
}

simple_from!(|x: ChainItem| -> ChainItemPerChild { ChainItemPerChild::Single(x) });
simple_from!(|x: Vec<Option<ChainItem>>| -> ChainItemPerChild { ChainItemPerChild::Many(x) });

impl EqByBigHash for ChainItem {
    fn hash(&self) -> HashBytes {
        self.hash
    }
}

impl_both_by_big_hash!(ChainItem);

impl Debug for ChainItem {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        [self.first.clone()]
            .into_iter()
            .chain(self.rest.clone())
            .collect::<Vec<_>>()
            .fmt(f)
    }
}

impl ChainItem {
    pub fn new(first: IterativeMatcherRc, rest: Vec<IterativeMatcherRc>) -> Self {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&first.hash);
        for x in &rest {
            hasher.update(&x.hash);
        }

        Self {
            first,
            rest,
            hash: hasher.finalize().into(),
        }
    }

    pub fn last(&self) -> &IterativeMatcherRc {
        self.rest.last().unwrap_or(&self.first)
    }
}

impl IterativeMatcherData {
    fn uuid(&self) -> [u8; 16] {
        match self {
            Self::Match(_) => uuid!("f1d5e8ec-cba0-496f-883e-78dd5cdc3a49"),
            Self::Term(_) => uuid!("365bc6b4-cbc6-4d82-8e14-7505e1229eec"),
            Self::Filter(_) => uuid!("bcc5ccaa-afbe-414d-88b4-b8eac8c93ece"),
            Self::Children(_) => uuid!("0081e9c9-7fdb-43e1-900e-f1adde28f23d"),
            Self::SpecCircuit(_) => uuid!("b728a8c3-0493-4ee5-96c2-71e4900fc0f8"),
            Self::NoModuleSpec(_) => uuid!("b728a8c3-0493-4ee5-96c2-71e4900fc0f8"),
            Self::Chains(_) => uuid!("958d03ed-7a1a-4ea9-8dd4-d4a8a68feecb"),
            Self::Raw(_) => uuid!("5838ac96-0f48-4cdb-874f-d4f68ce3a52b"),
            Self::PyFunc(_) => uuid!("d3afc3c0-5c86-46df-9e41-7944caedd901"),
        }
        .into_bytes()
    }

    fn item_hash(&self, hasher: &mut blake3::Hasher) {
        match self {
            Self::Match(x) => {
                hasher.update(&x.hash());
            }
            Self::Filter(FilterIterativeMatcher {
                iterative_matcher,
                term_if_matches,
                start_depth,
                end_depth,
                term_early_at,
                depth,
            }) => {
                hasher.update(&iterative_matcher.hash);
                hasher.update(&[*term_if_matches as u8]);
                hasher.update(&[start_depth.is_some() as u8]);
                hasher.update(&start_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&[end_depth.is_some() as u8]);
                hasher.update(&end_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&term_early_at.hash());
                hasher.update(&depth.to_le_bytes());
            }
            Self::Children(ChildrenMatcher {
                iterative_matcher,
                child_numbers,
            }) => {
                hasher.update(&iterative_matcher.hash);
                for num in child_numbers {
                    hasher.update(&num.to_le_bytes());
                }
            }
            Self::SpecCircuit(matcher) | Self::NoModuleSpec(matcher) => {
                hasher.update(&matcher.hash);
            }
            Self::Chains(chains) => {
                for chain in as_sorted(chains) {
                    hasher.update(&chain.hash);
                }
            }
            Self::Raw(x) => {
                hasher.update(&(Arc::as_ptr(&x.0) as *const () as usize).to_le_bytes());
            }
            Self::PyFunc(x) => {
                hasher.update(&(x.as_ptr() as usize).to_le_bytes());
            }
            &Self::Term(next) => {
                hasher.update(&[next as u8]);
            }
        }
    }
}

/// Helper with some basic rules you may want to use to control your node matching iterations.
#[derive(Clone, Debug)]
pub struct FilterIterativeMatcher {
    pub iterative_matcher: IterativeMatcherRc,
    ///if true, stops once it has found a match
    pub term_if_matches: bool,
    /// depth at which we start matching
    pub start_depth: Option<u32>,
    /// depth at which we stop matching
    pub end_depth: Option<u32>,
    /// terminate iterative matching if we reach a node which matches this
    pub term_early_at: MatcherRc,
    pub depth: u32,
}

impl FilterIterativeMatcher {
    /// Fancy constructor which supports range
    ///
    /// TODO: add support for a builder with defaults because this is really annoying...
    /// TODO: actually test this when builder is added!
    pub fn new_range<R: ops::RangeBounds<u32>>(
        iterative_matcher: IterativeMatcherRc,
        term_if_matches: bool,
        depth_range: R,
        term_early_at: MatcherRc,
    ) -> Self {
        use ops::Bound;

        let start_depth = match depth_range.start_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x),
            Bound::Excluded(x) => Some(*x + 1),
        };
        let end_depth = match depth_range.end_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x + 1),
            Bound::Excluded(x) => Some(*x),
        };
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn new(
        iterative_matcher: IterativeMatcherRc,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: MatcherRc,
    ) -> Self {
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let with_dist_of_end = |offset: u32| {
            self.end_depth
                .map(|x| self.depth >= x.saturating_sub(offset))
                .unwrap_or(false)
        };

        let after_end = with_dist_of_end(0);
        if after_end {
            return Ok(IterateMatchResults {
                updated: Some(None.into()),
                found: false,
            });
        }

        let before_start = self.start_depth.map(|x| self.depth < x).unwrap_or(false);
        if before_start {
            return Ok(IterateMatchResults {
                updated: Some(
                    Some(
                        IterativeMatcherData::Filter(FilterIterativeMatcher {
                            depth: self.depth + 1,
                            ..self.clone()
                        })
                        .into(),
                    )
                    .into(),
                ),
                found: false,
            });
        }

        let IterateMatchResults { updated, found } =
            self.iterative_matcher.match_iterate(circuit.clone())?;

        let reached_end = with_dist_of_end(1);
        if all_finished(&updated)
            || (found && self.term_if_matches)
            || reached_end
            || self.term_early_at.call(circuit)?
        {
            return Ok(IterateMatchResults {
                updated: Some(None.into()),
                found,
            });
        }

        let new_depth = if self.end_depth.is_some() {
            self.depth + 1
        } else {
            self.depth
        };

        let updated = if self.end_depth.is_some() {
            // we can't keep same if we need to update end_depth
            Some(updated.unwrap_or(Some(self.iterative_matcher.clone()).into()))
        } else {
            updated
        };

        let updated = map_updated(updated, |new| {
            IterativeMatcherData::Filter(FilterIterativeMatcher {
                iterative_matcher: new,
                depth: new_depth,
                ..self.clone()
            })
            .into()
        });

        Ok(IterateMatchResults { updated, found })
    }
}

#[derive(Clone, Debug)]
pub struct ChildrenMatcher {
    pub iterative_matcher: IterativeMatcherRc,
    pub child_numbers: BTreeSet<usize>,
}

impl ChildrenMatcher {
    pub fn new(
        iterative_matcher: IterativeMatcherRc,
        child_numbers: BTreeSet<usize>,
    ) -> Result<Self> {
        Ok(Self {
            iterative_matcher,
            child_numbers,
        })
    }

    pub fn check_num_children(&self, num_children: usize) -> Result<()> {
        for n in &self.child_numbers {
            if n >= &num_children {
                bail!(IterativeMatcherError::ChildNumbersOutOfBounds {
                    child_numbers: self.child_numbers.clone(),
                    num_children
                });
            }
        }
        Ok(())
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let num_children = circuit.num_children();
        let IterateMatchResults { updated, found } =
            self.iterative_matcher.match_iterate(circuit)?;

        let updated_to_children_matcher = |iterative_matcher| {
            IterativeMatcherData::Children(Self {
                iterative_matcher,
                child_numbers: self.child_numbers.clone(),
            })
            .into()
        };

        let out = if found {
            self.check_num_children(num_children)?;

            let per_child = per_child(updated, self.iterative_matcher.clone(), num_children);
            assert_eq!(per_child.len(), num_children);
            let updated = per_child
                .into_iter()
                .enumerate()
                .map(|(i, x)| {
                    Some(
                        IterativeMatcher::special_case_any(
                            x.map(updated_to_children_matcher)
                                .into_iter()
                                .chain(
                                    (self.child_numbers.contains(&i))
                                        .then(|| IterativeMatcher::term(true).into()),
                                )
                                .collect(),
                        )
                        .rc(),
                    )
                    .into()
                })
                .collect::<Vec<Update>>()
                .into();

            IterateMatchResults {
                updated: Some(updated),
                found: false,
            }
        } else {
            IterateMatchResults {
                updated: map_updated(updated, updated_to_children_matcher),
                found: false,
            }
        };
        Ok(out)
    }
}

impl circuit_base::opaque_iterative_matcher::HasTerm for IterativeMatcherRc {
    fn term() -> Self {
        IterativeMatcher::term(false).into()
    }
}

pub type Update = BaseUpdate<IterativeMatcherRc>;
pub type UpdatedIterativeMatcher = BaseUpdatedIterativeMatcher<IterativeMatcherRc>;

pub fn require_single(x: UpdatedIterativeMatcher) -> Result<Update> {
    match x {
        UpdatedIterativeMatcher::Many(matchers) => {
            bail!(IterativeMatcherError::OperationDoesntSupportArgPerChild { matchers })
        }
        UpdatedIterativeMatcher::Single(x) => Ok(x),
    }
}

pub fn per_child(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    num_children: usize,
) -> Vec<Option<IterativeMatcherRc>> {
    updated
        .unwrap_or(Some(matcher).into())
        .per_child(num_children)
}

pub fn per_child_with_term(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    num_children: usize,
) -> Vec<IterativeMatcherRc> {
    per_child(updated, matcher, num_children)
        .into_iter()
        .map(|x| x.unwrap_or_else(|| IterativeMatcher::term(false).into()))
        .collect()
}

pub fn function_per_child_op(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    circuit: CircuitRc,
    mut func: impl FnMut(CircuitRc, IterativeMatcherRc) -> Result<CircuitRc>,
) -> Result<Option<CircuitRc>> {
    if all_finished(&updated) {
        // special casing this isn't strictly required
        return Ok(None);
    }
    let mut new_matchers = per_child(updated, matcher, circuit.num_children());
    circuit
        .map_children_enumerate(|i, c| {
            std::mem::take(&mut new_matchers[i])
                .map(|new_matcher| func(c.clone(), new_matcher))
                .unwrap_or(Ok(c))
        })
        .map(Some)
}

pub fn function_per_child(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    circuit: CircuitRc,
    func: impl FnMut(CircuitRc, IterativeMatcherRc) -> Result<CircuitRc>,
) -> Result<CircuitRc> {
    function_per_child_op(updated, matcher, circuit.clone(), func).map(|x| x.unwrap_or(circuit))
}

pub fn map_updated(
    x: Option<UpdatedIterativeMatcher>,
    f: impl FnMut(IterativeMatcherRc) -> IterativeMatcherRc,
) -> Option<UpdatedIterativeMatcher> {
    x.map(|x| x.map_updated(f))
}

pub fn all_finished(x: &Option<UpdatedIterativeMatcher>) -> bool {
    x.as_ref().map(|x| x.all_finished()).unwrap_or(false)
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct IterateMatchResults {
    /// here None, is 'use same'
    #[pyo3(set, get)]
    pub updated: Option<UpdatedIterativeMatcher>,
    #[pyo3(set, get)]
    pub found: bool,
}

#[pymethods]
impl IterateMatchResults {
    #[new]
    #[args(updated = "None", found = "false")]
    fn new(updated: Option<UpdatedIterativeMatcher>, found: bool) -> Self {
        Self { updated, found }
    }

    #[staticmethod]
    #[args(found = "false")]
    pub fn new_finished(found: bool) -> Self {
        Self {
            updated: Some(None.into()),
            found,
        }
    }

    fn to_tup(&self) -> (Option<UpdatedIterativeMatcher>, bool) {
        (self.updated.clone(), self.found)
    }

    #[pyo3(name = "unwrap_or_same")]
    pub fn unwrap_or_same_py(
        &self,
        matcher: IterativeMatcherRc,
    ) -> (UpdatedIterativeMatcher, bool) {
        self.clone().unwrap_or_same(matcher)
    }
}

impl IterateMatchResults {
    pub fn unwrap_or_same(self, matcher: IterativeMatcherRc) -> (UpdatedIterativeMatcher, bool) {
        (self.updated.unwrap_or(Some(matcher).into()), self.found)
    }
}

impl IterativeMatcher {
    pub fn or(self, other: IterativeMatcherRc) -> Self {
        Self::any(vec![self.crc(), other])
    }

    // TODO: this is kinda shitty, see https://github.com/redwoodresearch/unity/issues/1524
    pub fn validate_matched(&self, matched: &BTreeSet<CircuitRc>) -> Result<()> {
        match &self.data {
            IterativeMatcherData::Match(m) => m.validate_matched(matched),
            IterativeMatcherData::Term(_) => Ok(()),
            IterativeMatcherData::Filter(m) => m.iterative_matcher.validate_matched(matched),
            IterativeMatcherData::Children(_) => Ok(()), /* not sure what else you could do here */
            IterativeMatcherData::SpecCircuit(_) => Ok(()), /* not sure what else you could do here */
            IterativeMatcherData::NoModuleSpec(m) => m.validate_matched(matched),
            IterativeMatcherData::Chains(m) => {
                for chain in m {
                    chain.last().validate_matched(matched)?;
                }
                Ok(())
            }
            IterativeMatcherData::PyFunc(_) | IterativeMatcherData::Raw(_) => Ok(()),
        }
    }
    // TODO: more rust niceness funcs like the py ones!
}

#[pymethods]
impl IterativeMatcher {
    #[new]
    #[args(inps = "*")]
    // also py_new
    fn special_case_any(inps: Vec<IterativeMatcherRc>) -> Self {
        match inps.into() {
            ESM::Empty => Self::term(false),
            ESM::Single(x) => arc_ref_clone(&x),
            ESM::Many(x) => Self::any(x),
        }
    }

    #[staticmethod]
    pub fn noop_traversal() -> Self {
        MatcherData::Always(true).into()
    }

    #[staticmethod]
    #[args(match_next = "false")]
    pub fn term(match_next: bool) -> Self {
        IterativeMatcherData::Term(match_next).into()
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let num_children = circuit.num_children();
        let res = match &self.data {
            IterativeMatcherData::Match(m) => IterateMatchResults {
                updated: None,
                found: m.call(circuit)?,
            },
            &IterativeMatcherData::Term(match_next) => {
                IterateMatchResults::new_finished(match_next)
            }
            IterativeMatcherData::Filter(filter) => filter.match_iterate(circuit)?,
            IterativeMatcherData::Children(children_matcher) => {
                children_matcher.match_iterate(circuit)?
            }
            IterativeMatcherData::SpecCircuit(module_matcher) => {
                let is_module = circuit.is_module();
                let IterateMatchResults { updated, found } =
                    module_matcher.match_iterate(circuit)?;
                let updated_to_spec_circuit_matcher =
                    |iterative_matcher| IterativeMatcherData::SpecCircuit(iterative_matcher).into();
                if found {
                    if !is_module {
                        bail!("not module!");
                    }

                    let per_child = per_child(updated, module_matcher.clone(), num_children);

                    let updated = per_child
                        .into_iter()
                        .enumerate()
                        .map(|(i, x)| {
                            Some(
                                IterativeMatcher::special_case_any(
                                    x.map(updated_to_spec_circuit_matcher)
                                        .into_iter()
                                        .chain(
                                            (i == 0) // spec circuit is child 0 on Module
                                                .then(|| IterativeMatcher::term(true).into()),
                                        )
                                        .collect(),
                                )
                                .rc(),
                            )
                            .into()
                        })
                        .collect::<Vec<Update>>()
                        .into();

                    IterateMatchResults {
                        updated: Some(updated),
                        found: false,
                    }
                } else {
                    IterateMatchResults {
                        updated: map_updated(updated, updated_to_spec_circuit_matcher),
                        found: false,
                    }
                }
            }
            IterativeMatcherData::NoModuleSpec(matcher) => {
                let is_module = circuit.is_module();
                let IterateMatchResults { updated, found } = matcher.match_iterate(circuit)?;
                if is_module {
                    let per_child = per_child(updated, matcher.clone(), num_children);
                    let updated = per_child
                        .into_iter()
                        .enumerate()
                        .map(|(i, x)| {
                            x.and_then(|x| {
                                (i != 0 && (i - 1) % 2 != 0)
                                    .then(|| IterativeMatcherData::NoModuleSpec(x).into())
                            })
                            .into()
                        })
                        .collect::<Vec<Update>>()
                        .into();

                    IterateMatchResults {
                        updated: Some(updated),
                        found,
                    }
                } else {
                    IterateMatchResults {
                        updated: map_updated(updated, |x| {
                            IterativeMatcherData::NoModuleSpec(x).into()
                        }),
                        found,
                    }
                }
            }
            IterativeMatcherData::Chains(chains) => {
                /// avoid some hashing and some copies - probably overkill
                #[derive(Clone, Copy)]
                enum MaybeChain<'a> {
                    Chain(&'a ChainItem),
                    Slices {
                        first: &'a IterativeMatcherRc,
                        rest: &'a [IterativeMatcherRc],
                    },
                }

                impl<'a> MaybeChain<'a> {
                    fn first(&'a self) -> &'a IterativeMatcherRc {
                        match self {
                            Self::Chain(x) => &x.first,
                            Self::Slices { first, .. } => first,
                        }
                    }

                    fn rest(&'a self) -> &'a [IterativeMatcherRc] {
                        match self {
                            Self::Chain(x) => &x.rest,
                            Self::Slices { rest, .. } => rest,
                        }
                    }

                    fn clone_chain(&'a self) -> ChainItem {
                        match self {
                            &Self::Chain(x) => x.clone(),
                            Self::Slices { first, rest } => {
                                ChainItem::new((*first).clone(), rest.to_vec())
                            }
                        }
                    }

                    fn with_first(&'a self, first: IterativeMatcherRc) -> ChainItem {
                        ChainItem::new(first, self.rest().to_vec()).into()
                    }
                }

                fn run_item(
                    chain: MaybeChain<'_>,
                    circuit: &CircuitRc,
                    new_items: &mut BTreeSet<ChainItemPerChild>,
                ) -> Result<bool> {
                    let IterateMatchResults { updated, found } =
                        chain.first().match_iterate(circuit.clone())?;

                    if !all_finished(&updated) {
                        use BaseUpdatedIterativeMatcher::*;
                        let new_chain = match (updated, chain) {
                            (None, _) => chain.clone_chain().into(),
                            (Some(Single(BaseUpdate(None))), _) => unreachable!(),
                            (Some(Single(BaseUpdate(Some(x)))), chain) => {
                                chain.with_first(x).into()
                            }
                            (Some(Many(items)), chain) => items
                                .into_iter()
                                .map(|x| x.0.map(|x| chain.with_first(x)))
                                .collect::<Vec<_>>()
                                .into(),
                        };
                        new_items.insert(new_chain);
                    }

                    if found {
                        match chain.rest() {
                            [] => Ok(true),
                            [rest_first, rest_rest @ ..] => run_item(
                                MaybeChain::Slices {
                                    first: rest_first,
                                    rest: rest_rest,
                                },
                                circuit,
                                new_items,
                            ),
                        }
                    } else {
                        Ok(false)
                    }
                }

                let mut new_items: BTreeSet<ChainItemPerChild> = Default::default();
                let mut any_chain_finished = false;
                for chain in chains {
                    let new_any_finished =
                        run_item(MaybeChain::Chain(chain), &circuit, &mut new_items)?;
                    any_chain_finished = new_any_finished || any_chain_finished;
                }

                let finished = new_items.is_empty();

                let updated = if new_items
                    .iter()
                    .any(|x| matches!(x, ChainItemPerChild::Many(_)))
                {
                    assert!(!finished);
                    let num_children = circuit.children().count();
                    let mut out = vec![BTreeSet::default(); num_children];
                    for item in new_items {
                        match item {
                            ChainItemPerChild::Single(x) => {
                                out.iter_mut().for_each(|child_chains| {
                                    child_chains.insert(x.clone());
                                })
                            }
                            ChainItemPerChild::Many(xs) => {
                                out.iter_mut().zip(xs).for_each(|(child_chains, x)| {
                                    if let Some(x) = x {
                                        child_chains.insert(x);
                                    }
                                })
                            }
                        }
                    }
                    Some(UpdatedIterativeMatcher::Many(
                        out.into_iter()
                            .map(|chains| {
                                (!chains.is_empty())
                                    .then(|| IterativeMatcherData::Chains(chains).into())
                                    .into()
                            })
                            .collect(),
                    ))
                } else {
                    let new_items = new_items
                        .into_iter()
                        .map(|x| match x {
                            ChainItemPerChild::Single(x) => x,
                            ChainItemPerChild::Many(_) => unreachable!(),
                        })
                        .collect();
                    (&new_items != chains).then(|| {
                        UpdatedIterativeMatcher::Single(
                            (!finished)
                                .then(|| IterativeMatcherData::Chains(new_items).into())
                                .into(),
                        )
                    })
                };

                IterateMatchResults {
                    updated,
                    found: any_chain_finished,
                }
            }
            IterativeMatcherData::Raw(f) => f.0(circuit)?,
            IterativeMatcherData::PyFunc(pyfunc) => {
                Python::with_gil(|py| pyfunc.call1(py, (circuit,)).and_then(|r| r.extract(py)))?
            }
        };

        if let Some(UpdatedIterativeMatcher::Many(items)) = &res.updated {
            // checking here allows us to assume valid in other places!
            if items.len() != num_children {
                bail!(IterativeMatcherError::NumUpdatedMatchersNEQToNumChildren {
                    num_updated_matchers: items.len(),
                    num_children,
                    updated_matchers: items.clone(),
                    from_matcher: self.crc()
                });
            }
        }

        Ok(res)
    }

    #[pyo3(name = "validate_matched")]
    fn validate_matched_py(&self, matched: BTreeSet<CircuitRc>) -> Result<()> {
        self.validate_matched(&matched)
    }

    #[staticmethod]
    #[args(matchers = "*")]
    pub fn any(matchers: Vec<IterativeMatcherRc>) -> Self {
        IterativeMatcherData::Chains(
            matchers
                .into_iter()
                .map(|x| ChainItem::new(x.into(), Vec::new()))
                .collect(),
        )
        .into()
    }

    #[staticmethod]
    #[args(first, rest = "*")]
    pub fn new_chain(first: IterativeMatcherRc, rest: Vec<IterativeMatcherRc>) -> Self {
        first.chain(rest)
    }

    #[staticmethod]
    #[args(chains = "*")]
    pub fn new_chain_many(chains: Vec<Vec<IterativeMatcherRc>>) -> Result<Self> {
        Ok(IterativeMatcherData::Chains(
            chains
                .into_iter()
                .map(|mut chain| match split_first_take(&mut chain) {
                    None => bail!("Received empty tuple for a chain, we expect len >= 1",),
                    Some((first, rest)) => Ok(ChainItem::new(first, rest.collect())),
                })
                .collect::<Result<_>>()?,
        )
        .into())
    }

    #[staticmethod]
    pub fn new_children_matcher(
        first_match: IterativeMatcherRc,
        child_numbers: BTreeSet<usize>,
    ) -> Self {
        first_match.children_matcher(child_numbers)
    }

    #[staticmethod]
    pub fn new_spec_circuit_matcher(module_matcher: IterativeMatcherRc) -> Self {
        module_matcher.spec_circuit_matcher()
    }

    #[staticmethod]
    #[pyo3(name = "new_func")]
    pub(super) fn new_func_py(f: PyObject) -> Self {
        IterativeMatcherData::PyFunc(f).into()
    }

    #[args(others = "*")]
    pub fn new_or(&self, others: Vec<IterativeMatcherRc>) -> Self {
        Self::any([self.clone().into()].into_iter().chain(others).collect())
    }

    fn __or__(&self, other: IterativeMatcherRc) -> Self {
        self.clone().or(other)
    }
    fn __ror__(&self, other: IterativeMatcherRc) -> Self {
        arc_unwrap_or_clone(other.0).or(self.crc())
    }

    // TODO: write flatten/simplify method if we want the extra speed + niceness!
}

macro_rules! dup_functions {
    {
        #[self_id($self_ident:ident)]
        impl IterativeMatcher {
            $(
            $( #[$($meta_tt:tt)*] )*
        //  ^~~~attributes~~~~^
            $vis:vis fn $name:ident (
                &self
                $(, $arg_name:ident : $arg_ty:ty )* $(,)?
        //      ^~~~~~~~~~~~~~~argument list!~~~~~~~~~~~^
                )
                $( -> $ret_ty:ty )?
        //      ^~~~return type~~~^
                { $($tt:tt)* }
            )*

        }
    } => {
        // paste is needed due to how pymethods proc macro works
        paste::paste!{
            #[pymethods]
            impl IterativeMatcher {
                $(
                    $(#[$($meta_tt)*])*
                    $vis fn $name(&self, $($arg_name : $arg_ty,)*) $(-> $ret_ty)* {
                        let $self_ident = self;
                        $($tt)*
                    }
                )*
            }

            #[pymethods]
            impl Matcher {
                $(
                    $(#[$($meta_tt)*])*
                    $vis fn $name(&self, $($arg_name : $arg_ty,)*) $(-> $ret_ty)* {
                        self.to_iterative_matcher().$name($($arg_name,)*)
                    }
                )*
            }
        }

    };
}

#[apply(dup_functions)]
#[self_id(self_)]
impl IterativeMatcher {
    #[args(
        term_if_matches = "false",
        start_depth = "None",
        end_depth = "None",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    pub fn filter(
        &self,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: MatcherRc,
    ) -> IterativeMatcher {
        // TODO: flatten
        IterativeMatcherData::Filter(FilterIterativeMatcher::new(
            self_.clone().into(),
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
        ))
        .into()
    }

    #[args(
        term_if_matches = "false",
        depth_slice = "Slice::IDENT",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    pub fn filter_sl(
        &self,
        term_if_matches: bool,
        depth_slice: Slice,
        term_early_at: MatcherRc,
    ) -> Result<IterativeMatcher> {
        Ok(self_.filter(
            term_if_matches,
            flip_op_result(depth_slice.start.map(|x| x.try_into()))?,
            flip_op_result(depth_slice.stop.map(|x| x.try_into()))?,
            term_early_at,
        ))
    }

    #[args(rest = "*")]
    pub fn chain(&self, rest: Vec<IterativeMatcherRc>) -> IterativeMatcher {
        // TODO: flatten
        IterativeMatcherData::Chains(
            [ChainItem::new(self_.clone().into(), rest)]
                .into_iter()
                .collect::<BTreeSet<_>>(),
        )
        .into()
    }

    #[args(rest = "*")]
    pub fn chain_many(&self, rest: Vec<Vec<IterativeMatcherRc>>) -> IterativeMatcher {
        // TODO: flatten
        IterativeMatcherData::Chains(
            rest.into_iter()
                .map(|x| ChainItem::new(self_.clone().into(), x))
                .collect(),
        )
        .into()
    }

    pub fn children_matcher(&self, child_numbers: BTreeSet<usize>) -> IterativeMatcher {
        IterativeMatcherData::Children(ChildrenMatcher {
            iterative_matcher: self_.clone().rc(),
            child_numbers,
        })
        .into()
    }

    pub fn spec_circuit_matcher(&self) -> IterativeMatcher {
        IterativeMatcherData::SpecCircuit(self_.clone().rc()).into()
    }

    #[args(enable = "true")]
    pub fn filter_module_spec(&self, enable: bool) -> IterativeMatcher {
        if enable {
            IterativeMatcherData::NoModuleSpec(self_.clone().rc()).into()
        } else {
            self_.clone()
        }
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get(&self, circuit: CircuitRc, fancy_validate: bool) -> Result<BTreeSet<CircuitRc>> {
        Getter::default().get(circuit, self_.crc(), Some(fancy_validate))
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique_op(
        &self,
        circuit: CircuitRc,
        fancy_validate: bool,
    ) -> Result<Option<CircuitRc>> {
        Getter::default().get_unique_op(circuit, self_.crc(), Some(fancy_validate))
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique(&self, circuit: CircuitRc, fancy_validate: bool) -> Result<CircuitRc> {
        Getter::default().get_unique(circuit, self_.crc(), Some(fancy_validate))
    }

    pub fn validate(&self, circuit: CircuitRc) -> Result<()> {
        Getter::default().validate(circuit, self_.crc())
    }

    #[args(default_fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn getter(&self, default_fancy_validate: bool) -> BoundGetter {
        Getter::new(default_fancy_validate).bind(self_.crc())
    }

    pub fn are_any_found(&self, circuit: CircuitRc) -> Result<bool> {
        AnyFound::new().are_any_found(circuit, self_.crc())
    }
    pub fn any_found(&self) -> BoundAnyFound {
        AnyFound::new().bind(self_.crc())
    }

    #[args(
        cache_transform = "Updater::default().cache_transform",
        cache_update = "Updater::default().cache_update",
        fancy_validate = "Updater::default().default_fancy_validate"
    )]
    pub fn update(
        &self,
        circuit: CircuitRc,
        transform: TransformRc,
        cache_transform: bool,
        cache_update: bool,
        fancy_validate: bool,
    ) -> Result<CircuitRc> {
        Updater::new(transform, cache_transform, cache_update, false).update(
            circuit,
            self_.crc(),
            Some(fancy_validate),
        )
    }

    #[args(
        cache_transform = "Updater::default().cache_transform",
        cache_update = "Updater::default().cache_update",
        default_fancy_validate = "Updater::default().default_fancy_validate"
    )]
    pub fn updater(
        &self,
        transform: TransformRc,
        cache_transform: bool,
        cache_update: bool,
        default_fancy_validate: bool,
    ) -> BoundUpdater {
        Updater::new(
            transform,
            cache_transform,
            cache_update,
            default_fancy_validate,
        )
        .bind(self_.crc())
    }

    pub fn apply_in_traversal(
        &self,
        circuit: CircuitRc,
        transform: TransformRc,
    ) -> Result<CircuitRc> {
        apply_in_traversal(circuit, self_.clone().rc(), |x| transform.run(x))
    }

    pub fn traversal_edges(&self, circuit: CircuitRc) -> Result<Vec<CircuitRc>> {
        Ok(
            replace_outside_traversal_symbols(circuit, self_.clone().rc(), |_| Ok(None))?
                .1
                .into_values()
                .collect(),
        )
    }
}

#[apply(python_error_exception)]
#[base_error_name(IterativeMatcher)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum IterativeMatcherError {
    #[error(
        "num_updated_matchers={num_updated_matchers} != num_children={num_children}\nupdated_matchers={updated_matchers:?}, from_matcher={from_matcher:?}\n({e_name})"
    )]
    NumUpdatedMatchersNEQToNumChildren {
        num_updated_matchers: usize,
        num_children: usize,
        updated_matchers: Vec<Update>,
        from_matcher: IterativeMatcherRc,
    },

    #[error("operation doesn't support per child matching matchers={matchers:?}\n({e_name})")]
    OperationDoesntSupportArgPerChild { matchers: Vec<Update> },

    #[error("some child_numbers={child_numbers:?} >= num_children={num_children} ({e_name})")]
    ChildNumbersOutOfBounds {
        child_numbers: BTreeSet<usize>,
        num_children: usize,
    },
}

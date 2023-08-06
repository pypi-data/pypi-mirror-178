use std::collections::BTreeSet;

use anyhow::{anyhow, bail, Result};
use circuit_base::{expand_node::expand_node, CircuitNode, CircuitRc};
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{
    cached_method,
    util::{transpose, HashBytes},
};

use crate::{
    iterative_matcher::{all_finished, function_per_child, per_child, per_child_with_term},
    IterateMatchResults, IterativeMatcherRc, Transform, TransformData, TransformRc,
};

#[pyclass]
#[derive(Debug, Clone)]
pub struct Updater {
    #[pyo3(get)]
    pub(super) transform: TransformRc,
    #[pyo3(get)]
    pub(super) cache_transform: bool,
    #[pyo3(get)]
    pub(super) cache_update: bool,
    #[pyo3(get, set)]
    pub(super) default_fancy_validate: bool,
    pub(super) transform_cache: cached::UnboundCache<HashBytes, CircuitRc>,
    pub(super) updated_cache: cached::UnboundCache<(HashBytes, IterativeMatcherRc), CircuitRc>,
    pub(super) validation_getter: Getter,
}

impl Default for Updater {
    fn default() -> Self {
        Self {
            transform: Transform::ident().into(),
            cache_transform: true,
            cache_update: true,
            default_fancy_validate: false,
            transform_cache: cached::UnboundCache::new(),
            updated_cache: cached::UnboundCache::new(),
            validation_getter: Default::default(),
        }
    }
}

#[pymethods]
impl Updater {
    #[new]
    #[args(
        cache_transform = "Updater::default().cache_transform",
        cache_update = "Updater::default().cache_update",
        default_fancy_validate = "Updater::default().default_fancy_validate"
    )]
    pub fn new(
        transform: TransformRc,
        cache_transform: bool,
        cache_update: bool,
        default_fancy_validate: bool,
    ) -> Self {
        Self {
            transform,
            cache_transform,
            cache_update,
            default_fancy_validate,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.update(circuit, matcher, fancy_validate)
    }

    pub fn update(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            self.validation_getter
                .validate(circuit.clone(), matcher.clone())?;
        }
        self.update_impl(circuit, matcher)
    }

    pub fn bind(&self, matcher: IterativeMatcherRc) -> BoundUpdater {
        BoundUpdater {
            updater: self.clone(),
            matcher,
        }
    }
}

impl Updater {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matcher.clone()))]
    #[use_try]
    #[cache_expr(updated_cache)]
    fn update_impl(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
    ) -> Result<CircuitRc> {
        let IterateMatchResults { updated, found } = matcher.match_iterate(circuit.clone())?;

        let mut new_circuit =
            function_per_child(updated, matcher, circuit.clone(), |circuit, new_matcher| {
                self_.update_impl(circuit, new_matcher)
            })?;

        if found {
            if !matches!(self_.transform.data(), TransformData::Ident) {
                new_circuit = self_.run_transform(new_circuit)?;
            }
        }

        Ok(new_circuit)
    }

    #[apply(cached_method)]
    #[self_id(self_)]
    #[key(circuit.info().hash)]
    #[use_try]
    #[cache_expr(transform_cache)]
    fn run_transform(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        self_.transform.run(circuit)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct BoundUpdater {
    #[pyo3(get, set)]
    pub updater: Updater,
    #[pyo3(get, set)]
    pub matcher: IterativeMatcherRc,
}

#[pymethods]
impl BoundUpdater {
    #[new]
    pub fn new(updater: Updater, matcher: IterativeMatcherRc) -> Self {
        Self { updater, matcher }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.update(circuit, fancy_validate)
    }

    pub fn update(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.updater
            .update(circuit, self.matcher.clone(), fancy_validate)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Getter {
    #[pyo3(get, set)]
    pub(super) default_fancy_validate: bool,
    pub(super) cache: cached::UnboundCache<(HashBytes, IterativeMatcherRc), BTreeSet<CircuitRc>>,
}

impl Default for Getter {
    fn default() -> Self {
        Self {
            default_fancy_validate: false,
            cache: cached::UnboundCache::new(),
        }
    }
}

#[pymethods]
impl Getter {
    #[new]
    #[args(default_fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn new(default_fancy_validate: bool) -> Self {
        Self {
            default_fancy_validate,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<BTreeSet<CircuitRc>> {
        self.get(circuit, matcher, fancy_validate)
    }

    pub fn get(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<BTreeSet<CircuitRc>> {
        let out = self.get_impl(circuit, matcher.clone())?;
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            matcher.validate_matched(&out)?;
        }
        Ok(out)
    }

    pub fn get_unique_op(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<Option<CircuitRc>> {
        let out = self.get(circuit, matcher, fancy_validate)?;
        if out.len() > 1 {
            bail!("found {} matches which is > 1", out.len());
        }
        Ok(out.into_iter().next())
    }

    pub fn get_unique(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.get_unique_op(circuit, matcher, fancy_validate)?
            .ok_or_else(|| anyhow!("found no matches!"))
    }

    pub fn validate(&mut self, circuit: CircuitRc, matcher: IterativeMatcherRc) -> Result<()> {
        self.get(circuit, matcher, Some(true))?;
        Ok(())
    }

    pub fn bind(&self, matcher: IterativeMatcherRc) -> BoundGetter {
        BoundGetter {
            getter: self.clone(),
            matcher,
        }
    }

    // TODO: add support for paths as needed!
}

impl Getter {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matcher.clone()))]
    #[use_try]
    #[cache_expr(cache)]
    fn get_impl(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
    ) -> Result<BTreeSet<CircuitRc>> {
        let IterateMatchResults { updated, found } = matcher.match_iterate(circuit.clone())?;

        let mut out: BTreeSet<CircuitRc> = Default::default();
        if found {
            out.insert(circuit.clone());
        }
        if !all_finished(&updated) {
            let new_matchers = per_child(updated, matcher, circuit.num_children());
            for (child, new_matcher) in circuit.children().zip(new_matchers) {
                if let Some(new_matcher) = new_matcher {
                    out.extend(self_.get_impl(child, new_matcher)?);
                }
            }
        }
        Ok(out)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct BoundGetter {
    #[pyo3(get, set)]
    pub getter: Getter,
    #[pyo3(get, set)]
    pub matcher: IterativeMatcherRc,
}

#[pymethods]
impl BoundGetter {
    #[new]
    pub fn new(getter: Getter, matcher: IterativeMatcherRc) -> Self {
        Self {
            getter,
            matcher: matcher.into(),
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<BTreeSet<CircuitRc>> {
        self.get(circuit, fancy_validate)
    }

    pub fn get(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<BTreeSet<CircuitRc>> {
        self.getter
            .get(circuit, self.matcher.clone(), fancy_validate)
    }

    pub fn get_unique_op(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<Option<CircuitRc>> {
        self.getter
            .get_unique_op(circuit, self.matcher.clone(), fancy_validate)
    }

    pub fn get_unique(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.getter
            .get_unique(circuit, self.matcher.clone(), fancy_validate)
    }

    pub fn validate(&mut self, circuit: CircuitRc) -> Result<()> {
        self.getter.validate(circuit, self.matcher.clone())
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct AnyFound {
    pub(super) cache: cached::UnboundCache<(HashBytes, IterativeMatcherRc), bool>,
}

#[pymethods]
impl AnyFound {
    #[new]
    pub fn new() -> Self {
        Self {
            cache: cached::UnboundCache::new(),
        }
    }
    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
    ) -> Result<bool> {
        self.are_any_found(circuit, matcher)
    }

    pub fn are_any_found(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
    ) -> Result<bool> {
        let out = self.any_impl(circuit, matcher.clone())?;
        Ok(out)
    }

    pub fn bind(&self, matcher: IterativeMatcherRc) -> BoundAnyFound {
        BoundAnyFound {
            any_found: self.clone(),
            matcher,
        }
    }
}

impl AnyFound {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matcher.clone()))]
    #[use_try]
    #[cache_expr(cache)]
    fn any_impl(&mut self, circuit: CircuitRc, matcher: IterativeMatcherRc) -> Result<bool> {
        let IterateMatchResults { updated, found } = matcher.match_iterate(circuit.clone())?;
        if found {
            return Ok(true);
        }

        if !all_finished(&updated) {
            let new_matchers = per_child(updated, matcher, circuit.num_children());
            for (child, new_matcher) in circuit.children().zip(new_matchers) {
                if let Some(new_matcher) = new_matcher {
                    if self_.any_impl(child, new_matcher)? {
                        return Ok(true);
                    }
                }
            }
        }
        Ok(false)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct BoundAnyFound {
    #[pyo3(get, set)]
    pub any_found: AnyFound,
    #[pyo3(get, set)]
    pub matcher: IterativeMatcherRc,
}

#[pymethods]
impl BoundAnyFound {
    #[new]
    pub fn new(any_found: AnyFound, matcher: IterativeMatcherRc) -> Self {
        Self {
            any_found,
            matcher: matcher.into(),
        }
    }

    fn __call__(&mut self, _py: Python<'_>, circuit: CircuitRc) -> Result<bool> {
        self.are_any_found(circuit)
    }

    pub fn are_any_found(&mut self, circuit: CircuitRc) -> Result<bool> {
        self.any_found.are_any_found(circuit, self.matcher.clone())
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Expander {
    /// Note: we don't currently cache these transforms individually. We could
    /// do this.
    #[pyo3(get)]
    pub(super) replacements: Vec<TransformRc>,
    /// Technically, having all of these matchers stored here isn't important
    /// for key functionality (like unused for caching).
    /// This is just nice for calling from python.
    ///
    /// invariant: replacements.len() == matchers.len()
    #[pyo3(get)]
    pub(super) matchers: Vec<IterativeMatcherRc>,
    #[pyo3(set, get)]
    pub ban_multiple_matches_on_node: bool,
    #[pyo3(set, get)]
    pub default_fancy_validate: bool,
    #[pyo3(get)]
    pub(super) suffix: Option<String>,
    pub(super) batch_cache: cached::UnboundCache<(HashBytes, Vec<IterativeMatcherRc>), CircuitRc>,
    pub(super) validation_getter: Getter,
}

impl Default for Expander {
    fn default() -> Self {
        Self {
            replacements: Vec::new(),
            matchers: Vec::new(),
            ban_multiple_matches_on_node: false,
            default_fancy_validate: false,
            suffix: None,
            batch_cache: cached::UnboundCache::new(),
            validation_getter: Default::default(),
        }
    }
}

#[pymethods]
impl Expander {
    #[new]
    #[args(
        expanders = "*",
        ban_multiple_matches_on_node = "Expander::default().ban_multiple_matches_on_node",
        default_fancy_validate = "Expander::default().default_fancy_validate",
        suffix = "None"
    )]
    pub fn new(
        expanders: Vec<(IterativeMatcherRc, TransformRc)>,
        ban_multiple_matches_on_node: bool,
        default_fancy_validate: bool,
        suffix: Option<String>,
    ) -> Self {
        let (matchers, replacements) = expanders
            .into_iter()
            .map(|(a, b)| (a.into(), b.into()))
            .unzip();
        Self {
            replacements,
            matchers,
            ban_multiple_matches_on_node,
            default_fancy_validate,
            suffix,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.batch(circuit, fancy_validate)
    }

    pub fn batch(&mut self, circuit: CircuitRc, fancy_validate: Option<bool>) -> Result<CircuitRc> {
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            for m in &self.matchers {
                self.validation_getter
                    .validate(circuit.clone(), m.clone())?;
            }
        }
        self.batch_impl(circuit, self.matchers.clone())
    }
}

impl Expander {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matchers.clone()))]
    #[use_try]
    #[cache_expr(batch_cache)]
    fn batch_impl(
        &mut self,
        circuit: CircuitRc,
        matchers: Vec<IterativeMatcherRc>,
    ) -> Result<CircuitRc> {
        let results = matchers
            .iter()
            .map(|m| m.match_iterate(circuit.clone()))
            .collect::<Result<Vec<_>>>()?;

        let filtered = results.iter().enumerate().filter(|(_, res)| res.found);

        if let Some((idx, _)) = filtered.clone().next() {
            if self_.ban_multiple_matches_on_node {
                let n_matches = filtered.count();
                if n_matches != 1 {
                    bail!("multiple matches! got {} != 1", n_matches);
                }
            }

            return self_.replacements[idx].run(circuit);
        }

        if results.iter().all(|x| all_finished(&x.updated)) {
            return Ok(circuit);
        }

        let num_children = circuit.num_children();

        let new_matchers: Vec<_> = results
            .into_iter()
            .zip(matchers)
            .map(|(res, matcher)| per_child_with_term(res.updated, matcher, num_children))
            .collect();
        let new_matchers_per = transpose(new_matchers, num_children);
        assert_eq!(new_matchers_per.len(), circuit.num_children());

        let new_children = circuit
            .children()
            .zip(new_matchers_per)
            .map(|(c, new_matchers)| self_.batch_impl(c, new_matchers))
            .collect::<Result<_>>()?;

        Ok(expand_node(circuit, &new_children)?.add_suffix(self_.suffix.as_ref().map(|x| &**x)))
    }

    pub fn suffix(&self) -> Option<&str> {
        self.suffix.as_ref().map(|x| &**x)
    }
}

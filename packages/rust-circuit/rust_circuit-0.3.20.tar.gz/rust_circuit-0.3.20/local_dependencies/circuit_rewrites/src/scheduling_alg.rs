use std::cmp::max;

use itertools::Itertools;
use pyo3::prelude::*;
use rr_util::{
    python_println, sv, timed,
    util::{is_unique, HashBytes},
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use smallvec::SmallVec as Sv;

use crate::{scheduled_execution::SchedulingOOMError, scheduling_z3::schedule_dag_strategy_ints};
pub struct DagSimpSettings {
    pub same_ratio: f64,
    pub tiny_size: usize,
    pub max_exhaustive_size: usize,
    pub max_z3_ints_size: usize,
    pub acceptable_subdag_max: usize,
    pub exhaustive_give_up_ns: usize,
    pub mem_limit: usize,
    pub num_mem_chunks: usize,
    pub timeout: usize,
    pub verbose: usize,
}

impl Default for DagSimpSettings {
    fn default() -> Self {
        Self {
            same_ratio: 0.25,
            tiny_size: 200_000,
            max_exhaustive_size: 60,
            max_z3_ints_size: 4000,
            acceptable_subdag_max: 100_000_000,
            exhaustive_give_up_ns: 40_000,
            verbose: 0,
            timeout: 5_000, // useless defaults, todo fix
            num_mem_chunks: 200,
            mem_limit: 10,
        }
    }
}

// rule: there can be only one edge between each pair of nodes
#[pyclass]
#[derive(Default, Clone, Debug)]
pub struct Dag {
    pub children: Vec<Sv<[u32; 6]>>,
    pub parents: Vec<Sv<[u32; 6]>>,
    /// the cost is the number of new elements computing the node entails allocating.
    /// some nodes compute views into existing memory, such as some indexes and all Arrays
    /// (as they're already allocated), so they have cost 0
    /// if a node computes a new tensor, the cost is the product of the shape.
    pub node_costs: Vec<usize>,
    pub node_to_orig: HashMap<u32, Sv<[u32; 6]>>,
    pub node_hashes: Vec<HashBytes>,
    pub hash_to_node: HashMap<HashBytes, usize>,
    pub pre_root_nodes: Vec<u32>,
}
impl Dag {
    pub fn get_outputs(&self) -> Vec<usize> {
        let result =
            rr_util::util::filter_to_idx(&self.parents.iter().collect(), &mut |y| y.is_empty());
        result
    }

    pub fn expand_order(&self, order: &Vec<u32>) -> Vec<u32> {
        self.pre_root_nodes
            .iter()
            .chain(order.iter().flat_map(|x| self.node_to_orig[x].iter()))
            .cloned()
            .collect()
    }

    pub fn compute_schedule_top_ints(
        &self,
        verbose: usize,
        mem_limit: usize,
        num_mem_chunks: usize,
        timeout: usize,
        required_first: Option<usize>,
    ) -> Result<Vec<u32>, SchedulingOOMError> {
        if self.node_to_orig.len() == 1 {
            return Ok(self.node_to_orig.keys().cloned().collect::<Vec<_>>());
        }
        schedule_dag_strategy_ints(
            &self,
            verbose,
            mem_limit,
            num_mem_chunks,
            timeout,
            required_first,
        )
        .map(|x| x.into_iter().map(|x| x as u32).collect())
    }

    pub fn compute_schedule(
        &self,
        verbose: usize,
        mem_limit: usize,
        num_mem_chunks: usize,
        timeout: usize,
    ) -> Result<Vec<u32>, SchedulingOOMError> {
        let mut self_useds = self.clone();
        self_useds.used_to_beginning();
        self_useds
            .compute_schedule_top_ints(verbose, mem_limit, num_mem_chunks, timeout, None)
            .map(|x| self_useds.expand_order(&x))
    }

    // Renumbers everything! breaks all node references!
    pub fn used_to_beginning(&mut self) {
        let new_to_old: Vec<u32> = self.node_to_orig.keys().cloned().collect();
        let old_to_new: HashMap<u32, u32> = new_to_old
            .iter()
            .enumerate()
            .map(|(i, j)| (*j, i as u32))
            .collect();
        self.node_to_orig = new_to_old
            .iter()
            .enumerate()
            .map(|(i, o)| (i as u32, self.node_to_orig[o].clone()))
            .collect();
        self.children = new_to_old
            .iter()
            .map(|i| {
                self.children[*i as usize]
                    .iter()
                    .map(|j| old_to_new[j])
                    .collect()
            })
            .collect();
        self.parents = new_to_old
            .iter()
            .map(|i| {
                self.parents[*i as usize]
                    .iter()
                    .map(|j| old_to_new[j])
                    .collect()
            })
            .collect();
        self.node_costs = new_to_old
            .iter()
            .map(|x| self.node_costs[*x as usize])
            .collect();
    }

    // UNFINISHED

    // simplify all

    pub fn simplify(&mut self, simp_settings: &DagSimpSettings) -> bool {
        // println!(
        //     "simplifying to_orig {:?} children {:?}",
        //     &self.node_to_orig, &self.children
        // );
        // self.print_cytoscape_link();
        let mut result = false;
        while self.simplify_pass(simp_settings) {
            result = true;
        }
        self.simplify_pass(simp_settings);
        // println!(
        //     "SIMPLIFIED to_orig {:?} children {:?} parents {:?} pre {:?}",
        //     &self.node_to_orig, &self.children, &self.parents, &self.pre_root_nodes
        // );
        // self.print_cytoscape_link();
        result
    }

    // warning: I'm modifying the graph as I'm traversing it. edits must not mess with topo frontier
    pub fn simplify_pass(&mut self, simp_settings: &DagSimpSettings) -> bool {
        // simplify bottom_up
        let mut did_anything = false;

        // we don't re-check whether leaves are still leaves, so
        // no rewrite can add children to an int which previously had no children
        let mut nodes_visited: HashSet<u32> = Default::default();
        let mut bottom_frontier: Vec<u32> = self.get_bottom_frontier();
        let mut parenties: Vec<u32> = vec![];
        while !bottom_frontier.is_empty() {
            let popped = bottom_frontier.pop().unwrap();
            nodes_visited.insert(popped);
            if !self.node_to_orig.contains_key(&popped) {
                continue;
            }
            macro_rules! and_namer {
                ($fnident:expr) => {
                    (stringify!($fnident), $fnident)
                };
            }
            let simps: [(
                &'static str,
                fn(&mut Dag, u32, &DagSimpSettings) -> Option<Vec<u32>>,
            ); 7] = [
                and_namer!(Dag::try_inline_lone_sibling),
                and_namer!(Dag::try_merge_simple_diamond),
                and_namer!(Dag::try_merge_chain_close),
                and_namer!(Dag::try_elim_middle_monotonic),
                and_namer!(Dag::try_merge_half_diamond),
                and_namer!(Dag::try_elim_small_leaf),
                and_namer!(Dag::try_merge_descending_peaks),
            ];
            for (_simp_name, simplification) in simps {
                if let Some(the_parenties) = simplification(self, popped, simp_settings) {
                    parenties = the_parenties;
                    did_anything = true;
                    // println!("did simp {}", simp_name);
                    break;
                }
            }
            // println!("frontier {:?}", &bottom_frontier);
            if self.node_to_orig.contains_key(&popped) {
                for parent in &self.parents[popped as usize] {
                    if self.children[*parent as usize]
                        .iter()
                        .all(|x| nodes_visited.contains(x))
                    {
                        bottom_frontier.push(*parent);
                    }
                }
            } else {
                for parent in &parenties {
                    if self.children[*parent as usize]
                        .iter()
                        .all(|x| nodes_visited.contains(x))
                    {
                        bottom_frontier.push(*parent);
                    }
                }
            }
        }
        if nodes_visited.len() < self.node_to_orig.len() {
            println!("didnt visit enough nodes {:?}", &self);
        }
        did_anything |= self.schedule_isolated(simp_settings);
        // println!("did it {:?}", self.node_to_orig);
        did_anything
    }

    // try simplification at point

    pub fn try_elim_small_leaf(
        &mut self,
        node: u32,
        simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if self.children[node as usize].is_empty() && self.is_tiny(node, simp_settings) {
            let result = Some(self.parents[node as usize].iter().cloned().collect());
            self.seperate_integrate_node(node);
            return result;
        }
        None
    }

    pub fn try_merge_half_diamond(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let [a, b] = self.parents[node as usize][..] {
            if let Some(parent) = self.get_sole_parent(a) && self.parents[b as usize].iter().contains(&parent){
                self.merge_add(node, b, false);
                return Some(Default::default());
            }
            if let Some(parent) = self.get_sole_parent(b) && self.parents[a as usize].iter().contains(&parent){
                self.merge_add(node, a, false);
                return Some(Default::default());
            }
        }
        None
    }

    pub fn try_merge_simple_diamond(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let [a, b] = self.parents[node as usize][..]  && a!=b{
            if self.parents[a as usize].len() == 1
                && self.parents[b as usize].len() == 1
                && self.parents[a as usize][0] == self.parents[b as usize][0]
            {
                let top = self.parents[a as usize][0];
                let new_cost = self.node_costs[a as usize] + self.node_costs[b as usize];
                let intermediate = self.split_node_extra_below(top);
                self.merge_add(intermediate, a, true);
                self.merge_add(intermediate, b, true);
                self.node_costs[intermediate as usize] = new_cost;
                return Some(Default::default());
            }
        }
        None
    }

    pub fn try_merge_chain_close(
        &mut self,
        node: u32,
        simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let Some(parent_node) = self.get_sole_parent(node) {
            if self.are_node_memories_similar(parent_node, node, simp_settings)
                || self.is_tiny(parent_node, simp_settings) && self.is_tiny(node, simp_settings)
            {
                self.merge_larger(node, parent_node, false);
                return Some(Default::default());
            }
        }
        None
    }

    pub fn try_elim_middle_monotonic(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if let Some(parent_node) = self.get_sole_parent(node) {
            if let Some(grandparent_node) = self.get_sole_parent(parent_node) {
                if self.node_costs[node as usize] <= self.node_costs[parent_node as usize]
                    && self.node_costs[parent_node as usize]
                        < self.node_costs[grandparent_node as usize]
                {
                    self.merge_larger(parent_node, grandparent_node, false);
                    return Some(Default::default());
                }
                if self.node_costs[node as usize] >= self.node_costs[parent_node as usize]
                    && self.node_costs[parent_node as usize]
                        >= self.node_costs[grandparent_node as usize]
                {
                    self.merge_larger(node, parent_node, false);
                    return Some(Default::default());
                }
            }
        }
        None
    }

    pub fn try_inline_lone_sibling(
        &mut self,
        node: u32,
        simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        if self.parents[node as usize].len() == 1
            && self.children[self.parents[node as usize][0] as usize].len() > 1
            && self.children[node as usize].is_empty()
        {
            let parent_node = self.parents[node as usize][0];
            if self.node_costs[parent_node as usize] as f64 * simp_settings.same_ratio
                >= self.node_costs[node as usize] as f64
            {
                self.merge_add(node, parent_node, false);
            } else {
                self.inline_sibling(self.parents[node as usize][0], node);
            }
            return Some(Default::default());
        }
        None
    }

    pub fn try_merge_descending_peaks(
        &mut self,
        node: u32,
        _simp_settings: &DagSimpSettings,
    ) -> Option<Vec<u32>> {
        let mut chain = self.get_parent_chain(node);
        if chain.len() <= 3 {
            return None;
        }
        let mut did_anything = false;
        // self.print_cytoscape_link();
        let mut counter = 0;
        while !chain.is_empty() {
            // println!(
            //     "merging descending peaks {:?}",
            //     chain
            //         .iter()
            //         .map(|x| (*x, self.node_costs[*x as usize]))
            //         .collect::<Vec<_>>()
            // );
            let max_val = chain
                .iter()
                .map(|x| self.node_costs[*x as usize])
                .max()
                .unwrap();
            let max_pos = chain
                .iter()
                .position(|x| self.node_costs[*x as usize] == max_val)
                .unwrap();
            // println!("max pos {}", max_pos);
            if counter != 0 {
                for i in 1..max_pos + 1 {
                    did_anything = true;
                    self.merge_larger(chain[0], chain[i], false);
                }
            }
            chain.drain(0..max_pos + 1);
            if chain.is_empty() {
                break;
            }
            let min_val = chain
                .iter()
                .map(|x| self.node_costs[*x as usize])
                .min()
                .unwrap();
            let min_pos = chain.len()
                - 1
                - chain
                    .iter()
                    .rev()
                    .position(|x| self.node_costs[*x as usize] == min_val)
                    .unwrap();
            // println!("min pos {}", min_pos);
            for i in 1..min_pos {
                did_anything = true;
                self.merge_larger(chain[0], chain[i], false);
            }
            chain.drain(0..min_pos + 1);
            counter += 1;
        }
        if did_anything {
            // self.print_cytoscape_link();
            return Some(vec![]);
        }
        None
    }

    // composite rewrites
    pub fn inline_sibling(&mut self, parent: u32, child: u32) {
        let new_lower = self.split_node_extra_below(parent);
        self.merge_add(child, new_lower, false);
    }

    // raw rewrites

    pub fn merge_add(&mut self, target: u32, absorbed: u32, is_target_top: bool) {
        let to_add = self.node_costs[absorbed as usize];
        self.merge_nodes(target, absorbed, is_target_top);
        self.node_costs[target as usize] += to_add;
    }

    pub fn merge_larger(&mut self, target: u32, absorbed: u32, is_target_top: bool) {
        let new_node_cost = max(
            self.node_costs[absorbed as usize],
            self.node_costs[target as usize],
        );
        self.merge_nodes(target, absorbed, is_target_top);
        self.node_costs[target as usize] = new_node_cost;
    }

    // doesn't change node_costs. you have to change this yourself
    pub fn merge_nodes(&mut self, target: u32, absorbed: u32, is_target_top: bool) {
        assert!(target != absorbed);
        if !self.node_to_orig.contains_key(&target) {
            self.print_cytoscape_link();
            dbg!(self);
            panic!("target not in graph")
        }
        self.children[target as usize] = self.children[target as usize]
            .iter()
            .chain(self.children[absorbed as usize].iter())
            .filter(|x| **x != absorbed && **x != target)
            .unique()
            .cloned()
            .collect();
        self.parents[target as usize] = self.parents[target as usize]
            .iter()
            .chain(self.parents[absorbed as usize].iter())
            .filter(|x| **x != absorbed && **x != target)
            .unique()
            .cloned()
            .collect();
        for absorbed_child in &self.children[absorbed as usize] {
            self.parents[*absorbed_child as usize] = self.parents[*absorbed_child as usize]
                .iter()
                .map(|x| if *x == absorbed { target } else { *x })
                .unique()
                .collect();
        }
        for absorbed_parent in &self.parents[absorbed as usize] {
            self.children[*absorbed_parent as usize] = self.children[*absorbed_parent as usize]
                .iter()
                .map(|x| if *x == absorbed { target } else { *x })
                .unique()
                .collect();
        }

        let removed_to_orig = if is_target_top {
            self.node_to_orig
                .remove(&absorbed)
                .unwrap()
                .into_iter()
                .chain(self.node_to_orig[&target].clone())
                .collect()
        } else {
            self.node_to_orig[&target]
                .clone()
                .into_iter()
                .chain(self.node_to_orig.remove(&absorbed).unwrap())
                .collect()
        };
        self.node_to_orig.insert(target, removed_to_orig);
    }

    pub fn split_node_extra_below(&mut self, node: u32) -> u32 {
        let new_id = self.node_costs.len() as u32;
        assert_eq!(self.node_costs.len(), self.children.len());
        assert_eq!(self.node_costs.len(), self.parents.len());
        self.node_costs.push(self.node_costs[node as usize]);
        self.node_to_orig.insert(new_id, sv![]);
        self.children.push(self.children[node as usize].clone());
        self.parents.push(sv![node]);
        self.children[node as usize] = sv![new_id];
        for child in &self.children[new_id as usize] {
            for x in self.parents[*child as usize].iter_mut() {
                if *x == node {
                    *x = new_id;
                }
            }
        }
        new_id
    }

    pub fn seperate_integrate_node(&mut self, node: u32) {
        assert!(self.children[node as usize].is_empty());
        let cost = self.node_costs[node as usize];
        for parent in &self.parents[node as usize] {
            self.children[*parent as usize] = self.children[*parent as usize]
                .iter()
                .filter(|x| **x != node)
                .cloned()
                .collect();
            self.node_costs[*parent as usize] += cost;
        }
        self.pre_root_nodes
            .extend(self.node_to_orig.remove(&node).unwrap());
    }

    // passes

    // schedule isolated pass
    pub fn schedule_isolated(&mut self, settings: &DagSimpSettings) -> bool {
        let isolated = self.find_isolated(settings);
        // self.print_cytoscape_link();
        // println!("{:?} ", &isolated);
        for iso in &isolated {
            let direct_only_sub = self.get_direct_only_sub(&iso.2);
            // direct_only_sub.print_cytoscape_link();
            let required_first = Some(
                *direct_only_sub
                    .node_to_orig
                    .iter()
                    .find(|(_k, v)| v[0] == iso.1)
                    .unwrap()
                    .0,
            );
            let order: Vec<(u32, usize)> = if iso.2.len() < settings.max_exhaustive_size
                || iso.2.len() > settings.max_exhaustive_size
            {
                timed!(
                    direct_only_sub
                        .schedule_exhaustive(required_first, settings)
                        .iter()
                        .map(|(k, v)| (direct_only_sub.node_to_orig[k][0], *v))
                        .collect(),
                    10,
                    settings.verbose >= 2
                )
            } else {
                let order = direct_only_sub
                    .compute_schedule_top_ints(
                        settings.verbose,
                        settings.mem_limit,
                        settings.num_mem_chunks,
                        settings.timeout,
                        required_first.map(|x| x as usize),
                    )
                    .unwrap();
                let inner_and_costs = direct_only_sub.get_costs_of_order(
                    &order, // bad unwrap todo fix
                );
                let result: Vec<(u32, usize)> = inner_and_costs
                    .into_iter()
                    .map(|(n, c)| (direct_only_sub.node_to_orig[&n][0], c))
                    .collect();
                if result.len() != direct_only_sub.node_costs.len() || !is_unique(&order) {
                    panic!(
                        "order wrong length {:?} {:?}, {}",
                        &order,
                        &result,
                        direct_only_sub.node_costs.len()
                    )
                }
                result
            };
            // assert!(order[0].0==iso.1 && order.last().unwrap().0==iso.0);
            self.replace_isolated_with_linear(&order);
            // println!("FINISHED ISOLATED SCHEDULE");
        }
        // self.print_cytoscape_link();
        !isolated.is_empty()
    }

    pub fn find_isolated(&self, _settings: &DagSimpSettings) -> Vec<(u32, u32, HashSet<u32>)> {
        let mut result = vec![];
        for &upper in self.node_to_orig.keys() {
            let mut done: HashSet<u32> = HashSet::from_iter([upper]);
            let mut frontier: Vec<u32> = self.children[upper as usize]
                .iter()
                .filter(|x| self.parents[**x as usize].len() == 1)
                .cloned()
                .collect();
            let mut children: HashSet<u32> =
                self.children[upper as usize].iter().cloned().collect();
            while !frontier.is_empty() {
                let popped = frontier.pop().unwrap();
                done.insert(popped);
                children.remove(&popped);
                if self.parents[popped as usize]
                    .iter()
                    .any(|x| !done.contains(x))
                {
                    break;
                }
                if children.is_empty() {
                    if done.len() > 3 {
                        result.push((upper, popped, done.clone()));
                    }
                    break;
                }
                // if self.children[popped as usize].is_empty() {
                //     break;
                // }
                children.extend(&self.children[popped as usize]);
                for &child in &self.children[popped as usize] {
                    if self.parents[child as usize]
                        .iter()
                        .all(|x| done.contains(x))
                    {
                        frontier.push(child);
                    }
                }
            }
        }
        result.sort_by(|a, b| a.2.len().cmp(&b.2.len()));
        result
    }

    pub fn schedule_exhaustive(
        &self,
        entry_point: Option<u32>,
        settings: &DagSimpSettings,
    ) -> Vec<(u32, usize)> {
        let mut parents_left: Vec<i32> = self.parents.iter().map(|x| x.len() as i32).collect();
        let mut children_left: Vec<i32> = self.children.iter().map(|x| x.len() as i32).collect();
        let mut best: (Vec<(u32, usize)>, usize) = (vec![], settings.mem_limit + 1);
        let mut order: Vec<(u32, u32, usize)> = Vec::with_capacity(self.node_costs.len());

        let mut options_stack: Vec<Sv<[u32; 16]>> = Vec::with_capacity(self.node_costs.len() + 2);
        options_stack.push(
            entry_point
                .map(|z| sv![z])
                .unwrap_or(filter_to_idx(&children_left, |x| *x == 0).collect()),
        );
        // want functions that modify stuff, using macros :|
        macro_rules! choose {
            ($i:expr) => {{
                let options = options_stack.last().unwrap();
                let choice = options[$i as usize] as u32;
                for child in &self.children[choice as usize] {
                    parents_left[*child as usize] -= 1;
                }
                for parent in &self.parents[choice as usize] {
                    children_left[*parent as usize] -= 1;
                }
                children_left[choice as usize] -= 1;
                let cost: usize = (0..parents_left.len() as u32)
                    .filter(|i| children_left[*i as usize] < 0 && parents_left[*i as usize] >= 1)
                    .map(|x| self.node_costs[x as usize])
                    .sum();
                order.push((choice, $i, cost));
                options_stack.push(filter_to_idx(&children_left, |x| *x == 0).collect())
            }};
        }
        macro_rules! pop {
            () => {{
                let popped = order.pop().unwrap();
                options_stack.pop();
                let choice = popped.0;
                // println!("choice {}", choice);
                for child in &self.children[choice as usize] {
                    parents_left[*child as usize] += 1;
                }
                for parent in &self.parents[choice as usize] {
                    children_left[*parent as usize] += 1;
                }
                children_left[choice as usize] += 1;
                // println!("popped");
                // dbg!(&order, &options_stack, &parents_left, &children_left, &live);

                popped.1
            }};
        }
        macro_rules! backtrack {
            () => {{
                while !order.is_empty()
                    && order.last().unwrap().1 + 1 >= options_stack[order.len() - 1].len() as u32
                {
                    pop!();
                }
                if !order.is_empty() {
                    let popped_idx = pop!();
                    if !order.is_empty() {
                        choose!(popped_idx + 1);
                    }
                }
            }};
        }
        let start_instant = std::time::Instant::now();
        loop {
            // dbg!(&order, &options_stack, &parents_left, &children_left, &live);
            if order.len() == self.node_costs.len() {
                best = (
                    order.iter().map(|(a, _b, c)| (*a, *c)).collect(),
                    *order.iter().map(|(_n, _i, c)| c).max().unwrap(),
                );
                if best.1 < settings.acceptable_subdag_max {
                    if start_instant.elapsed().as_nanos() > settings.exhaustive_give_up_ns as u128 {
                        break;
                    }
                }
                backtrack!();
            } else {
                choose!(0);
                if order.last().unwrap().2 >= best.1 {
                    backtrack!();
                }
            }
            if order.len() == 0 {
                break;
            }
        }
        best.0
    }

    pub fn replace_isolated_with_linear(&mut self, order: &Vec<(u32, usize)>) {
        // println!("linearizing order {:?}", order);
        // because this is isolated except for first children and last parents,
        // we don't need to fix up any backrefs
        for (i, (node, cost)) in order.iter().enumerate() {
            if i != 0 {
                self.children[*node as usize] = sv![order[i - 1 as usize].0];
            }
            if i != order.len() - 1 {
                self.parents[*node as usize] = sv![order[i + 1 as usize].0];
                self.node_costs[*node as usize] = *cost;
            }
        }
    }

    // util

    pub fn are_node_memories_similar(
        &self,
        a: u32,
        b: u32,
        simp_settings: &DagSimpSettings,
    ) -> bool {
        let result = (self.node_costs[a as usize] as f64 - self.node_costs[b as usize] as f64)
            .abs()
            < simp_settings.same_ratio
                * (self.node_costs[a as usize] as f64 + self.node_costs[b as usize] as f64)
                / 2.0;
        result
    }

    pub fn get_sole_parent(&self, node: u32) -> Option<u32> {
        if self.parents[node as usize].len() == 1
            && self.children[self.parents[node as usize][0] as usize].len() == 1
        {
            return Some(self.parents[node as usize][0]);
        }
        return None;
    }

    pub fn is_tiny(&self, node: u32, settings: &DagSimpSettings) -> bool {
        self.node_costs[node as usize] < settings.tiny_size
    }

    pub fn get_bottom_frontier(&self) -> Vec<u32> {
        self.node_to_orig
            .iter()
            .filter(|(k, _n)| self.children[**k as usize].len() == 0)
            .map(|(k, _n)| *k)
            .collect()
    }

    pub fn get_parent_chain(&self, node: u32) -> Vec<u32> {
        let mut result = vec![node];
        while self.parents[*result.last().unwrap() as usize].len() == 1
            && self.children[self.parents[*result.last().unwrap() as usize][0] as usize].len() == 1
        {
            result.push(self.parents[*result.last().unwrap() as usize][0]);
        }
        result
    }

    pub fn get_direct_only_sub(&self, set: &HashSet<u32>) -> Dag {
        let ordered: Vec<u32> = set.iter().cloned().collect();
        Dag {
            children: set
                .iter()
                .map(|x| {
                    self.children[*x as usize]
                        .iter()
                        .filter_map(|y| ordered.iter().position(|z| z == y).map(|z| z as u32))
                        .collect()
                })
                .collect(),
            parents: ordered
                .iter()
                .map(|x| {
                    self.parents[*x as usize]
                        .iter()
                        .filter_map(|y| ordered.iter().position(|z| z == y).map(|z| z as u32))
                        .collect()
                })
                .collect(),
            node_costs: ordered
                .iter()
                .map(|x| self.node_costs[*x as usize])
                .collect(),
            node_to_orig: ordered
                .iter()
                .enumerate()
                .map(|(i, x)| (i as u32, sv![*x]))
                .collect(),
            node_hashes: vec![],
            hash_to_node: Default::default(),
            pre_root_nodes: vec![],
        }
    }

    pub fn get_costs_of_order(&self, order: &[u32]) -> Vec<(u32, usize)> {
        let mut children: Vec<i32> = self.children.iter().map(|x| x.len() as i32).collect();
        let mut parents: Vec<i32> = self.parents.iter().map(|x| x.len() as i32).collect();
        let mut result = vec![];
        for o in order {
            children[*o as usize] -= 1;
            for parent in &self.parents[*o as usize] {
                children[*parent as usize] -= 1;
            }
            for child in &self.children[*o as usize] {
                parents[*child as usize] -= 1;
            }
            result.push((
                *o,
                self.node_to_orig
                    .keys()
                    .filter_map(|i| {
                        if children[*i as usize] < 0 && parents[*i as usize] >= 1 {
                            Some(self.node_costs[*i as usize])
                        } else {
                            None
                        }
                    })
                    .sum(),
            ));
        }
        result
    }

    // misc
    pub fn print_cytoscape_link(&self) {
        let not_excaped = format!(
            "{{\"graphName\":\"\",\"graphValue\":[{},{}]}}",
            self.node_to_orig
                .keys()
                .map(|i| format!(
                    "{{\"id\":\"{}\",\"name\":{:?},\"label\": \"{}: {}\"}}",
                    i, "", *i, self.node_costs[*i as usize]
                ))
                .collect::<Vec<_>>()
                .join(","),
            self.node_to_orig
                .keys()
                .flat_map(|i| self.children[*i as usize]
                    .iter()
                    .map(|j| format!(
                        "{{\"source\":\"{}\",\"target\":\"{}\",\"label\": \"\"}}",
                        i, j
                    ))
                    .collect::<Vec<_>>())
                .collect::<Vec<_>>()
                .join(",")
        );
        python_println!(
            "http://104.171.200.179:4573/#/networkgraph/{}",
            url_escape::encode_fragment(&not_excaped)
        )
    }
}

pub fn filter_to_idx<'a, T, F>(col: &'a [T], f: F) -> impl Iterator<Item = u32> + 'a
where
    F: Fn(&T) -> bool + 'a,
{
    col.iter()
        .enumerate()
        .filter(move |(_i, x)| f(x))
        .map(|(i, _x)| i as u32)
}

#![feature(let_chains)]
#![allow(clippy::borrow_deref_ref)]
use std::{
    collections::{BTreeMap, BTreeSet},
    fmt::{self, Debug},
    hash::Hash,
    iter::zip,
    ops::{Deref, DerefMut},
    sync::Arc,
};

use anyhow::{anyhow, bail, Context, Result};
use circuit_utils::{toposort_circuit, OperatorPriority};
pub use computational_node::{
    flat_concat, flat_concat_back, Add, Concat, Conv, Einsum, Index, Rearrange, Scatter,
};
pub use constant::{Array, Scalar, Symbol};
pub use cumulant::Cumulant;
pub use generalfunction::{GeneralFunction, GeneralFunctionSpec};
use itertools::Itertools;
use macro_rules_attribute::apply;
pub use module::{Module, ModuleArgSpec, ModuleSpec};
use num_bigint::BigUint;
use opaque_iterative_matcher::OpaqueIterativeMatcherVal;
use print::PrintOptions;
use print_html::{PrintHtmlOptions, PrintOptionsBase};
use pyo3::{
    exceptions::{self, PyValueError},
    prelude::*,
    pyclass::CompareOp,
    PyTypeInfo,
};
use rr_util::{
    cached_lambda,
    eq_by_big_hash::EqByBigHash,
    py_types::{reduction_to_ints, use_rust_comp, PyOpAtAxes, PyShape, Tensor, PY_CIRCUIT_ITEMS},
    pycall, pycallable, python_error_exception,
    rearrange_spec::{OpSize, PyCountsAtAxes, RInnerInts, RearrangeSpec},
    sv,
    symbolic_size::{SymbolicSizeConstraints, SymbolicSizeProduct},
    tensor_util::{check_canon_idxs, Shape, TensorIndex, TorchDeviceDtype, TorchDeviceDtypeOp},
    util::{
        arc_ref_clone, arc_unwrap_or_clone, AsOp, AxisInt, EinsumAxes, HashBytes, HashBytesToPy,
    },
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
pub use set_symbolic_size::SetSymbolicShape;
use thiserror::Error;
pub use variable_nodes::{DiscreteVar, StoredCumulantVar, Tag};

use crate::{module::substitute_all_modules, print::print_circuit_stats};
pub mod circuit_utils;
pub mod computational_node;
pub mod constant;
pub mod cumulant;
pub mod expand_node;
pub mod generalfunction;
pub mod module;
pub mod named_axes;
pub mod nrc;
pub mod opaque_iterative_matcher;
pub mod parsing;
pub mod print;
pub mod print_html;
pub mod set_symbolic_size;
pub mod variable_nodes;

mod circuit_node_private;
use circuit_node_private::*;

use self::circuit_utils::total_flops;
use crate::circuit_utils::total_arrayconstant_size;

fn check_canon_axes(rank: usize, axes: &[i64]) -> Result<Vec<usize>> {
    check_canon_idxs(rank, axes).context("axis out of bounds")
}
fn check_canon_axes_as(rank: usize, axes: &[i64]) -> Result<RInnerInts> {
    Ok(check_canon_axes(rank, axes)?
        .into_iter()
        .map(|x| x as u8)
        .collect())
}

pub type NamedAxes = BTreeMap<AxisInt, String>;

pub trait CircuitNodeSelfOnlyHash {
    fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher);
}

#[macro_export]
macro_rules! circuit_node_self_only_hash_default_impl {
    ($type_name:ty) => {
        impl $crate::CircuitNodeSelfOnlyHash for $type_name {
            fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher) {
                use $crate::circuit_node_private::CircuitNodeHashItems;
                self.compute_hash_non_name_non_children(hasher)
            }
        }
    };
}

pub trait CircuitNode: CircuitNodeInit + CircuitNodeSelfOnlyHash {
    // ==== implementable section ===
    //
    // NOTE: ALL FNS IN THIS SECTION *MUST* BE COPIED TO THE CIRCUIT NODE UNION IMPL!
    // If you add something here with a default impl, write a new impl for circuit node union!
    // (up until default only section)
    //
    // we could enforce this sort of stuff with some proc macros, but seems like overkill atm.

    fn info(&self) -> &CachedCircuitInfo;
    fn name(&self) -> Option<&str>;

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>>;

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_>;

    fn non_free_children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        self.children()
    }

    fn map_children_enumerate<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>;

    fn map_non_free_children_enumerate<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        self.map_children_enumerate(f)
    }

    fn node_type_uuid(&self) -> [u8; 16];

    fn self_flops(&self) -> BigUint {
        BigUint::from(0usize)
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor>;

    /// At most how many elements will evaluating this circuit require allocating
    /// new memory (that we are allowed to free ourselves) for? Used to improve scheduling.
    fn intermediate_cost_bound(&self) -> usize {
        self.info().numel_usize()
    }

    fn c(self) -> Circuit;
    fn rc(self) -> CircuitRc;

    /// for nodes with fixed uuid, should be same as node_type_uuid
    fn static_node_type_uuid() -> [u8; 16]
    where
        Self: Sized,
    {
        *uuid::Uuid::nil().as_bytes()
    }

    // ==== default only section ===
    // FUNCTIONS BELOW HERE *shouldn't* be overridden by implementors!
    // (if you do implement, this won't be picked up on by CircuitNodeDefer (union types etc)!)

    fn hash_base16(&self) -> String {
        base16::encode_lower(&self.info().hash)
    }

    fn init_info(self) -> Result<Self>
    where
        Self: Sized,
    {
        self.init_info_impl()
    }
    fn rename(self, new_name: Option<String>) -> Self
    where
        Self: Sized,
    {
        self.rename_impl(new_name)
    }
    fn update_info<F>(self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnOnce(&mut CachedCircuitInfo),
    {
        self.update_info_impl(f)
    }

    // implementation helper
    fn already_set_named_axes(&self) -> Option<NamedAxes> {
        (!self.info().named_axes.is_empty()).then(|| self.info().named_axes.clone())
    }

    fn crc(&self) -> CircuitRc
    where
        Self: Clone,
    {
        self.clone().rc()
    }
    fn name_cloned(&self) -> Option<String> {
        self.name().map(|x| x.to_owned())
    }

    // TODO: add more map utils for non_free as needed

    fn num_children(&self) -> usize {
        // not exactly peak efficiency...
        self.children().count()
    }

    fn map_children<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        self.map_children_enumerate(|_i, x| f(x))
    }
    fn map_non_free_children<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        self.map_non_free_children_enumerate(|_i, x| f(x))
    }

    fn map_children_idxs<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize) -> Result<CircuitRc>,
    {
        self.map_children_enumerate(|i, _x| f(i))
    }

    fn map_children_unwrap<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        self.map_children(|x| Ok(f(x))).unwrap()
    }
    fn map_non_free_children_unwrap<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        self.map_non_free_children(|x| Ok(f(x))).unwrap()
    }

    fn map_children_unwrap_enumerate<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> CircuitRc,
    {
        self.map_children_enumerate(|i, x| Ok(f(i, x))).unwrap()
    }

    fn map_children_unwrap_idxs<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(usize) -> CircuitRc,
    {
        self.map_children_enumerate(|i, _x| Ok(f(i))).unwrap()
    }

    /// if any return Some, return child mapped, otherwise None
    fn map_children_op<F>(&self, mut f: F) -> Option<Self>
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> Option<CircuitRc>,
    {
        let mut any_modified = false;
        let out = self.map_children_unwrap(|x| {
            if let Some(new) = f(x.clone()) {
                any_modified = true;
                new
            } else {
                x
            }
        });
        if any_modified {
            Some(out)
        } else {
            None
        }
    }

    fn repr(&self) -> Result<String>
    where
        Self: Clone,
    {
        PrintOptions::repr(&Default::default(), self.crc())
    }

    fn print(&self) -> Result<()>
    where
        Self: Clone,
    {
        rr_util::python_println!("{}", self.repr()?);
        Ok(())
    }

    fn repru(&self) -> String
    where
        Self: Clone,
    {
        self.repr().unwrap()
    }

    fn printu(&self)
    where
        Self: Clone,
    {
        self.print().unwrap()
    }

    fn debug_repr(&self) -> Result<String>
    where
        Self: Clone,
    {
        print::debug_repr(self.crc())
    }

    fn debug_repru(&self) -> String
    where
        Self: Clone,
    {
        self.debug_repr().unwrap()
    }

    fn get_hash(&self) -> HashBytes {
        self.info().hash
    }

    fn rank(&self) -> usize {
        self.info().rank()
    }
    fn ndim(&self) -> usize {
        self.info().rank()
    }
    fn shape(&self) -> &Shape {
        &self.info().shape
    }
    fn numel(&self) -> usize {
        self.info().numel_usize()
    }

    fn sum(&self, axes: &[i64], name: Option<String>) -> Result<Einsum>
    where
        Self: Clone,
    {
        let axes = check_canon_axes_as(self.info().rank(), axes)?;
        Ok(Einsum::new(
            vec![(self.crc(), (0u8..self.info().rank() as u8).collect())],
            (0u8..self.info().rank() as u8)
                .filter(|i| !axes.contains(&i))
                .collect(),
            name,
        ))
    }

    fn mean(&self, axes: &[i64], name: Option<String>) -> Result<Einsum>
    where
        Self: Clone,
    {
        let total_size: usize = check_canon_axes_as(self.info().rank(), axes)?
            .into_iter()
            .map(|i| self.info().shape[i as usize])
            .product();
        self.sum(axes, name)?
            .mul(Scalar::nrc(1. / (total_size as f64), sv![], None), None)
    }

    fn reduce(&self, op_name: String, axes: &[i64], name: Option<String>) -> Result<Circuit>
    where
        Self: Clone,
    {
        match op_name.as_str() {
            "mean" => return self.mean(axes, name).map(CircuitNode::c),
            "sum" => return self.sum(axes, name).map(CircuitNode::c),
            _ => (),
        }

        let axes = check_canon_axes_as(self.info().rank(), axes)?;

        Ok(GeneralFunction::new_by_name(
            vec![Rearrange::nrc(
                self.crc(),
                RearrangeSpec::combine_axes_at_end(self.info().rank().try_into()?, axes).unwrap(),
                None,
            )],
            op_name,
            name,
        )
        .unwrap()
        .c())
    }
    fn min_(&self, axes: &[i64], name: Option<String>) -> Result<Circuit>
    where
        Self: Clone,
    {
        self.reduce("min".to_owned(), axes, name)
    }
    fn max_(&self, axes: &[i64], name: Option<String>) -> Result<Circuit>
    where
        Self: Clone,
    {
        self.reduce("max".to_owned(), axes, name)
    }
    fn add(&self, other: CircuitRc, name: Option<String>) -> Result<Add>
    where
        Self: Clone,
    {
        Add::try_new(vec![self.crc(), other], name)
    }
    fn sub(&self, other: CircuitRc, name: Option<String>) -> Result<Add>
    where
        Self: Clone,
    {
        let other_neg_name = other.name().map(|s| format!("neg {}", s));
        self.add(
            Einsum::scalar_mul(other, -1.0, other_neg_name, Some("neg_1".to_owned())).rc(),
            name,
        )
    }
    fn mul(&self, other: CircuitRc, name: Option<String>) -> Result<Einsum>
    where
        Self: Clone,
    {
        Einsum::elementwise_broadcasted(vec![self.crc(), other], name)
    }
    fn mul_scalar(
        &self,
        scalar: f64,
        name: Option<String>,
        scalar_name: Option<String>,
    ) -> Result<Einsum>
    where
        Self: Clone,
    {
        self.mul(Scalar::nrc(scalar, sv![], scalar_name), name)
    }
    fn index(&self, index: TensorIndex, name: Option<String>) -> Result<Index>
    where
        Self: Clone,
    {
        Index::try_new(self.crc(), index, name)
    }
    fn expand_at_axes(
        &self,
        axes: Vec<usize>,
        counts: Vec<usize>,
        name: Option<String>,
    ) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::expand_at_axes(self.info().rank(), axes, counts)?,
            name,
        ))
    }
    fn unsqueeze(&self, axes: Vec<usize>, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unsqueeze(self.info().rank(), axes)?,
            name,
        ))
    }
    fn squeeze(&self, axes: PyOpAtAxes, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        let axes = check_canon_axes_as(
            self.info().rank(),
            &reduction_to_ints(Some(axes), self.info().rank()),
        )?;
        if axes.iter().any(|i| self.info().shape[*i as usize] != 1) {
            bail!(anyhow!(
                "trying to squeeze non-1 axes, shape {:?} axes {:?}",
                &self.info().shape,
                &axes
            ))
        }
        let num_ints = self.info().rank() - axes.len();
        let mut input_ints = sv![];
        let mut counter = 0;
        for i in 0..self.info().rank() as u8 {
            if axes.iter().contains(&i) {
                input_ints.push(sv![])
            } else {
                input_ints.push(sv![counter]);
                counter += 1;
            }
        }
        Rearrange::try_new(
            self.crc(),
            RearrangeSpec {
                input_ints,
                output_ints: (0..num_ints).map(|i| sv![i as u8]).collect(),
                int_sizes: sv![OpSize::NONE;num_ints],
            },
            name,
        )
    }
    fn flatten(&self, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::flatten_usize(self.ndim())?,
            name,
        ))
    }
    fn unflatten(&self, shape: Shape, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Rearrange::unflatten(self.crc(), shape, name)
    }
    fn unflatten_axis(&self, axis: i64, shape: Shape, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unflatten_axis(self.ndim(), axis, shape)?,
            name,
        ))
    }
    fn unflatten_axis_usize(
        &self,
        axis: usize,
        shape: Shape,
        name: Option<String>,
    ) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unflatten_axis_usize(self.ndim(), axis, shape)?,
            name,
        ))
    }
    fn rearrange(&self, spec: RearrangeSpec, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Rearrange::try_new(self.crc(), spec, name)
    }
    fn rearrange_str(&self, string: &str, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Rearrange::from_string(self.crc(), string, name)
    }
    fn add_suffix(self, suffix: Option<&str>) -> Self
    where
        Self: Sized,
    {
        match suffix {
            Some(suffix) => {
                let name = self.name().map(|x| format!("{}_{}", x, suffix));
                self.rename_impl(name)
            }
            None => self,
        }
    }
}

pub trait CircuitNodeAutoName: CircuitNode {
    /// There are three kinds of automatically generated names:
    /// - infix, like Add and Einsum. Parenthesis are added around children which would have had wrong priority
    /// - functions, like GeneralFunction and Cumulant, which use the standard function notation f(x1, ... xn)
    /// - postfix, like Rearrange and index, which behave like the unary operator "!". Parenthesis are added if needed
    /// utils to add the parenthesis can be found in circuit_utils.rs
    fn auto_name(&self, name: Option<String>) -> Option<String>;

    const PRIORITY: OperatorPriority = OperatorPriority::NotOperator {};
    const CHILD_NAME_MAX_LEN: usize = 100; // TODO: fix me!
    /// we shorten children names on multi child nodes
    fn shorten_child_name(name: &str) -> String {
        if name.len() > Self::CHILD_NAME_MAX_LEN {
            name[..Self::CHILD_NAME_MAX_LEN].to_owned() + "..."
        } else {
            name.to_owned()
        }
    }
}

pub trait CircuitNodeDefer: CircuitNodeInit {
    fn as_trait_obj(&self) -> &dyn CircuitNode;
    fn map_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>;
    fn map_non_free_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>;
    fn custom_c(self) -> Circuit;
    fn custom_rc(self) -> CircuitRc;
}

pub trait CircuitNodeUnion {
    type TypeTag;
    fn variant_string(&self) -> String;
    fn type_tag(&self) -> Self::TypeTag;
}

// not really needed to be so pedantic with ::std::...
#[macro_export]
macro_rules! circuit_node_eq_ord_debug {
    ($type_name:ty) => {
        rr_util::impl_eq_by_big_hash!($type_name);

        impl ::std::cmp::Ord for $type_name {
            fn cmp(&self, other: &Self) -> ::std::cmp::Ordering {
                use $crate::prelude::*;
                // name and then
                (self.name(), self.info().hash).cmp(&(other.name(), other.info().hash))
            }
        }

        impl ::std::cmp::PartialOrd for $type_name {
            fn partial_cmp(&self, other: &Self) -> ::std::option::Option<::std::cmp::Ordering> {
                Some(::std::cmp::Ord::cmp(self, other))
            }
        }

        impl std::fmt::Debug for $type_name {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                f.write_str(&self.debug_repru())
            }
        }
    };
}

// this is what peak rust development looks like
#[doc(hidden)]
#[macro_export]
macro_rules! define_circuit_union_impl {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        #[derive(::std::clone::Clone,pyo3::FromPyObject)]
        pub enum $name {
            $(
                $x($x),
            )*
        }

        paste::paste! {
            #[macro_export]
            macro_rules! [<$name:snake _map>] {
                ($match_expr:expr; $wrap_name:ident => $e:expr) => (
                    [<$name:snake _map_construct>]!($match_expr; ($wrap_name, __constructor_name) => $e)
                )
            }

            #[macro_export]
            macro_rules! [<$name:snake _map_construct>] {
                ($match_expr:expr; ($wrap_name:ident, $constructor_name:ident) => $e:expr) => (
                    match $match_expr {
                    $(
                        $name::$x($wrap_name) => {
                            let $constructor_name = $name::$x;
                            $e
                        },
                    )*
                    }
                )
            }

            #[macro_export]
            macro_rules! [<on_ $name:snake _names>] {
                ($m:ident) => (
                    $m!( $( $x,)*);
                )
            }
        }

        impl rr_util::eq_by_big_hash::EqByBigHash for $name {
            fn hash(&self) -> rr_util::util::HashBytes {
                self.info().hash
            }
        }

        paste::paste! {
            #[derive(Debug, Clone, Copy, Eq, PartialEq, Hash, PartialOrd, Ord)]
            pub enum [<$name Type>] {
                $(
                    $x,
                )*
            }


            impl<'source> pyo3::FromPyObject<'source> for [<$name Type>] {
                fn extract(inp: &'source pyo3::PyAny) -> pyo3::PyResult<Self> {
                    use pyo3::{ types::PyType};

                    let pairings: Vec<(Py<PyType>, [<$name Type>])> =
                        Python::with_gil(|py| vec![
                        $(
                            ($x::type_object(py).into(), [<$name Type>]::$x),
                        )*
                        ]);

                    for (t, out) in pairings {
                        if t.is(inp) {
                            return Ok(out);
                        }
                    }

                    Err(PyErr::new::<exceptions::PyTypeError, _>(format!(
                        "Expected one of the {} types",
                        stringify!($name)
                    )))
                }
            }

            impl pyo3::IntoPy<pyo3::PyObject> for [<$name Type>] {
                fn into_py(self, py: pyo3::Python<'_>) -> pyo3::PyObject {
                    match self {
                        $(
                            Self::$x => $x::type_object(py).into(),
                        )*
                    }
                }
            }

            impl std::fmt::Display for [<$name Type>] {
                fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                    let out = match self {
                        $(
                        Self::$x => stringify!($x),
                        )*
                    };
                    f.write_str(out)
                }
            }

            impl std::str::FromStr for [<$name Type>] {
                type Err = anyhow::Error;
                fn from_str(s: &str) -> Result<Self, Self::Err> {
                    let out = match s {
                        $(
                        stringify!($x) => Self::$x,
                        )*
                        v => bail!($crate::parsing::ParseCircuitError::InvalidVariant {
                            v: v.to_owned()
                        }),
                    };
                    Ok(out)
                }
            }

        }


        circuit_node_eq_ord_debug!($name);

        paste::paste! {
            $(
                impl $name {
                    pub fn [<into_ $x:snake>](self) -> Option<$crate::$x> {
                        self.into_op()
                    }
                    pub fn [<as_ $x:snake>](&self) -> Option<&$crate::$x> {
                        self.as_op()
                    }
                    pub fn [<as_mut_ $x:snake>](&mut self) -> Option<&mut $crate::$x> {
                        self.as_mut_op()
                    }

                    pub fn [<into_ $x:snake _unwrap>](self) -> $crate::$x {
                        self.into_unwrap()
                    }
                    pub fn [<as_ $x:snake _unwrap>](&self) -> &$crate::$x {
                        self.as_unwrap()
                    }
                    pub fn [<as_mut_ $x:snake _unwrap>](&mut self) -> &mut $crate::$x {
                        self.as_mut_unwrap()
                    }

                    pub fn [<is_ $x:snake>](&self) -> bool {
                        self.[<as_ $x:snake>]().is_some()
                    }
                }
                impl AsOp<$crate::$x> for $name {
                    fn into_op(self) -> Option<$crate::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_op(&self) -> Option<&$crate::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_mut_op(&mut self) -> Option<&mut $crate::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                }
            )*
        }


        paste::paste! {
        impl $crate::CircuitNodeInit for $name {
            fn init_info_impl(self) -> Result<Self> {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => Ok(construct(node.init_info()?)))
            }

            fn rename_impl(self, new_name: Option<String>) -> Self {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => construct(node.rename(new_name)))
            }

            fn update_info_impl<F>(self, f: F) -> Result<Self>
            where
                F: FnOnce(&mut $crate::CachedCircuitInfo),
            {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => Ok(construct(node.update_info(f)?)))
            }
        }

        impl $crate::CircuitNodeDefer for $name {
            #[inline] // hopefully inlined away?
            fn as_trait_obj(&self) -> &dyn $crate::CircuitNode {
                [<$name:snake _map>]!(self; node => node)
            }

            fn map_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
            where
                F: FnMut(usize,$crate::CircuitRc) -> Result<$crate::CircuitRc>,
            {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => $crate::CircuitNode::map_children_enumerate(node, f).map(|v| construct(v)))
            }

            fn map_non_free_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
            where
                F: FnMut(usize,$crate::CircuitRc) -> Result<$crate::CircuitRc>,
            {
                [<$name:snake _map_construct>]!(self;
                    (node, construct) => $crate::CircuitNode::map_non_free_children_enumerate(node, f).map(|v| construct(v)))
            }

            fn custom_c(self) -> $crate::Circuit {
                [<$name:snake _map>]!(self; node => node.c())
            }

            fn custom_rc(self) -> $crate::CircuitRc {
                [<$name:snake _map>]!(self; node => node.rc())
            }
        }
        }

        paste::paste! {
            impl $crate::CircuitNodeUnion for $name {
                type TypeTag = [<$name Type>];

                fn variant_string(&self) -> String {
                    self.type_tag().to_string()
                }

                fn type_tag(&self) -> Self::TypeTag {
                    match self {
                        $(
                            Self::$x(_) => Self::TypeTag::$x,
                        )*
                    }
                }
            }

            impl pyo3::IntoPy<pyo3::PyObject> for $name {
                fn into_py(self, py: pyo3::Python<'_>) -> pyo3::PyObject {
                    [<$name:snake _map>]!(self; node => pyo3::IntoPy::into_py(node, py))
                }
            }
        }

        $(
            impl From<$x> for $name {
                fn from(item: $x) -> Self {
                    Self::$x(item)
                }
            }
        )*
    }
}
macro_rules! define_circuit {
    [$($x:ident),+ $(,)?] => {
        define_circuit_union_impl!(Circuit {$($x,)*});



        // you have to wrap pymethods in the paste for this to work due to how
        // pymethods proc macro works
        paste::paste! {
            #[pymethods]
            impl PyCircuitBase {
            $(
                pub fn [<as_ $x:snake>](&self) -> Option<$crate::$x> {
                    arc_ref_clone(&self).into_op()
                }

                pub fn [<as_ $x:snake _unwrap>](&self) -> PyResult<$x> {
                    arc_ref_clone(&self).into_op().ok_or_else(|| {
                        // could use fresh error type if we wanted
                        PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                            "expected {} but got {}",
                            stringify!($x),
                            self.type_tag()
                        ))
                    })
                }

                pub fn [<is_ $x:snake>](&self) -> bool {
                    self.0.[<is_ $x:snake>]()
                }
            )*
            }
        }

    }
}

define_circuit!(
    Einsum,
    Array,
    Symbol,
    Scalar,
    Add,
    Rearrange,
    Index,
    GeneralFunction,
    Concat,
    Scatter,
    Conv,
    Module,
    SetSymbolicShape,
    Tag,
    DiscreteVar,
    StoredCumulantVar,
    Cumulant,
);

#[pyfunction]
pub fn print_circuit_type_check(x: CircuitType) -> CircuitType {
    dbg!(x);
    x
}

/// Define adhoc unions of different circuit types
#[macro_export]
macro_rules! define_circuit_union {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        $crate::define_circuit_union_impl!($name {$($x,)*});

        impl ::std::convert::From<$crate::Circuit> for ::std::option::Option<$name> {
            fn from(item: $crate::Circuit) -> ::std::option::Option<$name> {
                match item {
                    $(
                        $crate::Circuit::$x(node) => Some(node.into()),
                    )*
                    _=>None
                }
            }
        }
        impl $name{
            pub fn matches(circuit:&$crate::Circuit)->bool{
                let op: ::std::option::Option<$name>=circuit.clone().into();
                op.is_some()
            }
        }
        paste::paste! {
            impl ::std::convert::From<$name> for $crate::Circuit {
                fn from(item: $name) -> Self {
                    [<$name:snake _map>]!(item; node => node.into())
                }
            }

            fn [<circuit_is_ $name:snake>](circuit: &$crate::Circuit) -> bool {
                match circuit {
                    $(
                        $crate::Circuit::$x(_) => true,
                    )*
                    _ => false
                }
            }

            #[pyfunction]
            #[pyo3(name="circuit_is_" $name:snake)]
            pub fn [<circuit_is_ $name:snake _py>](circuit: $crate::CircuitRc) -> bool {
                [<circuit_is_ $name:snake>](&circuit)
            }
        }
    }
}

macro_rules! define_circuit_union_special {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        define_circuit_union!($name {$($x,)*});
        paste::paste! {
            impl Circuit {
                pub fn [<is_ $name:snake>](&self) -> bool {
                    [<circuit_is_ $name:snake>](self)
                }
                pub fn [<into_ $name:snake>](self) -> Option<$name> {
                    self.into()
                }
            }
        }
    }
}

// These nodes are uneffected by rewrites, and satisfy
// AlgebraicRewrite(Replace(X, IrreducibleNode->Y)) == Replace(AlgebraicRewrite(IrreducibleNode), IrreducibleNode->Y)
// except for hashmap iteration order or other unfortunate nondeterminism
define_circuit_union_special!(IrreducibleNode { Array, Symbol });

define_circuit_union_special!(Leaf {
    Array,
    Symbol,
    Scalar,
});

define_circuit_union_special!(LeafConstant { Array, Scalar });

define_circuit_union_special!(Var {
    StoredCumulantVar,
    DiscreteVar,
});

// work around for fact that we can't implement foreign trait on constrained type
#[macro_export]
macro_rules! circuit_node_extra_impl {
    ($type_name:ident, self_hash_default) => {
        $crate::circuit_node_extra_impl!($type_name);
        $crate::circuit_node_self_only_hash_default_impl!($type_name);
    };
    ($type_name:ident) => {
        $crate::circuit_node_eq_ord_debug!($type_name);

        impl $crate::CircuitNodePrivate for $type_name {
            fn info_mut(&mut self) -> &mut $crate::CachedCircuitInfo {
                &mut self.info
            }
            fn name_mut(&mut self) -> &mut Option<String> {
                &mut self.name
            }
        }
        impl rr_util::eq_by_big_hash::EqByBigHash for $type_name {
            fn hash(&self) -> rr_util::util::HashBytes {
                self.info().hash
            }
        }
        impl $type_name {
            fn into_init(self) -> PyClassInitializer<Self> {
                // kinda awkward clone... (but probably basically free)
                (self.clone(), $crate::PyCircuitBase(self.rc())).into()
            }
        }

        impl IntoPy<PyObject> for $type_name {
            fn into_py(self, py: Python<'_>) -> PyObject {
                // this is slightly gross. I wonder if possible to do better?
                // when does this unwrap fail?
                {
                    Py::new(py, self.into_init()).unwrap().into_py(py)
                }
            }
        }
    };
}

#[macro_export]
macro_rules! circuit_node_auto_impl {
    ($the_uuid:literal) => {
        fn info(&self) -> &$crate::CachedCircuitInfo {
            &self.info
        }
        fn name(&self) -> Option<&str> {
            self.name.as_deref()
        }
        fn node_type_uuid(&self) -> [u8; 16] {
            Self::static_node_type_uuid()
        }
        fn static_node_type_uuid() -> [u8; 16]
        where
            Self: Sized,
        {
            *uuid::uuid!($the_uuid).as_bytes()
        }
        fn c(self) -> $crate::Circuit {
            self.into()
        }
        fn rc(self) -> $crate::CircuitRc {
            $crate::CircuitRc(std::sync::Arc::new(self.c()))
        }
    };
}

impl<T: CircuitNodeDefer> CircuitNodeSelfOnlyHash for T {
    fn compute_self_only_hash(&self, hasher: &mut blake3::Hasher) {
        self.as_trait_obj().compute_self_only_hash(hasher)
    }
}

// UPDATE ME WHEN YOU CHANGE CircuitNode Trait!!!
impl<T: CircuitNodeDefer> CircuitNode for T {
    fn info(&self) -> &CachedCircuitInfo {
        self.as_trait_obj().info()
    }

    fn name(&self) -> Option<&str> {
        self.as_trait_obj().name()
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.as_trait_obj().child_axis_map()
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        self.as_trait_obj().children()
    }

    fn non_free_children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        self.as_trait_obj().non_free_children()
    }

    fn map_children_enumerate<F>(&self, f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        self.map_children_enumerate_impl(f)
    }

    fn map_non_free_children_enumerate<F>(&self, f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        self.map_non_free_children_enumerate_impl(f)
    }

    fn node_type_uuid(&self) -> [u8; 16] {
        self.as_trait_obj().node_type_uuid()
    }

    fn self_flops(&self) -> BigUint {
        self.as_trait_obj().self_flops()
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        self.as_trait_obj().eval_tensors(tensors, device_dtype)
    }

    fn intermediate_cost_bound(&self) -> usize {
        self.as_trait_obj().intermediate_cost_bound()
    }

    fn c(self) -> Circuit {
        self.custom_c()
    }

    fn rc(self) -> CircuitRc {
        self.custom_rc()
    }
}

#[derive(Clone, Default)]
pub struct CachedCircuitInfo {
    pub shape: Shape,
    pub is_constant: bool,
    pub is_explicitly_computable: bool,
    pub can_be_sampled: bool,
    pub hash: HashBytes,
    pub max_non_leaf_size: BigUint,
    pub device_dtype: TorchDeviceDtypeOp,
    pub named_axes: NamedAxes,
    pub symbolic_size_constraints: SymbolicSizeConstraints,
}

/// don't want to print hash with Debug, for now just print shape
impl Debug for CachedCircuitInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.shape)
    }
}

impl CachedCircuitInfo {
    pub fn numel(&self) -> BigUint {
        self.shape.iter().map(|x| BigUint::from(*x)).product()
    }
    /// Saturating element count
    pub fn numel_usize(&self) -> usize {
        let numel_digits = self.numel().to_u64_digits();
        if numel_digits.len() == 1 {
            numel_digits[0] as usize
        } else {
            usize::MAX
        }
    }
    pub fn rank(&self) -> usize {
        self.shape.len()
    }
    pub fn hash_usize(&self) -> usize {
        let mut hash_prefix: [u8; 8] = Default::default();
        hash_prefix.copy_from_slice(&self.hash[..8]);
        usize::from_le_bytes(hash_prefix)
    }
}

#[apply(python_error_exception)]
#[base_error_name(Construct)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ConstructError {
    #[error("{string} ({e_name})")]
    NotSupportedYet { string: String },

    #[error("Conv requires stride and padding to be full size, got stride len {stride} padding len {padding} ({e_name})")]
    ConvStridePaddingNotFull { stride: usize, padding: usize },

    #[error("Conv input wrong shape ({e_name})")]
    ConvInputWrongShape {},

    #[error("Conv input wrong shape ({e_name})")]
    ConvFilterWrongShape {},

    #[error("Conv kernel shape must be all odd, got ({e_name})")]
    ConvFilterMustBeOddLength { shape: Shape },

    #[error("Conv stride must evenly divide ({e_name})")]
    ConvStrideMustDivide { shape: Shape, stride: Vec<usize> },

    #[error("Conv groups ({groups}) must divide input channels ({in_channels}) and output channels ({out_channels}) ({e_name})")]
    ConvGroupsMustDivide {
        groups: usize,
        in_channels: usize,
        out_channels: usize,
    },

    #[error(
        "Conv input and filter must have same number of input channels, got {input} and {filter} ({e_name})"
    )]
    ConvInputFilterDifferentNumInputChannels { input: usize, filter: usize },
    #[error("DiscreteVar doesn't have leading 'samples' dim ({e_name})")]
    DiscreteVarNoSamplesDim {},

    #[error("DiscreteVar samples dim doesn't match probs, {node} vs {probs} ({e_name})")]
    DiscreteVarWrongSamplesDim { node: usize, probs: usize },

    #[error("DiscreteVar probs must be 1d with length matching samples axis 0, got probs of shape {shape:?} ({e_name})")]
    DiscreteVarProbsMustBe1d { shape: Shape },

    #[error("StoredCumulantVar needs first 2 cumulants specified ({e_name})")]
    StoredCumulantVarNeedsMeanVariance {},

    #[error("StoredCumulantVar invalid cumulant number {number} ({e_name})")]
    StoredCumulantVarInvalidCumulantNumber { number: usize },

    #[error("StoredCumulantVar cumulant number {cumulant_number} needs to be base shape, {base_shape:?} times cumulant number, got {cumulant_shape:?} ({e_name})")]
    StoredCumulantVarCumulantWrongShape {
        base_shape: Shape,
        cumulant_shape: Shape,
        cumulant_number: usize,
    },

    #[error("actual_num_children={actual_num_children} != expected_num_children_based_on_axes={expected_num_children_based_on_axes}\neinsum_name={einsum_name:?} ({e_name})")]
    EinsumWrongNumChildren {
        actual_num_children: usize,
        expected_num_children_based_on_axes: usize,
        einsum_name: Option<String>,
    },

    #[error("len_axes={len_axes} != child_len_shape={child_len_shape}\neinsum_name={einsum_name:?} child_circuit={child_circuit:?} ({e_name})")]
    EinsumLenShapeDifferentFromAxes {
        len_axes: usize,
        child_len_shape: usize,
        einsum_name: Option<String>,
        child_circuit: CircuitRc,
    },
    #[error("new_size={new_size}!=existing_size={existing_size} for axis={axis}\neinsum_name={einsum_name:?}, size introduced with child_circuit={child_circuit:?} ({e_name})")]
    EinsumAxisSizeDifferent {
        new_size: SymbolicSizeProduct,
        existing_size: SymbolicSizeProduct,
        axis: usize,
        einsum_name: Option<String>,
        child_circuit: CircuitRc,
    },
    #[error("circuit_name={circuit_name:?} all_input_axes={all_input_axes:?} output_axes={output_axes:?} ({e_name})")]
    EinsumOutputNotSubset {
        circuit_name: Option<String>,
        all_input_axes: HashSet<u8>,
        output_axes: EinsumAxes,
    },

    #[error("Rearrange takes different input shape, shape: {shape:?} spec: {spec:?} ({e_name})")]
    RearrangeWrongInputShape { spec: RearrangeSpec, shape: Shape },

    #[error("Wrong input shapes for GeneralFunction {input_shapes:?} {gf_spec:?} ({e_name})")]
    GeneralFunctionWrongInputShape {
        gf_spec: GeneralFunctionSpec,
        input_shapes: Vec<Shape>,
    },

    #[error("Passed python object isn't instance of GeneralFunctionSpec abstract class, ob={ob} ({e_name})")]
    GeneralFunctionPyNotInstance { ob: PyObject },

    #[error("Concat requires at least one node ({e_name})")]
    ConcatZeroNodes {},

    #[error("Concat nodes have different shapes {shapes:?} ({e_name})")]
    ConcatShapeDifferent { shapes: Vec<Shape> },

    #[error("axis out of bounds: {axis} vs {node_rank} ({e_name})")]
    AxisOutOfBounds { axis: i64, node_rank: usize },

    #[error("Scatter shape wrong, index: {index_shape:?} child: {shape:?} {index:?} ({e_name})")]
    ScatterShapeWrong {
        index: TensorIndex,
        shape: Shape,
        index_shape: Shape,
    },

    #[error("This scatter index not supported yet, {index:?} ({e_name})")]
    ScatterIndexTypeUnimplemented { index: TensorIndex },

    #[error("Unknown GeneralFunction name {spec_name} ({e_name})")]
    UnknownGeneralFunction { spec_name: String },

    #[error("Module wrong number of children, expected {expected} got {got}\narg_specs={arg_specs:?} nodes={nodes:?} ({e_name})")]
    ModuleWrongNumberChildren {
        expected: usize,
        got: usize,
        arg_specs: Vec<ModuleArgSpec>,
        nodes: Vec<CircuitRc>,
    },

    #[error(
        "Module got unknown keyword argument, {argument}, all_module_inputs={all_module_inputs:?} ({e_name})"
    )]
    ModuleUnknownArgument {
        argument: String,
        all_module_inputs: Vec<String>,
    },

    #[error("missing_arguments={missing_arguments:?} ({e_name})")]
    ModuleMissingNames { missing_arguments: Vec<String> },

    #[error("Module extract: not all leaves present in circuit, {subcirc:?} ({e_name})")]
    ModuleExtractNotPresent { subcirc: CircuitRc },

    #[error("symbols_named_none={symbols_named_none:?} ({e_name})")]
    ModuleSomeArgsNamedNone { symbols_named_none: Vec<Symbol> },

    #[error("dup_names={dup_names:?} ({e_name})")]
    ModuleArgsDupNames { dup_names: HashMap<String, usize> },

    #[error("spec_circuit={spec_circuit:?} missing_symbols={missing_symbols:?} ({e_name})")]
    ModuleSomeArgsNotPresent {
        spec_circuit: CircuitRc,
        missing_symbols: HashSet<Symbol>,
    },

    #[error("actual_circuit={actual_circuit:?}\n(module children are: spec,sym_0,inp_0,sym_1,inp_1,...,sym_n,inp_n) ({e_name})")]
    ModuleExpectedSymbol { actual_circuit: CircuitRc },

    #[error(
        "orig_module={orig_module:?} got_instead_of_symbol={got_instead_of_symbol:?} ({e_name})"
    )]
    ModuleExpectedSymbolOnMap {
        orig_module: Module,
        got_instead_of_symbol: CircuitRc,
    },

    #[error("Named axis higher than rank ({e_name})")]
    NamedAxisAboveRank {},

    #[error("Failed to construct equivalent explicitly computable circuit ({e_name})")]
    NoEquivalentExplicitlyComputable {},

    #[error("ndim={ndim} ({e_name})")]
    UnflattenButNDimNot1 { ndim: usize },

    #[error("name_prefix='{name_prefix}' module={module:?} ({e_name})")]
    ModulePassedNamePrefixAndUseSelfNameAsPrefix { name_prefix: String, module: Module },
}

pub type CircResult = Result<CircuitRc>;

const INTERNAL_EVAL_ERROR_MESSAGE: &str = "this is likely an internal error (earlier errors should have triggered or an invalid circuit was constructed)";

#[apply(python_error_exception)]
#[base_error_name(TensorEval)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum TensorEvalError {
    #[error(
        "reached not explicitly computable. {}\ncircuit={circuit:?}) ({e_name})",
        INTERNAL_EVAL_ERROR_MESSAGE
    )]
    NotExplicitlyComputableInternal { circuit: CircuitRc },
    #[error("not explicitly computable: {circuit:?}) ({e_name})")]
    NotExplicitlyComputable { circuit: CircuitRc },
    #[error("not constant: {circuit:?}) ({e_name})")]
    NotConstant { circuit: CircuitRc },
    #[error(
        "You can't directly evaluate  module. {}\nmodule={module:?}) ({e_name})",
        INTERNAL_EVAL_ERROR_MESSAGE
    )]
    ModulesCantBeDirectlyEvalutedInternal { module: Module },
    #[error("incompatible dtype circ:{circ:?} passed:{passed:?} ({e_name})")]
    DeviceDtypeError {
        circ: TorchDeviceDtypeOp,
        passed: TorchDeviceDtypeOp,
    },
}

#[derive(Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct CircuitRc(Arc<Circuit>);

impl fmt::Debug for CircuitRc {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Debug::fmt(&***self, f)
    }
}

pub fn make_children_zero<T: CircuitNode>(circuit: &T) -> T {
    circuit.map_children_unwrap(&mut |child: CircuitRc| {
        Scalar::new(0.0, child.info().shape.clone(), child.name_cloned()).rc()
    })
}

pub fn evaluate(circ: CircuitRc) -> Result<Tensor> {
    evaluate_device_dtype(circ, Default::default())
}

#[pyfunction]
pub fn check_evaluable(circuit: CircuitRc) -> Result<()> {
    if !circuit.info().is_explicitly_computable {
        bail!(TensorEvalError::NotExplicitlyComputable {
            circuit: circuit.clone()
        })
    }
    if !circuit.info().is_constant {
        bail!(TensorEvalError::NotConstant {
            circuit: circuit.clone()
        })
    }
    Ok(())
}

#[pyfunction(dtype_device = "TorchDeviceDtypeOp::NONE")]
#[pyo3(name = "evaluate")]
pub fn evaluate_device_dtype(circ: CircuitRc, device_dtype: TorchDeviceDtypeOp) -> Result<Tensor> {
    check_evaluable(circ.clone())?;
    let device_dtype = device_dtype
        .clone()
        .combine(circ.info().device_dtype.clone())
        .map_err(|_err| TensorEvalError::DeviceDtypeError {
            circ: circ.info().device_dtype.clone(),
            passed: device_dtype.clone(),
        })?
        .unwrap_or_defaults();
    let circ = substitute_all_modules(circ);
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<Tensor> {
        let child_tensors: Result<Vec<Tensor>> = circ.children().map(recurse).collect();
        let child_tensors = child_tensors?;

        circ.eval_tensors(&child_tensors, &device_dtype)
    }

    recurse(circ)
}

#[apply(pycallable)]
#[pyo3(name = "deep_map")]
pub fn deep_map<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn((circuit, CircuitRc)) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        let inner_mapped = circ.map_children(&mut recurse)?.rc();
        f(inner_mapped)
    }
    recurse(circuit)
}

#[apply(pycallable)]
#[pyo3(name = "deep_map_preorder")]
pub fn deep_map_preorder<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn((circuit, CircuitRc)) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        f(circ)?.map_children(&mut recurse).map(|z| z.rc())
    }
    recurse(circuit)
}

pub fn visit_circuit_with_parents<F>(circuit: CircuitRc, mut f: F)
where
    F: FnMut(CircuitRc, &Vec<CircuitRc>),
{
    let mut toposorted = toposort_circuit(circuit);
    toposorted.reverse(); // its children first by default

    let mut parents: HashMap<CircuitRc, Vec<CircuitRc>> = HashMap::default();
    for (_i, sub) in toposorted.into_iter().enumerate() {
        f(sub.clone(), parents.get(&sub).unwrap_or(&vec![]));
        for child in sub.children() {
            parents.entry(child).or_insert(vec![]).push(sub.clone());
        }
    }
}

pub fn visit_circuit_with_parents_fallible<F>(circuit: CircuitRc, mut f: F) -> Result<()>
where
    F: FnMut(CircuitRc, &Vec<CircuitRc>) -> Result<()>,
{
    let mut toposorted = toposort_circuit(circuit);
    toposorted.reverse(); // its children first by default

    let mut parents: HashMap<CircuitRc, Vec<CircuitRc>> = HashMap::default();
    for (_i, sub) in toposorted.into_iter().enumerate() {
        f(sub.clone(), parents.get(&sub).unwrap_or(&vec![]))?;
        for child in sub.children() {
            parents.entry(child).or_insert(vec![]).push(sub.clone());
        }
    }
    Ok(())
}

/// does not visit children of circuits where f fails. It does visit all children even if one fails
/// even though this is more work than stopping on the first child that fails
/// because it's semantically cleaner to not have to think about which children are first
pub fn visit_circuit_non_free<F>(circuit: CircuitRc, f: F, recur_into_free: bool) -> Result<()>
where
    F: FnMut(CircuitRc) -> Result<()>,
{
    let mut f = f;
    let mut seen: HashSet<HashBytes> = HashSet::default();

    fn recurse<F>(
        circ: CircuitRc,
        seen: &mut HashSet<HashBytes>,
        f: &mut F,
        recur_into_free: bool,
    ) -> Result<()>
    where
        F: FnMut(CircuitRc) -> Result<()>,
    {
        if seen.insert(circ.info().hash) {
            f(circ.clone())?;

            let children = if recur_into_free {
                circ.children()
            } else {
                circ.non_free_children()
            };
            children
                .map(|child| recurse(child, seen, f, recur_into_free))
                .collect::<Vec<_>>() // intermediate collect causes all recurses to happen even if one errors
                .into_iter()
                .collect::<Result<Vec<_>, _>>()?;
        }
        Ok(())
    }
    recurse(circuit, &mut seen, &mut f, recur_into_free)
}

#[apply(pycallable)]
#[pyo3(name = "visit_circuit")]
pub fn visit_circuit<F>(circuit: CircuitRc, mut f: F) -> Result<()>
where
    F: FnMut((circuit, CircuitRc)) -> Result<()>,
{
    visit_circuit_non_free(circuit, f, true)
}

// TODO: maybe this already exists?
#[pyfunction]
pub fn all_children(circuit: CircuitRc) -> HashSet<CircuitRc> {
    let mut seen: HashSet<CircuitRc> = HashSet::default();
    fn recurse(circ: CircuitRc, seen: &mut HashSet<CircuitRc>) {
        if seen.insert(circ.clone()) {
            for child in circ.children() {
                recurse(child, seen)
            }
        }
    }
    recurse(circuit, &mut seen);
    seen
}

pub fn visit_circuit_postorder<F>(circuit: CircuitRc, mut f: F)
where
    F: FnMut(CircuitRc),
{
    let mut seen: HashSet<HashBytes> = HashSet::default();

    fn recurse<F>(circ: CircuitRc, seen: &mut HashSet<HashBytes>, f: &mut F)
    where
        F: FnMut(CircuitRc),
    {
        if !seen.contains(&circ.info().hash) {
            seen.insert(circ.info().hash);
            for child in circ.children() {
                recurse(child, seen, f)
            }
            f(circ);
        }
    }
    recurse(circuit, &mut seen, &mut f);
}

pub fn deep_map_op<F>(circuit: CircuitRc, f: F) -> Option<CircuitRc>
where
    F: Fn(CircuitRc) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> Option<CircuitRc> {
        let inner_mapped = circ.map_children_op(&mut recurse).map(|z| z.rc());
        inner_mapped
            .map(|x| f(x.clone()).unwrap_or(x))
            .or_else(|| f(circ))
    }
    recurse(circuit)
}

pub fn deep_map_pre_new_children<F>(circuit: CircuitRc, f: F) -> CircuitRc
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> CircuitRc,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> CircuitRc {
        let old_children: Vec<CircuitRc> = circ.children().collect();
        let new_children = old_children.into_iter().map(recurse).collect();
        f(circ, &new_children)
    }
    recurse(circuit)
}

pub fn deep_map_op_pre_new_children<F>(circuit: CircuitRc, f: F) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> Option<CircuitRc> {
        let old_children: Vec<CircuitRc> = circ.children().collect();
        let new_children: Vec<Option<CircuitRc>> =
            old_children.iter().cloned().map(recurse).collect();
        if new_children.iter().all(|x| x.is_none()) {
            f(circ, &old_children)
        } else {
            let new_real_children = zip(old_children, new_children)
                .map(|(old, new)| new.unwrap_or(old))
                .collect();
            Some(f(circ.clone(), &new_real_children).unwrap_or_else(|| {
                circ.map_children_unwrap_idxs(|i| new_real_children[i].clone())
                    .rc()
            }))
        }
    }
    recurse(circuit)
}

pub fn deep_map_fallible_pre_new_children<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        let old_children: Vec<CircuitRc> = circ.children().collect(); // need to define this for borrow reasons
        let new_children: Result<Vec<CircuitRc>> = old_children.into_iter().map(recurse).collect();
        new_children.and_then(|a| f(circ, &a))
    }
    recurse(circuit)
}

pub fn apply_fn_cache<I, K, O, F, FK>(i: &I, f: F, c: &mut HashMap<K, O>, fk: FK) -> O
where
    F: Fn(&I) -> O,
    FK: Fn(&I) -> K,
    O: Clone,
    K: Eq + Hash,
{
    let k = fk(i);
    match c.get(&k) {
        Some(r) => r.clone(),
        None => {
            let r = f(i);
            c.insert(k, r.clone());
            r
        }
    }
}

pub fn deep_map_op_context<F, C>(
    circuit: CircuitRc,
    f: &F,
    context: &mut C,
    self_cache: &mut HashMap<HashBytes, Option<CircuitRc>>,
) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &mut C) -> Option<CircuitRc>,
{
    if let Some(z) = self_cache.get(&circuit.info().hash) {
        return z.clone();
    }
    let inner_mapped = circuit.map_children_op(|x| deep_map_op_context(x, f, context, self_cache));
    let result = match inner_mapped {
        Some(z) => f(z.crc(), context).or(Some(z.rc())),
        None => f(circuit.clone(), context),
    };
    self_cache.insert(circuit.info().hash, result.clone());
    result
}

pub fn deep_map_op_context_preorder_stoppable<F, C>(
    circuit: CircuitRc,
    f: &F,
    context: &mut C,
    self_cache: &mut HashMap<HashBytes, Option<CircuitRc>>,
) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &mut C) -> (Option<CircuitRc>, bool),
{
    if let Some(z) = self_cache.get(&circuit.info().hash) {
        return z.clone();
    }
    let (circuit_applied, stop) = f(circuit.clone(), context);
    if stop {
        return circuit_applied;
    }
    let result = if let Some(applied) = circuit_applied {
        Some(
            applied
                .map_children_op(|x| {
                    deep_map_op_context_preorder_stoppable(x, f, context, self_cache)
                })
                .map(|x| x.rc())
                .unwrap_or(applied.clone()),
        )
    } else {
        circuit
            .map_children_op(|x| deep_map_op_context_preorder_stoppable(x, f, context, self_cache))
            .map(|x| x.rc())
    };
    self_cache.insert(circuit.info().hash, result.clone());
    result
}

pub fn evaluate_fn_uncached(circ: CircuitRc, device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
    let child_tensors: Result<Vec<Tensor>> = circ
        .children()
        .map(|x| evaluate_fn_uncached(x, device_dtype))
        .collect();
    let child_tensors = child_tensors?;

    circ.eval_tensors(&child_tensors, device_dtype)
}

impl IntoPy<PyObject> for CircuitRc {
    fn into_py(self, py: Python<'_>) -> PyObject {
        {
            (*self.0).clone().into_py(py)
        }
    }
}

impl<'source> FromPyObject<'source> for CircuitRc {
    fn extract(circuit_obj: &'source PyAny) -> PyResult<Self> {
        {
            let circ: Circuit = circuit_obj.extract()?;
            Ok(circ.rc())
        }
    }
}

impl<T: CircuitNode + Into<Circuit>> From<T> for CircuitRc {
    fn from(x: T) -> Self {
        x.rc()
    }
}

impl From<Arc<Circuit>> for CircuitRc {
    fn from(x: Arc<Circuit>) -> Self {
        CircuitRc(x)
    }
}

impl Deref for CircuitRc {
    type Target = Arc<Circuit>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for CircuitRc {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl CircuitNodeInit for CircuitRc {
    fn init_info_impl(self) -> Result<Self> {
        Ok(self.c().clone().init_info()?.rc())
    }

    fn rename_impl(self, new_name: Option<String>) -> Self {
        self.c().clone().rename(new_name).rc()
    }

    fn update_info_impl<F>(self, f: F) -> Result<Self>
    where
        F: FnOnce(&mut CachedCircuitInfo),
    {
        Ok(self.c().clone().update_info_impl(f)?.rc())
    }
}

impl CircuitNodeDefer for CircuitRc {
    fn as_trait_obj(&self) -> &dyn CircuitNode {
        // deref to avoid infinite recursion
        (**self).as_trait_obj()
    }

    fn map_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        (**self).map_children_enumerate(f).map(CircuitNode::rc)
    }
    fn map_non_free_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        (**self)
            .map_non_free_children_enumerate(f)
            .map(CircuitNode::rc)
    }

    fn custom_c(self) -> Circuit {
        arc_unwrap_or_clone(self.0)
    }

    // fast custom impl
    fn custom_rc(self) -> CircuitRc {
        self
    }
}

#[pyclass(subclass, name = "Circuit")]
#[derive(Clone, Debug)]
pub struct PyCircuitBase(CircuitRc);

impl Deref for PyCircuitBase {
    type Target = CircuitRc;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for PyCircuitBase {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl EqByBigHash for PyCircuitBase {
    fn hash(&self) -> HashBytes {
        self.info().hash
    }
}

const DEFAULT_FANCY_VALIDATE: bool = false;

#[pymethods]
impl PyCircuitBase {
    #[getter]
    fn shape(&self) -> PyShape {
        PyShape(self.info().shape.clone())
    }

    #[getter]
    fn is_constant(&self) -> bool {
        self.info().is_constant
    }

    #[getter]
    fn is_explicitly_computable(&self) -> bool {
        self.info().is_explicitly_computable
    }

    #[getter]
    fn can_be_sampled(&self) -> bool {
        self.info().can_be_sampled
    }

    #[getter]
    fn name(&self) -> &str {
        self.0.name().unwrap_or("")
    }

    #[getter]
    fn intermediate_cost_bound(&self) -> usize {
        self.0.intermediate_cost_bound()
    }

    fn children(&self) -> Vec<CircuitRc> {
        self.0.children().collect()
    }

    fn non_free_children(&self) -> Vec<CircuitRc> {
        self.0.non_free_children().collect()
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self.0, &object.0, comp_op)
    }

    fn __repr__(&self) -> Result<String> {
        self.debug_repr()
    }

    #[getter]
    fn hash(&self) -> HashBytesToPy {
        self.info().hash.into()
    }

    #[getter]
    fn hash_base16(&self) -> String {
        base16::encode_lower(&self.info().hash)
    }

    fn __hash__(&self) -> u64 {
        self.first_u64()
    }

    pub fn self_flops(&self) -> BigUint {
        self.0.self_flops()
    }

    pub fn total_flops(&self) -> BigUint {
        total_flops((*self.0).crc())
    }

    pub fn max_non_input_size(&self) -> BigUint {
        (*self.0).info().max_non_leaf_size.clone()
    }

    pub fn print_stats(&self) {
        print_circuit_stats(&self.0)
    }

    #[args(options = "Default::default()")]
    fn repr(&self, options: PrintOptions) -> Result<String> {
        options.repr((*self.0).crc())
    }

    #[args(options = "Default::default()")]
    fn print(&self, options: PrintOptionsBase) -> Result<()> {
        options.print(vec![(*self.0).crc()])
    }

    #[args(options = "Default::default()")]
    fn print_html(&self, options: PrintHtmlOptions) -> Result<()> {
        options.print(vec![(*self.0).crc()])
    }

    fn numel(&self) -> BigUint {
        self.0.info().numel()
    }

    fn rank(&self) -> usize {
        self.0.info().rank()
    }
    fn ndim(&self) -> usize {
        self.rank()
    }
    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.0.child_axis_map()
    }

    fn to_py(&self) -> PyObject {
        circuit_rust_to_py(self.0.clone())
    }

    #[args(device_dtype = "Default::default()")]
    fn evaluate(&self, device_dtype: TorchDeviceDtypeOp) -> Result<Tensor> {
        evaluate_device_dtype(self.0.clone(), device_dtype)
    }

    fn map_children_enumerate(&self, f: PyObject) -> Result<CircuitRc> {
        self.0
            .map_children_enumerate(|i, child| pycall!(f, (i, child), anyhow))
    }

    fn map_children(&self, f: PyObject) -> Result<CircuitRc> {
        self.0.map_children(|child| pycall!(f, (child,), anyhow))
    }

    fn num_children(&self) -> usize {
        self.0.num_children()
    }

    fn total_arrayconstant_size(&self) -> BigUint {
        total_arrayconstant_size(self.0.clone())
    }

    fn get_compatible_device_dtype(&self) -> TorchDeviceDtype {
        get_compatible_dtype(&***self)
    }

    fn rename(&self, name: Option<String>) -> CircuitRc {
        self.0.clone().rename(name)
    }
    fn add_suffix(&self, suffix: Option<&str>) -> CircuitRc {
        self.0.clone().add_suffix(suffix)
    }

    fn visit(&self, f: PyObject) -> Result<()> {
        visit_circuit_py(self.0.clone(), f)
    }

    fn reduce(
        &self,
        op_name: String,
        axis: Option<PyOpAtAxes>,
        name: Option<String>,
    ) -> Result<Circuit> {
        self.0
            .reduce(op_name, &reduction_to_ints(axis, self.info().rank()), name)
    }

    fn sum(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<Einsum> {
        Ok(self
            .0
            .sum(&reduction_to_ints(axis, self.info().rank()), name)?)
    }
    fn mean(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<Einsum> {
        Ok(self
            .0
            .mean(&reduction_to_ints(axis, self.info().rank()), name)?)
    }
    fn min(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<CircuitRc> {
        Ok(self
            .0
            .min_(&reduction_to_ints(axis, self.info().rank()), name)?
            .rc())
    }
    fn max(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<CircuitRc> {
        Ok(self
            .0
            .max_(&reduction_to_ints(axis, self.info().rank()), name)?
            .rc())
    }

    fn add(&self, other: CircuitRc, name: Option<String>) -> Result<Add> {
        self.0.add(other, name)
    }
    fn sub(&self, other: CircuitRc, name: Option<String>) -> Result<Add> {
        self.0.sub(other, name)
    }
    fn mul(&self, other: CircuitRc, name: Option<String>) -> Result<Einsum> {
        self.0.mul(other, name)
    }
    fn mul_scalar(
        &self,
        scalar: f64,
        name: Option<String>,
        scalar_name: Option<String>,
    ) -> Result<Einsum> {
        self.0.mul_scalar(scalar, name, scalar_name)
    }
    fn index(&self, index: TensorIndex, name: Option<String>) -> Result<Index> {
        self.0.index(index, name)
    }
    fn expand_at_axes(
        &self,
        axes: PyOpAtAxes,
        counts: Option<PyCountsAtAxes>,
        name: Option<String>,
    ) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.0.crc(),
            RearrangeSpec::expand_at_axes_py(self.rank(), axes, counts)?,
            name,
        ))
    }
    fn unsqueeze(&self, axes: PyOpAtAxes, name: Option<String>) -> Result<Rearrange> {
        self.expand_at_axes(axes, None, name)
    }
    fn squeeze(&self, axes: PyOpAtAxes, name: Option<String>) -> Result<Rearrange> {
        CircuitNode::squeeze(&self.clone().crc(), axes, name)
    }
    fn flatten(&self, name: Option<String>) -> Result<Rearrange> {
        self.0.flatten(name)
    }
    fn unflatten(&self, shape: Shape, name: Option<String>) -> Result<Rearrange> {
        self.0.unflatten(shape, name)
    }
    fn unflatten_axis(&self, axis: i64, shape: Shape, name: Option<String>) -> Result<Rearrange> {
        self.0.unflatten_axis(axis, shape, name)
    }
    fn rearrange(&self, spec: RearrangeSpec, name: Option<String>) -> Result<Rearrange> {
        self.0.rearrange(spec, name)
    }
    fn rearrange_str(&self, string: &str, name: Option<String>) -> Result<Rearrange> {
        self.0.rearrange_str(string, name)
    }
    pub fn is_irreducible_node(&self) -> bool {
        self.0.is_irreducible_node()
    }
    pub fn is_leaf(&self) -> bool {
        self.0.is_leaf()
    }
    pub fn is_leaf_constant(&self) -> bool {
        self.0.is_leaf_constant()
    }
    pub fn is_var(&self) -> bool {
        self.0.is_var()
    }
    pub fn into_irreducible_node(&self) -> Option<IrreducibleNode> {
        self.0.clone().c().into()
    }
    pub fn into_leaf(&self) -> Option<Leaf> {
        self.0.clone().c().into()
    }
    pub fn into_leaf_constant(&self) -> Option<LeafConstant> {
        self.0.clone().c().into()
    }
    pub fn into_var(&self) -> Option<Var> {
        self.0.clone().c().into()
    }
    #[args(
        cache_transform = "true",
        cache_update = "true",
        fancy_validate = "DEFAULT_FANCY_VALIDATE"
    )]
    pub fn update(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        transform: PyObject,
        cache_transform: bool,
        cache_update: bool,
        fancy_validate: bool,
    ) -> PyResult<CircuitRc> {
        matcher.update(
            self.0.clone(),
            transform,
            cache_transform,
            cache_update,
            fancy_validate,
        )
    }
    #[args(fancy_validate = "DEFAULT_FANCY_VALIDATE")]
    pub fn get(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        fancy_validate: bool,
    ) -> PyResult<BTreeSet<CircuitRc>> {
        matcher.get(self.0.clone(), fancy_validate)
    }

    #[args(fancy_validate = "DEFAULT_FANCY_VALIDATE")]
    pub fn get_unique_op(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        fancy_validate: bool,
    ) -> PyResult<Option<CircuitRc>> {
        matcher.get_unique_op(self.0.clone(), fancy_validate)
    }

    #[args(fancy_validate = "DEFAULT_FANCY_VALIDATE")]
    pub fn get_unique(
        &self,
        matcher: OpaqueIterativeMatcherVal,
        fancy_validate: bool,
    ) -> PyResult<CircuitRc> {
        matcher.get_unique(self.0.clone(), fancy_validate)
    }

    pub fn are_any_found(&self, matcher: OpaqueIterativeMatcherVal) -> PyResult<bool> {
        matcher.are_any_found(self.0.clone())
    }
}

pub fn get_compatible_dtype(circ: &Circuit) -> TorchDeviceDtype {
    circ.info().device_dtype.clone().unwrap_or_defaults()
}

pub mod prelude {
    pub use crate::{
        Circuit, CircuitNode, CircuitNodeAutoName, CircuitNodeUnion, CircuitRc, ConstructError,
    };
}

pub fn circuit_rust_to_py(circ: CircuitRc) -> PyObject {
    Python::with_gil(|py| PY_CIRCUIT_ITEMS.rust_to_py.call(py, (circ,), None).unwrap())
}

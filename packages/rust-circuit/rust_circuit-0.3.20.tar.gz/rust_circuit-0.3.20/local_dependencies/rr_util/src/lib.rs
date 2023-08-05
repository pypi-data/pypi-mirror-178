#![feature(let_chains)]
/// reexport
pub use pyo3;
pub use uuid;

#[macro_use]
pub mod caching;
pub mod eq_by_big_hash;
pub mod repr;
#[macro_use]
pub mod errors_util;
pub mod lazy;
pub mod lru_cache;
pub mod opt_einsum;
pub mod py_types;
pub mod python_callables;
pub mod python_wrapped;
pub mod rearrange_spec;
pub mod rrfs;
pub mod set_cover;
pub mod symbolic_size;
pub mod tensor_db;
pub mod tensor_util;
pub mod union_find;
pub mod util;

#[macro_export]
macro_rules! sv {
    [$($tt:tt)*] => {
        smallvec::smallvec!($($tt)*)
    };
}

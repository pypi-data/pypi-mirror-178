# this file is included with `include_str!()` in py_types.rs
import functools
import itertools
import torch
import torch.nn.functional
from typing import List, Tuple
import math
import itertools


def check_type(x, type_v):
    if not isinstance(x, type_v):
        raise TypeError(f"expected type {repr(type_v)} but got {type(x)}")


def get_tensor_shape(x):
    check_type(x, torch.Tensor)
    return list(x.size())


dtype_from_string = {
    "float32": torch.float32,
    "float64": torch.float64,
    "float16": torch.float16,
    "int64": torch.int64,
    "int32": torch.int32,
    "int16": torch.int16,
    "int8": torch.int8,
}


def scalar_to_tensor(scalar, shape, device_dtype):
    "Makes a stride 0 repeat view into a 1 element tensor"
    scalar_tensor = torch.tensor(scalar, device=device_dtype.device, dtype=dtype_from_string[device_dtype.dtype])
    return torch.broadcast_to(scalar_tensor, tuple(shape))


def tensor_scale(tensor):
    return tensor.abs().mean().cpu().item()


def cast_tensor(tensor, device_dtype):
    return tensor.to(device=device_dtype.device, dtype=dtype_from_string[device_dtype.dtype])


zero_tensor = torch.zeros(())


def un_flat_concat(tensor: torch.Tensor, shapes) -> List[torch.Tensor]:
    lens = [math.prod(x) for x in shapes]
    flats = torch.split(tensor, lens, dim=0)
    return [x.reshape(shape) for x, shape in zip(flats, shapes)]


def log_exp_p_1_fn(x: torch.Tensor):
    # piecewise to nicely handle numerics
    addr = 1.0
    return torch.where(x < 0.0, torch.log(torch.exp(x) + addr), torch.log(1.0 + torch.exp(-x) * addr) + x)


generalfunctions = {
    "gelu": torch.nn.functional.gelu,
    "relu": torch.relu,
    "step": lambda x: torch.where(
        x > 0.0, torch.ones((), dtype=x.dtype, device=x.device), torch.zeros((), dtype=x.dtype, device=x.device)
    ),
    "sigmoid": torch.sigmoid,
    "rsqrt": torch.rsqrt,
    "reciprocal": torch.reciprocal,
    "tanh": torch.tanh,
    "softmax": functools.partial(torch.softmax, dim=-1),
    "log_softmax": functools.partial(torch.log_softmax, dim=-1),
    "log_exp_p_1": log_exp_p_1_fn,
    "gaussian_pdf": lambda x: torch.exp(-(x ** 2) / 2) / math.sqrt(2 * math.pi),
    "gaussian_cdf": lambda x: torch.distributions.normal.Normal(0, 1).cdf(x),
    "q_from_qr": lambda x: torch.linalg.qr(x)[0],
    "min": lambda x: torch.min(x, dim=-1)[0],
    "max": lambda x: torch.max(x, dim=-1)[0],
    "last_dim_size": lambda x: torch.full(x.shape[:-1], x.shape[-1], dtype=x.dtype, device=x.device),
}


def check_canon_idx(i: int, count: int):
    assert count >= 0, count
    if i >= 0:
        assert i < count, (i, count)
    else:
        assert i >= -count, (i, count)
    return i % count


def check_ints(x: torch.Tensor):
    assert (x.long().to(dtype=x.dtype) == x).all()


def gen_index_function(
    x: torch.Tensor, index: torch.Tensor, index_dim: int, use_index_as_prefix: bool, check_index_ints: bool
):
    # copy of  WildIndex from computational_node.py (maybe dedup?)
    if check_index_ints:
        check_ints(index)
    if use_index_as_prefix:
        prefix_len = index.ndim
        assert x.shape[:prefix_len] == index.shape
        suffix_len = x.ndim - prefix_len
        moved_x = x.movedim(check_canon_idx(index_dim, suffix_len) + prefix_len, 0)
        flattened_x = moved_x.flatten(start_dim=1, end_dim=len(index.shape))  # end_dim is inclusive, so this is right
        flattened_index = index.flatten().long()
        new_x = flattened_x[flattened_index, torch.arange(index.numel())]
        return new_x.reshape(moved_x.shape[1:])

    else:
        moved_out = torch.index_select(x, index_dim, index.long().flatten()).moveaxis(index_dim, 0)
        return moved_out.reshape(*index.shape, *moved_out.shape[1:])


assert_tensors_close = torch.testing.assert_close


def make_diagonal(tensor: torch.Tensor, tensor_ints: Tuple[int, ...], out_ints: Tuple[int, ...]):
    int_sizes = {x: tensor.shape[i] for i, x in enumerate(tensor_ints)}
    deduped_shape = [int_sizes[x] for x in tensor_ints]
    result = torch.zeros(tuple(int_sizes[x] for x in out_ints), dtype=tensor.dtype, device=tensor.device)
    normal_strides_out = result.stride()
    fancy_strides = []
    for i in tensor_ints:
        indices = [j for j, x in enumerate(out_ints) if x == i]
        strides = [normal_strides_out[k] for k in indices]
        stride_here = sum(strides)
        fancy_strides.append(stride_here)
    fancy_strided = torch.as_strided(result, deduped_shape, fancy_strides)
    fancy_strided += tensor
    return result


def tensor_to_bytes(x: torch.Tensor):
    return x.cpu().numpy().tobytes()


def tensor_from_bytes(device_dtype, shape, bytes, count):
    return (
        torch.frombuffer(bytes, count=count, offset=0, dtype=dtype_from_string[device_dtype.dtype])
        .reshape(shape)
        .to(device=device_dtype.device)
    )


einsum = lambda tensors_and_axes, out_axes: torch.einsum(*itertools.chain(*tensors_and_axes), out_axes)


def random_indices(input: torch.Tensor, shape, replacement: bool) -> torch.Tensor:
    shape = tuple(shape)
    return torch.multinomial(
        input,
        num_samples=math.prod(shape),
        replacement=replacement,
    ).reshape(shape)


# we use different axis layout than pytorch,
# batch_dims... height_width_ect... channels
# we also allow asymmetric padding to support InceptionV1
# which we have to do manually bc torch.conv doesn't support
def conv(dim, input, filter, stride, padding):
    import einops

    assert len(filter.shape) == 2 + dim, "don't support filter batching yet"
    stride = tuple(stride)

    batch_rank = len(input.shape) - dim - 1
    char_at = lambda i: chr(ord("a") + i)
    input_rearrange_string_i = " ".join([char_at(x) for x in range(len(input.shape))])
    input_rearrange_string_o = f"({' '.join([char_at(x) for x in range(batch_rank)])}) {char_at(len(input.shape)-1)} {' '.join([char_at(x) for x in range(batch_rank,len(input.shape)-1)])}"
    input_rearrange_string = f"{input_rearrange_string_i} -> {input_rearrange_string_o}"
    input_batches_together = einops.rearrange(input, input_rearrange_string)
    if any([x[0] != x[1] for x in padding]):
        padding_min = tuple([min(x) for x in padding])
        input_batches_together = torch.nn.functional.pad(
            input_batches_together,
            tuple(itertools.chain(*[(p[0] - pmin, p[1] - pmin) for p, pmin in zip(padding, padding_min)])),
        )
    padding = tuple([min(x) for x in padding])
    if dim == 1:
        filter = einops.rearrange(filter, "o a i -> o i a")
        result = torch.nn.functional.conv1d(input_batches_together, filter, None, stride, padding)
    elif dim == 2:
        filter = einops.rearrange(filter, "o a b i -> o i a b")
        result = torch.nn.functional.conv2d(input=input_batches_together, weight=filter, stride=stride, padding=padding)
    elif dim == 3:
        filter = einops.rearrange(filter, "o a b c i -> o i a b c")
        result = torch.nn.functional.conv3d(input=input_batches_together, weight=filter, stride=stride, padding=padding)
    else:
        raise ValueError("conv only supports 1, 2, or 3d convolutions")
    return einops.rearrange(
        result,
        f"{input_rearrange_string_o} -> {input_rearrange_string_i}",
        **{char_at(i): input.shape[i] for i in range(batch_rank)},
    )

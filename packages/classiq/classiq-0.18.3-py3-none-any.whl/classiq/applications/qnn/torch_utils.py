from collections.abc import Sized
from functools import reduce
from typing import Optional

import torch
import torch.nn as nn
from torch import Tensor

from classiq.applications.qnn.types import (
    ExecuteFuncitonOnlyArguments,
    PostProcessFunction,
    Shape,
    TensorToArgumentsCallable,
)
from classiq.exceptions import ClassiqValueError


def get_shape_second_dimension(shape: torch.Size):
    if not isinstance(shape, Sized):
        raise ClassiqValueError("Invalid shape type - must have `__len__`")

    if len(shape) == 1:
        return 1
    elif len(shape) == 2:
        return shape[1]
    else:
        raise ClassiqValueError("Invalid shape dimension - must be 1D or 2D")


def get_shape_first_dimension(shape: torch.Size):
    if not isinstance(shape, Sized):
        raise ClassiqValueError("Invalid shape type - must have `__len__`")

    if len(shape) in (1, 2):
        return shape[0]
    else:
        raise ClassiqValueError("Invalid shape dimension - must be 1D or 2D")


def _result_to_tensor(
    all_results: list,
    inputs: Tensor,
    weights: Tensor,
    expected_shape: Optional[Shape] = None,
    requires_grad: Optional[bool] = None,
) -> Tensor:
    expected_shape = expected_shape or torch.Size(
        [
            inputs.shape[0],  # batch size
            weights.shape[0],  # num circuits
        ]
    )

    # Note: we chose `dtype=weights.dtype`
    #   we could have chosen `dtype=inputs.dtype`
    #   It would be nearly identical
    #   but choosing weights is better since it must be float
    #       in order to have a tensor derivative

    # Todo: when creating this tensor, we set `requires_grad`, but don't define `grad_fn`
    #   This may cause problems later. Thus, we'll deal with it later.
    result = torch.tensor(
        all_results,
        dtype=weights.dtype,
    ).reshape(*expected_shape)

    if requires_grad is None:
        requires_grad = inputs.requires_grad or weights.requires_grad
    result.requires_grad_(requires_grad)

    return result


# Test
def iter_inputs_weights(
    inputs: Tensor,
    weights: Tensor,
    convert_tensors_to_arguments: TensorToArgumentsCallable,
    execute: ExecuteFuncitonOnlyArguments,
    post_process: PostProcessFunction,
    *,
    expected_shape: Optional[Shape] = None,
    requires_grad: Optional[bool] = None
) -> Tensor:
    all_arguments = sum(
        (
            convert_tensors_to_arguments(batch_item, out_weight)
            for batch_item in inputs  # this is the first for-loop
            for out_weight in weights  # this is the second
        ),
        (),
    )

    execution_results = execute(all_arguments)

    all_results = list(map(post_process, execution_results.details))

    return _result_to_tensor(
        all_results, inputs, weights, expected_shape, requires_grad
    )


def calculate_amount_of_parameters(net: nn.Module) -> int:
    return sum(  # sum over all parameters
        reduce(int.__mul__, i.shape)  # multiply all dimensions
        for i in net.parameters()
    )

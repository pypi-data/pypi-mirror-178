import itertools

import torch
from torch import Tensor

from classiq.applications.qnn.circuit_utils import batch_map_parameters
from classiq.applications.qnn.gradients.quantum_gradient import QuantumGradient
from classiq.applications.qnn.torch_utils import iter_inputs_weights
from classiq.applications.qnn.types import (
    Circuit,
    ExecuteFunciton,
    MultipleArguments,
    PostProcessFunction,
)

# only +1 or -1
Sign = float

#
# Gradient consts
#
EPSILON = 1e-2


class SimpleQuantumGradient(QuantumGradient):
    def __init__(
        self,
        circuit: Circuit,
        execute: ExecuteFunciton,
        post_process: PostProcessFunction,
        epsilon: float = EPSILON,
        *args,
        **kwargs
    ):
        super().__init__(circuit, execute, post_process)
        self._epsilon = epsilon

    # Test
    def _add_epsilon(self, weights: Tensor, index: int, sign: Sign = +1) -> Tensor:
        epsilon = torch.zeros_like(weights)
        epsilon[index] = self._epsilon

        return weights + sign * epsilon

    # Test
    def convert_tensors_to_arguments(
        self, inputs: Tensor, weights: Tensor
    ) -> MultipleArguments:
        return tuple(
            batch_map_parameters(
                self._parameters_names,
                itertools.repeat(inputs),
                (
                    self._add_epsilon(weights, index, sign)
                    for index in range(len(weights))  # this is the first for-loop
                    for sign in (+1, -1)  # this is the second
                ),
            )
        )

    # Test
    def _differentiate_results(self, result: Tensor) -> Tensor:
        # The `result` tensor is a rank-4-tensor.
        #   (num_of_batches X num_of_weight_groups X num_of_weights_in_a_group X 2)
        #   where 2 is for 2 items : + and - epsilon
        # Thus, the last axis, which is number 3 (zero based)
        #   is the one in which we differentiate
        #   and the one which is squeezed
        # The minus comes from the way pytorch defines diff
        #   it diffs the second object minus the first
        #     where we want the first minus the second
        diff = -result.diff(axis=3).squeeze(3)  # type: ignore[call-arg]
        return diff / (2 * self._epsilon)

    # Test somehow
    def gradient(self, inputs: Tensor, weights: Tensor, *args, **kwargs) -> Tensor:
        result = iter_inputs_weights(
            inputs,
            weights,
            self.convert_tensors_to_arguments,
            self.execute,
            self._post_process,
            expected_shape=(
                inputs.shape[0],
                weights.shape[0],
                weights.shape[1],
                2,
            ),
        )

        result = self._differentiate_results(result)

        result.requires_grad_(inputs.requires_grad or weights.requires_grad)
        return result

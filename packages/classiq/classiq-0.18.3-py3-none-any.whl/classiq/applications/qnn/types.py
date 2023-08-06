from typing import Callable, Dict, Tuple, Union

import torch
from torch import Tensor

from classiq.interface.executor.result import ExecutionDetails, MultipleExecutionDetails
from classiq.interface.generator.result import GeneratedCircuit

Arguments = Dict[str, float]
MultipleArguments = Tuple[Arguments, ...]

Circuit = GeneratedCircuit
ExecuteFunciton = Callable[
    [GeneratedCircuit, MultipleArguments], MultipleExecutionDetails
]
ExecuteFuncitonOnlyArguments = Callable[[MultipleArguments], MultipleExecutionDetails]
PostProcessFunction = Callable[[ExecutionDetails], Tensor]
TensorToArgumentsCallable = Callable[[Tensor, Tensor], MultipleArguments]

Shape = Union[torch.Size, Tuple[int, ...]]

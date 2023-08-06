from typing import Any, Dict

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_param_list_without_self_reference import (
    function_param_library_without_self_reference,
)
from classiq.interface.generator.function_params import (
    FunctionParams,
    IOName,
    parse_function_params_values,
)

PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME = "PHASE_ESTIMATION"


class PhaseEstimation(FunctionParams):
    """
    Quantum phase estimation of a given unitary function.
    """

    size: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits storing the estimated phase."
    )
    unitary: str = pydantic.Field(
        default="",
        description="The unitary function for phase estimation.",
    )
    unitary_params: FunctionParams = pydantic.Field(
        description="The unitary function parameters."
    )

    _output_name: IOName = pydantic.PrivateAttr(
        default=PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME
    )

    @property
    def output_name(self) -> str:
        return self._output_name

    def _create_ios(self) -> None:
        self._inputs = {**self.unitary_params.inputs}
        self._outputs = {**self.unitary_params.outputs}
        self._outputs[self._output_name] = RegisterUserInput(
            name=self._output_name, size=self.size
        )

    @pydantic.root_validator(pre=True)
    def parse_function_params(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        parse_function_params_values(
            values=values,
            params_key="unitary_params",
            discriminator_key="unitary",
            param_classes=function_param_library_without_self_reference.param_list,
        )
        return values

    @pydantic.validator("unitary_params")
    def validate_unitary_params(cls, unitary_params: FunctionParams) -> FunctionParams:
        if not unitary_params.is_powerable():
            raise ValueError(
                f"Phase estimation of {unitary_params.discriminator()} is currently not supported."
            )
        return unitary_params

import abc
import collections.abc
import functools
import re
from typing import (
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Match,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from classiq.interface.generator import (
    function_call,
    function_param_list,
    function_params,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.function_params import IOName
from classiq.interface.generator.user_defined_function_params import CustomFunction

from classiq.exceptions import ClassiqValueError, ClassiqWiringError
from classiq.model_designer.logic_flow import LogicFlowBuilder
from classiq.model_designer.wire import Wire
from classiq.quantum_functions.function_library import (
    FunctionData,
    FunctionLibrary,
    QuantumFunction,
)
from classiq.quantum_register import QReg

QregOrWire = Union[QReg, Wire]
WireOrWires = Union[Wire, Iterable[Wire]]
SupportedInputArgs = Union[
    Mapping[str, QregOrWire],
    Collection[QReg],
    QReg,
]

_SAME_INPUT_NAME_ERROR_MSG: str = "Cannot create multiple inputs with the same name"
_INPUT_AS_OUTPUT_ERROR_MSG: str = "Can't connect input directly to output"


class LogicFlowInputWire(Wire):
    def __init__(self, input_name: IOName) -> None:
        super().__init__()
        self._initialize_wire_name(wire_name=input_name)

    @property
    def is_connected(self) -> bool:
        return self.is_ended

    @property
    def is_ended(self) -> bool:
        return self._end_call is not None


class FunctionHandler(abc.ABC):
    def __init__(self) -> None:
        self._generated_wires: Set[Wire] = set()
        self._function_library: Optional[FunctionLibrary] = None
        self._generated_inputs: Dict[IOName, Tuple[Wire, RegisterUserInput]] = dict()
        self._generated_outputs: Dict[IOName, Tuple[Wire, RegisterUserInput]] = dict()
        self._logic_flow_builder: LogicFlowBuilder = LogicFlowBuilder()

    def _verify_legal_wires(self, wires: WireOrWires) -> None:
        if isinstance(wires, Wire):
            wires = [wires]
        if any(
            wire not in self._generated_wires and not wire.wired_to_zero
            for wire in wires
        ):
            raise ClassiqWiringError("Wire does not belong to this generator")

    def _update_generated_wires(self, wires: WireOrWires) -> None:
        if isinstance(wires, Wire):
            wires = [wires]
        self._generated_wires.update(wires)

    @staticmethod
    def _parse_control_states(
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None
    ) -> List[ControlState]:
        if control_states is None:
            return list()
        elif isinstance(control_states, ControlState):
            return [control_states]
        return list(control_states)

    def _validate_unique_inputs(
        self, input_registers: Dict[IOName, RegisterUserInput]
    ) -> None:
        if any(name in self._generated_inputs for name in input_registers):
            raise ClassiqWiringError(_SAME_INPUT_NAME_ERROR_MSG)

    def create_inputs(
        self,
        input_registers: Dict[IOName, RegisterUserInput],
    ) -> Dict[IOName, LogicFlowInputWire]:
        wires_dict = {}
        self._validate_unique_inputs(input_registers)

        for name, reg in input_registers.items():
            wire = LogicFlowInputWire(input_name=name)
            self._generated_inputs[name] = (wire, reg)
            self._update_generated_wires(wire)
            wires_dict[name] = wire

        return wires_dict

    def set_outputs(
        self, outputs: Dict[IOName, Tuple[Wire, RegisterUserInput]]
    ) -> None:
        self._verify_legal_wires(wires=[output[0] for output in outputs.values()])
        for output_name, output in outputs.items():
            output_wire, output_register = output
            wire_name = output_wire.wire_name
            if isinstance(output_wire, LogicFlowInputWire):
                raise ClassiqWiringError(f"{_INPUT_AS_OUTPUT_ERROR_MSG} {output_name}")
            output_wire.set_as_output(output_wire_name=wire_name)
            self._generated_outputs[output_name] = (output_wire, output_register)

    def apply(
        self,
        function_name: Union[
            str,
            FunctionData,
            QuantumFunction,
        ],
        in_wires: Optional[SupportedInputArgs] = None,
        out_wires: Optional[SupportedInputArgs] = None,
        is_inverse: bool = False,
        release_by_inverse: bool = False,
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None,
        should_control: bool = True,
        power: int = 1,
        call_name: Optional[str] = None,
    ) -> Dict[str, QregOrWire]:
        # if there's no function library, create one
        if self._function_library is None:
            self.include_library(FunctionLibrary())

        if isinstance(function_name, FunctionData):
            function_data = function_name
        elif isinstance(function_name, QuantumFunction):
            function_data = function_name.function_data
        else:
            function_data = None

        if function_data:
            if function_data not in self._function_library.data:  # type: ignore[union-attr]
                self._function_library.add_function(function_data)  # type: ignore[union-attr]

            function_name = function_data.name

        return self._add_function_call(
            CustomFunction.__name__,
            self._function_library.get_function(cast(str, function_name)),  # type: ignore[union-attr]
            in_wires=in_wires,
            out_wires=out_wires,
            is_inverse=is_inverse,
            release_by_inverse=release_by_inverse,
            control_states=control_states,
            should_control=should_control,
            power=power,
            call_name=call_name,
        )

    def release_qregs(self, qregs: Union[QReg, Collection[QReg]]) -> None:
        if isinstance(qregs, QReg):
            qregs = [qregs]
        for qreg in qregs:
            self._logic_flow_builder.connect_qreg_to_zero(qreg)

    def _add_function_call(
        self,
        function: str,
        params: function_params.FunctionParams,
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None,
        in_wires: Optional[SupportedInputArgs] = None,
        out_wires: Optional[SupportedInputArgs] = None,
        is_inverse: bool = False,
        release_by_inverse: bool = False,
        should_control: bool = True,
        power: int = 1,
        call_name: Optional[str] = None,
    ) -> Dict[str, QregOrWire]:
        if function != type(params).__name__:
            raise ClassiqValueError(
                "The FunctionParams type does not match function name"
            )

        if (
            isinstance(params, CustomFunction)
            and self._function_library
            and params not in self._function_library.data
        ):
            raise ClassiqValueError("The function is not found in included library.")

        call = function_call.FunctionCall(
            function=function,
            function_params=params,
            is_inverse=is_inverse ^ (power < 0),
            release_by_inverse=release_by_inverse,
            control_states=self._parse_control_states(control_states),
            should_control=should_control,
            power=abs(power),
            name=call_name,
        )

        if in_wires is not None:
            self._connect_in_wires(call=call, in_wires=in_wires)

        self._logic_flow.append(call)

        return self._connect_out_wires(
            call=call,
            out_wires=out_wires or {},
        )

    def _connect_in_wires(
        self,
        call: function_call.FunctionCall,
        in_wires: SupportedInputArgs,
    ) -> None:
        if isinstance(in_wires, dict):
            self._connect_named_in_wires(call=call, in_wires=in_wires)
        elif isinstance(in_wires, QReg):
            self._connect_unnamed_in_quantum_registers(
                call=call, quantum_registers=[in_wires]
            )
        elif isinstance(in_wires, collections.abc.Collection):
            self._connect_unnamed_in_quantum_registers(
                # mypy doesn't recognize that `dict` wouldn't reach this point
                call=call,
                quantum_registers=in_wires,  # type: ignore[arg-type]
            )
        else:
            raise ClassiqWiringError(
                f"Invalid in_wires type: {type(in_wires).__name__}"
            )

    def _connect_unnamed_in_quantum_registers(
        self,
        call: function_call.FunctionCall,
        quantum_registers: Collection[QReg],
    ) -> None:
        call_inputs = call.function_params.get_io_names(
            function_params.IO.Input, call.is_inverse, call.control_states
        )

        if len(call_inputs) != len(quantum_registers):
            raise ClassiqWiringError(
                f'A call to "{call.name}" requires {len(call_inputs)} items, but {len(quantum_registers)} were given'
            )
        self._connect_named_in_wires(call, dict(zip(call_inputs, quantum_registers)))

    def _connect_named_in_wires(
        self,
        call: function_call.FunctionCall,
        in_wires: Dict[str, QregOrWire],
    ) -> None:
        self._verify_legal_wires(
            [in_wire for in_wire in in_wires.values() if isinstance(in_wire, Wire)]
        )

        for input_name, in_wire in in_wires.items():
            if isinstance(in_wire, QReg):
                pin_name, pin_indices = self._get_pin_name_and_indices(
                    input_name, call.input_regs_dict
                )
                self._logic_flow_builder.connect_qreg_to_func_call(
                    in_wire, pin_name, call, pin_indices
                )
            else:
                in_wire.connect_wire_end(end_call=call, input_name=input_name)

    @staticmethod
    def _get_pin_name_and_indices(
        input_name: str, inputs_info: Dict[str, RegisterUserInput]
    ) -> Tuple[str, range]:
        name, slicing = function_call.FunctionCall.parse_io_slicing(input_name)
        pin_info = inputs_info.get(name)
        if pin_info is None:
            raise ClassiqWiringError(
                f"No register size information on input pin {name}"
            )
        indices = range(pin_info.size)[slicing]
        return name, indices

    def _connect_out_wires(
        self,
        call: function_call.FunctionCall,
        out_wires: SupportedInputArgs,
    ) -> Dict[str, QregOrWire]:
        if isinstance(out_wires, dict):
            wire_dict = self._connect_named_out_wires(call=call, out_wires=out_wires)
        elif isinstance(out_wires, QReg):
            wire_dict = self._connect_unnamed_out_quantum_registers(
                call=call, quantum_registers=[out_wires]
            )
        elif isinstance(out_wires, collections.abc.Collection):
            if not all(isinstance(i, QReg) for i in out_wires):
                raise ClassiqWiringError(
                    "When supplying an iterable, all items must be instances of QReg"
                )
            wire_dict = self._connect_unnamed_out_quantum_registers(
                call=call, quantum_registers=out_wires  # type: ignore[arg-type]
            )
        else:
            raise ClassiqWiringError(
                f"Invalid out_wires type: {type(out_wires).__name__}"
            )

        self._update_generated_wires(
            [wire for wire in wire_dict.values() if isinstance(wire, Wire)]
        )
        return wire_dict

    def _connect_named_out_wires(
        self,
        call: function_call.FunctionCall,
        out_wires: Dict[str, QregOrWire],
    ) -> Dict[str, QregOrWire]:
        wire_dict: Dict[str, QregOrWire] = {}
        output_names = call.function_params.get_io_names(
            function_params.IO.Output, call.is_inverse, call.control_states
        )

        specified_outputs: List[Tuple[str, str]] = list(tuple())
        for specified_output in out_wires.keys():
            match: Optional[Match] = re.fullmatch(
                function_call.IO_REGEX, specified_output
            )
            if match is None:
                raise ClassiqWiringError(
                    f"Output ({specified_output}) is not a valid expression"
                )
            name = match.groupdict().get(function_call.NAME)
            slicing = match.groupdict().get(function_call.SLICING)
            if name is None or name not in output_names:
                raise ClassiqWiringError(
                    f"Output name ({name}) does not belong to this function call"
                )
            if (
                slicing is not None
                and re.fullmatch(function_call.LEGAL_SLICING, slicing) is None
            ):
                raise ClassiqWiringError(
                    f"Slicing / indexing expression ({slicing}) is illegal"
                )

            specified_outputs.append(
                (name, f"[{slicing}]" if slicing is not None else "")
            )

        for output_name in output_names:
            connected_outputs = [
                name + slicing
                for name, slicing in specified_outputs
                if output_name == name
            ]

            if not connected_outputs:
                wire_dict[output_name] = self._output_wire_type(
                    start_call=call, output_name=output_name
                )
                continue

            for specified_output in connected_outputs:
                out_wire = out_wires[specified_output]
                if isinstance(out_wire, QReg):
                    self._logic_flow_builder.connect_func_call_to_qreg(
                        call, specified_output, out_wire
                    )
                else:
                    out_wire.connect_wire_start(
                        start_call=call, output_name=specified_output
                    )
                wire_dict[specified_output] = out_wire

        return wire_dict

    def _connect_unnamed_out_quantum_registers(
        self,
        call: function_call.FunctionCall,
        quantum_registers: Collection[QReg],
    ) -> Dict[str, QregOrWire]:
        output_names = call.function_params.get_io_names(
            function_params.IO.Output, call.is_inverse, call.control_states
        )
        return self._connect_named_out_wires(
            call, dict(zip(output_names, quantum_registers))
        )

    def __getattr__(self, item):
        is_builtin_function_name = any(
            item == func.__name__
            for func in function_param_list.function_param_library.param_list
        )

        if is_builtin_function_name:
            return functools.partial(self._add_function_call, item)

        is_user_function_name = (
            self._function_library is not None
            and item in self._function_library.function_names
        )

        if is_user_function_name:
            return functools.partial(self.apply, item)

        if (
            self._function_library is not None
            and item in self._function_library.function_factory_names
        ):
            return functools.partial(
                self._function_library.get_function_factory(item),
                add_method=functools.partial(
                    self._function_library.add_function,
                    override_existing_functions=True,
                ),
                apply_method=self.apply,
            )

        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

    def __dir__(self):
        builtin_func_name = [
            func.__name__
            for func in function_param_list.function_param_library.param_list
        ]
        user_func_names = (
            list(self._function_library.function_names)
            if self._function_library is not None
            else list()
        )
        return list(super().__dir__()) + builtin_func_name + user_func_names

    def include_library(self, library: FunctionLibrary) -> None:
        """Includes a function library.

        Args:
            library (FunctionLibrary): The function library.
        """
        if self._function_library is not None:
            raise ClassiqValueError("Another function library is already included.")

        self._function_library = library

    @property
    @abc.abstractmethod
    def _logic_flow(self) -> List[function_call.FunctionCall]:
        pass

    @property
    @abc.abstractmethod
    def _output_wire_type(self) -> Type[Wire]:
        pass

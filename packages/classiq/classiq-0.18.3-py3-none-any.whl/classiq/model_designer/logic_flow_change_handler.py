from typing import Optional

from classiq.interface.generator.function_call import ZERO_INDICATOR, FunctionCall


def _get_wire_name(
    source_call: FunctionCall,
    source_pin_name: str,
    dest_pin_name: str,
    dest_call: Optional[FunctionCall],
) -> str:
    if dest_call is None:
        assert dest_pin_name == ZERO_INDICATOR
        return ZERO_INDICATOR
    return f"{source_call.id}:{source_pin_name}->{dest_call.id}:{dest_pin_name}"


def _set_model_output(call: FunctionCall, pin_name: str, wire_name: str):
    call.outputs_dict[pin_name] = wire_name
    if wire_name != ZERO_INDICATOR:
        call.non_zero_output_wires.append(wire_name)


def _set_model_input(call: Optional[FunctionCall], pin_name: str, wire_name: str):
    if call is None:
        return
    call.inputs_dict[pin_name] = wire_name
    call.non_zero_input_wires.append(wire_name)


def handle(
    source_call: FunctionCall,
    source_pin_name: str,
    dest_pin_name: str,
    dest_call: Optional[FunctionCall],
) -> None:
    wire_name = _get_wire_name(source_call, source_pin_name, dest_pin_name, dest_call)
    _set_model_output(source_call, source_pin_name, wire_name)
    _set_model_input(dest_call, dest_pin_name, wire_name)

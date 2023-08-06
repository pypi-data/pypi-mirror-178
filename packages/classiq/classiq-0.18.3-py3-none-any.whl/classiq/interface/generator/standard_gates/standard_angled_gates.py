import pydantic

from classiq.interface.generator.standard_gates.standard_gates import _StandardGate


class RXGate(_StandardGate, angles=["theta"]):
    """
    Rotation by theta about the X axis
    """


class RYGate(_StandardGate, angles=["theta"]):
    """
    Rotation by theta about the Y axis
    """


class RZGate(_StandardGate, angles=["phi"]):
    """
    Rotation by phi about the Z axis
    """


class RGate(_StandardGate, angles=["theta", "phi"]):
    """
    Rotation by theta about the cos(phi)X + sin(phi)Y axis
    """


class PhaseGate(_StandardGate, angles=["theta"]):
    """
    Add relative phase of lambda
    """

    _name: str = "p"


class _DoubleRotationGate(_StandardGate, angles=["theta"]):
    """
    Base class for RXX, RYY, RZZ
    """

    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=2)


class RXXGate(_DoubleRotationGate):
    """
    Rotation by theta about the XX axis
    """


class RYYGate(_DoubleRotationGate):
    """
    Rotation by theta about the YY axis
    """


class RZZGate(_DoubleRotationGate):
    """
    Rotation by theta about the ZZ axis
    """

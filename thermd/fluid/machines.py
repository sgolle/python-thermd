# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations
from dataclasses import dataclass

# from typing import List, Dict, Union

# from CoolProp.CoolProp import PropsSI
# from CoolProp.HumidAirProp import HAPropsSI
# import math
import numpy as np

# from scipy import optimize as opt
from thermd.core import (
    BaseResultClass,
    BaseModelClass,
    # BasePortClass,
    BaseStateClass,
    # BaseSignalClass,
    PortState,
    # PortSignal,
    PortTypes,
    MediumPure,
    # MediumBinaryMixture,
)
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Result classes
@dataclass
class MachineResult(BaseResultClass):
    ...


# Machine classes
class PumpSimple(BaseModelClass):
    """PumpSimple class.

    The PumpSimple class implements a pump which delivers the mass flow from the inlet
    with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: PumpSimple, name: str, state0: BaseStateClass, dp: np.float64,
    ):
        """Initialize PumpSimple class.

        Init function of the PumpSimple class.

        """
        super().__init__(name=name)

        # Checks
        if not isinstance(state0, MediumPure):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumPure.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports:
        self.__port_a = name + "_port_a"
        self.__port_b = name + "_port_b"
        self.__ports = {
            self.__port_a: PortState(
                name=self.__port_a, port_type=PortTypes.STATE_INLET, port_attr=state0,
            ),
            self.__port_b: PortState(
                name=self.__port_b, port_type=PortTypes.STATE_OUTLET, port_attr=state0,
            ),
        }

        # Pump parameters
        self.__dp = dp

        # Stop criterions
        self.__last_hmass = state0.hmass
        self.__last_p = state0.p
        self.__last_m_flow = state0.m_flow

    @property
    def stop_criterion_energy(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.p - self.__last_p

    @property
    def stop_criterion_mass(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.m_flow - self.__last_m_flow

    def check(self: PumpSimple) -> bool:
        return True

    def get_results(self: PumpSimple) -> MachineResult:
        return MachineResult()

    def equation(self: PumpSimple):
        self.__ports[self.__port_b].state.set_ps(
            p=self.__ports[self.__port_a].state.p + self.__dp,
            s=self.__ports[self.__port_a].state.s,
        )

        # Stop criterions
        self.__last_hmass = self.__ports[self.__port_b].state.hmass
        self.__last_p = self.__ports[self.__port_b].state.p
        self.__last_m_flow = self.__ports[self.__port_b].state.m_flow


class CompressorSimple(BaseModelClass):
    """CompressorSimple class.

    The CompressorSimple class implements a pump which delivers the mass flow from the
    inlet with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: CompressorSimple, name: str, state0: BaseStateClass, dp: np.float64,
    ):
        """Initialize CompressorSimple class.

        Init function of the CompressorSimple class.

        """
        super().__init__(name=name)

        # Checks
        if not isinstance(state0, MediumPure):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumPure.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports
        self.__port_a = name + "_port_a"
        self.__port_b = name + "_port_b"
        self.__ports = {
            self.__port_a: PortState(
                name=self.__port_a, port_type=PortTypes.STATE_INLET, port_attr=state0,
            ),
            self.__port_b: PortState(
                name=self.__port_b, port_type=PortTypes.STATE_OUTLET, port_attr=state0,
            ),
        }

        # Pump parameters
        self.__dp = dp

        # Stop criterions
        self.__last_hmass = state0.hmass
        self.__last_p = state0.p
        self.__last_m_flow = state0.m_flow

    @property
    def stop_criterion_energy(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.p - self.__last_p

    @property
    def stop_criterion_mass(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.m_flow - self.__last_m_flow

    def check(self: CompressorSimple) -> bool:
        return True

    def get_results(self: CompressorSimple) -> MachineResult:
        return MachineResult()

    def equation(self: CompressorSimple):
        self.__ports[self.__port_b].state.set_ps(
            p=self.__ports[self.__port_a].state.p + self.__dp,
            s=self.__ports[self.__port_a].state.s,
        )

        # Stop criterions
        self.__last_hmass = self.__ports[self.__port_b].state.hmass
        self.__last_p = self.__ports[self.__port_b].state.p
        self.__last_m_flow = self.__ports[self.__port_b].state.m_flow


class TurbineSimple(BaseModelClass):
    """TurbineSimple class.

    The TurbineSimple class implements a pump which delivers the mass flow from the
    inlet with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: TurbineSimple, name: str, state0: BaseStateClass, dp: np.float64,
    ):
        """Initialize TurbineSimple class.

        Init function of the TurbineSimple class.

        """
        super().__init__(name=name)

        # Checks
        if not isinstance(state0, MediumPure):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumPure.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports
        self.__port_a = name + "_port_a"
        self.__port_b = name + "_port_b"
        self.__ports = {
            self.__port_a: PortState(
                name=self.__port_a, port_type=PortTypes.STATE_INLET, port_attr=state0,
            ),
            self.__port_b: PortState(
                name=self.__port_b, port_type=PortTypes.STATE_OUTLET, port_attr=state0,
            ),
        }

        # Pump parameters
        self.__dp = dp

        # Stop criterions
        self.__last_hmass = state0.hmass
        self.__last_p = state0.p
        self.__last_m_flow = state0.m_flow

    @property
    def stop_criterion_energy(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.p - self.__last_p

    @property
    def stop_criterion_mass(self: PumpSimple) -> np.float64:
        return self.__ports[self.__port_b].state.m_flow - self.__last_m_flow

    def check(self: TurbineSimple) -> bool:
        return True

    def get_results(self: TurbineSimple) -> MachineResult:
        return MachineResult()

    def equation(self: TurbineSimple):
        self.__ports[self.__port_b].state.set_ps(
            p=self.__ports[self.__port_a].state.p + self.__dp,
            s=self.__ports[self.__port_a].state.s,
        )

        # Stop criterions
        self.__last_hmass = self.__ports[self.__port_b].state.hmass
        self.__last_p = self.__ports[self.__port_b].state.p
        self.__last_m_flow = self.__ports[self.__port_b].state.m_flow


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("This is the file for the machine model classes.")

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
    BasePortClass,
    BaseResultClass,
    BaseModelClass,
    # BasePortClass,
    BaseStateClass,
    # BaseSignalClass,
    PortState,
    # PortSignal,
    PortTypes,
    MediumBase,
    # MediumHumidAir,
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
        if not isinstance(state0, MediumBase):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumBase.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name,
                port_type=PortTypes.STATE_INLET,
                port_attr=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0,
            )
        )

        # Pump parameters
        self._dp = dp

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: PumpSimple) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    def check(self: PumpSimple) -> bool:
        return True

    def get_results(self: PumpSimple) -> MachineResult:
        return MachineResult()

    def equation(self: PumpSimple):
        # New state
        self._ports[self._port_b_name].state.set_ps(
            p=self._ports[self._port_a_name].state.p + self._dp,
            s=self._ports[self._port_a_name].state.smass,
        )

        # New mass flow
        self._ports[self._port_b_name].state.m_flow = self._ports[
            self._port_a_name
        ].state.m_flow

        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_p = self._ports[self._port_b_name].state.p
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow


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
        if not isinstance(state0, MediumBase):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumBase.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name,
                port_type=PortTypes.STATE_INLET,
                port_attr=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0,
            )
        )

        # Pump parameters
        self._dp = dp

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: CompressorSimple) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: CompressorSimple) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    def check(self: CompressorSimple) -> bool:
        return True

    def get_results(self: CompressorSimple) -> MachineResult:
        return MachineResult()

    def equation(self: CompressorSimple):
        self._ports[self._port_b_name].state.set_ps(
            p=self._ports[self._port_a_name].state.p + self._dp,
            s=self._ports[self._port_a_name].state.smass,
        )

        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_p = self._ports[self._port_b_name].state.p
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow


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
        if not isinstance(state0, MediumBase):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumBase.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name,
                port_type=PortTypes.STATE_INLET,
                port_attr=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0,
            )
        )

        # Pump parameters
        self._dp = dp

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: TurbineSimple) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: TurbineSimple) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: PumpSimple) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    def check(self: TurbineSimple) -> bool:
        return True

    def get_results(self: TurbineSimple) -> MachineResult:
        return MachineResult()

    def equation(self: TurbineSimple):
        self._ports[self._port_b_name].state.set_ps(
            p=self._ports[self._port_a_name].state.p + self._dp,
            s=self._ports[self._port_a_name].state.smass,
        )

        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_p = self._ports[self._port_b_name].state.p
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the machine model classes.")

# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Union

from CoolProp.CoolProp import PropsSI
from CoolProp.HumidAirProp import HAPropsSI
import math
import numpy as np
from numpy.lib.ufunclike import isneginf
from scipy import optimize as opt
from thermd.core import (
    BaseResultClass,
    BaseModelClass,
    BasePortClass,
    BaseStateClass,
    BaseSignalClass,
    PortState,
    PortSignal,
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


# Mixin classes

# Machine classes
class HXSimple(BaseModelClass):
    """HXSimple class.

    The HXSimple class implements a pump which delivers the mass flow from the inlet
    with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: HXSimple, name: str, state0: BaseStateClass, dp: np.float64,
    ):
        super().__init__(name=name)

        # Checks
        if not isinstance(state0, MediumBase):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumBase.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports
        self._port_inlet = PortState(
            name=name + "_port_a", port_type=PortTypes.INLET, state=state0,
        )
        self._port_outlet = PortState(
            name=name + "_port_b", port_type=PortTypes.OUTLET, state=state0,
        )

        # Pump parameters
        # self._P = np.float64(0.0)
        self._dp = dp

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def stop_criterion_energy(self: HXSimple) -> np.float64:
        return self._port_outlet.state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: HXSimple) -> np.float64:
        return self._port_outlet.state.p - self._last_p

    @property
    def stop_criterion_mass(self: HXSimple) -> np.float64:
        return self._port_outlet.state.m_flow - self._last_m_flow

    def check(self: HXSimple) -> bool:
        return True

    def get_results(self: HXSimple) -> MachineResult:
        return MachineResult()

    def equation(self: HXSimple):
        self._port_outlet.state = self._port_inlet.state
        self._port_outlet.state.set_ps(
            p=self._port_inlet.state.p + self._dp, s=self._port_inlet.state.s
        )


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("This is the file for the machine model classes.")

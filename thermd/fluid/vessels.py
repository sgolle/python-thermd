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
    PortFunctionTypes,
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
        if not isinstance(state0, MediumPure):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumPure.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Ports
        self.__port_inlet = PortState(
            name=name + "_port_a", port_function=PortFunctionTypes.INLET, state=state0,
        )
        self.__port_outlet = PortState(
            name=name + "_port_b", port_function=PortFunctionTypes.OUTLET, state=state0,
        )

        # Pump parameters
        # self.__P = np.float64(0.0)
        self.__dp = dp

        # Stop criterions
        self.__last_hmass = state0.hmass
        self.__last_p = state0.p
        self.__last_m_flow = state0.m_flow

    @property
    def ports(self: HXSimple) -> List[BasePortClass]:
        return [self.__port_inlet, self.__port_outlet]

    # @property
    # def port_inlet(self: PumpSimple) -> BasePortClass:
    #     return self.__port_inlet

    # @port_inlet.setter
    # def port_inlet(self: PumpSimple, port: BasePortClass) -> None:
    #     self.__port_inlet = port

    # @property
    # def port_outlet(self: PumpSimple) -> BasePortClass:
    #     return self.__port_outlet

    # @port_outlet.setter
    # def port_outlet(self: PumpSimple, port: BasePortClass) -> None:
    #     self.__port_outlet = port

    @property
    def stop_criterion_energy(self: HXSimple) -> np.float64:
        return self.__port_outlet.state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: HXSimple) -> np.float64:
        return self.__port_outlet.state.p - self.__last_p

    @property
    def stop_criterion_mass(self: HXSimple) -> np.float64:
        return self.__port_outlet.state.m_flow - self.__last_m_flow

    def check(self: HXSimple) -> bool:
        return True

    def set_port_state(self: HXSimple, port_name: str, state: BaseStateClass,) -> None:
        if port_name == self.__port_inlet.name:
            self.__port_inlet.state = state

        elif port_name == self.__port_outlet.name:
            self.__port_outlet.state = state

        else:
            logger.error("Cannot set port state: Unknown port name.")
            raise SystemExit

    def set_port_signal(
        self: HXSimple, port_name: str, signal: BaseSignalClass,
    ) -> None:
        if port_name == self.__port_inlet.name:
            self.__port_inlet.signal = signal
        elif port_name == self.__port_outlet.name:
            self.__port_outlet.signal = signal
        else:
            logger.error("Cannot set port signal: Unknown port name.")
            raise SystemExit

    def get_port_state(self: HXSimple, port_name: str,) -> BaseStateClass:
        if port_name == self.__port_inlet.name:
            state = self.__port_inlet.state
        elif port_name == self.__port_outlet.name:
            state = self.__port_outlet.state
        else:
            logger.error("Cannot get port state: Unknown port name.")
            raise SystemExit

        return state

    def get_port_signal(self: HXSimple, port_name: str,) -> BaseSignalClass:
        if port_name == self.__port_inlet.name:
            signal = self.__port_inlet.signal
        elif port_name == self.__port_outlet.name:
            signal = self.__port_outlet.signal
        else:
            logger.error("Cannot get port signal: Unknown port name.")
            raise SystemExit

        return signal

    def get_results(self: HXSimple) -> MachineResult:
        return MachineResult()

    def equation(self: HXSimple):
        self.__port_outlet.state = self.__port_inlet.state
        self.__port_outlet.state.set_ps(
            p=self.__port_inlet.state.p + self.__dp, s=self.__port_inlet.state.s
        )


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("This is the file for the machine model classes.")


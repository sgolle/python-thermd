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
        self.__P = np.float64(0.0)
        self.__dp = dp

        # Stop criterions

    @property
    def ports(self: PumpSimple) -> List[BasePortClass]:
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
    def stop_criterion_energy(self: PumpSimple) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_momentum(self: PumpSimple) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: PumpSimple) -> np.float64:
        return np.float64(0.0)

    def check(self: PumpSimple) -> bool:
        return True

    def set_port_attr(
        self: BaseModelClass,
        port_name: str,
        port_attr: Union[BaseStateClass, BaseSignalClass],
    ) -> None:
        if port_name == self.__port_inlet.name:
            if isinstance(self.__port_inlet, PortState) and isinstance(
                port_attr, BaseStateClass
            ):
                self.__port_inlet.state = port_attr
            elif isinstance(self.__port_inlet, PortSignal) and isinstance(
                port_attr, BaseSignalClass
            ):
                self.__port_inlet.signal = port_attr
            else:
                logger.error("Cannot set port attribute: Wrong types.")
                raise SystemExit

        elif port_name == self.__port_outlet.name:
            if isinstance(self.__port_outlet, PortState) and isinstance(
                port_attr, BaseStateClass
            ):
                self.__port_outlet.state = port_attr
            elif isinstance(self.__port_outlet, PortSignal) and isinstance(
                port_attr, BaseSignalClass
            ):
                self.__port_outlet.signal = port_attr
            else:
                logger.error("Cannot set port attribute: Wrong types.")
                raise SystemExit

        else:
            logger.error("Cannot set port attribute: Unknown port name.")
            raise SystemExit

    def get_port_attr(
        self: BaseModelClass, port_name: str,
    ) -> Union[BaseStateClass, BaseSignalClass]:
        if port_name == self.__port_inlet.name:
            if isinstance(self.__port_inlet, PortState) and isinstance(
                port_attr, BaseStateClass
            ):
                self.__port_inlet.state = port_attr
            elif isinstance(self.__port_inlet, PortSignal) and isinstance(
                port_attr, BaseSignalClass
            ):
                self.__port_inlet.signal = port_attr
            else:
                logger.error("Cannot set port attribute: Wrong types.")
                raise SystemExit

        elif port_name == self.__port_outlet.name:
            if isinstance(self.__port_outlet, PortState) and isinstance(
                port_attr, BaseStateClass
            ):
                self.__port_outlet.state = port_attr
            elif isinstance(self.__port_outlet, PortSignal) and isinstance(
                port_attr, BaseSignalClass
            ):
                self.__port_outlet.signal = port_attr
            else:
                logger.error("Cannot set port attribute: Wrong types.")
                raise SystemExit

        else:
            logger.error("Cannot set port attribute: Unknown port name.")
            raise SystemExit

    def get_results(self: PumpSimple) -> MachineResult:
        return MachineResult()

    def equation(self: PumpSimple):
        self.__port_outlet.state = self.__port_inlet.state
        self.__port_outlet.state.set_ps(
            p=self.__port_inlet.state.p + self.__dp, s=self.__port_inlet.state.s
        )


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("This is the file for the machine model classes.")

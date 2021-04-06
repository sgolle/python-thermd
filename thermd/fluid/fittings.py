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
    MediumPure,
    # MediumBinaryMixture,
)
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Result classes
@dataclass
class FittingsResult(BaseResultClass):
    ...


# Machine classes
class JunctionOneToThree(BaseModelClass):
    """JunctionOneToThree class.

    The JunctionOneToThree class implements a pump which delivers the mass flow from the inlet
    with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: JunctionOneToThree,
        name: str,
        state0: BaseStateClass,
        fraction: np.float64,
    ):
        super().__init__(name=name)

        # Ports
        self.__port_a = name + "_port_a"
        self.__port_b1 = name + "_port_b1"
        self.__port_b2 = name + "_port_b2"
        self.__port_b3 = name + "_port_b3"
        self.__ports = {
            self.__port_a: PortState(
                name=self.__port_a, port_type=PortTypes.STATE_INLET, port_attr=state0,
            ),
            self.__port_b1: PortState(
                name=self.__port_b1, port_type=PortTypes.STATE_OUTLET, port_attr=state0,
            ),
            self.__port_b2: PortState(
                name=self.__port_b2, port_type=PortTypes.STATE_OUTLET, port_attr=state0,
            ),
            self.__port_b3: PortState(
                name=self.__port_b3, port_type=PortTypes.STATE_OUTLET, port_attr=state0,
            ),
        }

        # Junction parameters
        self.__fraction = fraction

        # Stop criterions
        self.__last_hmass = state0.hmass
        self.__last_p = state0.p
        self.__last_m_flow = state0.m_flow

    @property
    def stop_criterion_energy(self: JunctionOneToThree) -> np.float64:
        return self.__ports[self.__port_b].state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: JunctionOneToThree) -> np.float64:
        return self.__ports[self.__port_b].state.p - self.__last_p

    @property
    def stop_criterion_mass(self: JunctionOneToThree) -> np.float64:
        return self.__ports[self.__port_b].state.m_flow - self.__last_m_flow

    def check(self: JunctionOneToThree) -> bool:
        return True

    def get_results(self: JunctionOneToThree) -> FittingsResult:
        return FittingsResult()

    def equation(self: JunctionOneToThree):
        self.__port_outlet.state = self.__port_inlet.state
        self.__port_outlet.state.set_ps(
            p=self.__port_inlet.state.p + self.__dp, s=self.__port_inlet.state.s
        )

        # Stop criterions
        self.__last_hmass = self.__ports[self.__port_b].state.hmass
        self.__last_p = self.__ports[self.__port_b].state.p
        self.__last_m_flow = self.__ports[self.__port_b].state.m_flow


class JunctionTwoToOne(BaseModelClass):
    """JunctionOneToThree class.

    The JunctionOneToThree class implements a pump which delivers the mass flow from the inlet
    with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: JunctionTwoToOne, name: str, state0: BaseStateClass, dp: np.float64,
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

        # Junction parameters
        # self.__P = np.float64(0.0)
        self.__dp = dp

        # Stop criterions
        self.__last_hmass = state0.hmass
        self.__last_p = state0.p
        self.__last_m_flow = state0.m_flow

    @property
    def stop_criterion_energy(self: JunctionTwoToOne) -> np.float64:
        return self.__ports[self.__port_b].state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: JunctionTwoToOne) -> np.float64:
        return self.__ports[self.__port_b].state.p - self.__last_p

    @property
    def stop_criterion_mass(self: JunctionTwoToOne) -> np.float64:
        return self.__ports[self.__port_b].state.m_flow - self.__last_m_flow

    def check(self: JunctionTwoToOne) -> bool:
        return True

    def get_results(self: JunctionTwoToOne) -> FittingsResult:
        return FittingsResult()

    def equation(self: JunctionTwoToOne):
        self.__port_outlet.state = self.__port_inlet.state
        self.__port_outlet.state.set_ps(
            p=self.__port_inlet.state.p + self.__dp, s=self.__port_inlet.state.s
        )

        # Stop criterions
        self.__last_hmass = self.__ports[self.__port_b].state.hmass
        self.__last_p = self.__ports[self.__port_b].state.p
        self.__last_m_flow = self.__ports[self.__port_b].state.m_flow


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("Not implemented.")

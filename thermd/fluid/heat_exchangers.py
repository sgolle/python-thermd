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
from scipy import optimize as opt
from thermd.core import (
    BaseResultClass,
    BaseModelClass,
    BasePortClass,
    BaseStateClass,
    BaseSignalClass,
    MediumBinaryMixture,
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
class HXResult(BaseResultClass):
    ...


# Mixin classes
class HXMixin:
    """HX mixin class.

    The HX mixin class includes some base methods for calculating heat exchangers.

    """

    @staticmethod
    def N_eps_counterflow(eps, C):
        if C == 1:
            N = eps / (1 - eps)
        elif C == 0:
            N = -math.log(1 - eps)
        else:
            N = (1 / (1 - C)) * math.log((1 - C * eps) / (1 - eps))

        return N

    @staticmethod
    def eps_N_counterflow(N, C):
        if C == 1:
            eps = N / (1 + N)
        elif C == 0:
            eps = 1 - math.exp(-N)
        else:
            eps = (1 - math.exp((C - 1) * N)) / (1 - C * math.exp((C - 1) * N))

        return eps

    @staticmethod
    def N_eps_parallelflow(eps, C):
        if C == 0:
            N = -math.log(1 - eps)
        else:
            N = -1 * (math.log(1 - eps * (1 + C))) / (1 + C)

        return N

    @staticmethod
    def eps_N_parallelflow(N, C):
        if C == 0:
            eps = 1 - math.exp(-N)
        else:
            eps = (1 - math.exp(-1 * (1 + C) * N)) / (1 + C)

        return eps

    @staticmethod
    def N_eps_crossflow_oneside_mixed(eps, C):
        if C == 0:
            N = -math.log(1 - eps)
        else:
            N = (-1 / C) * math.log(1 + C * math.log(1 - eps))

        return N

    @staticmethod
    def eps_N_crossflow_oneside_mixed(N, C):
        if C == 0:
            eps = 1 - math.exp(-N)
        else:
            eps = 1 - math.exp((-1 / C) * (1 - math.exp(-C * N)))

        return eps

    @staticmethod
    def N_eps_crossflow_unmixed_interpol(N, eps, C):
        return eps - (
            1 - math.exp((1 / C) * (N ** 0.22) * (math.exp(-C * N ** 0.78) - 1))
        )

    def N_eps_crossflow_unmixed(self, eps, C):
        if C == 0:
            N = -math.log(1 - eps)
        else:
            N = opt.fsolve(self.N_eps_crossflow_unmixed_interpol, 0.0, args=(eps, C),)[
                0
            ]

        return N

    @staticmethod
    def eps_N_crossflow_unmixed(N, C):
        if C == 0:
            eps = 1 - math.exp(-N)
        else:
            eps = 1 - math.exp((1 / C) * (N ** 0.22) * (math.exp(-C * N ** 0.78) - 1))
        return eps


# Heat sink/source classes
class HeatSinkSource(BaseModelClass):
    """HeatSinkSource class.

    The HeatSinkSource class implements a simple heat exchanger with only one fluid
    heated or cooled by a heat source or sink.

    """

    def __init__(
        self: HeatSinkSource, name: str, state0: BaseStateClass, Q: np.float64,
    ):
        """Initialize HeatSinkSource class.

        Init function of the HeatSinkSource class.

        """
        super().__init__(name=name)

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

        # Heat sink/source parameters
        self.__Q = Q

        # Stop criterions
        self.__last_hmass = state0.hmass
        self.__last_p = state0.p
        self.__last_m_flow = state0.m_flow

    @property
    def stop_criterion_energy(self: HeatSinkSource) -> np.float64:
        return self.__ports[self.__port_b].state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: HeatSinkSource) -> np.float64:
        return self.__ports[self.__port_b].state.p - self.__last_p

    @property
    def stop_criterion_mass(self: HeatSinkSource) -> np.float64:
        return self.__ports[self.__port_b].state.m_flow - self.__last_m_flow

    def check(self: HeatSinkSource) -> bool:
        return True

    def get_results(self: HeatSinkSource) -> HXResult:
        return HXResult()

    def equation(self: HeatSinkSource):
        h_out = (
            self.__Q / self.__ports[self.__port_a].state.m_flow
            + self.__ports[self.__port_a].state.hmass
        )
        if isinstance(self.__ports[self.__port_a].state, MediumPure):
            self.__ports[self.__port_b].state.set_ph(
                p=self.__ports[self.__port_a].state.p, h=h_out,
            )
        elif isinstance(self.__ports[self.__port_a].state, MediumBinaryMixture):
            self.__ports[self.__port_b].state.set_phw(
                p=self.__ports[self.__port_a].state.p,
                h=h_out,
                w=self.__ports[self.__port_a].state.w,
            )
        else:
            logger.error(
                "Wrong medium class in HeatSinkSource class definition: %s. "
                "Must be MediumPure or MediumBinaryMixture.",
                self.__ports[self.__port_a].state.super().__class__.__name__,
            )
            raise SystemExit

        # Stop criterions
        self.__last_hmass = self.__ports[self.__port_b].state.hmass
        self.__last_p = self.__ports[self.__port_b].state.p
        self.__last_m_flow = self.__ports[self.__port_b].state.m_flow


# Heat exchanger classes
class HXSimple(BaseModelClass, HXMixin):
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
    def stop_criterion_energy(self: HXSimple) -> np.float64:
        return self.__ports[self.__port_b].state.hmass - self.__last_hmass

    @property
    def stop_criterion_momentum(self: HXSimple) -> np.float64:
        return self.__ports[self.__port_b].state.p - self.__last_p

    @property
    def stop_criterion_mass(self: HXSimple) -> np.float64:
        return self.__ports[self.__port_b].state.m_flow - self.__last_m_flow

    def check(self: HXSimple) -> bool:
        return True

    def get_results(self: HXSimple) -> HXResult:
        return HXResult()

    def equation(self: HXSimple):
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

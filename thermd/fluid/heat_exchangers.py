# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations
from dataclasses import dataclass

# from typing import List, Dict, Union

# from CoolProp.CoolProp import PropsSI
# from CoolProp.HumidAirProp import HAPropsSI
import math
import numpy as np
from scipy import optimize as opt
from thermd.core import (
    BaseModelClass,
    # BasePortClass,
    BaseStateClass,
    # BaseSignalClass,
    ModelResult,
    PortState,
    # PortSignal,
    PortTypes,
    MediumBase,
    MediumHumidAir,
)
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Result classes
@dataclass
class ResultHX(ModelResult):
    kA: np.float64


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
    def N_eps_crossflow_unmixed_interp(N, eps, C):
        return eps - (
            1 - math.exp((1 / C) * (N ** 0.22) * (math.exp(-C * N ** 0.78) - 1))
        )

    def N_eps_crossflow_unmixed(self, eps, C):
        if C == 0:
            N = -math.log(1 - eps)
        else:
            N = opt.fsolve(self.N_eps_crossflow_unmixed_interp, 0.0, args=(eps, C),)[0]

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
        self: HeatSinkSource,
        name: str,
        state0: BaseStateClass,
        Q: np.float64,
        dp: np.float64,
    ):
        """Initialize HeatSinkSource class.

        Init function of the HeatSinkSource class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name,
                port_type=PortTypes.STATE_INLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )

        # Heat sink/source parameters
        self._Q = Q
        self._dp = dp

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: HeatSinkSource) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: HeatSinkSource) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: HeatSinkSource) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: HeatSinkSource) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: HeatSinkSource) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    def check(self: HeatSinkSource) -> bool:
        return True

    def get_results(self: HeatSinkSource) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        return ModelResult(states=states, signals=None)

    def equation(self: HeatSinkSource):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_p = self._ports[self._port_b_name].state.p
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow

        # Check mass flow
        if self._ports[self._port_a_name].state.m_flow <= 0.0:
            logger.debug("No mass flow in model %s.", self._name)
            return

        # New state
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            h_out = (
                self._Q / self._ports[self._port_a_name].state.m_flow
                + self._ports[self._port_a_name].state.hmass
            )
            self._ports[self._port_b_name].state.set_ph(
                p=self._ports[self._port_a_name].state.p + self._dp, h=h_out,
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            h_out = (
                self._Q
                / (
                    self._ports[self._port_a_name].state.m_flow
                    / (1 + self._ports[self._port_a_name].state.w)
                )
                + self._ports[self._port_a_name].state.hmass
            )
            self._ports[self._port_b_name].state.set_phw(
                p=self._ports[self._port_a_name].state.p + self._dp,
                h=h_out,
                w=self._ports[self._port_a_name].state.w,
            )
        else:
            logger.error(
                "Wrong medium class in HeatSinkSource class definition: %s. "
                "Must be MediumBase or MediumHumidAir.",
                self._ports[self._port_a_name].state.super().__class__.__name__,
            )
            raise SystemExit

        # New mass flow
        self._ports[self._port_b_name].state.m_flow = self._ports[
            self._port_a_name
        ].state.m_flow


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
        """Initialize HXSimple class.

        Init function of the HXSimple class.

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
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )

        # Pump parameters
        self._dp = dp

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: HXSimple) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: HXSimple) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: HXSimple) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: HXSimple) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: HXSimple) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    def check(self: HXSimple) -> bool:
        return True

    def get_results(self: HeatSinkSource) -> ResultHX:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        return ResultHX(states=states, signals=None, kA=np.float64(-1.0),)

    def equation(self: HXSimple):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_p = self._ports[self._port_b_name].state.p
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow

        # Check mass flow
        if (
            self._ports[self._port_a1_name].state.m_flow <= 0.0
            and self._ports[self._port_a2_name].state.m_flow <= 0.0
        ):
            logger.debug("No mass flows in model %s.", self._name)
            return

        self._ports[self._port_b_name].state.set_ps(
            p=self._ports[self._port_a_name].state.p + self._dp,
            s=self._ports[self._port_a_name].state.s,
        )


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the heat exchanger model classes.")

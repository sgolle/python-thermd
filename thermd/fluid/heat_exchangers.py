# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations
from typing import Tuple

import numpy as np
from scipy import optimize as opt
from thermd.core import (
    BaseStateClass,
    # BaseSignalClass,
    MediumBase,
    MediumHumidAir,
)
from thermd.fluid.core import BaseFluidOneInletOneOutlet, BaseFluidTwoInletsTwoOutlets
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Result classes
# @dataclass
# class ResultHX(ModelResult):
#     kA: np.float64


# Mixin classes
class HXMixin:
    """HX mixin class.

    The HX mixin class includes some base methods for calculating heat exchangers.

    """

    @staticmethod
    def W(state: BaseStateClass):
        if isinstance(state, MediumBase):
            W = state.m_flow * state.cpmass
        elif isinstance(state, MediumHumidAir):
            W = state.m_flow / (1 + state.w) * state.cpmass
        else:
            logger.error(
                "Wrong medium class in HXSimple class: %s. "
                "Must be MediumBase or MediumHumidAir.",
                state.super().__class__.__name__,
            )
            raise SystemExit

        return W

    def C(self: HXMixin, state1: BaseStateClass, state2: BaseStateClass):
        W1 = self.W(state=state1)
        W2 = self.W(state=state2)

        return W1 / W2

    @staticmethod
    def eps(
        state1_in: BaseStateClass, state1_out: BaseStateClass, state2_in: BaseStateClass
    ):
        return (state1_in.T - state1_out.T) / (state1_in.T - state2_in.T)

    def T1_out(
        self: HXMixin,
        state1_in: BaseStateClass,
        state2_in: BaseStateClass,
        kA: np.float64,
    ):
        # Number of transfer units fluid 1
        N1 = kA / self.W(state=state1_in)

        # Ratio of heat capacity flows
        C1 = self.C(state1=state1_in, state2=state2_in,)

        # Normalized temperature difference fluid 1
        eps1 = self.eps_N_counterflow(N1, C1)

        # Outlet temperature fluid 1
        T1_out = state1_in.T - (state1_in.T - state2_in.T) * eps1

        return T1_out

    @staticmethod
    def N_eps_counterflow(eps: np.float64, C: np.float64) -> np.float64:
        if C == 1:
            N = eps / (1 - eps)
        elif C == 0:
            N = -np.log(1 - eps)
        else:
            N = (1 / (1 - C)) * np.log((1 - C * eps) / (1 - eps))

        return N

    @staticmethod
    def eps_N_counterflow(N: np.float64, C: np.float64) -> np.float64:
        if C == 1:
            eps = N / (1 + N)
        elif C == 0:
            eps = 1 - np.exp(-N)
        else:
            eps = (1 - np.exp((C - 1) * N)) / (1 - C * np.exp((C - 1) * N))

        return eps

    @staticmethod
    def N_eps_parallelflow(eps: np.float64, C: np.float64) -> np.float64:
        if C == 0:
            N = -np.log(1 - eps)
        else:
            N = -1 * (np.log(1 - eps * (1 + C))) / (1 + C)

        return N

    @staticmethod
    def eps_N_parallelflow(N: np.float64, C: np.float64) -> np.float64:
        if C == 0:
            eps = 1 - np.exp(-N)
        else:
            eps = (1 - np.exp(-1 * (1 + C) * N)) / (1 + C)

        return eps

    @staticmethod
    def N_eps_crossflow_oneside_mixed(eps: np.float64, C: np.float64) -> np.float64:
        if C == 0:
            N = -np.log(1 - eps)
        else:
            N = (-1 / C) * np.log(1 + C * np.log(1 - eps))

        return N

    @staticmethod
    def eps_N_crossflow_oneside_mixed(N: np.float64, C: np.float64) -> np.float64:
        if C == 0:
            eps = 1 - np.exp(-N)
        else:
            eps = 1 - np.exp((-1 / C) * (1 - np.exp(-C * N)))

        return eps

    @staticmethod
    def N_eps_crossflow_unmixed_interp(
        N: np.float64, eps: np.float64, C: np.float64
    ) -> np.float64:
        return eps - (1 - np.exp((1 / C) * (N ** 0.22) * (np.exp(-C * N ** 0.78) - 1)))

    def N_eps_crossflow_unmixed(
        self: HXMixin, eps: np.float64, C: np.float64
    ) -> np.float64:
        if C == 0:
            N = -np.log(1 - eps)
        else:
            N = opt.fsolve(self.N_eps_crossflow_unmixed_interp, 0.0, args=(eps, C),)[0]

        return N

    @staticmethod
    def eps_N_crossflow_unmixed(N: np.float64, C: np.float64) -> np.float64:
        if C == 0:
            eps = 1 - np.exp(-N)
        else:
            eps = 1 - np.exp((1 / C) * (N ** 0.22) * (np.exp(-C * N ** 0.78) - 1))
        return eps


# Heat sink/source classes
class HeatSinkSource(BaseFluidOneInletOneOutlet):
    """HeatSinkSource class.

    The HeatSinkSource class implements a simple heat exchanger with only one fluid
    heated or cooled by a heat source or sink and a fixed pressure drop.

    """

    def __init__(
        self: HeatSinkSource,
        name: str,
        state0: BaseStateClass,
        Q: np.float64,
        dp: np.float64,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, state0=state0)

        # Heat sink/source parameters
        self._Q = Q
        self._dp = dp

    def check_self(self: HeatSinkSource) -> bool:
        return True

    def equation(self: HeatSinkSource):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
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
class HXSimple(BaseFluidTwoInletsTwoOutlets, HXMixin):
    """HXSimple class.

    The HXSimple class implements a simple counter-flow heat exchanger 
    with fixed pressure drop and one fixed kA value for the whole area
    and every possible phase changes and with corresponding temperature difference
    from the inlets.

    """

    def __init__(
        self: HXSimple,
        name: str,
        state0_1: BaseStateClass,
        state0_2: BaseStateClass,
        dp_1: np.float64,
        dp_2: np.float64,
        kA: np.float64,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, state0_1=state0_1, state0_2=state0_2)

        # Heat exchanger parameters
        self._dp_1 = dp_1
        self._dp_2 = dp_2
        self._kA = kA

    def check_self(self: HXSimple) -> bool:
        return True

    def func_eps_N_method_helper(
        self,
        state1_in: BaseStateClass,
        state2_in: BaseStateClass,
        dp_1: np.float64,
        dp_2: np.float64,
    ) -> Tuple[BaseStateClass, BaseStateClass]:

        # Copy outlet states from inlet states
        state1_out = state1_in.copy()
        state2_out = state2_in.copy()

        T1_out = self.T1_out(state1_in=state1_in, state2_in=state2_in, kA=self._kA)

        # New state fluid 1
        if isinstance(state1_in, MediumBase):
            state1_out.set_pT(
                p=state1_in.p + dp_1, T=T1_out,
            )
            Q = state1_in.m_flow * (state1_out.hmass - state1_in.hmass)
        elif isinstance(state1_in, MediumHumidAir):
            state1_out.set_pTw(
                p=state1_in.p + dp_1, T=T1_out, w=state1_in.w,
            )
            Q = (
                state1_in.m_flow
                / (1 + state1_in.w)
                * (state1_out.hmass - state1_in.hmass)
            )
        else:
            logger.error(
                "Wrong medium class in HXSimple class definition: %s. "
                "Must be MediumBase or MediumHumidAir.",
                state1_in.super().__class__.__name__,
            )
            raise SystemExit

        # New state fluid 2
        if isinstance(state2_in, MediumBase):
            h2_out = state2_in.hmass - Q / state2_in.m_flow
            state2_out.set_ph(
                p=state2_in.p + dp_2, h=h2_out,
            )
        elif isinstance(state2_in, MediumHumidAir):
            h2_out = state2_in.hmass - Q / (state2_in.m_flow / (1 + state2_in.w))
            state2_out.set_phw(
                p=state2_in.p + dp_2, h=h2_out, w=state2_in.w,
            )
        else:
            logger.error(
                "Wrong medium class in HXSimple class definition: %s. "
                "Must be MediumBase or MediumHumidAir.",
                state2_in.super().__class__.__name__,
            )
            raise SystemExit

        return state1_out, state2_out

    def func_Q_helper(
        self,
        state1_in: BaseStateClass,
        state2_in: BaseStateClass,
        dp_1: np.float64,
        dp_2: np.float64,
    ) -> Tuple[BaseStateClass, BaseStateClass]:

        # Copy outlet states from inlet states
        state1_out = state1_in.copy()
        state2_out = state2_in.copy()

        Q = self._kA * (state1_in.T - state2_in.T)

        # New state fluid 1
        if isinstance(state1_in, MediumBase):
            h1_out = Q / state1_in.m_flow + state1_in.hmass
            state1_out.set_ph(
                p=state1_in.p + dp_1, h=h1_out,
            )
        elif isinstance(state1_in, MediumHumidAir):
            h1_out = Q / (state1_in.m_flow / (1 + state1_in.w)) + state1_in.hmass
            state1_out.set_phw(
                p=state1_in.p + dp_1, h=h1_out, w=state1_in.w,
            )
        else:
            logger.error(
                "Wrong medium class in HXSimple class definition: %s. "
                "Must be MediumBase or MediumHumidAir.",
                state1_in.super().__class__.__name__,
            )
            raise SystemExit

        # New state fluid 2
        if isinstance(state2_in, MediumBase):
            h2_out = state2_in.hmass - Q / state2_in.m_flow
            state2_out.set_ph(
                p=state2_in.p + dp_2, h=h2_out,
            )
        elif isinstance(state2_in, MediumHumidAir):
            h2_out = state2_in.hmass - Q / (state2_in.m_flow / (1 + state2_in.w))
            state2_out.set_phw(
                p=state2_in.p + dp_2, h=h2_out, w=state2_in.w,
            )
        else:
            logger.error(
                "Wrong medium class in HXSimple class definition: %s. "
                "Must be MediumBase or MediumHumidAir.",
                state2_in.super().__class__.__name__,
            )
            raise SystemExit

        return state1_out, state2_out

    def equation(self: HXSimple):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b1_name].state.hmass
        self._last_m_flow = self._ports[self._port_b1_name].state.m_flow

        # Check mass flow
        if (
            self._ports[self._port_a1_name].state.m_flow <= 0.0
            and self._ports[self._port_a2_name].state.m_flow <= 0.0
        ):
            logger.debug("No mass flows in model %s.", self._name)
            return

        # Main heat exchanger calculation with eps-NTU method
        if self._ports[self._port_a1_name].state.phase.value != 6:
            state1_out, state2_out = self.func_eps_N_method_helper(
                state1_in=self._ports[self._port_a1_name].state,
                state2_in=self._ports[self._port_a2_name].state,
                dp_1=self._dp_1,
                dp_2=self._dp_2,
            )

        elif self._ports[self._port_a2_name].state.phase.value != 6:
            state2_out, state1_out = self.func_eps_N_method_helper(
                state1_in=self._ports[self._port_a2_name].state,
                state2_in=self._ports[self._port_a1_name].state,
                dp_1=self._dp_2,
                dp_2=self._dp_1,
            )
        else:
            state1_out, state2_out = self.func_Q_helper(
                state1_in=self._ports[self._port_a1_name].state,
                state2_in=self._ports[self._port_a2_name].state,
                dp_1=self._dp_1,
                dp_2=self._dp_2,
            )

        self._ports[self._port_b1_name].state = state1_out
        self._ports[self._port_b2_name].state = state2_out


if __name__ == "__main__":
    logger.info("This is the file for the heat exchanger model classes.")

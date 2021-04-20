# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

import numpy as np
from thermd.core import (
    BaseStateClass,
    MediumBase,
    MediumHumidAir,
)
from thermd.fluid.core import BaseFluidOneInletOneOutlet
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Result classes
# @dataclass
# class ResultMachines(ModelResult):
#     power_electrical: np.float64
#     power_mechanical: np.float64
#     power_indicated_real: np.float64
#     power_indicated_ideal: np.float64
#     work_indicated_real: np.float64
#     work_indicated_ideal: np.float64
#     efficiency_electrical: np.float64
#     efficiency_mechanical: np.float64
#     efficiency_isentropic: np.float64
#     heat_loss: np.float64
#     n: np.float64

# Example ResultMachines:
# def get_results(self: PumpSimple) -> ResultMachines:
#     states = {
#         self._port_a_name: self._ports[self._port_a_name].state,
#         self._port_b_name: self._ports[self._port_b_name].state,
#     }
#     work = (
#         self._ports[self._port_b_name].state.hmass
#         - self._ports[self._port_a_name].state.hmass
#     )
#     power = self._ports[self._port_a_name].state.m_flow * work
#     return ResultMachines(
#         states=states,
#         signals=None,
#         power_electrical=power,
#         power_mechanical=power,
#         power_indicated_real=power,
#         power_indicated_ideal=power,
#         work_indicated_real=work,
#         work_indicated_ideal=work,
#         efficiency_electrical=np.float64(1.0),
#         efficiency_mechanical=np.float64(1.0),
#         efficiency_isentropic=np.float64(1.0),
#         heat_loss=np.float64(0.0),
#         n=np.float64(-1.0),
#     )

# Machine classes
class PumpSimple(BaseFluidOneInletOneOutlet):
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
        super().__init__(name=name, state0=state0)

        # Checks
        if not isinstance(state0, MediumBase):
            logger.error(
                "Wrong medium class in pump class definition: %s. Must be MediumBase.",
                state0.super().__class__.__name__,
            )
            raise SystemExit

        # Pump parameters
        self._dp = dp

    def check_self(self: PumpSimple) -> bool:
        return True

    def equation(self: PumpSimple):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow

        # Check mass flow
        if self._ports[self._port_a_name].state.m_flow <= 0.0:
            logger.debug("No mass flow in model %s.", self._name)
            return

        # New state
        self._ports[self._port_b_name].state.set_ps(
            p=self._ports[self._port_a_name].state.p + self._dp,
            s=self._ports[self._port_a_name].state.smass,
        )

        # New mass flow
        self._ports[self._port_b_name].state.m_flow = self._ports[
            self._port_a_name
        ].state.m_flow


class CompressorSimple(BaseFluidOneInletOneOutlet):
    """CompressorSimple class.

    The CompressorSimple class implements a pump which delivers the mass flow from the
    inlet with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: CompressorSimple, name: str, state0: BaseStateClass, pi: np.float64,
    ):
        """Initialize CompressorSimple class.

        Init function of the CompressorSimple class.

        """
        super().__init__(name=name, state0=state0)

        # Compressor parameters
        self._pi = pi

    def check_self(self: CompressorSimple) -> bool:
        return True

    def equation(self: CompressorSimple):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow

        # Check mass flow
        if self._ports[self._port_a_name].state.m_flow <= 0.0:
            logger.debug("No mass flow in model %s.", self._name)
            return

        # New state
        if isinstance(self._ports[self._port_a_name].state, MediumBase) and isinstance(
            self._ports[self._port_b_name].state, MediumBase
        ):
            self._ports[self._port_b_name].state.set_ps(
                p=self._ports[self._port_a_name].state.p * self._pi,
                s=self._ports[self._port_a_name].state.smass,
            )
        elif isinstance(
            self._ports[self._port_a_name].state, MediumHumidAir
        ) and isinstance(self._ports[self._port_b_name].state, MediumHumidAir):
            self._ports[self._port_b_name].state.set_psw(
                p=self._ports[self._port_a_name].state.p * self._pi,
                s=self._ports[self._port_a_name].state.smass,
                w=self._ports[self._port_a_name].state.w,
            )
        else:
            logger.error(
                (
                    "Wrong state classes in inlet and/or outlet: %s -> %s. "
                    "Should both be MediumBase or MediumHumidAir."
                ),
                self._ports[self._port_a_name].state.__class__.__name__,
                self._ports[self._port_b_name].state.__class__.__name__,
            )

        # New mass flow
        self._ports[self._port_b_name].state.m_flow = self._ports[
            self._port_a_name
        ].state.m_flow


class TurbineSimple(BaseFluidOneInletOneOutlet):
    """TurbineSimple class.

    The TurbineSimple class implements a pump which delivers the mass flow from the
    inlet with a constant pressure difference dp and ideal, isentropic behavior.
    No height or velocity difference between inlet and outlet.

    """

    def __init__(
        self: TurbineSimple, name: str, state0: BaseStateClass, pi: np.float64,
    ):
        """Initialize TurbineSimple class.

        Init function of the TurbineSimple class.

        """
        super().__init__(name=name, state0=state0)

        # Turbine parameters
        self._pi = pi

    def check_self(self: TurbineSimple) -> bool:
        return True

    def equation(self: TurbineSimple):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow

        # Check mass flow
        if self._ports[self._port_a_name].state.m_flow <= 0.0:
            logger.debug("No mass flow in model %s.", self._name)
            return

        # New state
        if isinstance(self._ports[self._port_a_name].state, MediumBase) and isinstance(
            self._ports[self._port_b_name].state, MediumBase
        ):
            self._ports[self._port_b_name].state.set_ps(
                p=self._ports[self._port_a_name].state.p * self._pi,
                s=self._ports[self._port_a_name].state.smass,
            )
        elif isinstance(
            self._ports[self._port_a_name].state, MediumHumidAir
        ) and isinstance(self._ports[self._port_b_name].state, MediumHumidAir):
            self._ports[self._port_b_name].state.set_psw(
                p=self._ports[self._port_a_name].state.p * self._pi,
                s=self._ports[self._port_a_name].state.smass,
                w=self._ports[self._port_a_name].state.w,
            )
        else:
            logger.error(
                (
                    "Wrong state classes in inlet and/or outlet: %s -> %s. "
                    "Should both be MediumBase or MediumHumidAir."
                ),
                self._ports[self._port_a_name].state.__class__.__name__,
                self._ports[self._port_b_name].state.__class__.__name__,
            )

        # New mass flow
        self._ports[self._port_b_name].state.m_flow = self._ports[
            self._port_a_name
        ].state.m_flow


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the sources model classes.")

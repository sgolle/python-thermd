# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

from thermd.core import (
    # BaseSignalClass,
    SignalFloat,
    BaseStateClass,
    # MediumBase,
    # MediumHumidAir,
)
from thermd.fluid.core import BaseFluidOneInletOneOutletOneSignalOutlet
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Sensor classes
class SensorP(BaseFluidOneInletOneOutletOneSignalOutlet):
    """SensorP class.

    The SensorP class implements a sensor which outputs the pressure of a fluid as
    a signal.

    """

    def __init__(self: SensorP, name: str, state0: BaseStateClass):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, state0=state0, signal0=SignalFloat(value=state0.p))

    def check_self(self: SensorP) -> bool:
        return True

    def equation(self: SensorP):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow

        # New state
        self._ports[self._port_b_name].state = self._ports[self._port_a_name].state

        # New Signal
        self._ports[self._port_d_name].signal = self._ports[self._port_a_name].state.p


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the sensors model classes.")

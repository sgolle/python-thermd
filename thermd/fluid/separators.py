# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

import numpy as np
from thermd.core import (
    # BaseSignalClass,
    BaseStateClass,
    # MediumBase,
    # MediumHumidAir,
)
from thermd.fluid.core import BaseFluidOneInletTwoOutlets
from thermd.media.coolprop import CoolPropFluid, CoolPropPureFluids, MediumCoolProp
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Sensor classes
class SeparatorWater(BaseFluidOneInletTwoOutlets):
    """SeparatorWater class.

    The SeparatorWater class separates liquid and solid water from a humid air flow. 

    """

    def __init__(
        self: SeparatorWater,
        name: str,
        state0: BaseStateClass,
        eta: np.float64 = np.float64(1.0),
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, state0=state0)

        # Separator parameters
        self._eta = eta

        # Set water outlet state
        state_water = MediumCoolProp.from_pT(
            p=state0.p,
            T=state0.T,
            fluid=CoolPropFluid.new_pure_fluid(fluid=CoolPropPureFluids.WATER),
        )
        self._ports[self._port_b2_name].state = state_water

    def check_self(self: SeparatorWater) -> bool:
        return True

    def equation(self: SeparatorWater):
        # Stop criterions
        self._last_hmass = self._ports[self._port_a_name].state.hmass
        self._last_m_flow = self._ports[self._port_a_name].state.m_flow

        # New state
        ws = self._ports[self._port_a_name].state.ws

        if self._ports[self._port_a_name].state.w >= ws:
            self._ports[self._port_b1_name].state = self._ports[self._port_a_name].state
        else:
            self._ports[self._port_b1_name].state = self._ports[self._port_a_name].state

        # New Signal
        self._ports[self._port_d_name].signal.value = self._ports[
            self._port_a_name
        ].state.p


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the separator model classes.")

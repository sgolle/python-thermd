# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations
from typing import Any

import numpy as np
from thermd.core import (
    BaseBlockClass,
    BaseSignalClass,
    BlockResult,
    PortSignal,
    PortTypes,
)
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Base block classes
class BaseBlockOneInlet(BaseBlockClass):
    """Generic block class.

    The generic block class implements a BaseBlockClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseBlockOneInlet, name: str, signal0: BaseSignalClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_c_name = self.name + "_port_c"
        self.add_port(
            PortSignal(
                name=self._port_c_name,
                port_type=PortTypes.SIGNAL_INLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_signal_value = signal0.value

    @property
    def port_c(self: BaseBlockOneInlet) -> PortSignal:
        return self._ports[self._port_c_name]

    @property
    def stop_criterion_signal(self: BaseBlockOneInlet) -> np.float64:
        return self._ports[self._port_c_name].signal.value - self._last_signal_value

    def get_results(self: BaseBlockOneInlet) -> BlockResult:
        signals = {
            self._port_c_name: self._ports[self._port_c_name].signal,
        }
        return BlockResult(signals=signals,)


class BaseBlockOneOutlet(BaseBlockClass):
    """Generic block class.

    The generic block class implements a BaseBlockClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseBlockOneOutlet, name: str, signal0: BaseSignalClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_d_name = self.name + "_port_d"
        self.add_port(
            PortSignal(
                name=self._port_d_name,
                port_type=PortTypes.SIGNAL_OUTLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_signal_value = signal0.value

    @property
    def port_d(self: BaseBlockOneOutlet) -> PortSignal:
        return self._ports[self._port_d_name]

    @property
    def stop_criterion_signal(self: BaseBlockOneOutlet) -> Any:
        return self._ports[self._port_d_name].signal.value - self._last_signal_value

    def get_results(self: BaseBlockOneInlet) -> BlockResult:
        signals = {
            self._port_d_name: self._ports[self._port_d_name].signal,
        }
        return BlockResult(signals=signals,)


class BaseBlockOneInletOneOutlet(BaseBlockClass):
    """Generic block class.

    The generic block class implements a BaseBlockClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseBlockOneInletOneOutlet, name: str, signal0: BaseSignalClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_c_name = self.name + "_port_c"
        self._port_d_name = self.name + "_port_d"
        self.add_port(
            PortSignal(
                name=self._port_c_name,
                port_type=PortTypes.SIGNAL_INLET,
                signal=signal0,
            )
        )
        self.add_port(
            PortSignal(
                name=self._port_d_name,
                port_type=PortTypes.SIGNAL_OUTLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_signal_value = signal0.value

    @property
    def port_c(self: BaseBlockOneInletOneOutlet) -> PortSignal:
        return self._ports[self._port_c_name]

    @property
    def port_d(self: BaseBlockOneInletOneOutlet) -> PortSignal:
        return self._ports[self._port_d_name]

    @property
    def stop_criterion_signal(self: BaseBlockOneInletOneOutlet) -> Any:
        return self._ports[self._port_d_name].signal.value - self._last_signal_value

    def get_results(self: BaseBlockOneInlet) -> BlockResult:
        signals = {
            self._port_c_name: self._ports[self._port_c_name].signal,
            self._port_d_name: self._ports[self._port_d_name].signal,
        }
        return BlockResult(signals=signals,)


class BaseBlockTwoInletsOneOutlet(BaseBlockClass):
    """Generic block class.

    The generic block class implements a BaseBlockClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseBlockTwoInletsOneOutlet,
        name: str,
        signal0_1: BaseSignalClass,
        signal0_2: BaseSignalClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_c1_name = self.name + "_port_c1"
        self._port_c2_name = self.name + "_port_c2"
        self._port_d_name = self.name + "_port_d"
        self.add_port(
            PortSignal(
                name=self._port_c1_name,
                port_type=PortTypes.SIGNAL_INLET,
                signal=signal0_1,
            )
        )
        self.add_port(
            PortSignal(
                name=self._port_c2_name,
                port_type=PortTypes.SIGNAL_INLET,
                signal=signal0_2,
            )
        )
        self.add_port(
            PortSignal(
                name=self._port_d_name,
                port_type=PortTypes.SIGNAL_OUTLET,
                signal=signal0_1,
            )
        )

        # Stop criterions
        self._last_signal_value = signal0_1.value

    @property
    def port_c1(self: BaseBlockTwoInletsOneOutlet) -> PortSignal:
        return self._ports[self._port_c1_name]

    @property
    def port_c2(self: BaseBlockTwoInletsOneOutlet) -> PortSignal:
        return self._ports[self._port_c2_name]

    @property
    def port_d(self: BaseBlockTwoInletsOneOutlet) -> PortSignal:
        return self._ports[self._port_d_name]

    @property
    def stop_criterion_signal(self: BaseBlockTwoInletsOneOutlet) -> Any:
        return self._ports[self._port_d_name].signal.value - self._last_signal_value

    def get_results(self: BaseBlockTwoInletsOneOutlet) -> BlockResult:
        signals = {
            self._port_c1_name: self._ports[self._port_c1_name].signal,
            self._port_c2_name: self._ports[self._port_c2_name].signal,
            self._port_d_name: self._ports[self._port_d_name].signal,
        }
        return BlockResult(signals=signals,)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the core block classes.")

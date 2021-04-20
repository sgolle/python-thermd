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
        self._port_a_name = self.name + "_port_a"
        self.add_port(
            PortSignal(
                name=self._port_a_name,
                port_type=PortTypes.SIGNAL_INLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_value = signal0.value

    @property
    def port_a(self: BaseBlockOneInlet) -> PortSignal:
        return self._ports[self._port_a_name]

    @property
    def stop_criterion_signal(self: BaseBlockOneInlet) -> np.float64:
        return self._ports[self._port_a_name].signal.value - self._last_value


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
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortSignal(
                name=self._port_b_name,
                port_type=PortTypes.SIGNAL_OUTLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_value = signal0.value

    @property
    def port_b(self: BaseBlockOneOutlet) -> PortSignal:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_signal(self: BaseBlockOneOutlet) -> Any:
        return self._ports[self._port_b_name].signal.value - self._last_value


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
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortSignal(
                name=self._port_a_name,
                port_type=PortTypes.SIGNAL_INLET,
                signal=signal0,
            )
        )
        self.add_port(
            PortSignal(
                name=self._port_b_name,
                port_type=PortTypes.SIGNAL_OUTLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_value = signal0.value

    @property
    def port_a(self: BaseBlockOneInletOneOutlet) -> PortSignal:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseBlockOneInletOneOutlet) -> PortSignal:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_signal(self: BaseBlockOneInletOneOutlet) -> Any:
        return self._ports[self._port_b_name].signal.value - self._last_value


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the core block classes.")

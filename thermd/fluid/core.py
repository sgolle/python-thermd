# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

import numpy as np
from thermd.core import (
    BaseModelClass,
    BaseSignalClass,
    BaseStateClass,
    PortSignal,
    PortState,
    PortTypes,
)
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Base block classes
class BaseFluidOneInlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInlet, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInlet) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInlet) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInlet) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInlet) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidOneInlet) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInlet) -> np.float64:
        return np.float64(0.0)


class BaseFluidOneOutlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneOutlet, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneOutlet) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneOutlet) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneOutlet) -> np.float64:
        return np.float64(0.0)


class BaseFluidOneInletOneOutlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletOneOutlet, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return np.float64(0.0)


class BaseFluidOneInletOneOutletOneSignal(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletOneOutletOneSignal, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletOneOutletOneSignal) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletOneOutletOneSignal) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletOneOutletOneSignal) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(
        self: BaseFluidOneInletOneOutletOneSignal,
    ) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidOneInletOneOutletOneSignal) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletOneOutletOneSignal) -> np.float64:
        return np.float64(0.0)


class BaseFluidOneInletTwoOutlets(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletTwoOutlets, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return np.float64(0.0)


class BaseFluidOneInletThreeOutlets(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletThreeOutlets, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return np.float64(0.0)


class BaseFluidOneInletFourOutlets(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletFourOutlets, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return np.float64(0.0)


class BaseFluidTwoInletsOneOutlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidTwoInletsOneOutlet, name: str, state0: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return np.float64(0.0)

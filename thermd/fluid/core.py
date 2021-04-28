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
    MediumBase,
    MediumHumidAir,
    ModelResult,
    PortSignal,
    PortState,
    PortTypes,
    SignalFloat,
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
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInlet) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInlet) -> np.float64:
        return self._ports[self._port_a_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInlet) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidOneInlet) -> np.float64:
        return self._ports[self._port_a_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInlet) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidOneInlet) -> None:
        self._energy_balance = np.float64(0.0)
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = np.float64(0.0)

    def get_results(self: BaseFluidOneInlet) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
        }
        return ModelResult(states=states, signals=None,)


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
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_b_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow

    @property
    def port_b(self: BaseFluidOneOutlet) -> PortState:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneOutlet) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneOutlet) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidOneOutlet) -> None:
        self._energy_balance = np.float64(0.0)
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = np.float64(0.0)

    def get_results(self: BaseFluidOneOutlet) -> ModelResult:
        states = {
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        return ModelResult(states=states, signals=None,)


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
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletOneOutlet) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletOneOutlet) -> PortState:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletOneOutlet) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidOneInletOneOutlet) -> None:
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                * self._ports[self._port_a_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                / (1 + self._ports[self._port_a_name].state.w)
            ) * self._ports[self._port_a_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b_name].state, MediumBase):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                * self._ports[self._port_b_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b_name].state, MediumHumidAir):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                / (1 + self._ports[self._port_b_name].state.w)
            ) * self._ports[self._port_b_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b_name].state.__class__.__name__,
            )
        self._energy_balance = Hb - Ha
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b_name].state.m_flow
            - self._ports[self._port_a_name].state.m_flow
        )

    def get_results(self: BaseFluidOneInletOneOutlet) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        return ModelResult(states=states, signals=None,)


class BaseFluidTwoInletsTwoOutlets(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidTwoInletsTwoOutlets,
        name: str,
        state0_1: BaseStateClass,
        state0_2: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a1_name = self.name + "_port_a1"
        self._port_a2_name = self.name + "_port_a2"
        self._port_b1_name = self.name + "_port_b1"
        self._port_b2_name = self.name + "_port_b2"
        self.add_port(
            PortState(
                name=self._port_a1_name,
                port_type=PortTypes.STATE_INLET,
                state=state0_1,
            )
        )
        self.add_port(
            PortState(
                name=self._port_a2_name,
                port_type=PortTypes.STATE_INLET,
                state=state0_2,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b1_name,
                port_type=PortTypes.STATE_OUTLET,
                state=state0_1,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b2_name,
                port_type=PortTypes.STATE_OUTLET,
                state=state0_2,
            )
        )

        # Stop criterions
        self._last_hmass = state0_1.hmass
        self._last_m_flow = state0_1.m_flow

    @property
    def port_a1(self: BaseFluidTwoInletsTwoOutlets) -> PortState:
        return self._ports[self._port_a1_name]

    @property
    def port_a2(self: BaseFluidTwoInletsTwoOutlets) -> PortState:
        return self._ports[self._port_a2_name]

    @property
    def port_b1(self: BaseFluidTwoInletsTwoOutlets) -> PortState:
        return self._ports[self._port_b1_name]

    @property
    def port_b2(self: BaseFluidTwoInletsTwoOutlets) -> PortState:
        return self._ports[self._port_b2_name]

    @property
    def stop_criterion_energy(self: BaseFluidTwoInletsTwoOutlets) -> np.float64:
        return self._ports[self._port_b1_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidTwoInletsTwoOutlets) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidTwoInletsTwoOutlets) -> np.float64:
        return self._ports[self._port_b1_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidTwoInletsTwoOutlets) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidTwoInletsTwoOutlets) -> None:
        if isinstance(self._ports[self._port_a1_name].state, MediumBase):
            Ha1 = (
                self._ports[self._port_a1_name].state.m_flow
                * self._ports[self._port_a1_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a1_name].state, MediumHumidAir):
            Ha1 = (
                self._ports[self._port_a1_name].state.m_flow
                / (1 + self._ports[self._port_a1_name].state.w)
            ) * self._ports[self._port_a1_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a1_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_a2_name].state, MediumBase):
            Ha2 = (
                self._ports[self._port_a2_name].state.m_flow
                * self._ports[self._port_a2_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a2_name].state, MediumHumidAir):
            Ha1 = (
                self._ports[self._port_a2_name].state.m_flow
                / (1 + self._ports[self._port_a2_name].state.w)
            ) * self._ports[self._port_a2_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a2_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b1_name].state, MediumBase):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                * self._ports[self._port_b1_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b1_name].state, MediumHumidAir):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                / (1 + self._ports[self._port_b1_name].state.w)
            ) * self._ports[self._port_b1_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b1_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b2_name].state, MediumBase):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                * self._ports[self._port_b2_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b2_name].state, MediumHumidAir):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                / (1 + self._ports[self._port_b2_name].state.w)
            ) * self._ports[self._port_b2_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b2_name].state.__class__.__name__,
            )
        self._energy_balance = Hb1 + Hb2 - Ha1 - Ha2
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b1_name].state.m_flow
            + self._ports[self._port_b2_name].state.m_flow
            - self._ports[self._port_a1_name].state.m_flow
            - self._ports[self._port_a2_name].state.m_flow
        )

    def get_results(self: BaseFluidTwoInletsTwoOutlets) -> ModelResult:
        states = {
            self._port_a1_name: self._ports[self._port_a1_name].state,
            self._port_a2_name: self._ports[self._port_a2_name].state,
            self._port_b1_name: self._ports[self._port_b1_name].state,
            self._port_b2_name: self._ports[self._port_b2_name].state,
        }
        return ModelResult(states=states, signals=None,)


class BaseFluidOneInletOneOutletOneSignalInlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletOneOutletOneSignalInlet,
        name: str,
        state0: BaseStateClass,
        signal0: BaseSignalClass = SignalFloat(value=np.float64(0.0)),
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self._port_c_name = self.name + "_port_c"
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
        self.add_port(
            PortSignal(
                name=self._port_c_name,
                port_type=PortTypes.SIGNAL_INLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow
        self._last_signal_value = signal0.value

    @property
    def port_a(self: BaseFluidOneInletOneOutletOneSignalInlet) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletOneOutletOneSignalInlet) -> PortState:
        return self._ports[self._port_b_name]

    @property
    def port_c(self: BaseFluidOneInletOneOutletOneSignalInlet) -> PortSignal:
        return self._ports[self._port_c_name]

    @property
    def stop_criterion_energy(
        self: BaseFluidOneInletOneOutletOneSignalInlet,
    ) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(
        self: BaseFluidOneInletOneOutletOneSignalInlet,
    ) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(
        self: BaseFluidOneInletOneOutletOneSignalInlet,
    ) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(
        self: BaseFluidOneInletOneOutletOneSignalInlet,
    ) -> np.float64:
        return self._ports[self._port_c_name].signal.value - self._last_signal_value

    def update_balances(self: BaseFluidOneInletOneOutletOneSignalInlet) -> None:
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                * self._ports[self._port_a_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                / (1 + self._ports[self._port_a_name].state.w)
            ) * self._ports[self._port_a_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b_name].state, MediumBase):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                * self._ports[self._port_b_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b_name].state, MediumHumidAir):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                / (1 + self._ports[self._port_b_name].state.w)
            ) * self._ports[self._port_b_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b_name].state.__class__.__name__,
            )
        self._energy_balance = Hb - Ha
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b_name].state.m_flow
            - self._ports[self._port_a_name].state.m_flow
        )

    def get_results(self: BaseFluidOneInletOneOutletOneSignalInlet) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        signals = {
            self._port_c_name: self._ports[self._port_c_name].signal,
        }
        return ModelResult(states=states, signals=signals,)


class BaseFluidOneInletOneOutletOneSignalOutlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletOneOutletOneSignalOutlet,
        name: str,
        state0: BaseStateClass,
        signal0: BaseSignalClass = SignalFloat(value=np.float64(0.0)),
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self._port_d_name = self.name + "_port_d"
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
        self.add_port(
            PortSignal(
                name=self._port_d_name,
                port_type=PortTypes.SIGNAL_OUTLET,
                signal=signal0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow
        self._last_signal_value = signal0.value

    @property
    def port_a(self: BaseFluidOneInletOneOutletOneSignalOutlet) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def port_b(self: BaseFluidOneInletOneOutletOneSignalOutlet) -> PortState:
        return self._ports[self._port_b_name]

    @property
    def port_d(self: BaseFluidOneInletOneOutletOneSignalOutlet) -> PortSignal:
        return self._ports[self._port_d_name]

    @property
    def stop_criterion_energy(
        self: BaseFluidOneInletOneOutletOneSignalOutlet,
    ) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(
        self: BaseFluidOneInletOneOutletOneSignalOutlet,
    ) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(
        self: BaseFluidOneInletOneOutletOneSignalOutlet,
    ) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(
        self: BaseFluidOneInletOneOutletOneSignalOutlet,
    ) -> np.float64:
        return self._ports[self._port_d_name].signal.value - self._last_signal_value

    def update_balances(self: BaseFluidOneInletOneOutletOneSignalOutlet) -> None:
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                * self._ports[self._port_a_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                / (1 + self._ports[self._port_a_name].state.w)
            ) * self._ports[self._port_a_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b_name].state, MediumBase):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                * self._ports[self._port_b_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b_name].state, MediumHumidAir):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                / (1 + self._ports[self._port_b_name].state.w)
            ) * self._ports[self._port_b_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b_name].state.__class__.__name__,
            )
        self._energy_balance = Hb - Ha
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b_name].state.m_flow
            - self._ports[self._port_a_name].state.m_flow
        )

    def get_results(self: BaseFluidOneInletOneOutletOneSignalOutlet) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        signals = {
            self._port_d_name: self._ports[self._port_d_name].signal,
        }
        return ModelResult(states=states, signals=signals,)


class BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
        name: str,
        state0: BaseStateClass,
        signal0: BaseSignalClass = SignalFloat(value=np.float64(0.0)),
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b_name = self.name + "_port_b"
        self._port_c_name = self.name + "_port_c"
        self._port_d_name = self.name + "_port_d"
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
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow
        self._last_signal_value = signal0.value

    @property
    def port_a(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def port_b(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> PortState:
        return self._ports[self._port_b_name]

    @property
    def port_c(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> PortSignal:
        return self._ports[self._port_c_name]

    @property
    def port_d(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> PortSignal:
        return self._ports[self._port_d_name]

    @property
    def stop_criterion_energy(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> np.float64:
        return self._ports[self._port_d_name].signal.value - self._last_signal_value

    def update_balances(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> None:
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                * self._ports[self._port_a_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                / (1 + self._ports[self._port_a_name].state.w)
            ) * self._ports[self._port_a_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b_name].state, MediumBase):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                * self._ports[self._port_b_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b_name].state, MediumHumidAir):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                / (1 + self._ports[self._port_b_name].state.w)
            ) * self._ports[self._port_b_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b_name].state.__class__.__name__,
            )
        self._energy_balance = Hb - Ha
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b_name].state.m_flow
            - self._ports[self._port_a_name].state.m_flow
        )

    def get_results(
        self: BaseFluidOneInletOneOutletOneSignalInletOneSignalOutlet,
    ) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        signals = {
            self._port_c_name: self._ports[self._port_c_name].signal,
            self._port_d_name: self._ports[self._port_d_name].signal,
        }
        return ModelResult(states=states, signals=signals,)


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
        self._port_b1_name = self.name + "_port_b1"
        self._port_b2_name = self.name + "_port_b2"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b1_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b2_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletTwoOutlets) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def port_b1(self: BaseFluidOneInletTwoOutlets) -> PortState:
        return self._ports[self._port_b1_name]

    @property
    def port_b2(self: BaseFluidOneInletTwoOutlets) -> PortState:
        return self._ports[self._port_b2_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return self._ports[self._port_a_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return self._ports[self._port_a_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletTwoOutlets) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidOneInletTwoOutlets) -> None:
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                * self._ports[self._port_a_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                / (1 + self._ports[self._port_a_name].state.w)
            ) * self._ports[self._port_a_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b1_name].state, MediumBase):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                * self._ports[self._port_b1_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b1_name].state, MediumHumidAir):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                / (1 + self._ports[self._port_b1_name].state.w)
            ) * self._ports[self._port_b1_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b1_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b2_name].state, MediumBase):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                * self._ports[self._port_b2_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b2_name].state, MediumHumidAir):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                / (1 + self._ports[self._port_b2_name].state.w)
            ) * self._ports[self._port_b2_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b2_name].state.__class__.__name__,
            )
        self._energy_balance = Hb1 + Hb2 - Ha
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b1_name].state.m_flow
            + self._ports[self._port_b2_name].state.m_flow
            - self._ports[self._port_a_name].state.m_flow
        )

    def get_results(self: BaseFluidOneInletTwoOutlets) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b1_name: self._ports[self._port_b1_name].state,
            self._port_b2_name: self._ports[self._port_b2_name].state,
        }
        return ModelResult(states=states, signals=None,)


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
        self._port_b1_name = self.name + "_port_b1"
        self._port_b2_name = self.name + "_port_b2"
        self._port_b3_name = self.name + "_port_b3"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b1_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b2_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b3_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletThreeOutlets) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def port_b1(self: BaseFluidOneInletThreeOutlets) -> PortState:
        return self._ports[self._port_b1_name]

    @property
    def port_b2(self: BaseFluidOneInletThreeOutlets) -> PortState:
        return self._ports[self._port_b2_name]

    @property
    def port_b3(self: BaseFluidOneInletThreeOutlets) -> PortState:
        return self._ports[self._port_b3_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return self._ports[self._port_a_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return self._ports[self._port_a_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletThreeOutlets) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidOneInletThreeOutlets) -> None:
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                * self._ports[self._port_a_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                / (1 + self._ports[self._port_a_name].state.w)
            ) * self._ports[self._port_a_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b1_name].state, MediumBase):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                * self._ports[self._port_b1_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b1_name].state, MediumHumidAir):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                / (1 + self._ports[self._port_b1_name].state.w)
            ) * self._ports[self._port_b1_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b1_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b2_name].state, MediumBase):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                * self._ports[self._port_b2_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b2_name].state, MediumHumidAir):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                / (1 + self._ports[self._port_b2_name].state.w)
            ) * self._ports[self._port_b2_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b2_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b3_name].state, MediumBase):
            Hb3 = (
                self._ports[self._port_b3_name].state.m_flow
                * self._ports[self._port_b3_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b3_name].state, MediumHumidAir):
            Hb3 = (
                self._ports[self._port_b3_name].state.m_flow
                / (1 + self._ports[self._port_b3_name].state.w)
            ) * self._ports[self._port_b3_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b3_name].state.__class__.__name__,
            )
        self._energy_balance = Hb1 + Hb2 + Hb3 - Ha
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b1_name].state.m_flow
            + self._ports[self._port_b2_name].state.m_flow
            + self._ports[self._port_b3_name].state.m_flow
            - self._ports[self._port_a_name].state.m_flow
        )

    def get_results(self: BaseFluidOneInletThreeOutlets) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b1_name: self._ports[self._port_b1_name].state,
            self._port_b2_name: self._ports[self._port_b2_name].state,
            self._port_b3_name: self._ports[self._port_b3_name].state,
        }
        return ModelResult(states=states, signals=None,)


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
        self._port_b1_name = self.name + "_port_b1"
        self._port_b2_name = self.name + "_port_b2"
        self._port_b3_name = self.name + "_port_b3"
        self._port_b4_name = self.name + "_port_b4"
        self.add_port(
            PortState(
                name=self._port_a_name, port_type=PortTypes.STATE_INLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b1_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b2_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b3_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b4_name, port_type=PortTypes.STATE_OUTLET, state=state0,
            )
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: BaseFluidOneInletFourOutlets) -> PortState:
        return self._ports[self._port_a_name]

    @property
    def port_b1(self: BaseFluidOneInletFourOutlets) -> PortState:
        return self._ports[self._port_b1_name]

    @property
    def port_b2(self: BaseFluidOneInletFourOutlets) -> PortState:
        return self._ports[self._port_b2_name]

    @property
    def port_b3(self: BaseFluidOneInletFourOutlets) -> PortState:
        return self._ports[self._port_b3_name]

    @property
    def port_b4(self: BaseFluidOneInletFourOutlets) -> PortState:
        return self._ports[self._port_b4_name]

    @property
    def stop_criterion_energy(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return self._ports[self._port_a_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return self._ports[self._port_a_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidOneInletFourOutlets) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidOneInletFourOutlets) -> None:
        if isinstance(self._ports[self._port_a_name].state, MediumBase):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                * self._ports[self._port_a_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a_name].state, MediumHumidAir):
            Ha = (
                self._ports[self._port_a_name].state.m_flow
                / (1 + self._ports[self._port_a_name].state.w)
            ) * self._ports[self._port_a_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b1_name].state, MediumBase):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                * self._ports[self._port_b1_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b1_name].state, MediumHumidAir):
            Hb1 = (
                self._ports[self._port_b1_name].state.m_flow
                / (1 + self._ports[self._port_b1_name].state.w)
            ) * self._ports[self._port_b1_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b1_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b2_name].state, MediumBase):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                * self._ports[self._port_b2_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b2_name].state, MediumHumidAir):
            Hb2 = (
                self._ports[self._port_b2_name].state.m_flow
                / (1 + self._ports[self._port_b2_name].state.w)
            ) * self._ports[self._port_b2_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b2_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b3_name].state, MediumBase):
            Hb3 = (
                self._ports[self._port_b3_name].state.m_flow
                * self._ports[self._port_b3_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b3_name].state, MediumHumidAir):
            Hb3 = (
                self._ports[self._port_b3_name].state.m_flow
                / (1 + self._ports[self._port_b3_name].state.w)
            ) * self._ports[self._port_b3_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b3_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b4_name].state, MediumBase):
            Hb4 = (
                self._ports[self._port_b4_name].state.m_flow
                * self._ports[self._port_b4_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b4_name].state, MediumHumidAir):
            Hb4 = (
                self._ports[self._port_b4_name].state.m_flow
                / (1 + self._ports[self._port_b4_name].state.w)
            ) * self._ports[self._port_b4_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b4_name].state.__class__.__name__,
            )
        self._energy_balance = Hb1 + Hb2 + Hb3 + Hb4 - Ha
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b1_name].state.m_flow
            + self._ports[self._port_b2_name].state.m_flow
            + self._ports[self._port_b3_name].state.m_flow
            + self._ports[self._port_b4_name].state.m_flow
            - self._ports[self._port_a_name].state.m_flow
        )

    def get_results(self: BaseFluidOneInletFourOutlets) -> ModelResult:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b1_name: self._ports[self._port_b1_name].state,
            self._port_b2_name: self._ports[self._port_b2_name].state,
            self._port_b3_name: self._ports[self._port_b3_name].state,
            self._port_b4_name: self._ports[self._port_b4_name].state,
        }
        return ModelResult(states=states, signals=None,)


class BaseFluidTwoInletsOneOutlet(BaseModelClass):
    """Generic block class.

    The generic fluid class implements a BaseModelClass with defined inlets and outlets.

    """

    def __init__(
        self: BaseFluidTwoInletsOneOutlet,
        name: str,
        state0_1: BaseStateClass,
        state0_2: BaseStateClass,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a1_name = self.name + "_port_a1"
        self._port_a2_name = self.name + "_port_a2"
        self._port_b_name = self.name + "_port_b"
        self.add_port(
            PortState(
                name=self._port_a1_name,
                port_type=PortTypes.STATE_INLET,
                state=state0_1,
            )
        )
        self.add_port(
            PortState(
                name=self._port_a2_name,
                port_type=PortTypes.STATE_INLET,
                state=state0_2,
            )
        )
        self.add_port(
            PortState(
                name=self._port_b_name,
                port_type=PortTypes.STATE_OUTLET,
                state=state0_1,
            )
        )

        # Stop criterions
        self._last_hmass = state0_1.hmass
        self._last_m_flow = state0_1.m_flow

    @property
    def port_a1(self: BaseFluidTwoInletsOneOutlet) -> PortState:
        return self._ports[self._port_a1_name]

    @property
    def port_a2(self: BaseFluidTwoInletsOneOutlet) -> PortState:
        return self._ports[self._port_a2_name]

    @property
    def port_b(self: BaseFluidTwoInletsOneOutlet) -> PortState:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return np.float64(0.0)

    @property
    def stop_criterion_mass(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    @property
    def stop_criterion_signal(self: BaseFluidTwoInletsOneOutlet) -> np.float64:
        return np.float64(0.0)

    def update_balances(self: BaseFluidTwoInletsOneOutlet) -> None:
        if isinstance(self._ports[self._port_a1_name].state, MediumBase):
            Ha1 = (
                self._ports[self._port_a1_name].state.m_flow
                * self._ports[self._port_a1_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a1_name].state, MediumHumidAir):
            Ha1 = (
                self._ports[self._port_a1_name].state.m_flow
                / (1 + self._ports[self._port_a1_name].state.w)
            ) * self._ports[self._port_a1_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a1_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_a2_name].state, MediumBase):
            Ha2 = (
                self._ports[self._port_a2_name].state.m_flow
                * self._ports[self._port_a2_name].state.hmass
            )
        elif isinstance(self._ports[self._port_a2_name].state, MediumHumidAir):
            Ha2 = (
                self._ports[self._port_a2_name].state.m_flow
                / (1 + self._ports[self._port_a2_name].state.w)
            ) * self._ports[self._port_a2_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_a2_name].state.__class__.__name__,
            )
        if isinstance(self._ports[self._port_b_name].state, MediumBase):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                * self._ports[self._port_b_name].state.hmass
            )
        elif isinstance(self._ports[self._port_b_name].state, MediumHumidAir):
            Hb = (
                self._ports[self._port_b_name].state.m_flow
                / (1 + self._ports[self._port_b_name].state.w)
            ) * self._ports[self._port_b_name].state.hmass
        else:
            logger.error(
                "Wrong state class: %s. Should be MediumBase or MediumHumidAir",
                self._ports[self._port_b_name].state.__class__.__name__,
            )
        self._energy_balance = Hb - Ha1 - Ha2
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = (
            self._ports[self._port_b_name].state.m_flow
            - self._ports[self._port_a1_name].state.m_flow
            - self._ports[self._port_a2_name].state.m_flow
        )

    def get_results(self: BaseFluidTwoInletsOneOutlet) -> ModelResult:
        states = {
            self._port_a1_name: self._ports[self._port_a1_name].state,
            self._port_a2_name: self._ports[self._port_a2_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        return ModelResult(states=states, signals=None,)


if __name__ == "__main__":
    logger.info("This is the file for the core fluid classes.")

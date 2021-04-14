# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations
from dataclasses import dataclass

# from typing import List, Dict, Union

# from CoolProp.CoolProp import PropsSI
# from CoolProp.HumidAirProp import HAPropsSI
# import math
import numpy as np

# from scipy import optimize as opt
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
class ResultFittings(ModelResult):
    ...


# Machine classes
class JunctionOneToTwo(BaseModelClass):
    """JunctionOneToTwo class.

    The JunctionOneToTwo class implements a ...

    """

    def __init__(
        self: JunctionOneToTwo,
        name: str,
        state0: BaseStateClass,
        fraction: np.ndarray[np.float64],
    ):
        """Initialize JunctionOneToTwo class.

        Init function of the JunctionOneToTwo class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b1_name = self.name + "_port_b1"
        self._port_b2_name = self.name + "_port_b2"
        self.add_port(
            PortState(
                name=self._port_a_name,
                port_type=PortTypes.STATE_INLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b1_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b2_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )

        # Junction parameters
        if fraction.sum() == 1.0 and fraction.ndim == 1 and fraction.shape[0] == 2:
            self._fraction = fraction
        else:
            logger.error(
                "Fractions of mass flow not defined correctly: %s.", str(fraction),
            )
            raise SystemExit

        # New mass flow fractions
        self._ports[self._port_b1_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[0]
        )
        self._ports[self._port_b2_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[1]
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: JunctionOneToTwo) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b1(self: JunctionOneToTwo) -> np.float64:
        return self._ports[self._port_b1_name]

    @property
    def port_b2(self: JunctionOneToTwo) -> np.float64:
        return self._ports[self._port_b2_name]

    @property
    def stop_criterion_energy(self: JunctionOneToTwo) -> np.float64:
        return self._ports[self._port_a_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: JunctionOneToTwo) -> np.float64:
        return self._ports[self._port_a_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: JunctionOneToTwo) -> np.float64:
        return self._ports[self._port_a_name].state.m_flow - self._last_m_flow

    def check(self: JunctionOneToTwo) -> bool:
        return True

    def get_results(self: JunctionOneToTwo) -> ResultFittings:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b1_name: self._ports[self._port_b1_name].state,
            self._port_b2_name: self._ports[self._port_b2_name].state,
        }
        return ResultFittings(states=states, signals=None)

    def equation(self: JunctionOneToTwo):
        # Stop criterions
        self._last_hmass = self._ports[self._port_a_name].state.hmass
        self._last_p = self._ports[self._port_a_name].state.p
        self._last_m_flow = self._ports[self._port_a_name].state.m_flow

        # New states
        self._ports[self._port_b1_name].state = self._ports[self._port_a_name].state
        self._ports[self._port_b2_name].state = self._ports[self._port_a_name].state

        # New mass flows
        self._ports[self._port_b1_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[0]
        )
        self._ports[self._port_b2_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[1]
        )


class JunctionOneToThree(BaseModelClass):
    """JunctionOneToThree class.

    The JunctionOneToThree class implements a ...

    """

    def __init__(
        self: JunctionOneToThree,
        name: str,
        state0: BaseStateClass,
        fraction: np.ndarray[np.float64],
    ):
        """Initialize JunctionOneToThree class.

        Init function of the JunctionOneToThree class.

        """
        super().__init__(name=name)

        # Ports
        self._port_a_name = self.name + "_port_a"
        self._port_b1_name = self.name + "_port_b1"
        self._port_b2_name = self.name + "_port_b2"
        self._port_b3_name = self.name + "_port_b3"
        self.add_port(
            PortState(
                name=self._port_a_name,
                port_type=PortTypes.STATE_INLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b1_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b2_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b3_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )

        # Junction parameters
        if fraction.sum() == 1.0 and fraction.ndim == 1 and fraction.shape[0] == 3:
            self._fraction = fraction
        else:
            logger.error(
                "Fractions of mass flow not defined correctly: %s.", str(fraction),
            )
            raise SystemExit

        # New mass flow fractions
        self._ports[self._port_b1_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[0]
        )
        self._ports[self._port_b2_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[1]
        )
        self._ports[self._port_b3_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[2]
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: JunctionOneToThree) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b1(self: JunctionOneToThree) -> np.float64:
        return self._ports[self._port_b1_name]

    @property
    def port_b2(self: JunctionOneToThree) -> np.float64:
        return self._ports[self._port_b2_name]

    @property
    def port_b3(self: JunctionOneToThree) -> np.float64:
        return self._ports[self._port_b3_name]

    @property
    def stop_criterion_energy(self: JunctionOneToThree) -> np.float64:
        return self._ports[self._port_a_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: JunctionOneToThree) -> np.float64:
        return self._ports[self._port_a_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: JunctionOneToThree) -> np.float64:
        return self._ports[self._port_a_name].state.m_flow - self._last_m_flow

    def check(self: JunctionOneToThree) -> bool:
        return True

    def get_results(self: JunctionOneToThree) -> ResultFittings:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b1_name: self._ports[self._port_b1_name].state,
            self._port_b2_name: self._ports[self._port_b2_name].state,
            self._port_b3_name: self._ports[self._port_b3_name].state,
        }
        return ResultFittings(states=states, signals=None)

    def equation(self: JunctionOneToThree):
        # Stop criterions
        self._last_hmass = self._ports[self._port_a_name].state.hmass
        self._last_p = self._ports[self._port_a_name].state.p
        self._last_m_flow = self._ports[self._port_a_name].state.m_flow

        # New states
        self._ports[self._port_b1_name].state = self._ports[self._port_a_name].state
        self._ports[self._port_b2_name].state = self._ports[self._port_a_name].state
        self._ports[self._port_b3_name].state = self._ports[self._port_a_name].state

        # New mass flows
        self._ports[self._port_b1_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[0]
        )
        self._ports[self._port_b2_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[1]
        )
        self._ports[self._port_b3_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[2]
        )


class JunctionOneToFour(BaseModelClass):
    """JunctionOneToFour class.

    The JunctionOneToFour class implements a ...

    """

    def __init__(
        self: JunctionOneToFour,
        name: str,
        state0: BaseStateClass,
        fraction: np.ndarray[np.float64],
    ):
        """Initialize JunctionOneToFour class.

        Init function of the JunctionOneToFour class.

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
                name=self._port_a_name,
                port_type=PortTypes.STATE_INLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b1_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b2_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b3_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_b4_name,
                port_type=PortTypes.STATE_OUTLET,
                port_attr=state0.copy(),
            )
        )

        # Junction parameters
        if fraction.sum() == 1.0 and fraction.ndim == 1 and fraction.shape[0] == 4:
            self._fraction = fraction
        else:
            logger.error(
                "Fractions of mass flow not defined correctly: %s.", str(fraction),
            )
            raise SystemExit

        # New mass flow fractions
        self._ports[self._port_b1_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[0]
        )
        self._ports[self._port_b2_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[1]
        )
        self._ports[self._port_b3_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[2]
        )
        self._ports[self._port_b4_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[3]
        )

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_a_name]

    @property
    def port_b1(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_b1_name]

    @property
    def port_b2(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_b2_name]

    @property
    def port_b3(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_b3_name]

    @property
    def port_b4(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_b4_name]

    @property
    def stop_criterion_energy(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_a_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_a_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: JunctionOneToFour) -> np.float64:
        return self._ports[self._port_a_name].state.m_flow - self._last_m_flow

    def check(self: JunctionOneToFour) -> bool:
        return True

    def get_results(self: JunctionOneToFour) -> ResultFittings:
        states = {
            self._port_a_name: self._ports[self._port_a_name].state,
            self._port_b1_name: self._ports[self._port_b1_name].state,
            self._port_b2_name: self._ports[self._port_b2_name].state,
            self._port_b3_name: self._ports[self._port_b3_name].state,
            self._port_b4_name: self._ports[self._port_b4_name].state,
        }
        return ResultFittings(states=states, signals=None)

    def equation(self: JunctionOneToFour):
        # Stop criterions
        self._last_hmass = self._ports[self._port_a_name].state.hmass
        self._last_p = self._ports[self._port_a_name].state.p
        self._last_m_flow = self._ports[self._port_a_name].state.m_flow

        # New states
        self._ports[self._port_b1_name].state = self._ports[self._port_a_name].state
        self._ports[self._port_b2_name].state = self._ports[self._port_a_name].state
        self._ports[self._port_b3_name].state = self._ports[self._port_a_name].state
        self._ports[self._port_b4_name].state = self._ports[self._port_a_name].state

        # New mass flows
        self._ports[self._port_b1_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[0]
        )
        self._ports[self._port_b2_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[1]
        )
        self._ports[self._port_b3_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[2]
        )
        self._ports[self._port_b4_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[3]
        )


class JunctionTwoToOne(BaseModelClass):
    """JunctionTwoToOne class.

    The JunctionTwoToOne class implements a ...

    """

    def __init__(self: JunctionTwoToOne, name: str, state0: BaseStateClass):
        """Initialize JunctionTwoToOne class.

        Init function of the JunctionTwoToOne class.

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
                port_attr=state0.copy(),
            )
        )
        self.add_port(
            PortState(
                name=self._port_a2_name,
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

        # Stop criterions
        self._last_hmass = state0.hmass
        self._last_p = state0.p
        self._last_m_flow = state0.m_flow

    @property
    def port_a1(self: JunctionTwoToOne) -> np.float64:
        return self._ports[self._port_a1_name]

    @property
    def port_a2(self: JunctionTwoToOne) -> np.float64:
        return self._ports[self._port_a2_name]

    @property
    def port_b(self: JunctionTwoToOne) -> np.float64:
        return self._ports[self._port_b_name]

    @property
    def stop_criterion_energy(self: JunctionTwoToOne) -> np.float64:
        return self._ports[self._port_b_name].state.hmass - self._last_hmass

    @property
    def stop_criterion_momentum(self: JunctionTwoToOne) -> np.float64:
        return self._ports[self._port_b_name].state.p - self._last_p

    @property
    def stop_criterion_mass(self: JunctionTwoToOne) -> np.float64:
        return self._ports[self._port_b_name].state.m_flow - self._last_m_flow

    def check(self: JunctionTwoToOne) -> bool:
        return True

    def get_results(self: JunctionTwoToOne) -> ResultFittings:
        states = {
            self._port_a1_name: self._ports[self._port_a1_name].state,
            self._port_a2_name: self._ports[self._port_a2_name].state,
            self._port_b_name: self._ports[self._port_b_name].state,
        }
        return ResultFittings(states=states, signals=None)

    def equation(self: JunctionTwoToOne):
        # Stop criterions
        self._last_hmass = self._ports[self._port_b_name].state.hmass
        self._last_p = self._ports[self._port_b_name].state.p
        self._last_m_flow = self._ports[self._port_b_name].state.m_flow

        # New states
        if isinstance(self._ports[self._port_a1_name].state, MediumBase) and isinstance(
            self._ports[self._port_a2_name].state, MediumBase
        ):
            h_out = (
                self._ports[self._port_a1_name1].state.m_flow
                * self._ports[self._port_a1_name1].state.hmass
                + self._ports[self._port_a2_name2].state.m_flow
                * self._ports[self._port_a2_name2].state.hmass
            ) / (
                self._ports[self._port_a1_name1].state.m_flow
                + self._ports[self._port_a2_name2].state.m_flow
            )
            self._ports[self._port_b_name].state.set_ph(
                p=np.min(
                    [
                        self._ports[self._port_a1_name1].state.p,
                        self._ports[self._port_a2_name2].state.p,
                    ]
                ),
                h=h_out,
            )
        elif isinstance(
            self._ports[self._port_a1_name].state, MediumHumidAir
        ) and isinstance(self._ports[self._port_a2_name].state, MediumHumidAir):
            w_out = (
                (
                    self._ports[self._port_a1_name1].state.m_flow
                    + self._ports[self._port_a2_name2].state.m_flow
                )
                / (
                    self._ports[self._port_a1_name1].state.m_flow
                    / (1 + self._ports[self._port_a1_name1].state.w)
                    + self._ports[self._port_a2_name2].state.m_flow
                    / (1 + self._ports[self._port_a2_name2].state.w)
                )
                - 1
            )
            h_out = (
                (
                    self._ports[self._port_a1_name1].state.m_flow
                    / (1 + self._ports[self._port_a1_name1].state.w)
                )
                * self._ports[self._port_a1_name1].state.hmass
                + (
                    self._ports[self._port_a2_name2].state.m_flow
                    / (1 + self._ports[self._port_a2_name2].state.w)
                )
                * self._ports[self._port_a2_name2].state.hmass
            ) / (
                (
                    self._ports[self._port_a1_name1].state.m_flow
                    + self._ports[self._port_a2_name2].state.m_flow
                )
                / (1 + w_out)
            )
            self._ports[self._port_b_name].state.set_phw(
                p=np.min(
                    [
                        self._ports[self._port_a1_name1].state.p,
                        self._ports[self._port_a2_name2].state.p,
                    ]
                ),
                h=h_out,
                w=w_out,
            )
        else:
            logger.error(
                "Different medium classes in the inlet ports: %s <-> %s.",
                self._ports[self._port_a1_name].state.super().__class__.__name__,
                self._ports[self._port_a2_name].state.super().__class__.__name__,
            )
            raise SystemExit

        # New mass flows
        self._ports[self._port_b_name].state.m_flow = (
            self._ports[self._port_a1_name1].state.m_flow
            + self._ports[self._port_a2_name2].state.m_flow
        )


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the fittings model classes.")

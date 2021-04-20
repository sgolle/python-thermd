# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

import numpy as np
from thermd.core import (
    BaseStateClass,
    # BaseSignalClass,
    ModelResult,
    MediumBase,
    MediumHumidAir,
)
from thermd.fluid.core import (
    BaseFluidOneInletTwoOutlets,
    BaseFluidOneInletThreeOutlets,
    BaseFluidOneInletFourOutlets,
    BaseFluidTwoInletOneOutlets,
)
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Result classes
# @dataclass
# class ResultFittings(ModelResult):
#     ...


# Machine classes
class JunctionOneToTwo(BaseFluidOneInletTwoOutlets):
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
        super().__init__(name=name, state0=state0)

        # Junction parameters
        if fraction.ndim == 1 and fraction.shape[0] == 2:
            self._fraction = fraction / fraction.sum()  # Normalize
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

    def check_self(self: JunctionOneToTwo) -> bool:
        return True

    def equation(self: JunctionOneToTwo):
        # Stop criterions
        self._last_hmass = self._ports[self._port_a_name].state.hmass
        self._last_p = self._ports[self._port_a_name].state.p
        self._last_m_flow = self._ports[self._port_a_name].state.m_flow

        # Check mass flow
        if self._ports[self._port_a_name].state.m_flow <= 0.0:
            logger.debug("No mass flow in model %s.", self._name)
            return

        # New states
        self._ports[self._port_b1_name].state = self._ports[
            self._port_a_name
        ].state.copy()
        self._ports[self._port_b2_name].state = self._ports[
            self._port_a_name
        ].state.copy()

        # New mass flows
        self._ports[self._port_b1_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[0]
        )
        self._ports[self._port_b2_name].state.m_flow = (
            self._ports[self._port_a_name].state.m_flow * self._fraction[1]
        )


class JunctionOneToThree(BaseFluidOneInletThreeOutlets):
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
        super().__init__(name=name, state0=state0)

        # Junction parameters
        if fraction.ndim == 1 and fraction.shape[0] == 3:
            self._fraction = fraction / fraction.sum()  # Normalize
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

    def check_self(self: JunctionOneToThree) -> bool:
        return True

    def equation(self: JunctionOneToThree):
        # Stop criterions
        self._last_hmass = self._ports[self._port_a_name].state.hmass
        self._last_p = self._ports[self._port_a_name].state.p
        self._last_m_flow = self._ports[self._port_a_name].state.m_flow

        # Check mass flow
        if self._ports[self._port_a_name].state.m_flow <= 0.0:
            logger.debug("No mass flow in model %s.", self._name)
            return

        # New states
        self._ports[self._port_b1_name].state = self._ports[
            self._port_a_name
        ].state.copy()
        self._ports[self._port_b2_name].state = self._ports[
            self._port_a_name
        ].state.copy()
        self._ports[self._port_b3_name].state = self._ports[
            self._port_a_name
        ].state.copy()

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


class JunctionOneToFour(BaseFluidOneInletFourOutlets):
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
        super().__init__(name=name, state0=state0)

        # Junction parameters
        if fraction.ndim == 1 and fraction.shape[0] == 4:
            self._fraction = fraction / fraction.sum()  # Normalize
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

    def check_self(self: JunctionOneToFour) -> bool:
        return True

    def equation(self: JunctionOneToFour):
        # Stop criterions
        self._last_hmass = self._ports[self._port_a_name].state.hmass
        self._last_p = self._ports[self._port_a_name].state.p
        self._last_m_flow = self._ports[self._port_a_name].state.m_flow

        # Check mass flow
        if self._ports[self._port_a_name].state.m_flow <= 0.0:
            logger.debug("No mass flow in model %s.", self._name)
            return

        # New states
        self._ports[self._port_b1_name].state = self._ports[
            self._port_a_name
        ].state.copy()
        self._ports[self._port_b2_name].state = self._ports[
            self._port_a_name
        ].state.copy()
        self._ports[self._port_b3_name].state = self._ports[
            self._port_a_name
        ].state.copy()
        self._ports[self._port_b4_name].state = self._ports[
            self._port_a_name
        ].state.copy()

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


class JunctionTwoToOne(BaseFluidTwoInletOneOutlets):
    """JunctionTwoToOne class.

    The JunctionTwoToOne class implements a ...

    """

    # def __init__(self: JunctionTwoToOne, name: str, state0: BaseStateClass):
    #     """Initialize JunctionTwoToOne class.

    #     Init function of the JunctionTwoToOne class.

    #     """
    #     super().__init__(name=name, state0=state0)

    def check_self(self: JunctionTwoToOne) -> bool:
        return True

    def equation(self: JunctionTwoToOne):
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

        # New states
        if isinstance(self._ports[self._port_a1_name].state, MediumBase) and isinstance(
            self._ports[self._port_a2_name].state, MediumBase
        ):
            h_out = (
                self._ports[self._port_a1_name].state.m_flow
                * self._ports[self._port_a1_name].state.hmass
                + self._ports[self._port_a2_name].state.m_flow
                * self._ports[self._port_a2_name].state.hmass
            ) / (
                self._ports[self._port_a1_name].state.m_flow
                + self._ports[self._port_a2_name].state.m_flow
            )
            self._ports[self._port_b_name].state.set_ph(
                p=np.min(
                    [
                        self._ports[self._port_a1_name].state.p,
                        self._ports[self._port_a2_name].state.p,
                    ]
                ),
                h=h_out,
            )
        elif isinstance(
            self._ports[self._port_a1_name].state, MediumHumidAir
        ) and isinstance(self._ports[self._port_a2_name].state, MediumHumidAir):
            w_out = (
                (
                    self._ports[self._port_a1_name].state.m_flow
                    + self._ports[self._port_a2_name].state.m_flow
                )
                / (
                    self._ports[self._port_a1_name].state.m_flow
                    / (1 + self._ports[self._port_a1_name].state.w)
                    + self._ports[self._port_a2_name].state.m_flow
                    / (1 + self._ports[self._port_a2_name].state.w)
                )
                - 1
            )
            h_out = (
                (
                    self._ports[self._port_a1_name].state.m_flow
                    / (1 + self._ports[self._port_a1_name].state.w)
                )
                * self._ports[self._port_a1_name].state.hmass
                + (
                    self._ports[self._port_a2_name].state.m_flow
                    / (1 + self._ports[self._port_a2_name].state.w)
                )
                * self._ports[self._port_a2_name].state.hmass
            ) / (
                (
                    self._ports[self._port_a1_name].state.m_flow
                    + self._ports[self._port_a2_name].state.m_flow
                )
                / (1 + w_out)
            )
            self._ports[self._port_b_name].state.set_phw(
                p=np.min(
                    [
                        self._ports[self._port_a1_name].state.p,
                        self._ports[self._port_a2_name].state.p,
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
            self._ports[self._port_a1_name].state.m_flow
            + self._ports[self._port_a2_name].state.m_flow
        )


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the fittings model classes.")

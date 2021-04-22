# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations
from typing import Union

import numpy as np
from thermd.core import SignalFloat
from thermd.blocks.core import BaseBlockOneInletOneOutlet, BaseBlockTwoInletsOneOutlet
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Base block classes
class Addition(BaseBlockTwoInletsOneOutlet):
    """Addition block class.

    The addition block class adds the values of inlet 1 and inlet 2.

    """

    def __init__(
        self: Addition, name: str, signal0_1: SignalFloat, signal0_2: SignalFloat,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0_1=signal0_1, signal0_2=signal0_2)

    def check_self(self: Addition) -> bool:
        return True

    def equation(self: Addition):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = (
            self._ports[self._port_c1_name].signal.value
            + self._ports[self._port_c2_name].signal.value
        )


class Subtraction(BaseBlockTwoInletsOneOutlet):
    """Subtraction block class.

    The subtraction block class subtracts the values of inlet 1 and inlet 2.

    """

    def __init__(
        self: Subtraction, name: str, signal0_1: SignalFloat, signal0_2: SignalFloat,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0_1=signal0_1, signal0_2=signal0_2)

    def check_self(self: Subtraction) -> bool:
        return True

    def equation(self: Subtraction):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = (
            self._ports[self._port_c1_name].signal.value
            - self._ports[self._port_c2_name].signal.value
        )


class Multiplication(BaseBlockTwoInletsOneOutlet):
    """Multiplication block class.

    The multiplication block class multyplies the values of inlet 1 and inlet 2.

    """

    def __init__(
        self: Multiplication, name: str, signal0_1: SignalFloat, signal0_2: SignalFloat,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0_1=signal0_1, signal0_2=signal0_2)

    def check_self(self: Multiplication) -> bool:
        return True

    def equation(self: Multiplication):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = (
            self._ports[self._port_c1_name].signal.value
            * self._ports[self._port_c2_name].signal.value
        )


class Division(BaseBlockTwoInletsOneOutlet):
    """Division block class.

    The division block class divides the values of inlet 1 and inlet 2.

    """

    def __init__(
        self: Division, name: str, signal0_1: SignalFloat, signal0_2: SignalFloat,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0_1=signal0_1, signal0_2=signal0_2)

    def check_self(self: Division) -> bool:
        return True

    def equation(self: Division):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = (
            self._ports[self._port_c1_name].signal.value
            / self._ports[self._port_c2_name].signal.value
        )


class Sin(BaseBlockOneInletOneOutlet):
    """Sin block class.

    The sin block class calculates the sine of the value of inlet 1.

    """

    def __init__(self: Sin, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Sin) -> bool:
        return True

    def equation(self: Sin):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.sin(
            self._ports[self._port_c_name].signal.value
        )


class Cos(BaseBlockOneInletOneOutlet):
    """Cos block class.

    The cos block class calculates the cosine of the value of inlet 1.

    """

    def __init__(self: Cos, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Cos) -> bool:
        return True

    def equation(self: Cos):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.cos(
            self._ports[self._port_c_name].signal.value
        )


class Tan(BaseBlockOneInletOneOutlet):
    """Tan block class.

    The tan block class calculates the tangent of the value of inlet 1.

    """

    def __init__(self: Tan, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Tan) -> bool:
        return True

    def equation(self: Tan):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.tan(
            self._ports[self._port_c_name].signal.value
        )


class Exp(BaseBlockOneInletOneOutlet):
    """Exp block class.

    The exp block class calculates the exponential (base e) of the value of inlet 1.

    """

    def __init__(self: Exp, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Exp) -> bool:
        return True

    def equation(self: Exp):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.exp(
            self._ports[self._port_c_name].signal.value
        )


class Log(BaseBlockOneInletOneOutlet):
    """Log block class.

    The log block class calculates the logarithm (base e) of the value of inlet 1.

    """

    def __init__(self: Log, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Log) -> bool:
        return True

    def equation(self: Log):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.log(
            self._ports[self._port_c_name].signal.value
        )


class Log10(BaseBlockOneInletOneOutlet):
    """Log10 block class.

    The log10 block class calculates the logarithm (base 10) of the value of inlet 1.

    """

    def __init__(self: Log10, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Log10) -> bool:
        return True

    def equation(self: Log10):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.log10(
            self._ports[self._port_c_name].signal.value
        )


class Sqrt(BaseBlockOneInletOneOutlet):
    """Sqrt block class.

    The sqrt block class calculates the square root of the value of inlet 1.

    """

    def __init__(self: Sqrt, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Sqrt) -> bool:
        return True

    def equation(self: Sqrt):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.sqrt(
            self._ports[self._port_c_name].signal.value
        )


class Power(BaseBlockOneInletOneOutlet):
    """Power block class.

    The power block class calculates the power of the value of inlet 1 (base).

    """

    def __init__(
        self: Power,
        name: str,
        signal0: SignalFloat,
        power: Union[np.float64, np.int64] = np.float64(2.0),
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

        # Power parameters
        self._power = power

    def check_self(self: Power) -> bool:
        return True

    def equation(self: Power):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.power(
            self._ports[self._port_c_name].signal.value, self._power
        )


class Asin(BaseBlockOneInletOneOutlet):
    """Asin block class.

    The asin block class calculates the arc sine of the value of inlet 1.

    """

    def __init__(self: Asin, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Asin) -> bool:
        return True

    def equation(self: Asin):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.arcsin(
            self._ports[self._port_c_name].signal.value
        )


class Acos(BaseBlockOneInletOneOutlet):
    """Acos block class.

    The acos block class calculates the arc cosine of the value of inlet 1.

    """

    def __init__(self: Acos, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Acos) -> bool:
        return True

    def equation(self: Acos):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.arccos(
            self._ports[self._port_c_name].signal.value
        )


class Atan(BaseBlockOneInletOneOutlet):
    """Atan block class.

    The atan block class calculates the arc tangent of the value of inlet 1.

    """

    def __init__(self: Atan, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Atan) -> bool:
        return True

    def equation(self: Atan):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.arctan(
            self._ports[self._port_c_name].signal.value
        )


class Atan2(BaseBlockOneInletOneOutlet):
    """Atan2 block class.

    The atan2 block class calculates the arc tangent 2 of the value of inlet 1.

    """

    def __init__(self: Atan2, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Atan2) -> bool:
        return True

    def equation(self: Atan2):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.arctan2(
            self._ports[self._port_c_name].signal.value
        )


class Sinh(BaseBlockOneInletOneOutlet):
    """Sinh block class.

    The sinh block class calculates the hyperbolic sine of the value of inlet 1.

    """

    def __init__(self: Sinh, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Sinh) -> bool:
        return True

    def equation(self: Sinh):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.sinh(
            self._ports[self._port_c_name].signal.value
        )


class Cosh(BaseBlockOneInletOneOutlet):
    """Cosh block class.

    The cosh block class calculates the hyperbolic cosine of the value of inlet 1.

    """

    def __init__(self: Cosh, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Cosh) -> bool:
        return True

    def equation(self: Cosh):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.cosh(
            self._ports[self._port_c_name].signal.value
        )


class Tanh(BaseBlockOneInletOneOutlet):
    """Tanh block class.

    The tanh block class calculates the hyperbolic tangent of the value of inlet 1.

    """

    def __init__(self: Tanh, name: str, signal0: SignalFloat):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=signal0)

    def check_self(self: Tanh) -> bool:
        return True

    def equation(self: Tanh):
        # Stop criterions
        self._last_signal_value = self._ports[self._port_d_name].signal.value

        self._ports[self._port_d_name].signal.value = np.tanh(
            self._ports[self._port_c_name].signal.value
        )


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the math (float) block classes.")

# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

import numpy as np
from thermd.core import SignalFloat
from thermd.blocks.core import BaseBlockOneOutlet
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Base block classes
class Constant(BaseBlockOneOutlet):
    """Constant block class.

    The constant block class implements an outlet signal port with a constant value.

    """

    def __init__(
        self: Constant, name: str, constant: np.float64,
    ):
        """Initialize class.

        Init function of the class.

        """
        super().__init__(name=name, signal0=SignalFloat(value=constant))

    def check_self(self: Constant) -> bool:
        return True

    def equation(self: Constant):
        return


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the file for the sources block classes.")

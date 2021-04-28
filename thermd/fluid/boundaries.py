# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

import numpy as np
from thermd.core import (
    BaseStateClass,
    MediumBase,
    MediumHumidAir,
)
from thermd.fluid.core import BaseFluidOneInlet, BaseFluidOneOutlet
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Boundary classes
class SourceFixedState(BaseFluidOneOutlet):
    """SourceFixedState class.

    The SourceFixedState class implements a fixed boundary with an outlet port.

    """

    def check_self(self: SourceFixedState) -> bool:
        return True

    def equation(self: SourceFixedState):
        return


class SinkFixedState(BaseFluidOneInlet):
    """SourceFixedState class.

    The SourceFixedState class implements a fixed boundary with an outlet port.

    """

    def check_self(self: SourceFixedState) -> bool:
        return True

    def equation(self: SourceFixedState):
        return


if __name__ == "__main__":
    logger.info("This is the file for the boundaries model classes.")

# -*- coding: utf-8 -*-

"""Simple example.

Simple example for a system declaration and iterative solver.

"""
import numpy as np

from thermd.core import SystemSimpleIterative
from thermd.helper import get_logger
from thermd.fluid.machines import PumpSimple
from thermd.media.coolprop import (
    CoolPropFluid,
    CoolPropIncompPureFluids,
    MediumCoolProp,
)

if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Start simple example.")

    # Define starting states
    fluid = CoolPropFluid.new_incomp(fluid=CoolPropIncompPureFluids.WATER)
    state0 = MediumCoolProp.from_pT(
        p=np.float64(10 ** 5), T=np.float64(300), m_flow=np.float64(0.01), fluid=fluid
    )

    # Create system
    system = SystemSimpleIterative()

    # Add models and/or blocks
    system.add_model(PumpSimple(name="pump", state0=state0, dp=np.float64(1000)))

    # Connect models and/or blocks

    # Solve system
    system.solve()

    # Save results

    logger.info("Simple example finished successfully.")

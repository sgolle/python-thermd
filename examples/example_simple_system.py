# -*- coding: utf-8 -*-

"""Simple example.

Simple example for a system declaration and iterative solver.

"""
import numpy as np
from pathlib import Path

from thermd.core import SystemSimpleIterative
from thermd.helper import get_logger
from thermd.fluid.machines import PumpSimple
from thermd.media.coolprop import (
    CoolPropBackends,
    CoolPropFluid,
    CoolPropIncompPureFluids,
    MediumCoolProp,
)

if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Start simple example.")

    # Define paths
    output_folder_path = Path(__file__).parent.absolute() / "Output/"
    output_folder_path.mkdir(parents=True, exist_ok=True)

    # Define starting states
    fluid = CoolPropFluid.new_incomp(fluid_name=CoolPropIncompPureFluids.WATER)
    state0 = MediumCoolProp.from_pT(
        p=np.float64(10 ** 5),
        T=np.float64(300),
        m_flow=np.float64(0.01),
        fluid=fluid,
        backend=CoolPropBackends.INCOMP,
    )

    # Create models
    pump1 = PumpSimple(name="pump1", state0=state0, dp=np.float64(2 * 10 ** 5))
    pump2 = PumpSimple(name="pump2", state0=state0, dp=np.float64(2 * 10 ** 5))

    # Create system
    system = SystemSimpleIterative(max_iteration_counter=100)

    # Add models and/or blocks to system
    system.add_model(pump1)
    system.add_model(pump2)

    # Connect models and/or blocks in system
    system.connect(pump1.port_b, pump2.port_a)

    # Solve system
    result = system.solve()
    logger.info(
        "Solver finished with status %s (%s)", str(result.status), result.message
    )

    # Save results
    system.save_results(output_folder_path / "results.ods")

    logger.info("Simple example finished successfully.")

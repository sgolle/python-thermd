# -*- coding: utf-8 -*-

"""Core library of thermd.

Library of 1-dimensional (modelica-like) models. Core file with the API of the library.

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Dict, Type, Union, Optional, Tuple, Any

# from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pyexcel as pe

# from CoolProp.CoolProp import AbstractState

from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)

# Enums
class NodeTypes(Enum):
    MODEL = auto()
    BLOCK = auto()
    PORT = auto()


class PortTypes(Enum):
    STATE_INLET = auto()
    STATE_OUTLET = auto()
    STATE_INLET_OUTLET = auto()
    SIGNAL_INLET = auto()
    SIGNAL_OUTLET = auto()
    SIGNAL_INLET_OUTLET = auto()


class StatePhases(Enum):
    LIQUID = 0
    SUPERCRITICAL = 1
    SUPERCRITICAL_GAS = 2
    SUPERCRITICAL_LIQUID = 3
    CRITICAL_POINT = 4
    GAS = 5
    TWOPHASE = 6
    UNKNOWN = 7
    NOT_IMPOSED = 8


# Result classes
class BaseResultClass(ABC):
    ...


@dataclass
class SystemResult(BaseResultClass):
    models: Optional[Dict[str, ModelResult]]
    blocks: Optional[Dict[str, BlockResult]]
    success: bool
    status: np.int8
    message: str
    nit: np.int16

    @classmethod
    def from_success(
        cls: Type[SystemResult],
        models: Optional[Dict[str, ModelResult]],
        blocks: Optional[Dict[str, BlockResult]],
        nit: np.int16,
    ) -> SystemResult:
        return cls(
            models=models,
            blocks=blocks,
            success=True,
            status=np.int8(0),
            message="Solver finished successfully.",
            nit=nit,
        )

    @classmethod
    def from_error(
        cls: Type[SystemResult],
        models: Optional[Dict[str, ModelResult]],
        blocks: Optional[Dict[str, BlockResult]],
        nit: np.int16,
    ) -> SystemResult:
        return cls(
            models=models,
            blocks=blocks,
            success=False,
            status=np.int8(2),
            message="Solver didn't finish successfully.",
            nit=nit,
        )

    @classmethod
    def from_convergence(
        cls: Type[SystemResult],
        models: Optional[Dict[str, ModelResult]],
        blocks: Optional[Dict[str, BlockResult]],
        nit: np.int16,
    ) -> SystemResult:
        return cls(
            models=models,
            blocks=blocks,
            success=False,
            status=np.int8(1),
            message="Solver didn't converge successfully.",
            nit=nit,
        )


@dataclass
class ModelResult(BaseResultClass):
    states: Optional[Dict[str, BaseStateClass]]
    signals: Optional[Dict[str, BaseSignalClass]]


@dataclass
class BlockResult(BaseResultClass):
    signals: Optional[Dict[str, BaseSignalClass]]


# Base classes
class BaseSystemClass(ABC):
    """Base class of the physical system.

    The abstract base class of the physical system describes the API of every
    derived physical system. Physical systems are the main classes of the library,
    which combines all components (models, blocks, connectors, etc.), as well as
    all methods to prepare, solve and illustrate the system.

    """

    def __init__(self: BaseSystemClass, **kwargs):
        """Initialize base system class.

        Init function of the base system class.

        """
        # System parameter
        self._stop_criterion_energy = np.float64(1)
        self._stop_criterion_momentum = np.float64(1)
        self._stop_criterion_mass = np.float64(0.001)
        self._stop_criterion_signal = np.float64(0.001)
        self._iteration_counter = np.uint16(0)
        self._max_iteration_counter = np.uint16(1000)

        if "stop_criterion_energy" in kwargs:
            self._stop_criterion_energy = np.float64(kwargs["stop_criterion_energy"])
        if "stop_criterion_momentum" in kwargs:
            self._stop_criterion_momentum = np.float64(
                kwargs["stop_criterion_momentum"]
            )
        if "stop_criterion_mass" in kwargs:
            self._stop_criterion_mass = np.float64(kwargs["stop_criterion_mass"])
        if "stop_criterion_signal" in kwargs:
            self._stop_criterion_signal = np.float64(kwargs["stop_criterion_signal"])
        if "max_iteration_counter" in kwargs:
            self._max_iteration_counter = np.uint16(kwargs["max_iteration_counter"])

        # Initialize index lists of models, blocks, ports, states and signals
        self._models: List[str] = list()
        self._blocks: List[str] = list()
        self._ports: Dict[str, List[str]] = dict()

        # Initialize result parameter
        self._result: Optional[SystemResult] = None

        # Initialize main graph
        self._network = nx.DiGraph()

    # @classmethod
    # def from_file(cls: Type[BaseSystemClass], filename: str) -> BaseSystemClass:
    #     return

    # def to_file(self: BaseSystemClass, filename: str):
    #     return

    @property
    def network(self):
        return self._network

    @property
    def result(self) -> Optional[SystemResult]:
        return self._result

    def clear(self: BaseSystemClass):
        self._network.clear()

    def freeze(self: BaseSystemClass):
        self._network.freeze()

    def is_frozen(self: BaseSystemClass):
        self._network.is_frozen()

    def add_model(
        self: BaseSystemClass, node_class: BaseModelClass,
    ):

        logger.info("Add model: %s", node_class.name)

        if node_class.name in self._models:
            logger.error("Model name already in use: %s", node_class.name)
            raise SystemExit

        self._network.add_node(
            node_class.name, node_type=NodeTypes.MODEL, node_class=node_class
        )
        self._models.append(node_class.name)
        self._ports[node_class.name] = list()

        for port in node_class.ports.values():

            logger.info("Add port: %s", port.name)

            self._network.add_node(port.name, node_type=NodeTypes.PORT)
            self._ports[node_class.name].append(port.name)

            if (
                port.port_type == PortTypes.STATE_INLET
                or port.port_type == PortTypes.SIGNAL_INLET
            ):
                self._network.add_edge(port.name, node_class.name)
            elif (
                port.port_type == PortTypes.STATE_OUTLET
                or port.port_type == PortTypes.SIGNAL_OUTLET
            ):
                self._network.add_edge(node_class.name, port.name)
            else:
                logger.error("Wrong port function: %s", port.port_type)
                raise SystemExit

    def add_block(
        self: BaseSystemClass, node_class: BaseBlockClass,
    ):

        logger.info("Add block: %s", node_class.name)

        if node_class.name in self._blocks:
            logger.error("Block name already in use: %s", node_class.name)
            raise SystemExit

        self._network.add_node(
            node_class.name, node_type=NodeTypes.BLOCK, node_class=node_class
        )
        self._blocks.append(node_class.name)
        self._ports[node_class.name] = list()

        for port in node_class.ports.values():

            logger.info("Add port: %s", port.name)

            self._network.add_node(port.name, node_type=NodeTypes.PORT)
            self._ports[node_class.name].append(port.name)

            if (
                port.port_type == PortTypes.STATE_INLET
                or port.port_type == PortTypes.SIGNAL_INLET
            ):
                self._network.add_edge(port.name, node_class.name)
            elif (
                port.port_type == PortTypes.STATE_OUTLET
                or port.port_type == PortTypes.SIGNAL_OUTLET
            ):
                self._network.add_edge(node_class.name, port.name)
            else:
                logger.error("Wrong port function: %s", port.port_type)
                raise SystemExit

    def connect(
        self: BaseSystemClass, port1: BasePortClass, port2: BasePortClass,
    ):
        if port1.__class__.__name__ == port2.__class__.__name__:
            if (
                port1.port_type
                in [
                    PortTypes.STATE_OUTLET,
                    PortTypes.STATE_INLET_OUTLET,
                    PortTypes.SIGNAL_OUTLET,
                    PortTypes.SIGNAL_INLET_OUTLET,
                ]
            ) and (
                port2.port_type
                in [
                    PortTypes.STATE_INLET,
                    PortTypes.STATE_INLET_OUTLET,
                    PortTypes.SIGNAL_INLET,
                    PortTypes.SIGNAL_INLET_OUTLET,
                ]
            ):

                self._network.add_edge(port1.name, port2.name)

            else:
                logger.error(
                    (
                        "First port must be outlet and second port must be "
                        "inlet port of associated models/blocks: %s <-> %s"
                    ),
                    port1.name,
                    port2.name,
                )
                raise SystemExit
        else:
            logger.error("Port types not compatible: %s <-> %s", port1.name, port2.name)
            raise SystemExit

    def check_self(self: BaseSystemClass):
        # Check all models
        for model in self._models:
            if not self._network.nodes[model]["node_class"].check_self():
                logger.error("Model %s shows an error.", model)

        # Check all blocks
        for block in self._blocks:
            if not self._network.nodes[block]["node_class"].check_self():
                logger.error("Block %s shows an error.", block)

    # def plot_graph(self: BaseSystemClass, path: Path):
    #     nx.draw(
    #         self._network,
    #         # pos=nx.spring_layout(self._network, scale=5),
    #         with_labels=True,
    #     )
    #     plt.savefig(path)

    # def save_graph(self: BaseSystemClass, path: Path):
    #     nx.write_graphml(self._network, path.as_posix())

    def get_node_results(
        self: BaseSystemClass,
    ) -> Tuple[Optional[Dict[str, ModelResult]], Optional[Dict[str, BlockResult]]]:
        models: Optional[Dict[str, ModelResult]] = dict()
        blocks: Optional[Dict[str, BlockResult]] = dict()

        if models is not None:
            for model_name in self._models:
                models[model_name] = self._network.nodes[model_name][
                    "node_class"
                ].get_results()
            if len(models) == 0:
                models = None

        if blocks is not None:
            for block_name in self._blocks:
                blocks[block_name] = self._network.nodes[block_name][
                    "node_class"
                ].get_results()
            if len(blocks) == 0:
                blocks = None

        return models, blocks

    @staticmethod
    def pyexcel_decimal_replace(s):
        s = s.replace(".", ",")
        return s

    def save_results(self: BaseSystemClass, path: Path):
        if self._result is None:
            logger.error(
                "No SystemResult in system class! Maybe system not solved yet."
            )
            model_results, block_results = self.get_node_results()
        else:
            model_results = self._result.models
            block_results = self._result.blocks

        states_results = list()
        states_results.append(
            [
                "Node name",
                "Node type",
                "Port name",
                "Fluid name",
                "Temperature in K",
                "Pressure in Pa",
                "Spec. enthalpy in J/kg",
                "Spec. entropy in J/(kg*K)",
                "Mass flow in kg/s",
            ]
        )
        signals_results = list()
        signals_results.append(
            ["Node name", "Node type", "Port name", "Signal value",]
        )
        if model_results is not None:
            for model_name, model_result in model_results.items():
                if model_result.states is not None:
                    for port_name, state in model_result.states.items():
                        states_results.append(
                            [
                                model_name,
                                "Model",
                                port_name,
                                str(state.fluid_name),
                                str(state.T),
                                str(state.p),
                                str(state.hmass),
                                str(state.smass),
                                str(state.m_flow),
                            ]
                        )
                if model_result.signals is not None:
                    for port_name, signal in model_result.signals.items():
                        signals_results.append(
                            [model_name, "Model", port_name, signal.value]
                        )

        if block_results is not None:
            for block_name, block_result in block_results.items():
                if block_result.signals is not None:
                    for port_name, signal in block_result.signals.items():
                        signals_results.append(
                            [block_name, "Block", port_name, str(signal.value)]
                        )

        book = pe.get_book(
            bookdict={"states": states_results, "signals": signals_results}
        )
        book.states.map(self.pyexcel_decimal_replace)
        book.signals.map(self.pyexcel_decimal_replace)
        book.save_as(filename=path.as_posix())

    @abstractmethod
    def stop_criterion(self: BaseSystemClass) -> bool:
        ...

    @abstractmethod
    def solve(self: BaseSystemClass) -> SystemResult:
        ...


class BaseModelClass(ABC):
    """Base class of the physical model/ component.

    The abstract base class of the physical model describes the API of every
    derived physical model and represents a physical component (e.g. heat exchanger).

    """

    def __init__(self: BaseModelClass, name: str):
        """Initialize base model class.

        Init function of the base model class.

        """
        # Class properties
        self._name = name
        self._ports: Dict[str, Union[PortState, PortSignal]] = dict()

        # Balances
        self._energy_balance = np.float64(0.0)
        self._momentum_balance = np.float64(0.0)
        self._mass_balance = np.float64(0.0)

    @property
    def name(self: BaseModelClass) -> str:
        return self._name

    @property
    def ports(self: BaseModelClass) -> Dict[str, Union[PortState, PortSignal]]:
        return self._ports

    @property
    @abstractmethod
    def stop_criterion_energy(self: BaseModelClass) -> np.float64:
        ...

    @property
    @abstractmethod
    def stop_criterion_momentum(self: BaseModelClass) -> np.float64:
        ...

    @property
    @abstractmethod
    def stop_criterion_mass(self: BaseModelClass) -> np.float64:
        ...

    @property
    @abstractmethod
    def stop_criterion_signal(self: BaseModelClass) -> np.float64:
        ...

    def add_port(self: BaseModelClass, port: Union[PortState, PortSignal]) -> None:
        self._ports[port.name] = port

    # def get_port_attr(
    #     self: BaseModelClass, port_name: str,
    # ) -> Union[BaseStateClass, BaseSignalClass]:
    #     if port_name not in self._ports:
    #         logger.error("Unknown port name: %s.", port_name)
    #         raise SystemExit

    #     if isinstance(self._ports[port_name], PortState):
    #         return self._ports[port_name].state
    #     elif isinstance(self._ports[port_name], PortSignal):
    #         return self._ports[port_name].signal
    #     else:
    #         logger.error(
    #             "Unknown port class: %s.", self._ports[port_name].__class__.__name__
    #         )
    #         raise SystemExit

    # def set_port_attr(
    #     self: BaseModelClass,
    #     port_name: str,
    #     port_attr: Union[BaseStateClass, BaseSignalClass],
    # ) -> None:
    #     if port_name in self._ports:
    #         if isinstance(self._ports[port_name], PortState) and isinstance(
    #             port_attr, BaseStateClass
    #         ):
    #             self._ports[port_name].state = port_attr
    #         elif isinstance(self._ports[port_name], PortSignal) and isinstance(
    #             port_attr, BaseSignalClass
    #         ):
    #             self._ports[port_name].signal = port_attr
    #         else:
    #             logger.error(
    #                 "Port attribute and class doesn't match: %s -> %s.",
    #                 self._ports[port_name].__class__.__name__,
    #                 port_attr.__class__.__name__,
    #             )
    #             raise SystemExit

    #     else:
    #         logger.error("Unknown port name: %s.", port_name)
    #         raise SystemExit

    def check_state(
        self: BaseModelClass,
        max_error_energy: np.float64 = np.float64(1),
        max_error_momentum: np.float64 = np.float64(1),
        max_error_mass: np.float64 = np.float64(0.001),
    ) -> bool:
        if self._energy_balance != max_error_energy:
            logger.info(
                "Energy balance of model %s above the maximum error %s: %s",
                self._name,
                str(max_error_energy),
                str(self._energy_balance),
            )
            return False
        if self._momentum_balance != max_error_momentum:
            logger.info(
                "Momentum balance of model %s above the maximum error %s: %s",
                self._name,
                str(max_error_momentum),
                str(self._momentum_balance),
            )
            return False
        if self._mass_balance != max_error_mass:
            logger.info(
                "Mass balance of model %s above the maximum error %s: %s",
                self._name,
                str(max_error_mass),
                str(self._mass_balance),
            )
            return False
        return True

    @abstractmethod
    def update_balances(self: BaseModelClass) -> None:
        ...

    @abstractmethod
    def check_self(self: BaseModelClass) -> BaseResultClass:
        ...

    @abstractmethod
    def get_results(self: BaseModelClass) -> ModelResult:
        ...

    @abstractmethod
    def equation(self: BaseModelClass):
        ...


class BaseBlockClass(ABC):
    """Base class of the mathematical block.

    The abstract base class of the mathematical block describes the API of every
    derived mathematical blocks.

    """

    def __init__(self: BaseBlockClass, name: str):
        """Initialize base block class.

        Init function of the base block class.

        """
        # Class properties
        self._name = name
        self._ports: Dict[str, PortSignal] = dict()

    @property
    def name(self: BaseBlockClass) -> str:
        return self._name

    @property
    def ports(self: BaseBlockClass) -> Dict[str, PortSignal]:
        return self._ports

    @property
    @abstractmethod
    def stop_criterion_signal(self: BaseBlockClass) -> np.float64:
        ...

    def add_port(self: BaseBlockClass, port: PortSignal) -> None:
        self._ports[port.name] = port

    # def get_port_attr(self: BaseBlockClass, port_name: str) -> BaseSignalClass:
    #     if port_name not in self._ports:
    #         logger.error("Unknown port name: %s.", port_name)
    #         raise SystemExit

    #     return self._ports[port_name].signal

    # def set_port_attr(
    #     self: BaseBlockClass, port_name: str, port_attr: BaseSignalClass,
    # ) -> None:
    #     if port_name in self._ports:
    #         if isinstance(self._ports[port_name], PortSignal) and isinstance(
    #             port_attr, BaseSignalClass
    #         ):
    #             self._ports[port_name].port_attr = port_attr
    #         else:
    #             logger.error(
    #                 (
    #                     "Port class must be PortSignal and port attribute must be "
    #                     "BaseSignalClass: %s -> %s."
    #                 ),
    #                 self._ports[port_name].__class__.__name__,
    #                 port_attr.__class__.__name__,
    #             )
    #             raise SystemExit

    #     else:
    #         logger.error("Unknown port name: %s.", port_name)
    #         raise SystemExit

    @abstractmethod
    def check_self(self: BaseBlockClass) -> bool:
        ...

    @abstractmethod
    def get_results(self: BaseBlockClass) -> BlockResult:
        ...

    @abstractmethod
    def equation(self: BaseBlockClass):
        ...


class BasePortClass(ABC):
    """Base class of the ports.

    The abstract base class of the ports.

    """

    def __init__(
        self: BasePortClass, name: str, port_type: PortTypes,
    ):
        """Initialize base port class.

        Init function of the base port class.

        """
        # Class properties
        self._name = name
        self._port_type = port_type

    @property
    def name(self: BasePortClass) -> str:
        return self._name

    @property
    def port_type(self: BasePortClass) -> PortTypes:
        return self._port_type


class BaseStateClass(ABC):
    """Base class of the states.

    The abstract base class of the states provides the API for all derived
    state classes. States are one type of connectors between models or blocks.

    """

    @abstractmethod
    def copy(self: BaseStateClass) -> BaseStateClass:
        """Copy the BaseStateClass object.

        Method to copy the class object.

        """
        ...

    @property
    @abstractmethod
    def cpmass(self: BaseStateClass) -> np.float64:
        """Mass-specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        ...

    @property
    @abstractmethod
    def cpmolar(self: BaseStateClass) -> np.float64:
        """Molar-specific heat at constant pressure in J/mol/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/mol/K

        """
        ...

    @property
    @abstractmethod
    def cvmass(self: BaseStateClass) -> np.float64:
        """Mass-specific heat at constant volume in J/kg/K.

        Returns:
            np.float64: Specific heat at constant volume in J/kg/K

        """
        ...

    @property
    @abstractmethod
    def cvmolar(self: BaseStateClass) -> np.float64:
        """Molar-specific heat at constant volume in J/mol/K.

        Returns:
            np.float64: Specific heat at constant volume in J/mol/K

        """
        ...

    @property
    @abstractmethod
    def hmass(self: BaseStateClass) -> np.float64:
        """Mass-specific enthalpy in J/kg.

        Returns:
            np.float64: Mass-specific enthalpy in J/kg

        """
        ...

    @property
    @abstractmethod
    def hmolar(self: BaseStateClass) -> np.float64:
        """Molar-specific enthalpy in J/mol.

        Returns:
            np.float64: Mass-specific enthalpy in J/mol

        """
        ...

    @property
    @abstractmethod
    def conductivity(self: BaseStateClass) -> np.float64:
        """Thermal conductivity in W/m/K.

        Returns:
            np.float64: Thermal conductivity in W/m/K

        """
        ...

    @property
    @abstractmethod
    def viscosity(self: BaseStateClass) -> np.float64:
        """Viscosity in Pa*s.

        Returns:
            np.float64: Viscosity in Pa*s

        """
        ...

    @property
    @abstractmethod
    def p(self: BaseStateClass) -> np.float64:
        """Pressure in Pa.

        Returns:
            np.float64: Pressure in Pa

        """
        ...

    @property
    @abstractmethod
    def rhomass(self: BaseStateClass) -> np.float64:
        """Mass-specific density in kg/m**3.

        Returns:
            np.float64: Density in kg/m**3

        """
        ...

    @property
    @abstractmethod
    def rhomolar(self: BaseStateClass) -> np.float64:
        """Molar-specific density in mol/m**3.

        Returns:
            np.float64: Density in mol/m**3

        """
        ...

    @property
    @abstractmethod
    def gas_constant(self: BaseStateClass) -> np.float64:
        """Specific gas constant in J/mol/K.

        Returns:
            np.float64: Specific gas constant in J/mol/K

        """
        ...

    @property
    @abstractmethod
    def m_flow(self: BaseStateClass) -> np.float64:
        """Mass flow in kg/s.

        Returns:
            np.float64: Mass flow in kg/s

        """
        ...

    @property
    @abstractmethod
    def smass(self: BaseStateClass) -> np.float64:
        """Mass-specific entropy in J/kg/K.

        Returns:
            np.float64: Mass-specific entropy in J/kg/K

        """
        ...

    @property
    @abstractmethod
    def smolar(self: BaseStateClass) -> np.float64:
        """Molar-specific entropy in J/mol/K.

        Returns:
            np.float64: Mass-specific entropy in J/mol/K

        """
        ...

    @property
    @abstractmethod
    def T(self: BaseStateClass) -> np.float64:
        """Temperature in K.

        Returns:
            np.float64: Temperature in K

        """
        ...

    @property
    @abstractmethod
    def vmass(self: BaseStateClass) -> np.float64:
        """Mass-specific volume in m**3/kg.

        Returns:
            np.float64: Specific volume in m**3/kg

        """
        ...

    @property
    @abstractmethod
    def vmolar(self: BaseStateClass) -> np.float64:
        """Molar-specific volume in m**3/mol.

        Returns:
            np.float64: Specific volume in m**3/mol

        """
        ...

    @property
    @abstractmethod
    def x(self: BaseStateClass) -> np.float64:
        """Vapor quality.

        Returns:
            np.float64: Vapor quality

        """
        ...

    @property
    @abstractmethod
    def Z(self: BaseStateClass) -> np.float64:
        """Compressibility factor.

        Returns:
            np.float64: Compressibility factor

        """
        ...

    @property
    @abstractmethod
    def phase(self: BaseStateClass) -> StatePhases:
        """State phase.

        Returns:
            StatePhases: State phase

        """
        ...

    @property
    @abstractmethod
    def fluid_name(self: BaseStateClass) -> str:
        ...


class BaseSignalClass(ABC):
    """Base class of the signals.

    The abstract base class of the signals provides the API for all derived
    signal classes. Signals are one type of connectors between models or blocks.

    """

    def __init__(self: BaseSignalClass, value: Any) -> None:
        """Initialize class.

        Init function of the class.

        """
        # Signal parameters
        self._value = value

    @abstractmethod
    def copy(self: BaseSignalClass) -> BaseSignalClass:
        """Copy the BaseSignalClass object.

        Method to copy the class object.

        """
        ...

    @property
    def value(self: BaseSignalClass) -> Any:
        return self._value

    @value.setter
    def value(self: BaseSignalClass, value: Any) -> None:
        self._value = value


# System classes
class SystemSimpleIterative(BaseSystemClass):
    """Class of a simple system.

    The simple system is the main starting point for all physical systems and
    represents an exemplary system class, which can be modified further.

    """

    def __init__(self: SystemSimpleIterative, **kwargs):
        """Initialize simple system class.

        Init function of the simple system class.

        """
        super().__init__(**kwargs)

        # Additional system parameter
        # self._start_node: List[str] = list()
        # self._end_node: List[str] = list()
        self._simulation_nodes: List[str] = list()

        # if "start_node" in kwargs:
        #     self._start_node = kwargs["start_node"]

        # if kwargs["start_node"] is None:
        #     kwargs["start_node"] = self._models[0]

    def stop_criterion(self: SystemSimpleIterative) -> bool:
        # Iteration counter
        if self._iteration_counter == 0:
            self._iteration_counter += np.uint16(1)
            return True
        self._iteration_counter += np.uint16(1)

        if self._iteration_counter > self._max_iteration_counter:
            return False

        # Stop criterions of models and blocks
        for node_name in self._simulation_nodes:
            if self.network.nodes[node_name]["node_type"] == NodeTypes.MODEL:
                if (
                    np.abs(
                        self._network.nodes[node_name][
                            "node_class"
                        ].stop_criterion_energy
                    )
                    > self._stop_criterion_energy
                ):
                    return True
                if (
                    np.abs(
                        self._network.nodes[node_name][
                            "node_class"
                        ].stop_criterion_momentum
                    )
                    > self._stop_criterion_momentum
                ):
                    return True
                if (
                    np.abs(
                        self._network.nodes[node_name]["node_class"].stop_criterion_mass
                    )
                    > self._stop_criterion_mass
                ):
                    return True
                if (
                    np.abs(
                        self._network.nodes[node_name][
                            "node_class"
                        ].stop_criterion_signal
                    )
                    > self._stop_criterion_signal
                ):
                    return True
            elif self.network.nodes[node_name]["node_type"] == NodeTypes.BLOCK:
                if (
                    np.abs(
                        self._network.nodes[node_name][
                            "node_class"
                        ].stop_criterion_signal
                    )
                    > self._stop_criterion_signal
                ):
                    return True
            else:
                logger.error(
                    "Node type in simulation nodes not defined: %s.",
                    self.network.nodes[node_name]["node_type"].value,
                )
                raise SystemExit

        return False

    def pre_solve(self: SystemSimpleIterative):
        self.check_self()
        self._simulation_nodes = self._models + self._blocks

    def solve(self: SystemSimpleIterative) -> SystemResult:
        logger.info("Start solver.")
        logger.info("Pre-solve.")
        self.pre_solve()

        logger.info("Solve.")

        try:
            while self.stop_criterion():
                logger.info(
                    "Iteration count: %s of %s",
                    str(self._iteration_counter),
                    str(self._max_iteration_counter),
                )
                for node_name in self._simulation_nodes:
                    logger.debug("Calculate node %s", node_name)

                    self._network.nodes[node_name]["node_class"].equation()

                    for outlet_port_name in self._network.successors(node_name):

                        if isinstance(
                            self._network.nodes[node_name]["node_class"].ports[
                                outlet_port_name
                            ],
                            PortState,
                        ):
                            if (
                                self._network.nodes[node_name]["node_class"]
                                .ports[outlet_port_name]
                                .state.m_flow
                                <= 0.0
                            ):
                                continue

                        for connected_port_name in self._network.successors(
                            outlet_port_name
                        ):
                            for successor_node_name in self._network.successors(
                                connected_port_name
                            ):
                                logger.debug(
                                    "Set port %s of node %s with port %s of node %s",
                                    connected_port_name,
                                    successor_node_name,
                                    outlet_port_name,
                                    node_name,
                                )

                                if (
                                    self._network.nodes[node_name]["node_class"]
                                    .ports[outlet_port_name]
                                    .port_type
                                    in [
                                        PortTypes.STATE_OUTLET,
                                        PortTypes.STATE_INLET_OUTLET,
                                    ]
                                ) and (
                                    self._network.nodes[successor_node_name][
                                        "node_class"
                                    ]
                                    .ports[connected_port_name]
                                    .port_type
                                    in [
                                        PortTypes.STATE_INLET,
                                        PortTypes.STATE_INLET_OUTLET,
                                    ]
                                ):
                                    self._network.nodes[successor_node_name][
                                        "node_class"
                                    ].ports[connected_port_name].state = (
                                        self._network.nodes[node_name]["node_class"]
                                        .ports[outlet_port_name]
                                        .state
                                    )
                                elif (
                                    self._network.nodes[node_name]["node_class"]
                                    .ports[outlet_port_name]
                                    .port_type
                                    in [
                                        PortTypes.SIGNAL_OUTLET,
                                        PortTypes.SIGNAL_INLET_OUTLET,
                                    ]
                                ) and (
                                    self._network.nodes[successor_node_name][
                                        "node_class"
                                    ]
                                    .ports[connected_port_name]
                                    .port_type
                                    in [
                                        PortTypes.SIGNAL_INLET,
                                        PortTypes.SIGNAL_INLET_OUTLET,
                                    ]
                                ):
                                    self._network.nodes[successor_node_name][
                                        "node_class"
                                    ].ports[connected_port_name].signal = (
                                        self._network.nodes[node_name]["node_class"]
                                        .ports[outlet_port_name]
                                        .signal
                                    )

        except BaseException as e:
            logger.error("Solver failed.")
            logger.exception("Error code: %s", str(e))

            models, blocks = self.get_node_results()
            self._result = SystemResult.from_error(
                models=models, blocks=blocks, nit=self._iteration_counter
            )
            return self._result

        # Post solve
        logger.info("Post-solve.")

        models, blocks = self.get_node_results()

        if self._iteration_counter > self._max_iteration_counter:
            logger.info("Solver did not converge.")
            self._result = SystemResult.from_convergence(
                models=models, blocks=blocks, nit=self._iteration_counter
            )
            return self._result

        logger.info("Solver finished successfully.")
        self._result = SystemResult.from_success(
            models=models, blocks=blocks, nit=self._iteration_counter
        )
        return self._result


# Port classes
class PortState(BasePortClass):
    """Class of a state port.

    The state port is a interface in a model and can connect different
    models with a fluid connection, which links the thermodynamic states.

    """

    def __init__(
        self: PortState, name: str, port_type: PortTypes, state: BaseStateClass
    ):
        """Initialize base port class.

        Init function of the base port class.

        """
        super().__init__(name=name, port_type=port_type)

        # Class properties
        self._state = state.copy()

    @property
    def state(self: PortState) -> BaseStateClass:
        return self._state

    @state.setter
    def state(self: PortState, state: BaseStateClass) -> None:
        self._state = state.copy()


class PortSignal(BasePortClass):
    """Class of a signal port.

    The signal port is a interface in a model and can connect different
    models with a signal connection, which links values. 

    """

    def __init__(
        self: PortSignal, name: str, port_type: PortTypes, signal: BaseSignalClass
    ):
        """Initialize base port class.

        Init function of the base port class.

        """
        super().__init__(name=name, port_type=port_type)

        # Class properties
        self._signal = signal.copy()

    @property
    def signal(self: PortSignal) -> BaseSignalClass:
        return self._signal

    @signal.setter
    def signal(self: PortSignal, signal: BaseSignalClass) -> None:
        self._signal = signal.copy()


# State/ media classes
class MediumBase(BaseStateClass):
    """Class of pure or pseudo-pure (mixtures) media.

    The medium class of pure fluids provides the API for all derived
    medium classes with pure or pseudo-pure (mixtures) behavior, hence only 
    two state values need to be given to define the state.

    """

    @abstractmethod
    def set_pT(self: BaseStateClass, p: np.float64, T: np.float64,) -> None:
        ...

    @abstractmethod
    def set_px(self: BaseStateClass, p: np.float64, x: np.float64,) -> None:
        ...

    @abstractmethod
    def set_Tx(self: BaseStateClass, T: np.float64, x: np.float64,) -> None:
        ...

    @abstractmethod
    def set_ph(self: BaseStateClass, p: np.float64, h: np.float64,) -> None:
        ...

    @abstractmethod
    def set_Th(self: BaseStateClass, T: np.float64, h: np.float64,) -> None:
        ...

    @abstractmethod
    def set_ps(self: BaseStateClass, p: np.float64, s: np.float64,) -> None:
        ...

    @abstractmethod
    def set_Ts(self: BaseStateClass, T: np.float64, s: np.float64,) -> None:
        ...


class MediumHumidAir(BaseStateClass):
    """Class of binary mixtures media.

    The medium class of binary mixtures provides the API for all derived
    medium classes with two pure or pseudo-pure but uneven components (e. g. humid air),
    hence three state values need to be given to define the state.

    """

    @property
    @abstractmethod
    def w(self: BaseStateClass) -> np.float64:
        """Humidity ratio in kg/kg.

        Returns:
            np.float64: Humidity ratio in kg/kg

        """
        ...

    @property
    @abstractmethod
    def w_gaseous(self: BaseStateClass) -> np.float64:
        """Humidity ratio of only gaseous water in kg/kg.

        Returns:
            np.float64: Humidity ratio of only gaseous water in kg/kg

        """
        ...

    @property
    @abstractmethod
    def w_liquid(self: BaseStateClass) -> np.float64:
        """Humidity ratio of only liquid water in kg/kg.

        Returns:
            np.float64: Humidity ratio of only liquid water in kg/kg

        """
        ...

    @property
    @abstractmethod
    def w_solid(self: BaseStateClass) -> np.float64:
        """Humidity ratio of only solid water in kg/kg.

        Returns:
            np.float64: Humidity ratio of only solid water in kg/kg

        """
        ...

    @property
    @abstractmethod
    def ws(self: MediumHumidAir) -> np.float64:
        """Humidity ratio at saturation condition.

        Returns:
            np.float64: Humidity ratio at saturation condition

        """
        ...

    @property
    @abstractmethod
    def phi(self: MediumHumidAir) -> np.float64:
        """Relative humidity.

        Returns:
            np.float64: Relative humidity

        """
        ...

    @abstractmethod
    def set_pTw(
        self: BaseStateClass, p: np.float64, T: np.float64, w: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_phw(
        self: BaseStateClass, p: np.float64, h: np.float64, w: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_Thw(
        self: BaseStateClass, T: np.float64, h: np.float64, w: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_psw(
        self: BaseStateClass, p: np.float64, s: np.float64, w: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_Tsw(
        self: BaseStateClass, T: np.float64, s: np.float64, w: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_pTphi(
        self: BaseStateClass, p: np.float64, T: np.float64, phi: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_phphi(
        self: BaseStateClass, p: np.float64, h: np.float64, phi: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_Thphi(
        self: BaseStateClass, T: np.float64, h: np.float64, phi: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_psphi(
        self: BaseStateClass, p: np.float64, s: np.float64, phi: np.float64
    ) -> None:
        ...

    @abstractmethod
    def set_Tsphi(
        self: BaseStateClass, T: np.float64, s: np.float64, phi: np.float64
    ) -> None:
        ...


# Signal classes
class SignalBoolean(BaseSignalClass):
    """Signal class.

    The signal class is derived from the BaseSignalClass and defines a certain
    data type for the value of the signal.

    """

    def __init__(self: SignalBoolean, value: np.bool8) -> None:
        """Initialize class.

        Init function of the class.

        """
        super().__init__(value=value)

    def copy(self: SignalBoolean) -> SignalBoolean:
        """Copy the BaseSignalClass object.

        Method to copy the class object.

        """
        return SignalBoolean(self._value)

    @property
    def value(self: SignalBoolean) -> np.bool8:
        return self._value

    @value.setter
    def value(self: SignalBoolean, value: np.bool8) -> None:
        self._value = value


class SignalInteger(BaseSignalClass):
    """Signal class.

    The signal class is derived from the BaseSignalClass and defines a certain
    data type for the value of the signal.

    """

    def __init__(self: SignalInteger, value: np.int64) -> None:
        """Initialize class.

        Init function of the class.

        """
        super().__init__(value=value)

    def copy(self: SignalInteger) -> SignalInteger:
        """Copy the BaseSignalClass object.

        Method to copy the class object.

        """
        return SignalInteger(self._value)

    @property
    def value(self: SignalInteger) -> np.int64:
        return self._value

    @value.setter
    def value(self: SignalInteger, value: np.int64) -> None:
        self._value = value


class SignalFloat(BaseSignalClass):
    """Signal class.

    The signal class is derived from the BaseSignalClass and defines a certain
    data type for the value of the signal.

    """

    def __init__(self: SignalFloat, value: np.float64) -> None:
        """Initialize class.

        Init function of the class.

        """
        super().__init__(value=value)

    def copy(self: SignalFloat) -> SignalFloat:
        """Copy the BaseSignalClass object.

        Method to copy the class object.

        """
        return SignalFloat(self._value)

    @property
    def value(self: SignalFloat) -> np.float64:
        return self._value

    @value.setter
    def value(self: SignalFloat, value: np.float64) -> None:
        self._value = value


class SignalComplex(BaseSignalClass):
    """Signal class.

    The signal class is derived from the BaseSignalClass and defines a certain
    data type for the value of the signal.

    """

    def __init__(self: SignalComplex, value: np.complex128) -> None:
        """Initialize class.

        Init function of the class.

        """
        super().__init__(value=value)

    def copy(self: SignalComplex) -> SignalComplex:
        """Copy the BaseSignalClass object.

        Method to copy the class object.

        """
        return SignalComplex(self._value)

    @property
    def value(self: SignalComplex) -> np.complex128:
        return self._value

    @value.setter
    def value(self: SignalComplex, value: np.complex128) -> None:
        self._value = value


if __name__ == "__main__":
    logger.info("This is the core file of the thermd library.")

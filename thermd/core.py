# -*- coding: utf-8 -*-

"""Core library of thermd.

Library of 1-dimensional (modelica-like) models. Core file with the API of the library.

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Dict, Type, Union  # , Union, Dict, Tuple, Type, TypeVar

from matplotlib import pyplot as plt
import networkx as nx
import numpy as np

# from CoolProp.CoolProp import AbstractState

from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)

# Enums
class NodeTypes(Enum):
    MODEL = auto()
    BLOCK = auto()
    PORT = auto()


class PortFunctionTypes(Enum):
    INLET = auto()
    OUTLET = auto()


# Result classes
class BaseResultClass(ABC):
    ...


@dataclass
class SystemResult(BaseResultClass):
    states: List[BaseStateClass]
    success: bool
    status: np.int8
    message: str
    nit: np.int16

    @classmethod
    def from_success(
        cls: Type[SystemResult], states: List[BaseStateClass], nit: np.int16
    ) -> SystemResult:
        return cls(
            states=states,
            success=True,
            status=np.int8(0),
            message="Solver finished successfully.",
            nit=nit,
        )

    @classmethod
    def from_error(
        cls: Type[SystemResult], states: List[BaseStateClass], nit: np.int16
    ) -> SystemResult:
        return cls(
            states=states,
            success=False,
            status=np.int8(-1),
            message="Solver didn't finish successfully.",
            nit=nit,
        )

    @classmethod
    def from_convergence(
        cls: Type[SystemResult], states: List[BaseStateClass], nit: np.int16
    ) -> SystemResult:
        return cls(
            states=states,
            success=False,
            status=np.int8(1),
            message="Solver didn't converge successfully.",
            nit=nit,
        )


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
        self.__stop_criterion_energy: Union[np.float64, None] = None
        self.__stop_criterion_momentum: Union[np.float64, None] = None
        self.__stop_criterion_mass: Union[np.float64, None] = None

        if "stop_criterion_energy" in kwargs:
            self.__stop_criterion_energy = kwargs["stop_criterion_energy"]
        if "stop_criterion_momentum" in kwargs:
            self.__stop_criterion_momentum = kwargs["stop_criterion_momentum"]
        if "stop_criterion_mass" in kwargs:
            self.__stop_criterion_mass = kwargs["stop_criterion_mass"]

        # Initialize index lists of models, blocks, ports, states and signals
        self.__models: List[str] = list()
        self.__blocks: List[str] = list()
        self.__ports: List[str] = list()

        # Initialize main graph
        self.__network = nx.DiGraph()

    # @classmethod
    # def from_file(cls: Type[BaseSystemClass], filename: str) -> BaseSystemClass:
    #     return

    # def to_file(self: BaseSystemClass, filename: str):
    #     return

    # @property
    # def network(self):
    #     return self.__network

    # def add_model(self: BaseSystemClass, name: str, dclass: BaseModelClass):
    #     self.__network.add_node(name, dclass=dclass)

    # def add_block(self: BaseSystemClass, name: str, dclass: BaseBlockClass):
    #     self.__network.add_node(name, dclass=dclass)

    # def add_connector(
    #     self: BaseSystemClass, name1: str, name2: str, dclass: BaseConnectorClass,
    # ):
    #     self.__network.add_edge(name1, name2, dclass=dclass)

    # def add_models_from(
    #     self: BaseSystemClass, models: List[Tuple[str, BaseModelClass]],
    # ):
    #     self.__network.add_nodes_from(
    #         [(models[i][0], {"dclass": models[i][1]}) for i in range(0, len(models))]
    #     )

    # def add_blocks_from(
    #     self: BaseSystemClass, blocks: List[Tuple[str, BaseModelClass]],
    # ):
    #     self.__network.add_nodes_from(
    #         [(blocks[i][0], {"dclass": blocks[i][1]}) for i in range(0, len(blocks))]
    #     )

    # def add_connectors_from(
    #     self: BaseSystemClass, connectors: List[Tuple[str, str, BaseConnectorClass]],
    # ):
    #     self.__network.add_nodes_from(
    #         [
    #             (connectors[i][0], connectors[i][1], {"dclass": connectors[i][2]})
    #             for i in range(0, len(connectors))
    #         ]
    #     )

    # def remove_model(self: BaseSystemClass, name: str):
    #     self.__network.remove_node(name)

    # def remove_block(self: BaseSystemClass, name: str):
    #     self.__network.remove_node(name)

    # def remove_connector(
    #     self: BaseSystemClass, name1: str, name2: str,
    # ):
    #     self.__network.remove_edge(name1, name2)

    # def remove_models_from(
    #     self: BaseSystemClass, models: List[str],
    # ):
    #     self.__network.remove_nodes_from(models)

    # def remove_blocks_from(
    #     self: BaseSystemClass, blocks: List[str],
    # ):
    #     self.__network.remove_nodes_from(blocks)

    # def remove_connectors_from(
    #     self: BaseSystemClass, connectors: List[Tuple[str, str]],
    # ):
    #     self.__network.remove_edges_from(connectors)

    # def set_model_attributes(self: BaseSystemClass, name: str, dclass: BaseModelClass):
    #     nx.set_node_attributes(self.__network, {name: {"dclass": dclass}})

    # def set_block_attributes(self: BaseSystemClass, name: str, dclass: BaseBlockClass):
    #     nx.set_node_attributes(self.__network, {name: {"dclass": dclass}})

    # def set_connector_attributes(
    #     self: BaseSystemClass, name1: str, name2: str, dclass: BaseConnectorClass,
    # ):
    #     nx.set_edge_attributes(self.__network, {(name1, name2): {"dclass": dclass}})

    # def set_model_attributes_from(
    #     self: BaseSystemClass, models: List[Tuple[str, BaseModelClass]],
    # ):
    #     nx.set_node_attributes(
    #         self.__network,
    #         {models[i][0]: {"dclass": models[i][1]} for i in range(0, len(models))},
    #     )

    # def set_block_attributes_from(
    #     self: BaseSystemClass, blocks: List[Tuple[str, BaseBlockClass]],
    # ):
    #     nx.set_node_attributes(
    #         self.__network,
    #         {blocks[i][0]: {"dclass": blocks[i][1]} for i in range(0, len(blocks))},
    #     )

    # def set_connector_attributes_from(
    #     self: BaseSystemClass, connectors: List[Tuple[str, str, BaseConnectorClass]],
    # ):
    #     nx.set_edge_attributes(
    #         self.__network,
    #         {
    #             (connectors[i][0], connectors[i][1]): {"dclass": connectors[i][2]}
    #             for i in range(0, len(connectors))
    #         },
    #     )

    # def get_model_attributes(self: BaseSystemClass, name: str) -> BaseModelClass:
    #     return self.__network[name]["dclass"]

    # def get_block_attributes(self: BaseSystemClass, name: str) -> BaseBlockClass:
    #     return self.__network[name]["dclass"]

    # def get_connector_attributes(
    #     self: BaseSystemClass, name1: str, name2: str,
    # ) -> BaseConnectorClass:
    #     return self.__network[name1][name2]["dclass"]

    # def get_model_attributes_from(
    #     self: BaseSystemClass, models: List[str],
    # ) -> List[Tuple[str, BaseModelClass]]:
    #     return [
    #         (models[i], self.__network[models[i]]["dclass"])
    #         for i in range(0, len(models))
    #     ]

    # def get_block_attributes_from(
    #     self: BaseSystemClass, blocks: List[str],
    # ) -> List[Tuple[str, BaseBlockClass]]:
    #     return [
    #         (blocks[i], self.__network[blocks[i]]["dclass"])
    #         for i in range(0, len(blocks))
    #     ]

    # def get_connector_attributes_from(
    #     self: BaseSystemClass, connectors: List[Tuple[str, str]],
    # ) -> List[Tuple[str, str, BaseConnectorClass]]:
    #     return [
    #         (
    #             connectors[i][0],
    #             connectors[i][1],
    #             self.__network[connectors[i][0]][connectors[i][1]]["dclass"],
    #         )
    #         for i in range(0, len(connectors))
    #     ]

    def clear(self: BaseSystemClass):
        self.__network.clear()

    def freeze(self: BaseSystemClass):
        self.__network.freeze()

    def is_frozen(self: BaseSystemClass):
        self.__network.is_frozen()

    def add_model(
        self: BaseSystemClass, node_class: BaseModelClass,
    ):

        logger.info("Add model: %s", node_class.name)

        if node_class.name in self.__blocks:
            logger.error("Model name already in use: %s", node_class.name)

        self.__network.add_node(
            node_class.name, node_type=NodeTypes.MODEL, node_class=node_class
        )
        self.__models.append(node_class.name)

        for port in node_class.ports:

            logger.info("Add port: %s", port.name)

            self.__network.add_node(port.name, node_type=NodeTypes.PORT)
            self.__ports.append(port.name)

            if port.port_function == PortFunctionTypes.INLET:
                self.__network.add_edge(port.name, node_class.name)
            elif port.port_function == PortFunctionTypes.OUTLET:
                self.__network.add_edge(node_class.name, port.name)
            else:
                logger.error("Wrong port function: %s", port.port_function)
                raise SystemExit

    def add_block(
        self: BaseSystemClass, node_class: BaseBlockClass,
    ):

        logger.info("Add block: %s", node_class.name)

        if node_class.name in self.__blocks:
            logger.error("Block name already in use: %s", node_class.name)

        self.__network.add_node(
            node_class.name, node_type=NodeTypes.BLOCK, node_class=node_class
        )
        self.__blocks.append(node_class.name)

        for port in node_class.ports:

            logger.info("Add port: %s", port.name)

            self.__network.add_node(port.name, node_type=NodeTypes.PORT)
            self.__ports.append(port.name)

            if port.port_function == PortFunctionTypes.INLET:
                self.__network.add_edge(port.name, node_class.name)
            elif port.port_function == PortFunctionTypes.OUTLET:
                self.__network.add_edge(node_class.name, port.name)
            else:
                logger.error("Wrong port function: %s", port.port_function)
                raise SystemExit

    def connect(
        self: BaseSystemClass, port1: BasePortClass, port2: BasePortClass,
    ):
        if port1.__class__.__name__ == port2.__class__.__name__:

            self.__network.add_edge(port1.name, port2.name)

        else:
            logger.error("Port types not compatible: %s <-> %s", port1.name, port2.name)
            raise SystemExit

    # def get_inlet_connector(
    #     self: BaseSystemClass, port_name: str
    # ) -> Union[BaseStateClass, BaseSignalClass]:
    #     connector = None
    #     for connector_node in self.__network.predecessors(port_name):
    #         connector = connector_node["node_class"]

    #     if connector is None:
    #         logger.error(
    #             "Port %s does not have a predecessor connector node!", port_name
    #         )
    #         raise SystemExit

    #     return connector

    # def get_outlet_connector(
    #     self: BaseSystemClass, port_name: str
    # ) -> Union[BaseStateClass, BaseSignalClass]:
    #     connector = None
    #     for connector_node in self.__network.successors(port_name):
    #         connector = connector_node["node_class"]

    #     if connector is None:
    #         logger.error("Port %s does not have a successor connector node!", port_name)
    #         raise SystemExit

    #     return connector

    def check(self: BaseSystemClass):
        # Check all models
        for model in self.__models:
            if not self.__network[model]["node_class"].check():
                logger.error("Model %s shows an error.", model)

        # Check all blocks
        for block in self.__blocks:
            if not self.__network[block]["node_class"].check():
                logger.error("Block %s shows an error.", block)

    def plot_graph(self: BaseSystemClass, path: Path):
        nx.draw(self.__network, with_labels=True)
        plt.savefig(path)

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
        self.__name = name

        # Balances
        self.__energy_balance = np.float64(0.0)
        self.__momentum_balance = np.float64(0.0)
        self.__mass_balance = np.float64(0.0)

    @property
    def name(self: BaseModelClass) -> str:
        return self.__name

    @property
    @abstractmethod
    def ports(self: BaseModelClass) -> List[BasePortClass]:
        ...

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

    @abstractmethod
    def check(self: BaseModelClass) -> bool:
        ...

    @abstractmethod
    def set_port_state(
        self: BaseModelClass, port_name: str, state: BaseStateClass,
    ) -> None:
        ...

    @abstractmethod
    def set_port_signal(
        self: BaseModelClass, port_name: str, signal: BaseSignalClass,
    ) -> None:
        ...

    @abstractmethod
    def get_port_state(self: BaseModelClass, port_name: str,) -> BaseStateClass:
        ...

    @abstractmethod
    def get_port_signal(self: BaseModelClass, port_name: str,) -> BaseSignalClass:
        ...

    @abstractmethod
    def get_results(self: BaseModelClass) -> BaseResultClass:
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
        self.__name = name

    @property
    def name(self: BaseBlockClass) -> str:
        return self.__name

    @property
    @abstractmethod
    def ports(self: BaseBlockClass) -> List[BasePortClass]:
        ...

    @property
    @abstractmethod
    def stop_criterion_energy(self: BaseBlockClass) -> np.float64:
        ...

    @property
    @abstractmethod
    def stop_criterion_momentum(self: BaseBlockClass) -> np.float64:
        ...

    @property
    @abstractmethod
    def stop_criterion_mass(self: BaseBlockClass) -> np.float64:
        ...

    @abstractmethod
    def check(self: BaseBlockClass) -> bool:
        ...

    @abstractmethod
    def set_port_signal(
        self: BaseBlockClass, port_name: str, signal: BaseSignalClass,
    ) -> None:
        ...

    @abstractmethod
    def get_port_signal(self: BaseBlockClass, port_name: str,) -> BaseSignalClass:
        ...

    @abstractmethod
    def get_results(self: BaseBlockClass) -> BaseResultClass:
        ...

    @abstractmethod
    def equation(self: BaseBlockClass):
        ...


class BasePortClass(ABC):
    """Base class of the ports.

    The abstract base class of the ports.

    """

    def __init__(self: BasePortClass, name: str, port_function: PortFunctionTypes):
        """Initialize base port class.

        Init function of the base port class.

        """
        # Class properties
        self.__name = name
        self.__port_function = port_function

    @property
    def name(self: BasePortClass) -> str:
        return self.__name

    @property
    def port_function(self: BasePortClass) -> PortFunctionTypes:
        return self.__port_function

    @abstractmethod
    def check(self: BasePortClass) -> bool:
        ...


class BaseStateClass(ABC):
    """Base class of the states.

    The abstract base class of the states provides the API for all derived
    state classes. States are one type of connectors between models or blocks.

    """

    def __init__(self: BaseStateClass, name: str):
        """Initialize base state class.

        Init function of the base state class.

        """
        # Class properties
        self.__name = name

    @property
    def name(self: BaseStateClass) -> str:
        return self.__name

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


class BaseSignalClass(ABC):
    """Base class of the signals.

    The abstract base class of the signals provides the API for all derived
    signal classes. Signals are one type of connectors between models or blocks.

    """

    def __init__(self: BaseSignalClass, name: str):
        """Initialize base signal class.

        Init function of the base signal class.

        """
        # Class properties
        self.__name = name

    @property
    def name(self: BaseSignalClass) -> str:
        return self.__name


# System classes
class SystemSimpleIterative(BaseSystemClass):
    """Class of a simple system.

    The simple system is the main starting point for all physical systems and
    represents an exemplary system class, which can be modified further.

    """

    # def __init__(self, **kwargs):
    #     """Initialize simple system class.

    #     Init function of the simple system class.

    #     """
    #     super().__init__(**kwargs)

    def stop_criterion(self: BaseSystemClass) -> bool:
        ...

    def solve(self: BaseSystemClass):
        ...


# Port classes
class PortState(BasePortClass):
    """Class of a state port.

    The state port is a interface in a model and can connect different
    models with a fluid connection, which links the thermodynamic states.

    """

    def __init__(
        self: PortState,
        name: str,
        port_function: PortFunctionTypes,
        state: BaseStateClass,
    ):
        """Initialize base port class.

        Init function of the base port class.

        """
        super().__init__(name=name, port_function=port_function)

        # Class properties
        self.__state = state

    @property
    def state(self: PortState) -> BaseStateClass:
        return self.__state

    @state.setter
    def state(self: PortState, state: BaseStateClass) -> None:
        self.__state = state

    def check(self: PortState) -> bool:
        ...


class PortSignal(BasePortClass):
    """Class of a signal port.

    The signal port is a interface in a model and can connect different
    models with a signal connection, which links values. 

    """

    def __init__(
        self: PortSignal,
        name: str,
        port_function: PortFunctionTypes,
        signal: BaseSignalClass,
    ):
        """Initialize base port class.

        Init function of the base port class.

        """
        super().__init__(name=name, port_function=port_function)

        # Class properties
        self.__signal = signal

    @property
    def signal(self: PortSignal) -> BaseSignalClass:
        return self.__signal

    @signal.setter
    def signal(self: PortSignal, signal: BaseSignalClass) -> None:
        self.__signal = signal

    def check(self: PortSignal) -> bool:
        ...


# State/ media classes
class MediumPure(BaseStateClass):
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


class MediumBinaryMixture(BaseStateClass):
    """Class of binary mixtures media.

    The medium class of binary mixtures provides the API for all derived
    medium classes with two pure or pseudo-pure but uneven components (e. g. humid air),
    hence three state values need to be given to define the state.

    """

    @property
    @abstractmethod
    def w(self: BaseStateClass) -> np.float64:
        """Humidity ratio.

        Returns:
            np.float64: Humidity ratio

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


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("This is the core file of the thermd library.")

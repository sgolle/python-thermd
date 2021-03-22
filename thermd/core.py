# -*- coding: utf-8 -*-

"""Core library of thermd.

Library of 1-dimensional (modelica-like) models. Core file with the API of the library.

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Tuple, Dict, Union  # , Type, TypeVar

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
    STATE = auto()
    SIGNAL = auto()


class PortFunctions(Enum):
    INLET = auto()
    OUTLET = auto()


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
        # Model parameter
        if "keyname" in kwargs:
            # TODO
            pass

        # Initialize index lists of models, blocks, ports, states and signals
        self.__models: List[str] = list()
        self.__blocks: List[str] = list()
        self.__ports: List[str] = list()
        self.__states: List[str] = list()
        self.__signals: List[str] = list()

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

    def add_model(self: BaseSystemClass, node_class: BaseModelClass):

        logger.info("Add model: %s", node_class.name)

        if node_class.name in self.__blocks:
            logger.error("Model name already in use: %s", node_class.name)

        self.__network.add_node(
            node_class.name, node_type=NodeTypes.MODEL, node_class=node_class
        )
        self.__models.append(node_class.name)

        for port in node_class.ports:

            logger.info("Add port: %s", port.name)

            self.__network.add_node(
                port.name, node_type=NodeTypes.PORT, node_class=port
            )
            self.__ports.append(port.name)

            if port.port_function == PortFunctions.INLET:
                self.__network.add_edge(port.name, node_class.name)
            elif port.port_function == PortFunctions.OUTLET:
                self.__network.add_edge(node_class.name, port.name)
            else:
                logger.error("Wrong port function: %s", port.port_function)
                raise SystemExit

    def add_block(self: BaseSystemClass, node_class: BaseBlockClass):

        logger.info("Add block: %s", node_class.name)

        if node_class.name in self.__blocks:
            logger.error("Block name already in use: %s", node_class.name)

        self.__network.add_node(
            node_class.name, node_type=NodeTypes.BLOCK, node_class=node_class
        )
        self.__blocks.append(node_class.name)

        for port in node_class.ports:

            logger.info("Add port: %s", port.name)

            self.__network.add_node(
                port.name, node_type=NodeTypes.PORT, node_class=port
            )
            self.__ports.append(port.name)

            if port.port_function == PortFunctions.INLET:
                self.__network.add_edge(port.name, node_class.name)
            elif port.port_function == PortFunctions.OUTLET:
                self.__network.add_edge(node_class.name, port.name)
            else:
                logger.error("Wrong port function: %s", port.port_function)
                raise SystemExit

    def connect(
        self: BaseSystemClass,
        port1: BasePortClass,
        port2: BasePortClass,
        connector: Union[BaseStateClass, BaseSignalClass],
    ):
        if port1.__class__.__name__ == port2.__class__.__name__:

            if isinstance(port1, PortState):
                self.__network.add_node(
                    connector.name, node_type=NodeTypes.STATE, node_class=connector
                )

                self.__network.add_edge(port1.name, connector.name)
                self.__network.add_edge(connector.name, port2.name)
                self.__states.append(connector.name)

            elif isinstance(port1, PortSignal):
                self.__network.add_node(
                    connector.name, node_type=NodeTypes.SIGNAL, node_class=connector
                )

                self.__network.add_edge(port1.name, connector.name)
                self.__network.add_edge(connector.name, port2.name)
                self.__signals.append(connector.name)

            else:
                logger.error("Wrong port type: %s ", port1.__class__.__name__)
                raise SystemExit
        else:
            logger.error("Port types not compatible: %s <-> %s", port1.name, port2.name)
            raise SystemExit

    def get_inlet_connector(
        self: BaseSystemClass, port_name: str
    ) -> Union[BaseStateClass, BaseSignalClass]:
        connector = None
        for connector_node in self.__network.predecessors(port_name):
            connector = connector_node["node_class"]

        if connector is None:
            logger.error(
                "Port %s does not have a predecessor connector node!", port_name
            )
            raise SystemExit

        return connector

    def get_outlet_connector(
        self: BaseSystemClass, port_name: str
    ) -> Union[BaseStateClass, BaseSignalClass]:
        connector = None
        for connector_node in self.__network.successors(port_name):
            connector = connector_node["node_class"]

        if connector is None:
            logger.error("Port %s does not have a successor connector node!", port_name)
            raise SystemExit

        return connector

    def check(self: BaseSystemClass):
        # Check all models
        for model in self.__models:
            self.__network[model]["node_class"].check()

        # Check all blocks
        for block in self.__blocks:
            self.__network[block]["node_class"].check()

        # Check all ports
        for port in self.__ports:
            self.__network[port]["node_class"].check()

        # Check all states
        for state in self.__states:
            self.__network[state]["node_class"].check()

        # Check all signals
        for signal in self.__signals:
            self.__network[signal]["node_class"].check()

    # def plot_graph(self: BaseSystemClass):
    #     ...

    @abstractmethod
    def solve(self: BaseSystemClass):
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

    @property
    def name(self: BaseModelClass) -> str:
        return self.__name

    @property
    @abstractmethod
    def ports(self: BaseModelClass) -> List[BasePortClass]:
        ...

    @abstractmethod
    def check(self: BaseModelClass) -> bool:
        ...

    @abstractmethod
    def equation(self: BaseModelClass) -> BaseStateClass:
        ...


class BaseBlockClass(ABC):
    """Base class of the mathematical block.

    The abstract base class of the mathematical block describes the API of every
    derived mathematical blocks.

    """

    def __init__(self: BaseBlockClass, name: str, ports: List[BasePortClass]):
        """Initialize base block class.

        Init function of the base block class.

        """
        # Class properties
        self.__name = name
        self.__ports = ports

    @property
    def name(self: BaseBlockClass) -> str:
        return self.__name

    @property
    def ports(self: BaseBlockClass) -> List[BasePortClass]:
        return self.__ports

    @abstractmethod
    def check(self: BaseBlockClass):
        ...

    @abstractmethod
    def equation(self: BaseBlockClass) -> BaseSignalClass:
        ...


class BasePortClass(ABC):
    """Base class of the ports.

    The abstract base class of the ports.

    """

    def __init__(self: BasePortClass, name: str, port_function: PortFunctions):
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
    def port_function(self: BasePortClass) -> PortFunctions:
        return self.__port_function

    @abstractmethod
    def check(self: BasePortClass):
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
    def cp(self: BaseStateClass) -> np.float64:
        """Specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        ...

    @property
    @abstractmethod
    def cv(self: BaseStateClass) -> np.float64:
        """Specific heat at constant volume in J/kg/K.

        Returns:
            np.float64: Specific heat at constant volume in J/kg/K

        """
        ...

    @property
    @abstractmethod
    def h(self: BaseStateClass) -> np.float64:
        """Mass-specific enthalpy in J/kg.

        Returns:
            np.float64: Mass-specific enthalpy in J/kg

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
    def density(self: BaseStateClass) -> np.float64:
        """Density in kg/m**3.

        Returns:
            np.float64: Density in kg/m**3

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
    def s(self: BaseStateClass) -> np.float64:
        """Mass-specific entropy in J/kg/K.

        Returns:
            np.float64: Mass-specific entropy in J/kg/K

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
    def v(self: BaseStateClass) -> np.float64:
        """Specific volume in m**3/kg.

        Returns:
            np.float64: Specific volume in m**3/kg

        """
        ...

    @property
    @abstractmethod
    def x(self: BaseStateClass) -> np.float64:
        """Quality.

        Returns:
            np.float64: Quality

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

    @abstractmethod
    def check(self: BaseStateClass):
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

    @abstractmethod
    def check(self: BaseSignalClass):
        ...


# System classes
class SystemSimple(BaseSystemClass):
    """Class of a simple system.

    The simple system is the main starting point for all physical systems and
    represents an exemplary system class, which can be modified further.

    """

    # def __init__(self, **kwargs):
    #     """Initialize simple system class.

    #     Init function of the simple system class.

    #     """
    #     super().__init__(**kwargs)

    def solve(self: BaseSystemClass):
        ...


# Port classes
class PortState(BasePortClass):
    """Class of a state port.

    The state port is a interface in a model and can connect different
    models with a fluid connection, which links the thermodynamic states.

    """

    def check(self: PortState):
        ...


class PortSignal(BasePortClass):
    """Class of a signal port.

    The signal port is a interface in a model and can connect different
    models with a signal connection, which links values. 

    """

    def check(self: PortSignal):
        ...


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("This is the core file of the thermd library.")

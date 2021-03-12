# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple, Type, TypeVar

# import math
import networkx as nx
import numpy as np

from CoolProp.CoolProp import AbstractState

from thermn.convection import *
from thermn.helper import get_logger
from thermn.material import *
from thermn.solver import *

# Initialize global logger
logger = get_logger(__name__)

# Custom type declarations
BasePackageClassType = TypeVar("BasePackageClassType", bound="BasePackageClass")
BaseSystemClassType = TypeVar("BaseSystemClassType", bound="BaseSystemClass")
BaseModelClassType = TypeVar("BaseModelClassType", bound="BaseModelClass")
BaseBlockClassType = TypeVar("BaseBlockClassType", bound="BaseBlockClass")
BaseConnectorClassType = TypeVar("BaseConnectorClassType", bound="BaseConnectorClass")


# Base classes
class BasePackageClass(ABC):
    """TODO:Docstring.
    
    Arguments:
        BasePackageClass {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    ...


class BaseSystemClass(ABC):
    """Base class of the physical system.

    The abstract base class of the physical system describes the API of every
    derived physical system. Physical systems are the main classes of the library,
    which combines all components (models, blocks, connectors, etc.), as well as
    all methods to prepare, solve and illustrate the system.

    """

    def __init__(self, **kwargs):
        # Model parameter
        if "keyname" in kwargs:
            # TODO
            pass

        # Initialize main thermal network as networkx graph
        self.__network = nx.MultiDiGraph()

    def __add__(
        self: BaseThermalModel, other_thermal_model: BaseThermalModel
    ) -> BaseThermalModel:
        self.__network = nx.compose(self.network, other_thermal_model.network)
        return self

    def __sub__(
        self: BaseThermalModel, other_thermal_model: BaseThermalModel
    ) -> BaseThermalModel:
        self.remove_nodes_from(nodes=list(other_thermal_model.network.nodes))
        return self

    @property
    def network(self):
        return self.__network

    def add_node(self: BaseThermalModel, name: np.uint32, dclass: BaseNodeClass):
        self.__network.add_node(name, dclass=dclass)

    def add_conductor(
        self: BaseThermalModel,
        name1: np.uint32,
        name2: np.uint32,
        dclass: BaseConductorClass,
    ):
        self.__network.add_edge(name1, name2, dclass=dclass)

    def add_nodes_from(
        self: BaseThermalModel, nodes: List[Tuple[np.uint32, BaseNodeClass]],
    ):
        self.__network.add_nodes_from(
            [(nodes[i][0], {"dclass": nodes[i][1]}) for i in range(0, len(nodes))]
        )

    def add_conductors_from(
        self: BaseThermalModel,
        conductors: List[Tuple[np.uint32, np.uint32, BaseConductorClass]],
    ):
        self.__network.add_nodes_from(
            [
                (conductors[i][0], conductors[i][1], {"dclass": conductors[i][2]})
                for i in range(0, len(conductors))
            ]
        )

    def remove_node(self: BaseThermalModel, name: np.uint32):
        self.__network.remove_node(name)

    def remove_conductor(
        self: BaseThermalModel, name1: np.uint32, name2: np.uint32,
    ):
        self.__network.remove_edge(name1, name2)

    def remove_nodes_from(
        self: BaseThermalModel, nodes: List[np.uint32],
    ):
        self.__network.remove_nodes_from(nodes)

    def remove_conductors_from(
        self: BaseThermalModel, conductors: List[Tuple[np.uint32, np.uint32]],
    ):
        self.__network.remove_edges_from(conductors)

    def set_node_attributes(
        self: BaseThermalModel, name: np.uint32, dclass: BaseNodeClass
    ):
        nx.set_node_attributes(self.__network, {name: {"dclass": dclass}})

    def set_conductor_attributes(
        self: BaseThermalModel,
        name1: np.uint32,
        name2: np.uint32,
        dclass: BaseConductorClass,
    ):
        nx.set_edge_attributes(self.__network, {(name1, name2): {"dclass": dclass}})

    def set_node_attributes_from(
        self: BaseThermalModel, nodes: List[Tuple[np.uint32, BaseNodeClass]],
    ):
        nx.set_node_attributes(
            self.__network,
            {nodes[i][0]: {"dclass": nodes[i][1]} for i in range(0, len(nodes))},
        )

    def set_conductor_attributes_from(
        self: BaseThermalModel,
        conductors: List[Tuple[np.uint32, np.uint32, BaseConductorClass]],
    ):
        nx.set_edge_attributes(
            self.__network,
            {
                (conductors[i][0], conductors[i][1]): {"dclass": conductors[i][2]}
                for i in range(0, len(conductors))
            },
        )

    def get_node_attributes(self: BaseThermalModel, name: np.uint32) -> BaseNodeClass:
        return self.__network[name]["dclass"]

    def get_conductor_attributes(
        self: BaseThermalModel, name1: np.uint32, name2: np.uint32,
    ) -> BaseConductorClass:
        return self.__network[name1][name2]["dclass"]

    def get_node_attributes_from(
        self: BaseThermalModel, nodes: List[np.uint32],
    ) -> List[Tuple[np.uint32, BaseNodeClass]]:
        return [
            (nodes[i], self.__network[nodes[i]]["dclass"]) for i in range(0, len(nodes))
        ]

    def get_conductor_attributes_from(
        self: BaseThermalModel, conductors: List[Tuple[np.uint32, np.uint32]],
    ) -> List[Tuple[np.uint32, np.uint32, BaseConductorClass]]:
        return [
            (
                conductors[i][0],
                conductors[i][1],
                self.__network[conductors[i][0]][conductors[i][1]]["dclass"],
            )
            for i in range(0, len(conductors))
        ]

    def clear(self: BaseThermalModel):
        self.__network.clear()

    def freeze(self: BaseThermalModel):
        self.__network.freeze()

    def is_frozen(self: BaseThermalModel):
        self.__network.is_frozen()

    # def write_file(self: Type[BaseThermalModel], filename: str):
    #     return

    # def read_file(self: BaseThermalModel, filename: str):
    #     return

    @abstractmethod
    def pre_cond(self: BaseThermalModel):
        ...

    @abstractmethod
    def solve(self: BaseThermalModel):
        ...


class BaseModelClass(ABC):
    """TODO:Docstring.
    
    Arguments:
        BaseModelClass {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    ...


class BaseBlockClass(ABC):
    """TODO:Docstring.
    
    Arguments:
        BaseBlockClass {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    ...


class BaseConnectorClass(ABC):
    """TODO:Docstring.
    
    Arguments:
        BaseConnectorClass {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    ...


# Model Class


if __name__ == "__main__":
    print("Not implemented.")

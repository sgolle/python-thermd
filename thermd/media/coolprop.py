# -*- coding: utf-8 -*-

"""CoolProp media model library.

The CoolProp media model library provides interfaces to calculations of
equations of state and transport properties with the CoolProp and
CoolProp HumidAir library.

"""

from __future__ import annotations
from enum import Enum
from typing import Type

from CoolProp import AbstractState, CoolProp
from CoolProp.HumidAirProp import HAPropsSI
import numpy as np
from thermd.core import BaseStateClass
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)

# Enums
class CoolPropBackends(Enum):
    HEOS = "HEOS"
    REFPROP = "REFPROP"
    INCOMP = "INCOMP"
    TTSE_HEOS = "TTSE&HEOS"
    TTSE_REFPROP = "TTSE&REFPROP"
    BICUBIC_HEOS = "BICUBIC&HEOS"
    BICUBIC_REFPROP = "BICUBIC&REFPROP"
    IF97 = "IF97"
    TREND = "TREND"
    SRK = "SRK"
    PR = "PR"
    VTPR = "VTPR"
    PCSAFT = "PCSAFT"


class CoolPropPhases(Enum):
    LIQUID = "liquid"
    SUPERCRITICAL = "supercritical"
    SUPERCRITICAL_GAS = "supercritical_gas"
    SUPERCRITICAL_LIQUID = "supercritical_liquid"
    CRITICAL_POINT = "critical_point"
    GAS = "gas"
    TWOPHASE = "twophase"
    UNKNOWN = "unknown"
    NOT_IMPOSED = "not_imposed"


class CoolPropPureFluids(Enum):
    BUTENE = "1-Butene"
    ACETONE = "Aceton"
    AIR = "Air"
    AMMONIA = "Ammonia"
    ARGON = "Argon"
    BENZENE = "Benzene"
    CARBONDIOXIDE = "CarbonDioxide"
    CARBONMONOXIDE = "CarbonMonoxide"
    CARBONYLSULFIDE = "CarbonylSulfide"
    CYCLOHEXANE = "CycloHexane"
    CYCLOPROPANE = "CycloPropane"
    CYCLOPENTANE = "Cyclopentane"
    D4 = "D4"
    D5 = "D5"
    D6 = "D6"
    DEUTERIUM = "Deuterium"
    DICHLORETHANE = "Dichloroethane"
    DIETHYLETHER = "DiethylEther"
    DIMETHYLCARBONATE = "DimethylCarbonate"
    DIMETHYLETHER = "DimethylEther"
    ETHANE = "Ethane"
    ETHANOL = "Ethanol"
    ETHYLBENZENE = "EthylBenzene"
    ETHYLENE = "Ethylene"
    ETHYLENEOXIDE = "EthyleneOxide"
    FLUORINE = "Fluorine"
    HFE143m = "HFE144m"
    HEAVYWATER = "HeavyWater"
    HELIUM = "Helium"
    HYDROGEN = "Hydrogen"
    HYDROGENCHLORIDE = "HydrogenChloride"
    HYDROGENSULFIDE = "HydrogenSulfide"
    ISOBUTANE = "IsoButane"
    ISOBUTENE = "IsoButene"
    ISOHEXANE = "Isohexane"
    ISOPENTANE = "Isopentane"
    KRYPTON = "Krypton"
    MD2M = "MD2M"
    MD3M = "MD3M"
    MD4M = "MD4M"
    MDM = "MDM"
    MM = "MM"
    METHANE = "Methane"
    METHANOL = "Methanol"
    METHYLLINOLEATE = "MethylLinoleate"
    METHYLLINOLENATE = "MethylLinolenate"
    METHYLOLEATE = "MethylOleate"
    METHYLPALMITATE = "MethylPalmitate"
    METHYLSTEARATE = "MethylStearate"
    NEON = "Neon"
    NEOPENTANE = "Neopentane"
    NITROGEN = "Nitrogen"
    NITROUSOXIDE = "NitrousOxide"
    NOVEC649 = "Novec649"
    ORTHODEUTERIUM = "OrthoDeuterium"
    ORTHOHYDROGEN = "OrthoHydrogen"
    OXYGEN = "Oxygen"
    PARADEUTERIUM = "ParaDeuterium"
    PARAHYDROGEN = "ParaHydrogen"
    PROPYLENE = "Propylene"
    PROPYNE = "Propyne"
    R11 = "R11"
    R113 = "R113"
    R114 = "R114"
    R115 = "R115"
    R116 = "R116"
    R12 = "R12"
    R123 = "R123"
    R1233ZD_E = "R1233zd(E)"
    R1234YF = "R1234yf"
    R1234ZE_E = "R1234ze(E)"
    R1234ZE_Z = "R1234ze(Z)"
    R124 = "R124"
    R1234ZF = "R1243zf"
    R125 = "R125"
    R13 = "R13"
    R134a = "R134a"
    R13I1 = "R13I1"
    R14 = "R14"
    R141B = "R141b"
    R142B = "R142b"
    R143A = "R143a"
    R152A = "R152A"
    R161 = "R161"
    R21 = "R21"
    R218 = "R218"
    R22 = "R22"
    R227EA = "R227EA"
    R23 = "R23"
    R236EA = "R236EA"
    R236FA = "R236FA"
    R245CA = "R245ca"
    R245FA = "R245fa"
    R32 = "R32"
    R365MFC = "R365MFC"
    R40 = "R40"
    R404A = "R404A"
    R407C = "R407C"
    R41 = "R41"
    R410A = "R410A"
    R507A = "R507A"
    RC318 = "RC318"
    SES36 = "SES36"
    SULFURDIOXIDE = "SulfurDioxide"
    SULFURHEXAFLUORIDE = "SulfurHexafluoride"
    TOLUENE = "Toluene"
    WATER = "Water"
    XENON = "Xenon"
    CIS_2_BUTENE = "cis-2-Butene"
    M_XYLENE = "m-Xylene"
    N_BUTANE = "n-Butane"
    N_DECANE = "n-Decane"
    N_DODECANE = "n-Dodecane"
    N_HEPTANE = "n-Heptane"
    N_HEXANE = "n-Hexane"
    N_NONANE = "n-Nonane"
    N_OCTANE = "n-Octane"
    P_PENTANE = "n-Pentane"
    N_PROPANE = "n-Propane"
    N_UNDECANE = "n-Undecane"
    O_XYLENE = "o-Xylene"
    P_XYLENE = "p-Xylene"
    TRANS_2_BUTENE = "trans-2-Butene"


class CoolPropIncompPureFluids(Enum):
    AS10 = "AS10"
    AS20 = "AS20"
    AS30 = "AS30"
    AS40 = "AS40"
    AS55 = "AS55"
    DEB = "DEB"
    DSF = "DSF"
    DOWJ = "DowJ"
    DOWJ2 = "DowJ2"
    DOWQ = "DowQ"
    DOWQ2 = "DowQ2"
    HC10 = "HC10"
    HC20 = "HC20"
    HC30 = "HC30"
    HC40 = "HC40"
    HC50 = "HC50"
    HCB = "HCB"
    HCM = "HCM"
    HFE = "HFE"
    HFE2 = "HFE2"
    HY20 = "HY20"
    HY30 = "HY30"
    HY40 = "HY40"
    HY45 = "HY45"
    HY50 = "HY50"
    NBS = "NBS"
    NAK = "NaK"
    PBB = "PBB"
    PCL = "PCL"
    PCR = "PCR"
    PGLT = "PGLT"
    PHE = "PHE"
    PHR = "PHR"
    PLR = "PLR"
    PMR = "PMR"
    PMS1 = "PMS1"
    PMS2 = "PMS2"
    PNF = "PNF"
    PNF2 = "PNF2"
    S800 = "S800"
    SAB = "SAB"
    T66 = "T66"
    T72 = "T72"
    TCO = "TCO"
    TD12 = "TD12"
    TVP1 = "TVP1"
    TVP1869 = "TVP1869"
    TX22 = "TX22"
    TY10 = "TY10"
    TY15 = "TY15"
    TY20 = "TY20"
    TY24 = "TY24"
    WATER = "Water"
    XLT = "XLT"
    XLT2 = "XLT2"
    ZS10 = "ZS10"
    ZS25 = "ZS25"
    ZS40 = "ZS40"
    ZS45 = "ZS45"
    ZS55 = "ZS55"


class CoolPropIncompMixturesMassBased(Enum):
    FRE = "FRE"
    ICEEA = "IceEA"
    ICENA = "IceNA"
    ICEPG = "IcePG"
    LIBR = "LiBr"
    MAM = "MAM"
    MAM2 = "MAM2"
    MCA = "MCA"
    MCA2 = "MCA2"
    MEA = "MEA"
    MEA2 = "MEA2"
    MEG = "MEG"
    MEG2 = "MEG2"
    MGL = "MGL"
    MGL2 = "MGL2"
    MITSW = "MITSW"
    MKA = "MKA"
    MKA2 = "MKA2"
    MKC = "MKC"
    MKC2 = "MKC2"
    MKF = "MKF"
    MLI = "MLI"
    MMA = "MMA"
    MMA2 = "MMA2"
    MMG = "MMG"
    MMG2 = "MMG2"
    MNA = "MNA"
    MNA2 = "MNA2"
    MPG = "MPG"
    MPG2 = "MPG2"
    VCA = "VCA"
    VKC = "VKC"
    VMA = "VMA"
    VMG = "VMG"
    VNA = "VNA"


class CoolPropIncompMixturesVolumeBased(Enum):
    AEG = "AEG"
    AKF = "AKF"
    AL = "AL"
    AN = "AN"
    APG = "APG"
    GKN = "GKN"
    PK2 = "PK2"
    PKL = "PKL"
    ZAC = "ZAC"
    ZFC = "ZFC"
    ZLC = "ZLC"
    ZM = "ZM"
    ZMC = "ZMC"


# Fluid class for fluid names
class CoolPropFluid:
    """CoolProp fluid class.

    The CoolProp fluid class wraps and includes all available fluids in CoolProp
    and provides the correct strings for the CoolProp library.

    """

    def __init__(self: CoolPropFluid, name: str, state: AbstractState) -> None:
        """Initialize CoolProp fluid class.

        The init function of the CoolProp fluid class.

        """

        self.__state = state

    @classmethod
    def from_pT(
        cls: Type[MediumCoolProp],
        name: str,
        p: np.float64,
        T: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
    ) -> MediumCoolProp:
        state = AbstractState(backend.value, fluid.value)
        state.update(CoolProp.PT_INPUTS, p, T)
        return cls(name=name, state=state)


# Media classes as derivation of base state class
class MediumCoolProp(BaseStateClass):
    """MediumCoolProp class.

    The MediumCoolProp class is a wrapper around the low-level interface of CoolProp
    with the AbstractState object.

    """

    def __init__(self: MediumCoolProp, name: str, state: AbstractState) -> None:
        """Initialize MediumCoolProp class.

        The init function of the MediumCoolProp class.

        """
        super().__init__(name=name)

        self.__state = state

    @classmethod
    def from_pT(
        cls: Type[MediumCoolProp],
        name: str,
        p: np.float64,
        T: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
    ) -> MediumCoolProp:
        state = AbstractState(backend.value, fluid.value)
        state.update(CoolProp.PT_INPUTS, p, T)
        return cls(name=name, state=state)

    @classmethod
    def from_px(
        cls: Type[MediumCoolProp],
        name: str,
        p: np.float64,
        x: np.float64,
        fluid: str,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
    ) -> MediumCoolProp:
        state = AbstractState(backend.value, fluid)
        state.update(CoolProp.PQ_INPUTS, p, x)
        return cls(name=name, state=state)

    @classmethod
    def from_Tx(
        cls: Type[MediumCoolProp],
        name: str,
        T: np.float64,
        x: np.float64,
        fluid: str,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
    ) -> MediumCoolProp:
        state = AbstractState(backend.value, fluid)
        state.update(CoolProp.QT_INPUTS, x, T)
        return cls(name=name, state=state)

    @classmethod
    def from_ph(
        cls: Type[MediumCoolProp],
        name: str,
        p: np.float64,
        h: np.float64,
        fluid: str,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
    ) -> MediumCoolProp:
        state = AbstractState(backend.value, fluid)
        state.update(CoolProp.HmassP_INPUTS, h, p)
        return cls(name=name, state=state)

    @classmethod
    def from_Th(
        cls: Type[MediumCoolProp],
        name: str,
        T: np.float64,
        h: np.float64,
        fluid: str,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
    ) -> MediumCoolProp:
        state = AbstractState(backend.value, fluid)
        state.update(CoolProp.HmassT_INPUTS, h, T)
        return cls(name=name, state=state)

    @property
    def cp(self: MediumCoolProp) -> np.float64:
        """Specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        return np.float64(self.__state.cpmass())

    @property
    def cpmass(self: MediumCoolProp) -> np.float64:
        """Specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        return np.float64(self.__state.cpmass())

    @property
    def cpmolar(self: MediumCoolProp) -> np.float64:
        """Specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        return np.float64(self.__state.cpmolar())

    @property
    def cv(self: MediumCoolProp) -> np.float64:
        """Specific heat at constant volume in J/kg/K.

        Returns:
            np.float64: Specific heat at constant volume in J/kg/K

        """
        ...

    @property
    def h(self: MediumCoolProp) -> np.float64:
        """Mass-specific enthalpy in J/kg.

        Returns:
            np.float64: Mass-specific enthalpy in J/kg

        """
        ...

    @property
    def conductivity(self: MediumCoolProp) -> np.float64:
        """Thermal conductivity in W/m/K.

        Returns:
            np.float64: Thermal conductivity in W/m/K

        """
        ...

    @property
    def viscosity(self: MediumCoolProp) -> np.float64:
        """Viscosity in Pa*s.

        Returns:
            np.float64: Viscosity in Pa*s

        """
        ...

    @property
    def p(self: MediumCoolProp) -> np.float64:
        """Pressure in Pa.

        Returns:
            np.float64: Pressure in Pa

        """
        ...

    @property
    def density(self: MediumCoolProp) -> np.float64:
        """Density in kg/m**3.

        Returns:
            np.float64: Density in kg/m**3

        """
        ...

    @property
    def gas_constant(self: MediumCoolProp) -> np.float64:
        """Specific gas constant in J/mol/K.

        Returns:
            np.float64: Specific gas constant in J/mol/K

        """
        ...

    @property
    def m_flow(self: BaseStateClass) -> np.float64:
        """Mass flow in kg/s.

        Returns:
            np.float64: Mass flow in kg/s

        """
        ...

    @property
    def s(self: MediumCoolProp) -> np.float64:
        """Mass-specific entropy in J/kg/K.

        Returns:
            np.float64: Mass-specific entropy in J/kg/K

        """
        ...

    @property
    def T(self: MediumCoolProp) -> np.float64:
        """Temperature in K.

        Returns:
            np.float64: Temperature in K

        """
        ...

    @property
    def v(self: MediumCoolProp) -> np.float64:
        """Specific volume in m**3/kg.

        Returns:
            np.float64: Specific volume in m**3/kg

        """
        ...

    @property
    def x(self: MediumCoolProp) -> np.float64:
        """Quality.

        Returns:
            np.float64: Quality

        """
        ...

    @property
    def Z(self: MediumCoolProp) -> np.float64:
        """Compressibility factor.

        Returns:
            np.float64: Compressibility factor

        """
        ...


class MediumCoolPropHumidAir(BaseStateClass):
    """MediumCoolPropHumidAir class.

    The MediumCoolPropHumidAir class is an interface to the 
    CoolProp HumidAirProp module.

    """

    def __init__(self: MediumCoolPropHumidAir) -> None:
        """Initialize MediumCoolProp class.

        The init function of the MediumCoolProp class.

        """
        super().__init__()

        self.__state = AbstractState()

    @property
    def cp(self: MediumCoolPropHumidAir) -> np.float64:
        """Specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        ...

    @property
    def cv(self: MediumCoolPropHumidAir) -> np.float64:
        """Specific heat at constant volume in J/kg/K.

        Returns:
            np.float64: Specific heat at constant volume in J/kg/K

        """
        ...

    @property
    def h(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific enthalpy in J/kg.

        Returns:
            np.float64: Mass-specific enthalpy in J/kg

        """
        ...

    @property
    def conductivity(self: MediumCoolPropHumidAir) -> np.float64:
        """Thermal conductivity in W/m/K.

        Returns:
            np.float64: Thermal conductivity in W/m/K

        """
        ...

    @property
    def viscosity(self: MediumCoolPropHumidAir) -> np.float64:
        """Viscosity in Pa*s.

        Returns:
            np.float64: Viscosity in Pa*s

        """
        ...

    @property
    def p(self: MediumCoolPropHumidAir) -> np.float64:
        """Pressure in Pa.

        Returns:
            np.float64: Pressure in Pa

        """
        ...

    @property
    def density(self: MediumCoolPropHumidAir) -> np.float64:
        """Density in kg/m**3.

        Returns:
            np.float64: Density in kg/m**3

        """
        ...

    @property
    def gas_constant(self: MediumCoolPropHumidAir) -> np.float64:
        """Specific gas constant in J/mol/K.

        Returns:
            np.float64: Specific gas constant in J/mol/K

        """
        ...

    @property
    def m_flow(self: BaseStateClass) -> np.float64:
        """Mass flow in kg/s.

        Returns:
            np.float64: Mass flow in kg/s

        """
        ...

    @property
    def s(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific entropy in J/kg/K.

        Returns:
            np.float64: Mass-specific entropy in J/kg/K

        """
        ...

    @property
    def T(self: MediumCoolPropHumidAir) -> np.float64:
        """Temperature in K.

        Returns:
            np.float64: Temperature in K

        """
        ...

    @property
    def v(self: MediumCoolPropHumidAir) -> np.float64:
        """Specific volume in m**3/kg.

        Returns:
            np.float64: Specific volume in m**3/kg

        """
        ...

    @property
    def x(self: MediumCoolPropHumidAir) -> np.float64:
        """Quality.

        Returns:
            np.float64: Quality

        """
        ...

    @property
    def Z(self: MediumCoolPropHumidAir) -> np.float64:
        """Compressibility factor.

        Returns:
            np.float64: Compressibility factor

        """
        ...


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("Not implemented.")


# -*- coding: utf-8 -*-

"""CoolProp media model library.

The CoolProp media model library provides interfaces to calculations of
equations of state and transport properties with the CoolProp and
CoolProp HumidAir library.

"""

from __future__ import annotations
from enum import Enum, auto
from typing import List, Type

from CoolProp import AbstractState, CoolProp
from CoolProp.CoolProp import PropsSI
from CoolProp.HumidAirProp import HAPropsSI
import math
import numpy as np
from thermd.core import MediumPure, MediumBinaryMixture
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


class CoolPropInputTypes(Enum):
    QT = CoolProp.QT_INPUTS
    PQ = CoolProp.PQ_INPUTS
    QSmolar = CoolProp.QSmolar_INPUTS
    QSmass = CoolProp.QSmass_INPUTS
    HmolarQ = CoolProp.HmolarQ_INPUTS
    HmassQ = CoolProp.HmassQ_INPUTS
    DmolarQ = CoolProp.DmolarQ_INPUTS
    DmassQ = CoolProp.DmassQ_INPUTS
    PT = CoolProp.PT_INPUTS
    DmassT = CoolProp.DmassT_INPUTS
    DmolarT = CoolProp.DmolarT_INPUTS
    HmolarT = CoolProp.HmolarT_INPUTS
    HmassT = CoolProp.HmassT_INPUTS
    SmolarT = CoolProp.SmolarT_INPUTS
    SmassT = CoolProp.SmassT_INPUTS
    TUmolar = CoolProp.TUmolar_INPUTS
    TUmass = CoolProp.TUmass_INPUTS
    DmassP = CoolProp.DmassP_INPUTS
    DmolarP = CoolProp.DmolarP_INPUTS
    HmassP = CoolProp.HmassP_INPUTS
    HmolarP = CoolProp.HmolarP_INPUTS
    PSmass = CoolProp.PSmass_INPUTS
    PSmolar = CoolProp.PSmolar_INPUTS
    PUmass = CoolProp.PUmass_INPUTS
    PUmolar = CoolProp.PUmolar_INPUTS
    HmassSmass = CoolProp.HmassSmass_INPUTS
    HmolarSmolar = CoolProp.HmolarSmolar_INPUTS
    SmassUmass = CoolProp.SmassUmass_INPUTS
    SmolarUmolar = CoolProp.SmolarUmolar_INPUTS
    DmassHmass = CoolProp.DmassHmass_INPUTS
    DmolarHmolar = CoolProp.DmolarHmolar_INPUTS
    DmassSmass = CoolProp.DmassSmass_INPUTS
    DmolarSmolar = CoolProp.DmolarSmolar_INPUTS
    DmassUmass = CoolProp.DmassUmass_INPUTS
    DmolarUmolar = CoolProp.DmolarUmolar_INPUTS


class CoolPropOutputTypes(Enum):
    DELTA = CoolProp.iDelta
    DMOLAR = CoolProp.iDmolar
    DMASS = CoolProp.iDmass
    HMOLAR = CoolProp.iHmolar
    HMASS = CoolProp.iHmass
    P = CoolProp.iP
    Q = CoolProp.iQ
    SMOLAR = CoolProp.iSmolar
    SMASS = CoolProp.iSmass
    TAU = CoolProp.iTau
    T = CoolProp.iT
    UMOLAR = CoolProp.iUmolar
    UMASS = CoolProp.iUmass
    ACENTRIC = CoolProp.iacentric_factor
    ALPHA0 = CoolProp.ialpha0
    ALPHAR = CoolProp.ialphar
    SPEED_OF_SOUND = CoolProp.ispeed_sound
    BVIRIAL = CoolProp.iBvirial
    CONDUCTIVITY = CoolProp.iconductivity
    CP0MASS = CoolProp.iCp0mass
    CP0MOLAR = CoolProp.iCp0molar
    CPMOLAR = CoolProp.iCpmolar
    CVIRIAL = CoolProp.iCvirial
    CVMASS = CoolProp.iCvmass
    CVMOLAR = CoolProp.iCvmass
    CPMASS = CoolProp.iCpmass
    DALPHA0_DDELTA_CONSTTAU = CoolProp.idalpha0_ddelta_consttau
    DALPHA0_DTAU_CONSTDELTA = CoolProp.idalpha0_dtau_constdelta
    DALPHAR_DDELTA_CONSTTAU = CoolProp.idalphar_ddelta_consttau
    DALPHAR_DTAU_CONSTDELTA = CoolProp.idalphar_dtau_constdelta
    DBVIRIAL_DT = CoolProp.idBvirial_dT
    DCVIRIAL_DT = CoolProp.idCvirial_dT
    DIPOLE_MOMENT = CoolProp.idipole_moment
    FH = CoolProp.iFH
    FRACTION_MAX = CoolProp.ifraction_max
    FRACTION_MIN = CoolProp.ifraction_min
    FUNDAMENTAL_DERIVATIVE_OF_GAS_DYNAMICS = (
        CoolProp.ifundamental_derivative_of_gas_dynamics
    )
    GAS_CONSTANT = CoolProp.igas_constant
    GMOLAR_RESIDUAL = CoolProp.iGmolar_residual
    GMOLAR = CoolProp.iGmolar
    GWP100 = CoolProp.iGWP100
    GWP20 = CoolProp.iGWP20
    GWP500 = CoolProp.iGWP500
    GMASS = CoolProp.iGmass
    HELMHOLTZMASS = CoolProp.iHelmholtzmass
    HELMHOLTZMOLAR = CoolProp.iHelmholtzmolar
    HH = CoolProp.iHH
    HMOLAR_RESIDUAL = CoolProp.iHmolar_residual
    ISENTROPIC_EXPANSION_COEFFICIENT = CoolProp.iisentropic_expansion_coefficient
    ISOBARIC_EXPANSION_COEFFICIENT = CoolProp.iisobaric_expansion_coefficient
    ISOTHERMAL_COMPRESSIBILITY = CoolProp.iisothermal_compressibility
    SURFACE_TENSION = CoolProp.isurface_tension
    MOLARMASS = CoolProp.imolar_mass
    ODP = CoolProp.iODP
    P_CRIT = CoolProp.iP_critical
    PHASE = CoolProp.iPhase
    PH = CoolProp.iPH
    PIP = CoolProp.iPIP
    P_MAX = CoolProp.iP_max
    P_MIN = CoolProp.iP_min
    PRANDTL = CoolProp.iPrandtl
    P_TRIPLE = CoolProp.iP_triple
    P_REDUCING = CoolProp.iP_reducing
    RHOMASS_CRITICAL = CoolProp.irhomass_critical
    RHOMASS_REDUCING = CoolProp.irhomass_reducing
    RHOMOLAR_CRITICAL = CoolProp.irhomolar_critical
    RHOMOLAR_REDUCING = CoolProp.irhomolar_reducing
    SMOLAR_RESIDUAL = CoolProp.iSmolar_residual
    T_CRIT = CoolProp.iT_critical
    T_MAX = CoolProp.iT_max
    T_MIN = CoolProp.iT_min
    T_TRIPLE = CoolProp.iT_triple
    T_FREEZE = CoolProp.iT_freeze
    T_REDUCING = CoolProp.iT_reducing
    VISCOSITY = CoolProp.iviscosity
    Z = CoolProp.iZ


class CoolPropFluidTypes(Enum):
    PURE = auto()
    MIXTURE = auto()
    INCOMP = auto()
    INCOMPMIXTURE = auto()


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


# CoolProp fluid class
class CoolPropFluid:
    """CoolProp fluid class.

    The CoolProp fluid class wraps and includes all available fluids in CoolProp
    and provides the correct strings for the CoolProp library.

    """

    def __init__(
        self: CoolPropFluid, fluid_name: str, fluid_type: CoolPropFluidTypes,
    ) -> None:
        """Initialize CoolProp fluid class.

        The init function of the CoolProp fluid class.

        """
        self.__fluid_name = fluid_name
        self.__fluid_type = fluid_type

    @classmethod
    def new_pure_fluid(
        cls: Type[CoolPropFluid], fluid: CoolPropPureFluids,
    ) -> CoolPropFluid:
        return cls(fluid_name=fluid.value, fluid_type=CoolPropFluidTypes.PURE)

    @classmethod
    def new_mixture(
        cls: Type[CoolPropFluid],
        fluids: List[CoolPropPureFluids],
        fractions: List[np.float64],
    ) -> CoolPropFluid:
        if len(fluids) == len(fractions):
            if np.array(fractions).sum() == 1.0:
                fluid_name = str()
                for i, fluid in enumerate(fluids):
                    fluid_name += str(fluid)
                    fluid_name += "[" + str(fractions[i]) + "]"
                    if i < len(fluids):
                        fluid_name += "&"
            else:
                logger.error(
                    "Sum of the fluid fractions must be 1.0: %f != 1.0",
                    np.array(fractions).sum(),
                )
                raise SystemExit
        else:
            logger.error(
                "Length of the lists fluids and fractions must be equal: %i == %i",
                len(fluids),
                len(fractions),
            )
            raise SystemExit

        return cls(fluid_name=fluid_name, fluid_type=CoolPropFluidTypes.MIXTURE)

    @classmethod
    def new_incomp(
        cls: Type[CoolPropFluid], fluid: CoolPropIncompPureFluids
    ) -> CoolPropFluid:
        return cls(fluid_name=fluid.value, fluid_type=CoolPropFluidTypes.INCOMP)

    @classmethod
    def new_incomp_mass_based(
        cls: Type[CoolPropFluid],
        fluid: CoolPropIncompMixturesMassBased,
        fraction: np.float64,
    ) -> CoolPropFluid:
        fluid_name = fluid.value + "[" + str(fraction) + "]"
        return cls(fluid_name=fluid_name, fluid_type=CoolPropFluidTypes.INCOMPMIXTURE)

    @classmethod
    def new_incomp_volume_based(
        cls: Type[CoolPropFluid],
        fluid: CoolPropIncompMixturesVolumeBased,
        fraction: np.float64,
    ) -> CoolPropFluid:
        fluid_name = fluid.value + "[" + str(fraction) + "]"
        return cls(fluid_name=fluid_name, fluid_type=CoolPropFluidTypes.INCOMPMIXTURE)

    @property
    def fluid_name(self: CoolPropFluid) -> str:
        return self.__fluid_name

    @property
    def fluid_type(self: CoolPropFluid) -> CoolPropFluidTypes:
        return self.__fluid_type


# Media classes as derivation of base state class
class MediumCoolProp(MediumPure):
    """MediumCoolProp class.

    The MediumCoolProp class is a wrapper around the low-level interface of CoolProp
    with the AbstractState object.

    """

    def __init__(
        self: MediumCoolProp,
        name: str,
        state: AbstractState,
        m_flow: np.float64 = np.float64(0.0),
    ) -> None:
        """Initialize MediumCoolProp class.

        The init function of the MediumCoolProp class.

        """
        super().__init__(name=name)

        # Class parameters
        self.__state = state
        self.__m_flow = m_flow

    @classmethod
    def from_pT(
        cls: Type[MediumCoolProp],
        name: str,
        p: np.float64,
        T: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
        m_flow: np.float64 = np.float64(0.0),
    ) -> MediumCoolProp:
        if (
            fluid.fluid_type == CoolPropFluidTypes.INCOMP
            or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
        ) and backend != CoolPropBackends.INCOMP:
            logger.error(
                "Incompressible fluids and mixtures must use the INCOMP backend."
            )
            raise SystemExit

        state = AbstractState(backend.value, fluid.fluid_name)
        state.update(CoolProp.PT_INPUTS, p, T)
        return cls(name=name, state=state, m_flow=m_flow)

    @classmethod
    def from_px(
        cls: Type[MediumCoolProp],
        name: str,
        p: np.float64,
        x: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
        m_flow: np.float64 = np.float64(0.0),
    ) -> MediumCoolProp:
        if (
            fluid.fluid_type == CoolPropFluidTypes.INCOMP
            or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
        ) and backend != CoolPropBackends.INCOMP:
            logger.error(
                "Incompressible fluids and mixtures must use the INCOMP backend."
            )
            raise SystemExit

        state = AbstractState(backend.value, fluid.fluid_name)
        state.update(CoolProp.PQ_INPUTS, p, x)
        return cls(name=name, state=state, m_flow=m_flow)

    @classmethod
    def from_Tx(
        cls: Type[MediumCoolProp],
        name: str,
        T: np.float64,
        x: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
        m_flow: np.float64 = np.float64(0.0),
    ) -> MediumCoolProp:
        if (
            fluid.fluid_type == CoolPropFluidTypes.INCOMP
            or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
        ) and backend != CoolPropBackends.INCOMP:
            logger.error(
                "Incompressible fluids and mixtures must use the INCOMP backend."
            )
            raise SystemExit

        state = AbstractState(backend.value, fluid.fluid_name)
        state.update(CoolProp.QT_INPUTS, x, T)
        return cls(name=name, state=state, m_flow=m_flow)

    @classmethod
    def from_ph(
        cls: Type[MediumCoolProp],
        name: str,
        p: np.float64,
        h: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
        m_flow: np.float64 = np.float64(0.0),
    ) -> MediumCoolProp:
        if (
            fluid.fluid_type == CoolPropFluidTypes.INCOMP
            or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
        ) and backend != CoolPropBackends.INCOMP:
            logger.error(
                "Incompressible fluids and mixtures must use the INCOMP backend."
            )
            raise SystemExit

        state = AbstractState(backend.value, fluid.fluid_name)
        state.update(CoolProp.HmassP_INPUTS, h, p)
        return cls(name=name, state=state, m_flow=m_flow)

    @classmethod
    def from_Th(
        cls: Type[MediumCoolProp],
        name: str,
        T: np.float64,
        h: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
        m_flow: np.float64 = np.float64(0.0),
    ) -> MediumCoolProp:
        if (
            fluid.fluid_type == CoolPropFluidTypes.INCOMP
            or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
        ) and backend != CoolPropBackends.INCOMP:
            logger.error(
                "Incompressible fluids and mixtures must use the INCOMP backend."
            )
            raise SystemExit

        state = AbstractState(backend.value, fluid.fluid_name)
        state.update(CoolProp.HmassT_INPUTS, h, T)
        return cls(name=name, state=state, m_flow=m_flow)

    @classmethod
    def from_generic(
        cls: Type[MediumCoolProp],
        name: str,
        input_type: CoolPropInputTypes,
        prop1: np.float64,
        prop2: np.float64,
        fluid: CoolPropFluid,
        backend: CoolPropBackends = CoolPropBackends.HEOS,
        m_flow: np.float64 = np.float64(0.0),
    ) -> MediumCoolProp:
        if (
            fluid.fluid_type == CoolPropFluidTypes.INCOMP
            or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
        ) and backend != CoolPropBackends.INCOMP:
            logger.error(
                "Incompressible fluids and mixtures must use the INCOMP backend."
            )
            raise SystemExit

        state = AbstractState(backend.value, fluid.fluid_name)
        state.update(input_type.value, prop1, prop2)
        return cls(name=name, state=state, m_flow=m_flow)

    @property
    def cpmass(self: MediumCoolProp) -> np.float64:
        """Mass-specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        return np.float64(self.__state.cpmass())

    @property
    def cpmolar(self: MediumCoolProp) -> np.float64:
        """Molar-specific heat at constant pressure in J/mol/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/mol/K

        """
        return np.float64(self.__state.cpmolar())

    @property
    def cvmass(self: MediumCoolProp) -> np.float64:
        """Mass-specific heat at constant volume in J/kg/K.

        Returns:
            np.float64: Specific heat at constant volume in J/kg/K

        """
        return np.float64(self.__state.cvmass())

    @property
    def cvmolar(self: MediumCoolProp) -> np.float64:
        """Molar-specific heat at constant volume in J/mol/K.

        Returns:
            np.float64: Specific heat at constant volume in J/mol/K

        """
        return np.float64(self.__state.cvmolar())

    @property
    def hmass(self: MediumCoolProp) -> np.float64:
        """Mass-specific enthalpy in J/kg.

        Returns:
            np.float64: Mass-specific enthalpy in J/kg

        """
        return np.float64(self.__state.hmass())

    @property
    def hmolar(self: MediumCoolProp) -> np.float64:
        """Molar-specific enthalpy in J/mol.

        Returns:
            np.float64: Mass-specific enthalpy in J/mol

        """
        return np.float64(self.__state.hmolar())

    @property
    def conductivity(self: MediumCoolProp) -> np.float64:
        """Thermal conductivity in W/m/K.

        Returns:
            np.float64: Thermal conductivity in W/m/K

        """
        return np.float64(self.__state.conductivity())

    @property
    def viscosity(self: MediumCoolProp) -> np.float64:
        """Viscosity in Pa*s.

        Returns:
            np.float64: Viscosity in Pa*s

        """
        return np.float64(self.__state.viscosity())

    @property
    def p(self: MediumCoolProp) -> np.float64:
        """Pressure in Pa.

        Returns:
            np.float64: Pressure in Pa

        """
        return np.float64(self.__state.p())

    @property
    def rhomass(self: MediumCoolProp) -> np.float64:
        """Mass-specific density in kg/m**3.

        Returns:
            np.float64: Density in kg/m**3

        """
        return np.float64(self.__state.rhomass())

    @property
    def rhomolar(self: MediumCoolProp) -> np.float64:
        """Molar-specific density in mol/m**3.

        Returns:
            np.float64: Density in mol/m**3

        """
        return np.float64(self.__state.rhomolar())

    @property
    def gas_constant(self: MediumCoolProp) -> np.float64:
        """Specific gas constant in J/mol/K.

        Returns:
            np.float64: Specific gas constant in J/mol/K

        """
        return np.float64(self.__state.gas_constant())

    @property
    def m_flow(self: MediumCoolProp) -> np.float64:
        """Mass flow in kg/s.

        Returns:
            np.float64: Mass flow in kg/s

        """
        return self.__m_flow

    @m_flow.setter
    def m_flow(self: MediumCoolProp, value: np.float64) -> None:
        """Mass flow in kg/s.

        Returns:
            np.float64: Mass flow in kg/s

        """
        self.__m_flow = value

    @property
    def smass(self: MediumCoolProp) -> np.float64:
        """Mass-specific entropy in J/kg/K.

        Returns:
            np.float64: Mass-specific entropy in J/kg/K

        """
        return np.float64(self.__state.smass())

    @property
    def smolar(self: MediumCoolProp) -> np.float64:
        """Molar-specific entropy in J/mol/K.

        Returns:
            np.float64: Mass-specific entropy in J/mol/K

        """
        return np.float64(self.__state.smolar())

    @property
    def T(self: MediumCoolProp) -> np.float64:
        """Temperature in K.

        Returns:
            np.float64: Temperature in K

        """
        return np.float64(self.__state.T())

    @property
    def vmass(self: MediumCoolProp) -> np.float64:
        """Mass-specific volume in m**3/kg.

        Returns:
            np.float64: Specific volume in m**3/kg

        """
        return np.float64(1.0 / self.__state.rhomass())

    @property
    def vmolar(self: MediumCoolProp) -> np.float64:
        """Molar-specific volume in m**3/mol.

        Returns:
            np.float64: Specific volume in m**3/mol

        """
        return np.float64(1.0 / self.__state.rhomolar())

    @property
    def x(self: MediumCoolProp) -> np.float64:
        """Vapor quality.

        Returns:
            np.float64: Vapor quality

        """
        return np.float64(self.__state.Q())

    @property
    def Z(self: MediumCoolProp) -> np.float64:
        """Compressibility factor.

        Returns:
            np.float64: Compressibility factor

        """
        return np.float64(self.__state.compressibility_factor())

    def set_pT(self: MediumCoolProp, p: np.float64, T: np.float64) -> None:
        self.__state.update(CoolProp.PT_INPUTS, p, T)

    def set_px(self: MediumCoolProp, p: np.float64, x: np.float64) -> None:
        self.__state.update(CoolProp.PQ_INPUTS, p, x)

    def set_Tx(self: MediumCoolProp, T: np.float64, x: np.float64) -> None:
        self.__state.update(CoolProp.QT_INPUTS, x, T)

    def set_ph(self: MediumCoolProp, p: np.float64, h: np.float64) -> None:
        self.__state.update(CoolProp.HmassP_INPUTS, h, p)

    def set_Th(self: MediumCoolProp, T: np.float64, h: np.float64) -> None:
        self.__state.update(CoolProp.HmassT_INPUTS, h, T)

    def set_ps(self: MediumCoolProp, p: np.float64, s: np.float64) -> None:
        self.__state.update(CoolProp.PSmass_INPUTS, p, s)

    def set_Ts(self: MediumCoolProp, T: np.float64, s: np.float64) -> None:
        self.__state.update(CoolProp.SmassT_INPUTS, s, T)

    def set_state_generic(
        self: MediumCoolProp,
        input_type: CoolPropInputTypes,
        prop1: np.float64,
        prop2: np.float64,
    ) -> None:
        self.__state.update(input_type.value, prop1, prop2)

    def get_state_generic(
        self: MediumCoolProp, output_type: CoolPropOutputTypes,
    ) -> np.float64:
        return np.float64(self.__state.keyed_output(output_type))

    def get_state_generic_list(
        self: MediumCoolProp, output_types: List[CoolPropOutputTypes],
    ) -> List[np.float64]:
        return [np.float64(self.__state.keyed_output(k)) for k in output_types]


class MediumCoolPropHumidAir(MediumBinaryMixture):
    """MediumCoolPropHumidAir class.

    The MediumCoolPropHumidAir class is an interface to the 
    CoolProp HumidAirProp module.

    """

    def __init__(
        self: MediumCoolPropHumidAir,
        name: str,
        p: np.float64,
        T: np.float64,
        w: np.float64,
        m_flow: np.float64 = np.float64(0.0),
    ) -> None:
        """Initialize MediumCoolProp class.

        The init function of the MediumCoolProp class.

        """
        super().__init__(name=name)

        # Class parameters
        self.__p = p
        self.__T = T
        self.__w = w
        self.__m_flow = m_flow

        # Constants
        self.__R_air = 287.0474730938159
        self.__R_water = 461.5230869726723

        self.__cp_air_poly = np.poly1d(
            [-1.02982783e-07, 4.29730845e-04, 1.46305349e-02, 1.00562420e03]
        )
        self.__cp_water_vapor_poly = np.poly1d(
            [
                3.05228669e-11,
                -1.57712722e-08,
                1.04676045e-06,
                1.27256322e-03,
                1.82289816e-01,
                1.85835959e03,
            ]
        )
        self.__cp_water_liquid_poly = np.poly1d(
            [
                -9.13327305e-14,
                9.89764971e-11,
                -4.24011913e-08,
                9.47137661e-06,
                -1.15186890e-03,
                8.34474494e-02,
                -2.98605473e00,
                4.21866441e03,
            ]
        )
        self.__cp_water_ice_poly = np.poly1d(
            [-1.03052963e-04, -2.77224838e-02, 4.87648024e00, 2.05097273e03]
        )
        self.__cv_air = 718
        self.__cv_water_vapor = 1435.9

        self.__delta_h_evaporation = 2500900
        self.__delta_h_melting = 333400

        self.__T_triple = 273.16
        self.__p_triple = 611.657 / 10 ** 5

        # Reference state
        self.__h_humid_air_0 = HAPropsSI(
            "H", "T", self.__T_triple, "P", self.__p_triple * 10 ** 5, "R", 0
        )
        self.__h_water_liquid_0 = PropsSI(
            "H", "T", self.__T_triple, "P", self.__p_triple * 10 ** 5, "Water"
        )
        self.__h_water_ice_0 = 0.0
        self.__s_humid_air_0 = HAPropsSI(
            "S", "T", self.__T_triple, "P", self.__p_triple * 10 ** 5, "R", 0
        )
        self.__s_water_liquid_0 = PropsSI(
            "S", "T", self.__T_triple, "P", self.__p_triple * 10 ** 5, "Water"
        )
        self.__s_water_ice_0 = 0.0

    @property
    def cpmass(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific heat at constant pressure in J/kg/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/kg/K

        """
        ws = self.__x_tpphi(T=self.__T, p=self.__p, R=1.0)

        if ws >= self.__w:  # under-saturated
            cp_fl = HAPropsSI("C", "T", self.__T, "P", self.__p, "W", self.__w)

        else:  # saturated
            cp_fl = HAPropsSI("C", "T", self.__T, "P", self.__p, "R", 1)

        return cp_fl

    @property
    def cpmolar(self: MediumCoolPropHumidAir) -> np.float64:
        """Molar-specific heat at constant pressure in J/mol/K.

        Returns:
            np.float64: Specific heat at constant pressure in J/mol/K

        """
        logger.error("Not implemented.")
        raise SystemExit

    @property
    def cvmass(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific heat at constant volume in J/kg/K.

        Returns:
            np.float64: Specific heat at constant volume in J/kg/K

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def cvmolar(self: MediumCoolPropHumidAir) -> np.float64:
        """Molar-specific heat at constant volume in J/mol/K.

        Returns:
            np.float64: Specific heat at constant volume in J/mol/K

        """
        logger.error("Not implemented.")
        raise SystemExit

    @property
    def hmass(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific enthalpy in J/kg.

        Returns:
            np.float64: Mass-specific enthalpy in J/kg

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def hmolar(self: MediumCoolPropHumidAir) -> np.float64:
        """Molar-specific enthalpy in J/mol.

        Returns:
            np.float64: Mass-specific enthalpy in J/mol

        """
        logger.error("Not implemented.")
        raise SystemExit

    @property
    def conductivity(self: MediumCoolPropHumidAir) -> np.float64:
        """Thermal conductivity in W/m/K.

        Returns:
            np.float64: Thermal conductivity in W/m/K

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def viscosity(self: MediumCoolPropHumidAir) -> np.float64:
        """Viscosity in Pa*s.

        Returns:
            np.float64: Viscosity in Pa*s

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def p(self: MediumCoolPropHumidAir) -> np.float64:
        """Pressure in Pa.

        Returns:
            np.float64: Pressure in Pa

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def rhomass(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific density in kg/m**3.

        Returns:
            np.float64: Density in kg/m**3

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def rhomolar(self: MediumCoolPropHumidAir) -> np.float64:
        """Molar-specific density in mol/m**3.

        Returns:
            np.float64: Density in mol/m**3

        """
        logger.error("Not implemented.")
        raise SystemExit

    @property
    def gas_constant(self: MediumCoolPropHumidAir) -> np.float64:
        """Specific gas constant in J/mol/K.

        Returns:
            np.float64: Specific gas constant in J/mol/K

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def m_flow(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass flow in kg/s.

        Returns:
            np.float64: Mass flow in kg/s

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @m_flow.setter
    def m_flow(self: MediumCoolProp, value: np.float64) -> None:
        """Mass flow in kg/s.

        Returns:
            np.float64: Mass flow in kg/s

        """
        self.__m_flow = value

    @property
    def smass(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific entropy in J/kg/K.

        Returns:
            np.float64: Mass-specific entropy in J/kg/K

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def smolar(self: MediumCoolPropHumidAir) -> np.float64:
        """Molar-specific entropy in J/mol/K.

        Returns:
            np.float64: Mass-specific entropy in J/mol/K

        """
        logger.error("Not implemented.")
        raise SystemExit

    @property
    def T(self: MediumCoolPropHumidAir) -> np.float64:
        """Temperature in K.

        Returns:
            np.float64: Temperature in K

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def vmass(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass-specific volume in m**3/kg.

        Returns:
            np.float64: Specific volume in m**3/kg

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def vmolar(self: MediumCoolPropHumidAir) -> np.float64:
        """Molar-specific volume in m**3/mol.

        Returns:
            np.float64: Specific volume in m**3/mol

        """
        logger.error("Not implemented.")
        raise SystemExit

    @property
    def x(self: MediumCoolPropHumidAir) -> np.float64:
        """Quality.

        Returns:
            np.float64: Quality

        """
        logger.error("Not implemented.")
        raise SystemExit

    @property
    def Z(self: MediumCoolPropHumidAir) -> np.float64:
        """Compressibility factor.

        Returns:
            np.float64: Compressibility factor

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def w(self: MediumCoolPropHumidAir) -> np.float64:
        """Mass ratio.

        Returns:
            np.float64: Mass ratio

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    @property
    def phi(self: MediumCoolPropHumidAir) -> np.float64:
        """Relative humidity.

        Returns:
            np.float64: Relative humidity

        """
        return HAPropsSI("R", "T", self.__T, "P", self.__p, "W", self.__w)

    def __ps_hardy_pT(self: MediumCoolPropHumidAir, p, T):
        if T >= 273.15:
            ps = math.exp(
                (-2.8365744) * 10 ** 3 * T ** (-2)
                + (-6.028076559) * 10 ** 3 * T ** (-1)
                + 1.954263612 * 10 ** 1 * T ** 0
                + (-2.737830188) * 10 ** (-2) * T ** 1
                + 1.6261698 * 10 ** (-5) * T ** 2
                + 7.0229056 * 10 ** (-10) * T ** 3
                + (-1.8680009) * 10 ** (-13) * T ** 4
                + 2.7150305 * math.log(T)
            )
            alpha = (
                3.53624 * 10 ** (-4) * (T - 273.15) ** 0
                + 2.9328363 * 10 ** (-5) * (T - 273.15) ** 1
                + 2.6168979 * 10 ** (-7) * (T - 273.15) ** 2
                + 8.5813609 * 10 ** (-9) * (T - 273.15) ** 3
            )
            beta = math.exp(
                (-1.07588) * 10 ** 1 * (T - 273.15) ** 0
                + 6.3268134 * 10 ** (-2) * (T - 273.15) ** 1
                + (-2.5368934) * 10 ** (-4) * (T - 273.15) ** 2
                + 6.3405286 * 10 ** (-7) * (T - 273.15) ** 3
            )
        else:
            ps = math.exp(
                (-5.8666426) * 10 ** 3 * T ** (-1)
                + 2.232870244 * 10 ** 1 * T ** 0
                + 1.39387003 * 10 ** (-2) * T ** 1
                + (-3.4262402) * 10 ** (-5) * T ** 2
                + 2.7040955 * 10 ** (-8) * T ** 3
                + 6.7063522 * 10 ** (-1) * math.log(T)
            )
            alpha = (
                3.64449 * 10 ** (-4) * (T - 273.15) ** 0
                + 2.9367585 * 10 ** (-5) * (T - 273.15) ** 1
                + 4.8874766 * 10 ** (-7) * (T - 273.15) ** 2
                + 4.3669918 * 10 ** (-9) * (T - 273.15) ** 3
            )
            beta = math.exp(
                (-1.07271) * 10 ** 1 * (T - 273.15) ** 0
                + 7.6215115 * 10 ** (-2) * (T - 273.15) ** 1
                + (-1.7490155) * 10 ** (-4) * (T - 273.15) ** 2
                + 2.4668279 * 10 ** (-6) * (T - 273.15) ** 3
            )

        f = math.exp(alpha * (1 - (ps / p)) + beta * ((p / ps) - 1))
        ps *= f

        return ps

    def __ws_hardy_pT(self: MediumCoolPropHumidAir, p, T):
        ps = ps_hardy_tp(t, p)

        xs = abs(0.622 * (ps / (p - ps)))
        return xs

    def __w_hardy_pTphi(self: MediumCoolPropHumidAir, t, p=1.01325, phi=1.0):
        ps = ps_hardy_tp(t, p)

        x = abs(0.622 * ((phi * ps) / (p - phi * ps)))
        return x

    def __phi_hardy_pTw(self: MediumCoolPropHumidAir, t, p=1.01325, x=0.0):
        phi = (p / ps_hardy_tp(t, p)) * (x / (0.622 + x))

        return phi

    def __w_pTphi(self: MediumCoolPropHumidAir, p, T, phi):
        if -100 + 273.15 <= T <= 100 + 273.15:

            w = HAPropsSI("W", "T", T, "P", p, "R", phi)

        else:
            logger.debug("Out of definition range.")

            if T < -100 + 273.15:
                w = 0.0
            else:
                w = 1.0

        if w < 0:
            logger.debug("Error in calculation of water content. Use Hardy.")
            w = self.__w_hardy_pTphi(p, T, phi)

        return w

    def set_pTw(
        self: MediumCoolPropHumidAir, p: np.float64, T: np.float64, w: np.float64
    ) -> None:
        ...

    def set_phw(
        self: MediumCoolPropHumidAir, p: np.float64, h: np.float64, w: np.float64
    ) -> None:
        ...

    def set_Thw(
        self: MediumCoolPropHumidAir, T: np.float64, h: np.float64, w: np.float64
    ) -> None:
        ...

    def set_psw(
        self: MediumCoolPropHumidAir, p: np.float64, s: np.float64, w: np.float64
    ) -> None:
        ...

    def set_Tsw(
        self: MediumCoolPropHumidAir, T: np.float64, s: np.float64, w: np.float64
    ) -> None:
        ...


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("Not implemented.")


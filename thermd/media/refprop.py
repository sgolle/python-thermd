# -*- coding: utf-8 -*-

"""CoolProp media model library.

The CoolProp media model library provides interfaces to calculations of
equations of state and transport properties with the CoolProp and
CoolProp HumidAir library.

"""

# from __future__ import annotations
# from enum import Enum, auto
# from typing import List, Type, Union, Optional

# from CoolProp import AbstractState, CoolProp
# from CoolProp.CoolProp import PropsSI
# from CoolProp.HumidAirProp import HAPropsSI
# import math
# import numpy as np
# from scipy import optimize as opt
# from scipy.constants import gas_constant
# from thermd.core import MediumBase, MediumHumidAir, StatePhases
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)

# Enums
# class CoolPropBackends(Enum):
#     HEOS = "HEOS"
#     REFPROP = "REFPROP"
#     INCOMP = "INCOMP"
#     TTSE_HEOS = "TTSE&HEOS"
#     TTSE_REFPROP = "TTSE&REFPROP"
#     BICUBIC_HEOS = "BICUBIC&HEOS"
#     BICUBIC_REFPROP = "BICUBIC&REFPROP"
#     IF97 = "IF97"
#     TREND = "TREND"
#     SRK = "SRK"
#     PR = "PR"
#     VTPR = "VTPR"
#     PCSAFT = "PCSAFT"


# class CoolPropInputTypes(Enum):
#     QT = CoolProp.QT_INPUTS
#     PQ = CoolProp.PQ_INPUTS
#     QSmolar = CoolProp.QSmolar_INPUTS
#     QSmass = CoolProp.QSmass_INPUTS
#     HmolarQ = CoolProp.HmolarQ_INPUTS
#     HmassQ = CoolProp.HmassQ_INPUTS
#     DmolarQ = CoolProp.DmolarQ_INPUTS
#     DmassQ = CoolProp.DmassQ_INPUTS
#     PT = CoolProp.PT_INPUTS
#     DmassT = CoolProp.DmassT_INPUTS
#     DmolarT = CoolProp.DmolarT_INPUTS
#     HmolarT = CoolProp.HmolarT_INPUTS
#     HmassT = CoolProp.HmassT_INPUTS
#     SmolarT = CoolProp.SmolarT_INPUTS
#     SmassT = CoolProp.SmassT_INPUTS
#     TUmolar = CoolProp.TUmolar_INPUTS
#     TUmass = CoolProp.TUmass_INPUTS
#     DmassP = CoolProp.DmassP_INPUTS
#     DmolarP = CoolProp.DmolarP_INPUTS
#     HmassP = CoolProp.HmassP_INPUTS
#     HmolarP = CoolProp.HmolarP_INPUTS
#     PSmass = CoolProp.PSmass_INPUTS
#     PSmolar = CoolProp.PSmolar_INPUTS
#     PUmass = CoolProp.PUmass_INPUTS
#     PUmolar = CoolProp.PUmolar_INPUTS
#     HmassSmass = CoolProp.HmassSmass_INPUTS
#     HmolarSmolar = CoolProp.HmolarSmolar_INPUTS
#     SmassUmass = CoolProp.SmassUmass_INPUTS
#     SmolarUmolar = CoolProp.SmolarUmolar_INPUTS
#     DmassHmass = CoolProp.DmassHmass_INPUTS
#     DmolarHmolar = CoolProp.DmolarHmolar_INPUTS
#     DmassSmass = CoolProp.DmassSmass_INPUTS
#     DmolarSmolar = CoolProp.DmolarSmolar_INPUTS
#     DmassUmass = CoolProp.DmassUmass_INPUTS
#     DmolarUmolar = CoolProp.DmolarUmolar_INPUTS


# class CoolPropOutputTypes(Enum):
#     DELTA = CoolProp.iDelta
#     DMOLAR = CoolProp.iDmolar
#     DMASS = CoolProp.iDmass
#     HMOLAR = CoolProp.iHmolar
#     HMASS = CoolProp.iHmass
#     P = CoolProp.iP
#     Q = CoolProp.iQ
#     SMOLAR = CoolProp.iSmolar
#     SMASS = CoolProp.iSmass
#     TAU = CoolProp.iTau
#     T = CoolProp.iT
#     UMOLAR = CoolProp.iUmolar
#     UMASS = CoolProp.iUmass
#     ACENTRIC = CoolProp.iacentric_factor
#     ALPHA0 = CoolProp.ialpha0
#     ALPHAR = CoolProp.ialphar
#     SPEED_OF_SOUND = CoolProp.ispeed_sound
#     BVIRIAL = CoolProp.iBvirial
#     CONDUCTIVITY = CoolProp.iconductivity
#     CP0MASS = CoolProp.iCp0mass
#     CP0MOLAR = CoolProp.iCp0molar
#     CPMOLAR = CoolProp.iCpmolar
#     CVIRIAL = CoolProp.iCvirial
#     CVMASS = CoolProp.iCvmass
#     CVMOLAR = CoolProp.iCvmass
#     CPMASS = CoolProp.iCpmass
#     DALPHA0_DDELTA_CONSTTAU = CoolProp.idalpha0_ddelta_consttau
#     DALPHA0_DTAU_CONSTDELTA = CoolProp.idalpha0_dtau_constdelta
#     DALPHAR_DDELTA_CONSTTAU = CoolProp.idalphar_ddelta_consttau
#     DALPHAR_DTAU_CONSTDELTA = CoolProp.idalphar_dtau_constdelta
#     DBVIRIAL_DT = CoolProp.idBvirial_dT
#     DCVIRIAL_DT = CoolProp.idCvirial_dT
#     DIPOLE_MOMENT = CoolProp.idipole_moment
#     FH = CoolProp.iFH
#     FRACTION_MAX = CoolProp.ifraction_max
#     FRACTION_MIN = CoolProp.ifraction_min
#     FUNDAMENTAL_DERIVATIVE_OF_GAS_DYNAMICS = (
#         CoolProp.ifundamental_derivative_of_gas_dynamics
#     )
#     GAS_CONSTANT = CoolProp.igas_constant
#     GMOLAR_RESIDUAL = CoolProp.iGmolar_residual
#     GMOLAR = CoolProp.iGmolar
#     GWP100 = CoolProp.iGWP100
#     GWP20 = CoolProp.iGWP20
#     GWP500 = CoolProp.iGWP500
#     GMASS = CoolProp.iGmass
#     HELMHOLTZMASS = CoolProp.iHelmholtzmass
#     HELMHOLTZMOLAR = CoolProp.iHelmholtzmolar
#     HH = CoolProp.iHH
#     HMOLAR_RESIDUAL = CoolProp.iHmolar_residual
#     ISENTROPIC_EXPANSION_COEFFICIENT = CoolProp.iisentropic_expansion_coefficient
#     ISOBARIC_EXPANSION_COEFFICIENT = CoolProp.iisobaric_expansion_coefficient
#     ISOTHERMAL_COMPRESSIBILITY = CoolProp.iisothermal_compressibility
#     SURFACE_TENSION = CoolProp.isurface_tension
#     MOLARMASS = CoolProp.imolar_mass
#     ODP = CoolProp.iODP
#     P_CRIT = CoolProp.iP_critical
#     PHASE = CoolProp.iPhase
#     PH = CoolProp.iPH
#     PIP = CoolProp.iPIP
#     P_MAX = CoolProp.iP_max
#     P_MIN = CoolProp.iP_min
#     PRANDTL = CoolProp.iPrandtl
#     P_TRIPLE = CoolProp.iP_triple
#     P_REDUCING = CoolProp.iP_reducing
#     RHOMASS_CRITICAL = CoolProp.irhomass_critical
#     RHOMASS_REDUCING = CoolProp.irhomass_reducing
#     RHOMOLAR_CRITICAL = CoolProp.irhomolar_critical
#     RHOMOLAR_REDUCING = CoolProp.irhomolar_reducing
#     SMOLAR_RESIDUAL = CoolProp.iSmolar_residual
#     T_CRIT = CoolProp.iT_critical
#     T_MAX = CoolProp.iT_max
#     T_MIN = CoolProp.iT_min
#     T_TRIPLE = CoolProp.iT_triple
#     T_FREEZE = CoolProp.iT_freeze
#     T_REDUCING = CoolProp.iT_reducing
#     VISCOSITY = CoolProp.iviscosity
#     Z = CoolProp.iZ


# class CoolPropFluidTypes(Enum):
#     PURE = auto()
#     MIXTURE = auto()
#     INCOMP = auto()
#     INCOMPMIXTURE = auto()


# class CoolPropPureFluids(Enum):
#     BUTENE = "1-Butene"
#     ACETONE = "Aceton"
#     AIR = "Air"
#     AMMONIA = "Ammonia"
#     ARGON = "Argon"
#     BENZENE = "Benzene"
#     CARBONDIOXIDE = "CarbonDioxide"
#     CARBONMONOXIDE = "CarbonMonoxide"
#     CARBONYLSULFIDE = "CarbonylSulfide"
#     CYCLOHEXANE = "CycloHexane"
#     CYCLOPROPANE = "CycloPropane"
#     CYCLOPENTANE = "Cyclopentane"
#     D4 = "D4"
#     D5 = "D5"
#     D6 = "D6"
#     DEUTERIUM = "Deuterium"
#     DICHLORETHANE = "Dichloroethane"
#     DIETHYLETHER = "DiethylEther"
#     DIMETHYLCARBONATE = "DimethylCarbonate"
#     DIMETHYLETHER = "DimethylEther"
#     ETHANE = "Ethane"
#     ETHANOL = "Ethanol"
#     ETHYLBENZENE = "EthylBenzene"
#     ETHYLENE = "Ethylene"
#     ETHYLENEOXIDE = "EthyleneOxide"
#     FLUORINE = "Fluorine"
#     HFE143m = "HFE144m"
#     HEAVYWATER = "HeavyWater"
#     HELIUM = "Helium"
#     HYDROGEN = "Hydrogen"
#     HYDROGENCHLORIDE = "HydrogenChloride"
#     HYDROGENSULFIDE = "HydrogenSulfide"
#     ISOBUTANE = "IsoButane"
#     ISOBUTENE = "IsoButene"
#     ISOHEXANE = "Isohexane"
#     ISOPENTANE = "Isopentane"
#     KRYPTON = "Krypton"
#     MD2M = "MD2M"
#     MD3M = "MD3M"
#     MD4M = "MD4M"
#     MDM = "MDM"
#     MM = "MM"
#     METHANE = "Methane"
#     METHANOL = "Methanol"
#     METHYLLINOLEATE = "MethylLinoleate"
#     METHYLLINOLENATE = "MethylLinolenate"
#     METHYLOLEATE = "MethylOleate"
#     METHYLPALMITATE = "MethylPalmitate"
#     METHYLSTEARATE = "MethylStearate"
#     NEON = "Neon"
#     NEOPENTANE = "Neopentane"
#     NITROGEN = "Nitrogen"
#     NITROUSOXIDE = "NitrousOxide"
#     NOVEC649 = "Novec649"
#     ORTHODEUTERIUM = "OrthoDeuterium"
#     ORTHOHYDROGEN = "OrthoHydrogen"
#     OXYGEN = "Oxygen"
#     PARADEUTERIUM = "ParaDeuterium"
#     PARAHYDROGEN = "ParaHydrogen"
#     PROPYLENE = "Propylene"
#     PROPYNE = "Propyne"
#     R11 = "R11"
#     R113 = "R113"
#     R114 = "R114"
#     R115 = "R115"
#     R116 = "R116"
#     R12 = "R12"
#     R123 = "R123"
#     R1233ZD_E = "R1233zd(E)"
#     R1234YF = "R1234yf"
#     R1234ZE_E = "R1234ze(E)"
#     R1234ZE_Z = "R1234ze(Z)"
#     R124 = "R124"
#     R1234ZF = "R1243zf"
#     R125 = "R125"
#     R13 = "R13"
#     R134a = "R134a"
#     R13I1 = "R13I1"
#     R14 = "R14"
#     R141B = "R141b"
#     R142B = "R142b"
#     R143A = "R143a"
#     R152A = "R152A"
#     R161 = "R161"
#     R21 = "R21"
#     R218 = "R218"
#     R22 = "R22"
#     R227EA = "R227EA"
#     R23 = "R23"
#     R236EA = "R236EA"
#     R236FA = "R236FA"
#     R245CA = "R245ca"
#     R245FA = "R245fa"
#     R32 = "R32"
#     R365MFC = "R365MFC"
#     R40 = "R40"
#     R404A = "R404A"
#     R407C = "R407C"
#     R41 = "R41"
#     R410A = "R410A"
#     R507A = "R507A"
#     RC318 = "RC318"
#     SES36 = "SES36"
#     SULFURDIOXIDE = "SulfurDioxide"
#     SULFURHEXAFLUORIDE = "SulfurHexafluoride"
#     TOLUENE = "Toluene"
#     WATER = "Water"
#     XENON = "Xenon"
#     CIS_2_BUTENE = "cis-2-Butene"
#     M_XYLENE = "m-Xylene"
#     N_BUTANE = "n-Butane"
#     N_DECANE = "n-Decane"
#     N_DODECANE = "n-Dodecane"
#     N_HEPTANE = "n-Heptane"
#     N_HEXANE = "n-Hexane"
#     N_NONANE = "n-Nonane"
#     N_OCTANE = "n-Octane"
#     P_PENTANE = "n-Pentane"
#     N_PROPANE = "n-Propane"
#     N_UNDECANE = "n-Undecane"
#     O_XYLENE = "o-Xylene"
#     P_XYLENE = "p-Xylene"
#     TRANS_2_BUTENE = "trans-2-Butene"


# class CoolPropIncompPureFluids(Enum):
#     AS10 = "AS10"
#     AS20 = "AS20"
#     AS30 = "AS30"
#     AS40 = "AS40"
#     AS55 = "AS55"
#     DEB = "DEB"
#     DSF = "DSF"
#     DOWJ = "DowJ"
#     DOWJ2 = "DowJ2"
#     DOWQ = "DowQ"
#     DOWQ2 = "DowQ2"
#     HC10 = "HC10"
#     HC20 = "HC20"
#     HC30 = "HC30"
#     HC40 = "HC40"
#     HC50 = "HC50"
#     HCB = "HCB"
#     HCM = "HCM"
#     HFE = "HFE"
#     HFE2 = "HFE2"
#     HY20 = "HY20"
#     HY30 = "HY30"
#     HY40 = "HY40"
#     HY45 = "HY45"
#     HY50 = "HY50"
#     NBS = "NBS"
#     NAK = "NaK"
#     PBB = "PBB"
#     PCL = "PCL"
#     PCR = "PCR"
#     PGLT = "PGLT"
#     PHE = "PHE"
#     PHR = "PHR"
#     PLR = "PLR"
#     PMR = "PMR"
#     PMS1 = "PMS1"
#     PMS2 = "PMS2"
#     PNF = "PNF"
#     PNF2 = "PNF2"
#     S800 = "S800"
#     SAB = "SAB"
#     T66 = "T66"
#     T72 = "T72"
#     TCO = "TCO"
#     TD12 = "TD12"
#     TVP1 = "TVP1"
#     TVP1869 = "TVP1869"
#     TX22 = "TX22"
#     TY10 = "TY10"
#     TY15 = "TY15"
#     TY20 = "TY20"
#     TY24 = "TY24"
#     WATER = "Water"
#     XLT = "XLT"
#     XLT2 = "XLT2"
#     ZS10 = "ZS10"
#     ZS25 = "ZS25"
#     ZS40 = "ZS40"
#     ZS45 = "ZS45"
#     ZS55 = "ZS55"


# class CoolPropIncompMixturesMassBased(Enum):
#     FRE = "FRE"
#     ICEEA = "IceEA"
#     ICENA = "IceNA"
#     ICEPG = "IcePG"
#     LIBR = "LiBr"
#     MAM = "MAM"
#     MAM2 = "MAM2"
#     MCA = "MCA"
#     MCA2 = "MCA2"
#     MEA = "MEA"
#     MEA2 = "MEA2"
#     MEG = "MEG"
#     MEG2 = "MEG2"
#     MGL = "MGL"
#     MGL2 = "MGL2"
#     MITSW = "MITSW"
#     MKA = "MKA"
#     MKA2 = "MKA2"
#     MKC = "MKC"
#     MKC2 = "MKC2"
#     MKF = "MKF"
#     MLI = "MLI"
#     MMA = "MMA"
#     MMA2 = "MMA2"
#     MMG = "MMG"
#     MMG2 = "MMG2"
#     MNA = "MNA"
#     MNA2 = "MNA2"
#     MPG = "MPG"
#     MPG2 = "MPG2"
#     VCA = "VCA"
#     VKC = "VKC"
#     VMA = "VMA"
#     VMG = "VMG"
#     VNA = "VNA"


# class CoolPropIncompMixturesVolumeBased(Enum):
#     AEG = "AEG"
#     AKF = "AKF"
#     AL = "AL"
#     AN = "AN"
#     APG = "APG"
#     GKN = "GKN"
#     PK2 = "PK2"
#     PKL = "PKL"
#     ZAC = "ZAC"
#     ZFC = "ZFC"
#     ZLC = "ZLC"
#     ZM = "ZM"
#     ZMC = "ZMC"


# # CoolProp fluid class
# class CoolPropFluid:
#     """CoolProp fluid class.

#     The CoolProp fluid class wraps and includes all available fluids in CoolProp
#     and provides the correct strings for the CoolProp library.

#     """

#     def __init__(
#         self: CoolPropFluid,
#         fluid_name: Union[
#             CoolPropPureFluids,
#             List[CoolPropPureFluids],
#             CoolPropIncompPureFluids,
#             CoolPropIncompMixturesMassBased,
#             CoolPropIncompMixturesVolumeBased,
#         ],
#         fluid_full_name: str,
#         fluid_type: CoolPropFluidTypes,
#         fluid_fraction: Optional[List[np.float64]] = None,
#     ) -> None:
#         """Initialize CoolProp fluid class.

#         The init function of the CoolProp fluid class.

#         """
#         if fluid_fraction is None:
#             fluid_fraction = [np.float64(1.0)]

#         # Checks
#         if fluid_type in [CoolPropFluidTypes.PURE, CoolPropFluidTypes.INCOMP]:
#             if isinstance(
#                 fluid_name, (CoolPropPureFluids, CoolPropIncompPureFluids),
#             ) and isinstance(fluid_fraction, list):
#                 if not len(fluid_fraction) == 1 and fluid_fraction[0] == 1.0:
#                     logger.error("Fluid_fraction must equal [1.0].")
#                     raise Exception
#             else:
#                 logger.error(
#                     (
#                         "Fluid must be of type CoolPropPureFluids or "
#                         "CoolPropIncompPureFluids and fluid_fraction must "
#                         "be of type list for pure and pure incompressible fluids."
#                     )
#                 )
#                 raise Exception
#         elif fluid_type == CoolPropFluidTypes.MIXTURE:
#             if isinstance(fluid_name, list) and isinstance(fluid_fraction, list):
#                 if not len(fluid_name) == len(fluid_fraction):
#                     logger.error("Length of lists fluid and fluid_fraction not equal.")
#                     raise Exception
#             else:
#                 logger.error("Fluid and fluid_fraction must be a list for mixtures.")
#                 raise Exception
#         elif fluid_type == CoolPropFluidTypes.INCOMPMIXTURE:
#             if isinstance(
#                 fluid_name,
#                 (CoolPropIncompMixturesMassBased, CoolPropIncompMixturesVolumeBased),
#             ) and isinstance(fluid_fraction, list):
#                 if not len(fluid_fraction) == 2:
#                     logger.error("Length of list fluid_fraction must equal 2.")
#                     raise Exception
#             else:
#                 logger.error(
#                     (
#                         "Fluid must be of type CoolPropIncompMixturesMassBased or "
#                         "CoolPropIncompMixturesVolumeBased and fluid_fraction must "
#                         "be of type list for incompressible mixtures."
#                     )
#                 )
#                 raise Exception
#         else:
#             logger.error("CoolPropFluidTypes not defined correctly.")
#             raise Exception

#         self._fluid_name = fluid_name
#         self._fluid_full_name = fluid_full_name
#         self._fluid_type = fluid_type
#         self._fluid_fraction = fluid_fraction

#     @classmethod
#     def new_pure_fluid(
#         cls: Type[CoolPropFluid], fluid_name: CoolPropPureFluids,
#     ) -> CoolPropFluid:
#         return cls(
#             fluid_name=fluid_name,
#             fluid_full_name=fluid_name.value,
#             fluid_type=CoolPropFluidTypes.PURE,
#         )

#     @classmethod
#     def new_mixture(
#         cls: Type[CoolPropFluid],
#         fluid_names: List[CoolPropPureFluids],
#         fractions: List[np.float64],
#     ) -> CoolPropFluid:
#         if len(fluid_names) == len(fractions):
#             if np.array(fractions).sum() == 1.0:
#                 fluid_full_name = str()
#                 for i, fluid in enumerate(fluid_names):
#                     fluid_full_name += str(fluid)
#                     fluid_full_name += "[" + str(fractions[i]) + "]"
#                     if i < len(fluid_names):
#                         fluid_full_name += "&"
#             else:
#                 logger.error(
#                     "Sum of the fluid fractions must be 1.0: %f != 1.0",
#                     np.array(fractions).sum(),
#                 )
#                 raise Exception
#         else:
#             logger.error(
#                 "Length of the lists fluids and fractions must be equal: %i == %i",
#                 len(fluid_names),
#                 len(fractions),
#             )
#             raise Exception

#         return cls(
#             fluid_name=fluid_names,
#             fluid_full_name=fluid_full_name,
#             fluid_type=CoolPropFluidTypes.MIXTURE,
#             fluid_fraction=fractions,
#         )

#     @classmethod
#     def new_incomp(
#         cls: Type[CoolPropFluid], fluid_name: CoolPropIncompPureFluids
#     ) -> CoolPropFluid:
#         return cls(
#             fluid_name=fluid_name,
#             fluid_full_name=fluid_name.value,
#             fluid_type=CoolPropFluidTypes.INCOMP,
#         )

#     @classmethod
#     def new_incomp_mass_based(
#         cls: Type[CoolPropFluid],
#         fluid_name: CoolPropIncompMixturesMassBased,
#         fraction: np.float64,
#     ) -> CoolPropFluid:
#         fluid_full_name = fluid_name.value + "[" + str(fraction) + "]"
#         return cls(
#             fluid_name=fluid_name,
#             fluid_full_name=fluid_full_name,
#             fluid_type=CoolPropFluidTypes.INCOMPMIXTURE,
#             fluid_fraction=[1.0 - fraction, fraction],
#         )

#     @classmethod
#     def new_incomp_volume_based(
#         cls: Type[CoolPropFluid],
#         fluid_name: CoolPropIncompMixturesVolumeBased,
#         fraction: np.float64,
#     ) -> CoolPropFluid:
#         fluid_full_name = fluid_name.value + "[" + str(fraction) + "]"
#         return cls(
#             fluid_name=fluid_name,
#             fluid_full_name=fluid_full_name,
#             fluid_type=CoolPropFluidTypes.INCOMPMIXTURE,
#             fluid_fraction=[1.0 - fraction, fraction],
#         )

#     @property
#     def fluid_name(
#         self: CoolPropFluid,
#     ) -> Union[
#         CoolPropPureFluids,
#         List[CoolPropPureFluids],
#         CoolPropIncompPureFluids,
#         CoolPropIncompMixturesMassBased,
#         CoolPropIncompMixturesVolumeBased,
#     ]:
#         return self._fluid_name

#     @property
#     def fluid_full_name(self: CoolPropFluid) -> str:
#         return self._fluid_full_name

#     @property
#     def fluid_type(self: CoolPropFluid) -> CoolPropFluidTypes:
#         return self._fluid_type

#     @property
#     def fluid_fraction(self: CoolPropFluid) -> List[np.float64]:
#         return self._fluid_fraction


# # Media classes as derivation of base state class
# class MediumCoolProp(MediumBase):
#     """MediumCoolProp class.

#     The MediumCoolProp class is a wrapper around the low-level interface of CoolProp
#     with the AbstractState object.

#     """

#     def __init__(
#         self: MediumCoolProp,
#         state: AbstractState,
#         fluid: CoolPropFluid,
#         backend: CoolPropBackends = CoolPropBackends.HEOS,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> None:
#         """Initialize MediumCoolProp class.

#         The init function of the MediumCoolProp class.

#         """
#         # Class parameters
#         self._state = state
#         self._fluid = fluid
#         self._backend = backend
#         self._m_flow = m_flow

#     def copy(self: MediumCoolProp) -> MediumCoolProp:
#         """Copy the MediumCoolProp class object.

#         Magic method to copy the class object.

#         """
#         return MediumCoolProp.from_ph(
#             p=np.float64(self._state.p()),
#             h=np.float64(self._state.hmass()),
#             fluid=self._fluid,
#             backend=self._backend,
#             m_flow=self._m_flow,
#         )

#     @classmethod
#     def from_pT(
#         cls: Type[MediumCoolProp],
#         p: np.float64,
#         T: np.float64,
#         fluid: CoolPropFluid,
#         backend: CoolPropBackends = CoolPropBackends.HEOS,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> MediumCoolProp:
#         if (
#             fluid.fluid_type == CoolPropFluidTypes.INCOMP
#             or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
#         ) and backend != CoolPropBackends.INCOMP:
#             logger.error(
#                 "Incompressible fluids and mixtures must use the INCOMP backend."
#             )
#             raise Exception

#         state = AbstractState(backend.value, fluid.fluid_full_name)
#         state.update(CoolProp.PT_INPUTS, p, T)
#         return cls(state=state, fluid=fluid, backend=backend, m_flow=m_flow)

#     @classmethod
#     def from_px(
#         cls: Type[MediumCoolProp],
#         p: np.float64,
#         x: np.float64,
#         fluid: CoolPropFluid,
#         backend: CoolPropBackends = CoolPropBackends.HEOS,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> MediumCoolProp:
#         if (
#             fluid.fluid_type == CoolPropFluidTypes.INCOMP
#             or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
#         ) and backend != CoolPropBackends.INCOMP:
#             logger.error(
#                 "Incompressible fluids and mixtures must use the INCOMP backend."
#             )
#             raise Exception

#         state = AbstractState(backend.value, fluid.fluid_full_name)
#         state.update(CoolProp.PQ_INPUTS, p, x)
#         return cls(state=state, fluid=fluid, backend=backend, m_flow=m_flow)

#     @classmethod
#     def from_Tx(
#         cls: Type[MediumCoolProp],
#         T: np.float64,
#         x: np.float64,
#         fluid: CoolPropFluid,
#         backend: CoolPropBackends = CoolPropBackends.HEOS,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> MediumCoolProp:
#         if (
#             fluid.fluid_type == CoolPropFluidTypes.INCOMP
#             or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
#         ) and backend != CoolPropBackends.INCOMP:
#             logger.error(
#                 "Incompressible fluids and mixtures must use the INCOMP backend."
#             )
#             raise Exception

#         state = AbstractState(backend.value, fluid.fluid_full_name)
#         state.update(CoolProp.QT_INPUTS, x, T)
#         return cls(state=state, fluid=fluid, backend=backend, m_flow=m_flow)

#     @classmethod
#     def from_ph(
#         cls: Type[MediumCoolProp],
#         p: np.float64,
#         h: np.float64,
#         fluid: CoolPropFluid,
#         backend: CoolPropBackends = CoolPropBackends.HEOS,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> MediumCoolProp:
#         if (
#             fluid.fluid_type == CoolPropFluidTypes.INCOMP
#             or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
#         ) and backend != CoolPropBackends.INCOMP:
#             logger.error(
#                 "Incompressible fluids and mixtures must use the INCOMP backend."
#             )
#             raise Exception

#         state = AbstractState(backend.value, fluid.fluid_full_name)
#         state.update(CoolProp.HmassP_INPUTS, h, p)
#         return cls(state=state, fluid=fluid, backend=backend, m_flow=m_flow)

#     @classmethod
#     def from_Th(
#         cls: Type[MediumCoolProp],
#         T: np.float64,
#         h: np.float64,
#         fluid: CoolPropFluid,
#         backend: CoolPropBackends = CoolPropBackends.HEOS,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> MediumCoolProp:
#         if (
#             fluid.fluid_type == CoolPropFluidTypes.INCOMP
#             or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
#         ) and backend != CoolPropBackends.INCOMP:
#             logger.error(
#                 "Incompressible fluids and mixtures must use the INCOMP backend."
#             )
#             raise Exception

#         state = AbstractState(backend.value, fluid.fluid_full_name)
#         state.update(CoolProp.HmassT_INPUTS, h, T)
#         return cls(state=state, fluid=fluid, backend=backend, m_flow=m_flow)

#     @classmethod
#     def from_generic(
#         cls: Type[MediumCoolProp],
#         input_type: CoolPropInputTypes,
#         prop1: np.float64,
#         prop2: np.float64,
#         fluid: CoolPropFluid,
#         backend: CoolPropBackends = CoolPropBackends.HEOS,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> MediumCoolProp:
#         if (
#             fluid.fluid_type == CoolPropFluidTypes.INCOMP
#             or fluid.fluid_type == CoolPropFluidTypes.INCOMPMIXTURE
#         ) and backend != CoolPropBackends.INCOMP:
#             logger.error(
#                 "Incompressible fluids and mixtures must use the INCOMP backend."
#             )
#             raise Exception

#         state = AbstractState(backend.value, fluid.fluid_full_name)
#         state.update(input_type.value, prop1, prop2)
#         return cls(state=state, fluid=fluid, backend=backend, m_flow=m_flow)

#     @property
#     def fluid(self: MediumCoolProp) -> CoolPropFluid:
#         return self._fluid

#     @property
#     def fluid_name(
#         self: MediumCoolProp,
#     ) -> Union[
#         CoolPropPureFluids,
#         List[CoolPropPureFluids],
#         CoolPropIncompPureFluids,
#         CoolPropIncompMixturesMassBased,
#         CoolPropIncompMixturesVolumeBased,
#     ]:
#         return self._fluid.fluid_name

#     @property
#     def fluid_full_name(self: MediumCoolProp) -> str:
#         return self._fluid.fluid_full_name

#     @property
#     def fluid_type(self: MediumCoolProp) -> CoolPropFluidTypes:
#         return self._fluid.fluid_type

#     @property
#     def fluid_fraction(self: MediumCoolProp) -> List[np.float64]:
#         return self._fluid.fluid_fraction

#     @property
#     def backend(self: MediumCoolProp) -> CoolPropBackends:
#         return self._backend

#     @property
#     def cpmass(self: MediumCoolProp) -> np.float64:
#         """Mass-specific heat at constant pressure in J/kg/K.

#         Returns:
#             np.float64: Specific heat at constant pressure in J/kg/K

#         """
#         return np.float64(self._state.cpmass())

#     @property
#     def cpmolar(self: MediumCoolProp) -> np.float64:
#         """Molar-specific heat at constant pressure in J/mol/K.

#         Returns:
#             np.float64: Specific heat at constant pressure in J/mol/K

#         """
#         return np.float64(self._state.cpmolar())

#     @property
#     def cvmass(self: MediumCoolProp) -> np.float64:
#         """Mass-specific heat at constant volume in J/kg/K.

#         Returns:
#             np.float64: Specific heat at constant volume in J/kg/K

#         """
#         return np.float64(self._state.cvmass())

#     @property
#     def cvmolar(self: MediumCoolProp) -> np.float64:
#         """Molar-specific heat at constant volume in J/mol/K.

#         Returns:
#             np.float64: Specific heat at constant volume in J/mol/K

#         """
#         return np.float64(self._state.cvmolar())

#     @property
#     def hmass(self: MediumCoolProp) -> np.float64:
#         """Mass-specific enthalpy in J/kg.

#         Returns:
#             np.float64: Mass-specific enthalpy in J/kg

#         """
#         return np.float64(self._state.hmass())

#     @property
#     def hmolar(self: MediumCoolProp) -> np.float64:
#         """Molar-specific enthalpy in J/mol.

#         Returns:
#             np.float64: Mass-specific enthalpy in J/mol

#         """
#         return np.float64(self._state.hmolar())

#     @property
#     def conductivity(self: MediumCoolProp) -> np.float64:
#         """Thermal conductivity in W/m/K.

#         Returns:
#             np.float64: Thermal conductivity in W/m/K

#         """
#         return np.float64(self._state.conductivity())

#     @property
#     def viscosity(self: MediumCoolProp) -> np.float64:
#         """Viscosity in Pa*s.

#         Returns:
#             np.float64: Viscosity in Pa*s

#         """
#         return np.float64(self._state.viscosity())

#     @property
#     def p(self: MediumCoolProp) -> np.float64:
#         """Pressure in Pa.

#         Returns:
#             np.float64: Pressure in Pa

#         """
#         return np.float64(self._state.p())

#     @property
#     def rhomass(self: MediumCoolProp) -> np.float64:
#         """Mass-specific density in kg/m**3.

#         Returns:
#             np.float64: Density in kg/m**3

#         """
#         return np.float64(self._state.rhomass())

#     @property
#     def rhomolar(self: MediumCoolProp) -> np.float64:
#         """Molar-specific density in mol/m**3.

#         Returns:
#             np.float64: Density in mol/m**3

#         """
#         return np.float64(self._state.rhomolar())

#     @property
#     def R_s(self: MediumCoolProp) -> np.float64:
#         """Specific gas constant in J/kg/K.

#         Returns:
#             np.float64: Specific gas constant in J/kg/K

#         """
#         return np.float64(self._state.gas_constant() / self._state.M())

#     @property
#     def M(self: MediumBase) -> np.float64:
#         """Molar mass in kg/mol.

#         Returns:
#             np.float64: Molar mass in kg/mol

#         """
#         return np.float64(self._state.M())

#     @property
#     def m_flow(self: MediumCoolProp) -> np.float64:
#         """Mass flow in kg/s.

#         Returns:
#             np.float64: Mass flow in kg/s

#         """
#         return self._m_flow

#     @m_flow.setter
#     def m_flow(self: MediumCoolProp, value: np.float64) -> None:
#         """Mass flow in kg/s.

#         Returns:
#             np.float64: Mass flow in kg/s

#         """
#         self._m_flow = value

#     @property
#     def n_flow(self: MediumCoolProp) -> np.float64:
#         """Amount of substance flow in mol/s.

#         Returns:
#             np.float64: Amount of substance flow in mol/s

#         """
#         return self._m_flow / self._state.M()

#     @n_flow.setter
#     def n_flow(self: MediumCoolProp, value: np.float64) -> None:
#         """Amount of substance flow in mol/s.

#         Returns:
#             np.float64: Amount of substance flow in mol/s

#         """
#         self._m_flow = value * self._state.M()

#     @property
#     def smass(self: MediumCoolProp) -> np.float64:
#         """Mass-specific entropy in J/kg/K.

#         Returns:
#             np.float64: Mass-specific entropy in J/kg/K

#         """
#         return np.float64(self._state.smass())

#     @property
#     def smolar(self: MediumCoolProp) -> np.float64:
#         """Molar-specific entropy in J/mol/K.

#         Returns:
#             np.float64: Mass-specific entropy in J/mol/K

#         """
#         return np.float64(self._state.smolar())

#     @property
#     def T(self: MediumCoolProp) -> np.float64:
#         """Temperature in K.

#         Returns:
#             np.float64: Temperature in K

#         """
#         return np.float64(self._state.T())

#     @property
#     def vmass(self: MediumCoolProp) -> np.float64:
#         """Mass-specific volume in m**3/kg.

#         Returns:
#             np.float64: Specific volume in m**3/kg

#         """
#         return np.float64(1.0 / self._state.rhomass())

#     @property
#     def vmolar(self: MediumCoolProp) -> np.float64:
#         """Molar-specific volume in m**3/mol.

#         Returns:
#             np.float64: Specific volume in m**3/mol

#         """
#         return np.float64(1.0 / self._state.rhomolar())

#     @property
#     def x(self: MediumCoolProp) -> np.float64:
#         """Vapor quality.

#         Returns:
#             np.float64: Vapor quality

#         """
#         return np.float64(self._state.Q())

#     @property
#     def Z(self: MediumCoolProp) -> np.float64:
#         """Compressibility factor.

#         Returns:
#             np.float64: Compressibility factor

#         """
#         return np.float64(self._state.compressibility_factor())

#     @property
#     def phase(self: MediumCoolProp) -> StatePhases:
#         """State phase.

#         Returns:
#             StatePhases: State phase

#         """
#         if self._backend == CoolPropBackends.INCOMP:
#             return StatePhases(0)

#         return StatePhases(self._state.phase())

#     @property
#     def Gmass(self: MediumCoolProp) -> np.float64:
#         """Mass specific Gibbs energy in J/kg.

#         Returns:
#             np.float64: Mass specific Gibbs energy in J/kg

#         """
#         ...
#         return np.float64(self._state.gibbsmass())

#     @property
#     def Gmolar(self: MediumCoolProp) -> np.float64:
#         """Molar specific Gibbs energy in J/mol.

#         Returns:
#             np.float64: Molar specific Gibbs energy in J/mol

#         """
#         ...
#         return np.float64(self._state.gibbsmolar())

#     @property
#     def Helmholtzmass(self: MediumCoolProp) -> np.float64:
#         """Mass specific Helmholtz energy in J/kg.

#         Returns:
#             np.float64: Mass specific Helmholtz energy in J/kg

#         """
#         ...
#         return np.float64(self._state.helmholtzmass())

#     @property
#     def Helmholtzmolar(self: MediumCoolProp) -> np.float64:
#         """Molar specific Helmholtz energy in J/mol.

#         Returns:
#             np.float64: Molar specific Helmholtz energy in J/mol

#         """
#         ...
#         return np.float64(self._state.helmholtzmolar())

#     @property
#     def p_critical(self: MediumCoolProp) -> np.float64:
#         """Pressure at the critical point in Pa.

#         Returns:
#             np.float64: Pressure at the critical point in Pa

#         """
#         ...
#         return np.float64(self._state.p_critical())

#     @property
#     def p_reducing(self: MediumCoolProp) -> np.float64:
#         """Pressure at reducing point in Pa.

#         Returns:
#             np.float64: Pressure at reducing point in Pa

#         """
#         ...
#         return np.float64(self._state.p_reducing())

#     @property
#     def p_triple(self: MediumCoolProp) -> np.float64:
#         """Pressure at triple point in Pa.

#         Returns:
#             np.float64: Pressure at triple point in Pa

#         """
#         ...
#         return np.float64(self._state.p_triple())

#     @property
#     def rhomass_critical(self: MediumCoolProp) -> np.float64:
#         """Mass density at critical point in kg/m**3.

#         Returns:
#             np.float64: Mass density at critical point in kg/m**3

#         """
#         ...
#         return np.float64(self._state.rhomass_critical())

#     @property
#     def rhomass_reducing(self: MediumCoolProp) -> np.float64:
#         """Mass density at reducing point in kg/m**3.

#         Returns:
#             np.float64: Mass density at reducing point in kg/m**3

#         """
#         ...
#         return np.float64(self._state.rhomass_reducing())

#     @property
#     def rhomolar_critical(self: MediumCoolProp) -> np.float64:
#         """Molar density at critical point in mol/m**3.

#         Returns:
#             np.float64: Molar density at critical point in mol/m**3

#         """
#         ...
#         return np.float64(self._state.rhomolar_critical())

#     @property
#     def rhomolar_reducing(self: MediumCoolProp) -> np.float64:
#         """Molar density at reducing point in mol/m**3.

#         Returns:
#             np.float64: Molar density at reducing point in mol/m**3

#         """
#         ...
#         return np.float64(self._state.rhomolar_reducing())

#     @property
#     def surface_tension(self: MediumCoolProp) -> np.float64:
#         """Surface tension in N/m.

#         Returns:
#             np.float64: Surface tension in N/m

#         """
#         ...
#         return np.float64(self._state.surface_tension())

#     @property
#     def T_critical(self: MediumCoolProp) -> np.float64:
#         """Temperature at critical point in K.

#         Returns:
#             np.float64: Temperature at critical point in K

#         """
#         ...
#         return np.float64(self._state.T_critical())

#     @property
#     def T_reducing(self: MediumCoolProp) -> np.float64:
#         """Temperature at reducing point in K.

#         Returns:
#             np.float64: Temperature at reducing point in K

#         """
#         ...
#         return np.float64(self._state.T_reducing())

#     @property
#     def T_triple(self: MediumCoolProp) -> np.float64:
#         """Temperature at triple point in K.

#         Returns:
#             np.float64: Temperature at triple point in K

#         """
#         ...
#         return np.float64(self._state.T_triple())

#     def set_pT(self: MediumCoolProp, p: np.float64, T: np.float64) -> None:
#         self._state.update(CoolProp.PT_INPUTS, p, T)

#     def set_px(self: MediumCoolProp, p: np.float64, x: np.float64) -> None:
#         self._state.update(CoolProp.PQ_INPUTS, p, x)

#     def set_Tx(self: MediumCoolProp, T: np.float64, x: np.float64) -> None:
#         self._state.update(CoolProp.QT_INPUTS, x, T)

#     def set_ph(self: MediumCoolProp, p: np.float64, h: np.float64) -> None:
#         self._state.update(CoolProp.HmassP_INPUTS, h, p)

#     def set_Th(self: MediumCoolProp, T: np.float64, h: np.float64) -> None:
#         self._state.update(CoolProp.HmassT_INPUTS, h, T)

#     def set_ps(self: MediumCoolProp, p: np.float64, s: np.float64) -> None:
#         self._state.update(CoolProp.PSmass_INPUTS, p, s)

#     def set_Ts(self: MediumCoolProp, T: np.float64, s: np.float64) -> None:
#         self._state.update(CoolProp.SmassT_INPUTS, s, T)

#     def set_state_generic(
#         self: MediumCoolProp,
#         input_type: CoolPropInputTypes,
#         prop1: np.float64,
#         prop2: np.float64,
#     ) -> None:
#         self._state.update(input_type.value, prop1, prop2)

#     def get_state_generic(
#         self: MediumCoolProp, output_type: CoolPropOutputTypes,
#     ) -> np.float64:
#         return np.float64(self._state.keyed_output(output_type))

#     def get_state_generic_list(
#         self: MediumCoolProp, output_types: List[CoolPropOutputTypes],
#     ) -> List[np.float64]:
#         return [np.float64(self._state.keyed_output(k)) for k in output_types]


if __name__ == "__main__":
    logger.info("This is the media refprop library.")

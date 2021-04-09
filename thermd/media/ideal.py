# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

from __future__ import annotations

from CoolProp.CoolProp import PropsSI
from CoolProp.HumidAirProp import HAPropsSI
import math
import numpy as np
from scipy import optimize as opt
from thermd.core import MediumBase, MediumHumidAir
from thermd.helper import get_logger

# Initialize global logger
logger = get_logger(__name__)


# Media classes as derivation of base state class
# class MediumIdeal(MediumBase):
#     """MediumIdeal class.

#     The MediumIdeal class implements the ideal gas law for pure and pseudo-pure fluids.

#     """

#     def __init__(
#         self: MediumIdeal,
#         name: str,
#         p: np.float64,
#         T: np.float64,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> None:
#         """Initialize MediumIdeal class.

#         The init function of the MediumIdeal class.

#         """
#         super().__init__(name=name)

#         # Class parameters
#         self._p = p
#         self._T = T
#         self._m_flow = m_flow


# class MediumIdealHumidAir(MediumHumidAir):
#     """MediumIdealHumidAir class.

#     The MediumIdealHumidAir class is an interface to the
#     CoolProp HumidAirProp module.

#     """

#     def __init__(
#         self: MediumIdealHumidAir,
#         name: str,
#         p: np.float64,
#         T: np.float64,
#         w: np.float64,
#         m_flow: np.float64 = np.float64(0.0),
#     ) -> None:
#         """Initialize MediumIdealHumidAir class.

#         The init function of the MediumIdealHumidAir class.

#         """
#         super().__init__(name=name)

#         # Class parameters
#         self._p = p
#         self._T = T
#         self._w = w
#         self._m_flow = m_flow

#         # Constants
#         self._R_air = np.float64(287.0474730938159)
#         self._R_water = np.float64(461.5230869726723)

#         # self._cp_air_poly = np.poly1d(
#         #     [-1.02982783e-07, 4.29730845e-04, 1.46305349e-02, 1.00562420e03]
#         # )
#         # self._cp_water_vapor_poly = np.poly1d(
#         #     [
#         #         3.05228669e-11,
#         #         -1.57712722e-08,
#         #         1.04676045e-06,
#         #         1.27256322e-03,
#         #         1.82289816e-01,
#         #         1.85835959e03,
#         #     ]
#         # )
#         # self._cp_water_liquid_poly = np.poly1d(
#         #     [
#         #         -9.13327305e-14,
#         #         9.89764971e-11,
#         #         -4.24011913e-08,
#         #         9.47137661e-06,
#         #         -1.15186890e-03,
#         #         8.34474494e-02,
#         #         -2.98605473e00,
#         #         4.21866441e03,
#         #     ]
#         # )
#         self._cp_water_ice_poly = np.poly1d(
#             [-1.03052963e-04, -2.77224838e-02, 4.87648024e00, 2.05097273e03]
#         )
#         # self._cv_air = np.float64(718)
#         # self._cv_water_vapor = np.float64(1435.9)

#         # self._delta_h_evaporation = np.float64(2500900)
#         self._delta_h_melting = np.float64(333400)

#         self._T_triple = np.float64(273.16)
#         self._p_triple = np.float64(611.657 / 10 ** 5)

#         # Reference state
#         self._h_humid_air_0 = np.float64(
#             HAPropsSI("H", "T", self._T_triple, "P", self._p_triple * 10 ** 5, "R", 0)
#         )
#         self._h_water_liquid_0 = np.float64(
#             PropsSI("H", "T", self._T_triple, "P", self._p_triple * 10 ** 5, "Water")
#         )
#         self._h_water_ice_0 = np.float64(0.0)
#         self._s_humid_air_0 = np.float64(
#             HAPropsSI("S", "T", self._T_triple, "P", self._p_triple * 10 ** 5, "R", 0)
#         )
#         self._s_water_liquid_0 = np.float64(
#             PropsSI("S", "T", self._T_triple, "P", self._p_triple * 10 ** 5, "Water")
#         )
#         self._s_water_ice_0 = np.float64(0.0)

#     @property
#     def cpmass(self: MediumIdealHumidAir) -> np.float64:
#         """Mass-specific heat at constant pressure in J/kg/K.

#         Returns:
#             np.float64: Specific heat at constant pressure in J/kg/K

#         """
#         if self.ws >= self._w:  # under-saturated
#             cp = HAPropsSI("C", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             cp = HAPropsSI("C", "T", self._T, "P", self._p, "R", 1)

#         return np.float64(cp)

#     @property
#     def cpmolar(self: MediumIdealHumidAir) -> np.float64:
#         """Molar-specific heat at constant pressure in J/mol/K.

#         Returns:
#             np.float64: Specific heat at constant pressure in J/mol/K

#         """
#         logger.error("Not implemented.")
#         raise SystemExit

#     @property
#     def cvmass(self: MediumIdealHumidAir) -> np.float64:
#         """Mass-specific heat at constant volume in J/kg/K.

#         Returns:
#             np.float64: Specific heat at constant volume in J/kg/K

#         """
#         if self.ws >= self._w:  # under-saturated
#             cv = HAPropsSI("CV", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             cv = HAPropsSI("CV", "T", self._T, "P", self._p, "R", 1)

#         return np.float64(cv)

#     @property
#     def cvmolar(self: MediumIdealHumidAir) -> np.float64:
#         """Molar-specific heat at constant volume in J/mol/K.

#         Returns:
#             np.float64: Specific heat at constant volume in J/mol/K

#         """
#         logger.error("Not implemented.")
#         raise SystemExit

#     @property
#     def hmass(self: MediumIdealHumidAir) -> np.float64:
#         """Mass-specific enthalpy in J/kg.

#         Returns:
#             np.float64: Mass-specific enthalpy in J/kg

#         """
#         return self._h_pTw(p=self._p, T=self._T, w=self._w)

#     @property
#     def hmolar(self: MediumIdealHumidAir) -> np.float64:
#         """Molar-specific enthalpy in J/mol.

#         Returns:
#             np.float64: Mass-specific enthalpy in J/mol

#         """
#         logger.error("Not implemented.")
#         raise SystemExit

#     @property
#     def conductivity(self: MediumIdealHumidAir) -> np.float64:
#         """Thermal conductivity in W/m/K.

#         Returns:
#             np.float64: Thermal conductivity in W/m/K

#         """
#         if self.ws >= self._w:  # under-saturated
#             conductivity = HAPropsSI("K", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             conductivity = HAPropsSI("K", "T", self._T, "P", self._p, "R", 1)

#         return np.float64(conductivity)

#     @property
#     def viscosity(self: MediumIdealHumidAir) -> np.float64:
#         """Dynamic viscosity in Pa*s.

#         Returns:
#             np.float64: Dynamic viscosity in Pa*s

#         """
#         if self.ws >= self._w:  # under-saturated
#             viscosity = HAPropsSI("M", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             viscosity = HAPropsSI("M", "T", self._T, "P", self._p, "R", 1)

#         return np.float64(viscosity)

#     @property
#     def p(self: MediumIdealHumidAir) -> np.float64:
#         """Pressure in Pa.

#         Returns:
#             np.float64: Pressure in Pa

#         """
#         return self._p

#     @property
#     def rhomass(self: MediumIdealHumidAir) -> np.float64:
#         """Mass-specific density in kg/m**3.

#         Returns:
#             np.float64: Density in kg/m**3

#         """
#         if self.ws >= self._w:  # under-saturated
#             rho = 1.0 / HAPropsSI("V", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             rho = 1.0 / HAPropsSI("V", "T", self._T, "P", self._p, "R", 1)

#         return np.float64(rho)

#     @property
#     def rhomolar(self: MediumIdealHumidAir) -> np.float64:
#         """Molar-specific density in mol/m**3.

#         Returns:
#             np.float64: Density in mol/m**3

#         """
#         logger.error("Not implemented.")
#         raise SystemExit

#     @property
#     def gas_constant(self: MediumIdealHumidAir) -> np.float64:
#         """Specific gas constant in J/mol/K.

#         Returns:
#             np.float64: Specific gas constant in J/mol/K

#         """
#         if self._w <= self.ws:  # under-saturated
#             gas_constant = (1 - self._w / (1 + self._w)) * self._R_air + (
#                 self._w / (1 + self._w)
#             ) * self._R_water
#         else:  # saturated
#             gas_constant = (1 - self.ws / (1 + self.ws)) * self._R_air + (
#                 self.ws / (1 + self.ws)
#             ) * self._R_water

#         return gas_constant

#     @property
#     def m_flow(self: MediumIdealHumidAir) -> np.float64:
#         """Mass flow in kg/s.

#         Returns:
#             np.float64: Mass flow in kg/s

#         """
#         return self._m_flow

#     @m_flow.setter
#     def m_flow(self: MediumIdealHumidAir, value: np.float64) -> None:
#         """Mass flow in kg/s.

#         Returns:
#             np.float64: Mass flow in kg/s

#         """
#         self._m_flow = value

#     @property
#     def smass(self: MediumIdealHumidAir) -> np.float64:
#         """Mass-specific entropy in J/kg/K.

#         Returns:
#             np.float64: Mass-specific entropy in J/kg/K

#         """
#         return self._s_pTw(p=self._p, T=self._T, w=self._w)

#     @property
#     def smolar(self: MediumIdealHumidAir) -> np.float64:
#         """Molar-specific entropy in J/mol/K.

#         Returns:
#             np.float64: Mass-specific entropy in J/mol/K

#         """
#         logger.error("Not implemented.")
#         raise SystemExit

#     @property
#     def T(self: MediumIdealHumidAir) -> np.float64:
#         """Temperature in K.

#         Returns:
#             np.float64: Temperature in K

#         """
#         return self._T

#     @property
#     def vmass(self: MediumIdealHumidAir) -> np.float64:
#         """Mass-specific volume in m**3/kg.

#         Returns:
#             np.float64: Specific volume in m**3/kg

#         """
#         if self.ws >= self._w:  # under-saturated
#             v = HAPropsSI("V", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             v = HAPropsSI("V", "T", self._T, "P", self._p, "R", 1)

#         return np.float64(v)

#     @property
#     def vmolar(self: MediumIdealHumidAir) -> np.float64:
#         """Molar-specific volume in m**3/mol.

#         Returns:
#             np.float64: Specific volume in m**3/mol

#         """
#         logger.error("Not implemented.")
#         raise SystemExit

#     @property
#     def x(self: MediumIdealHumidAir) -> np.float64:
#         """Quality.

#         Returns:
#             np.float64: Quality

#         """
#         logger.error("Not implemented.")
#         raise SystemExit

#     @property
#     def Z(self: MediumIdealHumidAir) -> np.float64:
#         """Compressibility factor.

#         Returns:
#             np.float64: Compressibility factor

#         """
#         if self.ws >= self._w:  # under-saturated
#             Z = HAPropsSI("Z", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             Z = HAPropsSI("Z", "T", self._T, "P", self._p, "R", 1)

#         return np.float64(Z)

#     @property
#     def w(self: MediumIdealHumidAir) -> np.float64:
#         """Humidity ratio.

#         Returns:
#             np.float64: Humidity ratio

#         """
#         return self._w

#     @property
#     def ws(self: MediumIdealHumidAir) -> np.float64:
#         """Humidity ratio.

#         Returns:
#             np.float64: Humidity ratio

#         """
#         return self._ws_pT(p=self._p, T=self._T)

#     @property
#     def phi(self: MediumIdealHumidAir) -> np.float64:
#         """Relative humidity.

#         Returns:
#             np.float64: Relative humidity

#         """
#         if self.ws >= self._w:  # under-saturated
#             phi = HAPropsSI("R", "T", self._T, "P", self._p, "W", self._w)

#         else:  # saturated
#             phi = 1.0

#         return np.float64(phi)

#     @staticmethod
#     def __ps_hardy_pT(p: np.float64, T: np.float64) -> np.float64:
#         if T >= 273.15:
#             ps = math.exp(
#                 (-2.8365744) * 10 ** 3 * T ** (-2)
#                 + (-6.028076559) * 10 ** 3 * T ** (-1)
#                 + 1.954263612 * 10 ** 1 * T ** 0
#                 + (-2.737830188) * 10 ** (-2) * T ** 1
#                 + 1.6261698 * 10 ** (-5) * T ** 2
#                 + 7.0229056 * 10 ** (-10) * T ** 3
#                 + (-1.8680009) * 10 ** (-13) * T ** 4
#                 + 2.7150305 * math.log(T)
#             )
#             alpha = (
#                 3.53624 * 10 ** (-4) * (T - 273.15) ** 0
#                 + 2.9328363 * 10 ** (-5) * (T - 273.15) ** 1
#                 + 2.6168979 * 10 ** (-7) * (T - 273.15) ** 2
#                 + 8.5813609 * 10 ** (-9) * (T - 273.15) ** 3
#             )
#             beta = math.exp(
#                 (-1.07588) * 10 ** 1 * (T - 273.15) ** 0
#                 + 6.3268134 * 10 ** (-2) * (T - 273.15) ** 1
#                 + (-2.5368934) * 10 ** (-4) * (T - 273.15) ** 2
#                 + 6.3405286 * 10 ** (-7) * (T - 273.15) ** 3
#             )
#         else:
#             ps = math.exp(
#                 (-5.8666426) * 10 ** 3 * T ** (-1)
#                 + 2.232870244 * 10 ** 1 * T ** 0
#                 + 1.39387003 * 10 ** (-2) * T ** 1
#                 + (-3.4262402) * 10 ** (-5) * T ** 2
#                 + 2.7040955 * 10 ** (-8) * T ** 3
#                 + 6.7063522 * 10 ** (-1) * math.log(T)
#             )
#             alpha = (
#                 3.64449 * 10 ** (-4) * (T - 273.15) ** 0
#                 + 2.9367585 * 10 ** (-5) * (T - 273.15) ** 1
#                 + 4.8874766 * 10 ** (-7) * (T - 273.15) ** 2
#                 + 4.3669918 * 10 ** (-9) * (T - 273.15) ** 3
#             )
#             beta = math.exp(
#                 (-1.07271) * 10 ** 1 * (T - 273.15) ** 0
#                 + 7.6215115 * 10 ** (-2) * (T - 273.15) ** 1
#                 + (-1.7490155) * 10 ** (-4) * (T - 273.15) ** 2
#                 + 2.4668279 * 10 ** (-6) * (T - 273.15) ** 3
#             )

#         f = math.exp(alpha * (1 - (ps / p)) + beta * ((p / ps) - 1))
#         ps *= f

#         return ps

#     def __w_hardy_pTphi(
#         self: MediumIdealHumidAir, p: np.float64, T: np.float64, phi: np.float64
#     ) -> np.float64:
#         ps = self._ps_hardy_pT(p, T)

#         w = abs(0.622 * ((phi * ps) / (p - phi * ps)))
#         return w

#     def __ws_hardy_pT(self: MediumIdealHumidAir, p: np.float64, T: np.float64):
#         ps = self._ps_hardy_pT(p, T)

#         ws = abs(0.622 * (ps / (p - ps)))
#         return ws

#     # def __phi_hardy_pTw(
#     #     self: MediumIdealHumidAir, p: np.float64, T: np.float64, w: np.float64
#     # ) -> np.float64:
#     #     phi = (p / self._ps_hardy_pT(p, T)) * (w / (0.622 + w))
#     #     return phi

#     def __w_pTphi(
#         self: MediumIdealHumidAir, p: np.float64, T: np.float64, phi: np.float64
#     ) -> np.float64:
#         if -100 + 273.15 <= T <= 100 + 273.15:

#             w = np.float64(HAPropsSI("W", "T", T, "P", p, "R", phi))

#         else:
#             logger.debug("Humid air water content out of definition range in CoolProp.")

#             if 0.0 <= phi < 1.0:
#                 w = self._w_hardy_pTphi(p, T, phi)
#             elif phi == 1.0:
#                 w = self._ws_hardy_pT(p, T)
#             else:
#                 logger.error(
#                     "Humid air relative humidity is not between 0 and 1: %f", phi
#                 )
#                 raise SystemExit

#         return w

#     def __ws_pT(self: MediumIdealHumidAir, p: np.float64, T: np.float64) -> np.float64:
#         return self._w_pTphi(p=p, T=T, phi=np.float64(1.0))

#     def __h_pTw(
#         self: MediumIdealHumidAir, p: np.float64, T: np.float64, w: np.float64
#     ) -> np.float64:
#         """Mass-specific enthalpy in J/kg.

#         Returns:
#             np.float64: Mass-specific enthalpy in J/kg

#         """
#         ws = self._ws_pT(p=p, T=T)

#         if ws >= w:  # under saturated
#             h = HAPropsSI("H", "T", T, "P", p, "W", w) - self._h_humid_air_0

#         else:  # saturated
#             if T > self._T_tr:  # saturated with liquid water
#                 h = (
#                     HAPropsSI("H", "T", T, "P", p, "R", 1)
#                     - self._h_humid_air_0
#                     + (w - ws)
#                     * (PropsSI("H", "T", T, "Q", 0, "Water") - self._h_water_liquid_0)
#                 )

#             elif T < self._T_tr:  # saturated with water ice
#                 h = (
#                     HAPropsSI("H", "T", T, "P", p, "R", 1)
#                     - self._h_humid_air_0
#                     + (w - ws)
#                     * (
#                         (
#                             -self._delta_h_melting
#                             + self._cp_water_ice_poly(T - 273.15) * (T - self._T_tr)
#                         )
#                         - self._h_water_ice_0
#                     )
#                 )

#             else:
#                 logger.error("Humid air is not defined at T = T_triple.")
#                 raise SystemExit

#         return np.float64(h)

#     def __s_pTw(
#         self: MediumIdealHumidAir, p: np.float64, T: np.float64, w: np.float64
#     ) -> np.float64:
#         """Mass-specific entropy in J/kg/K.

#         Returns:
#             np.float64: Mass-specific entropy in J/kg/K

#         """
#         ws = self._ws_pT(p=p, T=T)

#         if ws >= w:  # under saturated
#             s = HAPropsSI("S", "T", T, "P", p, "W", w) - self._s_humid_air_0

#         else:  # saturated
#             if T > self._T_tr:  # saturated with liquid water
#                 s = (
#                     HAPropsSI("S", "T", T, "P", p, "R", 1)
#                     - self._s_humid_air_0
#                     + (w - ws)
#                     * (PropsSI("S", "T", T, "Q", 0, "Water") - self._s_water_liquid_0)
#                 )

#             elif T < self._T_tr:  # saturated with water ice
#                 s = (
#                     HAPropsSI("S", "T", T, "P", p, "R", 1)
#                     - self._s_humid_air_0
#                     + (w - ws)
#                     * (
#                         (
#                             (-1.0) * (self._delta_h_melting / self._T_tr)
#                             + self._cp_water_ice_poly(T - 273.15)
#                             * math.log(T)
#                             / self._T_tr
#                         )
#                     )
#                     - self._s_water_ice_0
#                 )

#             else:
#                 logger.error("Humid air is not defined at T = T_triple.")
#                 raise SystemExit

#         return np.float64(s)

#     def __T_phw_fun(
#         self: MediumIdealHumidAir,
#         T: np.float64,
#         p: np.float64,
#         h: np.float64,
#         w: np.float64,
#     ):
#         return h - self._h_pTw(p=p, T=T, w=w)

#     def __T_phw(self: MediumIdealHumidAir, p: np.float64, h: np.float64, w: np.float64):
#         T = opt.fsolve(self._T_phw_fun, self._T, args=(p, h, w))[0]

#         return np.float64(T)

#     def __T_psw_fun(
#         self: MediumIdealHumidAir,
#         T: np.float64,
#         p: np.float64,
#         s: np.float64,
#         w: np.float64,
#     ):
#         return s - self._s_pTw(p=p, T=T, w=w)

#     def __T_psw(self: MediumIdealHumidAir, p: np.float64, s: np.float64, w: np.float64):
#         T = opt.fsolve(self._T_psw_fun, self._T, args=(p, s, w))[0]

#         return np.float64(T)

#     def __p_Thw_fun(
#         self: MediumIdealHumidAir,
#         p: np.float64,
#         T: np.float64,
#         h: np.float64,
#         w: np.float64,
#     ):
#         return h - self._h_pTw(p=p, T=T, w=w)

#     def __p_Thw(self: MediumIdealHumidAir, T: np.float64, h: np.float64, w: np.float64):
#         p = opt.fsolve(self._p_Thw_fun, self._p, args=(T, h, w))[0]

#         return np.float64(p)

#     def __p_Tsw_fun(
#         self: MediumIdealHumidAir,
#         p: np.float64,
#         T: np.float64,
#         s: np.float64,
#         w: np.float64,
#     ):
#         return s - self._s_pTw(p=p, T=T, w=w)

#     def __p_Tsw(self: MediumIdealHumidAir, T: np.float64, s: np.float64, w: np.float64):
#         p = opt.fsolve(self._p_Tsw_fun, self._p, args=(T, s, w))[0]

#         return np.float64(p)

#     def set_pTw(
#         self: MediumIdealHumidAir, p: np.float64, T: np.float64, w: np.float64
#     ) -> None:
#         self._p = p
#         self._T = T
#         self._w = w

#     def set_phw(
#         self: MediumIdealHumidAir, p: np.float64, h: np.float64, w: np.float64
#     ) -> None:
#         self._p = p
#         self._T = self._T_phw(p=p, h=h, w=w)
#         self._w = w

#     def set_Thw(
#         self: MediumIdealHumidAir, T: np.float64, h: np.float64, w: np.float64
#     ) -> None:
#         self._p = self._p_Thw(T=T, h=h, w=w)
#         self._T = T
#         self._w = w

#     def set_psw(
#         self: MediumIdealHumidAir, p: np.float64, s: np.float64, w: np.float64
#     ) -> None:
#         self._p = p
#         self._T = self._T_psw(p=p, s=s, w=w)
#         self._w = w

#     def set_Tsw(
#         self: MediumIdealHumidAir, T: np.float64, s: np.float64, w: np.float64
#     ) -> None:
#         self._p = self._p_Tsw(T=T, s=s, w=w)
#         self._T = T
#         self._w = w


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.warning("Not implemented.")

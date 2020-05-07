# -*- coding: utf-8 -*-

"""
    Berechnungsprozeduren/ -funktionen für die Berechnung der
    Stoffeigenschaften von feuchter Luft.

    Nullpunkt-Festlegung:
        h_l(flideal.T_tr) = 0 für trockene Luft
        h_w(flideal.T_tr) = 0 für flüssiges Wasser
        s_l(flideal.T_tr, flideal.p_tr) = 0 für trockene Luft
        s_w(flideal.T_tr, flideal.p_tr) = 0 für flüssiges Wasser
"""

import logging
import math
from scipy import optimize as opt
from CoolProp.CoolProp import PropsSI
from CoolProp.HumidAirProp import HAPropsSI
from stoffwerte import feuchteluftideal as flideal

# Protokollinstanz definieren
logger = logging.getLogger(__name__)

# Nullpunkt-Festlegung
h_fl_0 = HAPropsSI("H", "T", flideal.T_tr, "P", flideal.p_tr * 10 ** 5, "R", 0)
h_w_f_0 = PropsSI("H", "T", flideal.T_tr, "P", flideal.p_tr * 10 ** 5, "Water")
h_w_e_0 = 0.0
s_fl_0 = HAPropsSI("S", "T", flideal.T_tr, "P", flideal.p_tr * 10 ** 5, "R", 0)
s_w_f_0 = PropsSI("S", "T", flideal.T_tr, "P", flideal.p_tr * 10 ** 5, "Water")
s_w_e_0 = 0.0


def FeuchteLuftSI(
    ausgangsRef,
    eingangsRef1,
    eingangsWert1,
    eingangsRef2,
    eingangsWert2,
    eingangsRef3,
    eingangsWert3,
):
    """
    Hauptfunktion zur Einbindung aller weiteren Funktionen.

    Parameters
    ----------
    ausgangsRef : string
        'H' -- spez. Enthalpie [J/kg] \n
        'S' -- spez. Entropie [J/kg*K] \n
        'D' -- Dichte [kg/m**3] \n
        'C' -- spez. Wärmekapazität bei konstantem Druck [J/kg*K]
        'K' -- Wärmeleitfähigkeit [W/m*K]
        'M' -- Dynamische Viskosität [Pa*s]
    eingangsRef1 : string
        'T' -- Temperatur [K] \n
        'H' -- spez. Enthalpie [J/kg] \n
        'S' -- spez. Entropie (nur bei Berechnung der spez. Enthalpie) [J/kg*K]
    eingangsWert1 : float
        Eingangswert 1 entsprechend der Eingangsreferenz 1
    eingangsRef2 : string
        'P' -- Druck [Pa]
    eingangsWert2 : float
        Eingangswert 2 entsprechend der Eingangsreferenz 2
    eingangsRef3 : string
        'R' -- Relative Luftfeuchte [-]
        'W' -- Gesamter Wassergehalt für gasförmige, flüssige und feste
        Phase des Wassers [kgW/kgtL]
    eingangsWert3 : float
        Eingangswert 3 entsprechend der Eingangsreferenz 3

    Returns
    -------
    ausgangsWert : float
        Ausgangswert entsprechend der Ausgangsreferenz

    Examples
    --------
    >>>  from stoffwerte.feuchteluftideal import FeuchteLuftSI
    >>>  FeuchteLuftSI('H','T',34 + 273.15,'P',2.84 * 10 ** 5,'R',1)
    64538.305078052916

    Notes
    -----
    Gültigkeitsbereich:
        -

    Quelle:
        Baehr, H.-D.: Thermodynamik: Grundlagen und technische Anwendungen.
        Springer Berlin Heidelberg. 2013.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    # Überprüfung des Definitionsbereichs
    if eingangsRef1 == "T":
        if not -143.15 <= eingangsWert1 - 273.15 <= 350:
            logger.warning(
                "Die übergebene Temperatur ist außerhalb des Definitionsbereichs: "
                + "-143.15 <= %s <= 350 °C",
                str(eingangsWert1 - 273.15),
            )
    if eingangsRef2 == "P":
        if not 10 <= eingangsWert2 <= 10 * 10 ** 6:
            logger.warning(
                "Der übergebene Druck ist außerhalb des Definitionsbereichs: "
                + "10 <= %s <= 10 * 10 ** 6 Pa",
                str(eingangsWert2),
            )
    if eingangsRef3 == "R":
        if not 0 <= eingangsWert3 <= 1:
            logger.warning(
                "Die übergebene Luftfeuchtigkeit ist außerhalb des Definitionsbereichs: "
                + "0 <= %s <= 1",
                str(eingangsWert3),
            )
    if eingangsRef3 == "W":
        if not 0 <= eingangsWert3 <= 10:
            logger.warning(
                "Die übergebene Wasserbeladung ist außerhalb des Definitionsbereichs: "
                + "0 <= %s <= 10 kg/kg",
                str(eingangsWert3),
            )

    try:
        if (
            ausgangsRef == "H"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = h_tpx(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "H"
            and eingangsRef1 == "S"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            t = t_spx(eingangsWert1, eingangsWert2 * 10 ** (-5), eingangsWert3)

            ausgangsWert = h_tpx(t, eingangsWert2 * 10 ** (-5), eingangsWert3)

        elif (
            ausgangsRef == "S"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = s_tpx(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "T"
            and eingangsRef1 == "S"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = (
                t_spx(eingangsWert1, eingangsWert2 * 10 ** (-5), eingangsWert3) + 273.15
            )

        elif (
            ausgangsRef == "T"
            and eingangsRef1 == "H"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = (
                t_hpx(eingangsWert1, eingangsWert2 * 10 ** (-5), eingangsWert3) + 273.15
            )

        elif (
            ausgangsRef == "R"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = phi_tpx(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "W"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "R"
        ):

            ausgangsWert = x_tpphi(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "V"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = v_tpx(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "D"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = rho_tpx(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "C"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = cp_tpx(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "K"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = HAPropsSI(
                ausgangsRef,
                eingangsRef1,
                eingangsWert1,
                eingangsRef2,
                eingangsWert2,
                eingangsRef3,
                eingangsWert3,
            )

        elif (
            ausgangsRef == "M"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "W"
        ):

            ausgangsWert = HAPropsSI(
                ausgangsRef,
                eingangsRef1,
                eingangsWert1,
                eingangsRef2,
                eingangsWert2,
                eingangsRef3,
                eingangsWert3,
            )

        else:
            logger.error(
                "Berechnung der Stoffwerte gescheitert! Die Referenzen sind fehlerhaft"
            )
            ausgangsWert = 0.0

    except BaseException as e:
        logger.error("Berechnung des Stoffwerts gescheitert.")
        logger.exception("Fehlercode: %s", str(e))

        # Ausweichlösung ideales Gas
        ausgangsWert = flideal.FeuchteLuftSI(
            ausgangsRef,
            eingangsRef1,
            eingangsWert1,
            eingangsRef2,
            eingangsWert2,
            eingangsRef3,
            eingangsWert3,
        )

    return float(ausgangsWert)


def x_tpphi(t, p=1.01325, phi=1.0):
    """
    Berechnung des Sättigungswasserbeladung von feuchter Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    phi : float, optional
        Relative Luftfeuchtigkeit (0...1) (Standard: 1.) [-]

    Returns
    -------
    x : float
        Wasserbeladung [kgW/kgTL]

    Notes
    -----
    -
    """
    if -100 <= t <= 100:

        x = HAPropsSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", phi)

    else:
        logger.debug(
            "Für die Berechnung des Wassergehalts wurde der Definitionsbereich "
            "überschritten!"
        )

        if t < -100:
            x = 0.0
        else:
            x = 1.0

    if x < 0:
        logger.debug(
            "Die Berechnung des Wassergehalts mit CoolProp ist fehlerhaft. Verwende Hardy."
        )
        x = flideal.FeuchteLuftSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", phi)

    return x


def phi_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung des Sättigungswasserbeladung von feuchter Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wassergehalt (Standard: 0) [kg/kg]

    Returns
    -------
    phi : float
        Relative Luftfeuchtigkeit (0...1) [-]

    Notes
    -----
    -
    """
    return HAPropsSI("R", "T", t + 273.15, "P", p * 10 ** 5, "W", x)


def cp_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der spezifischen Wärmekapazität der feuchten Luft
    bei konstanten Druck. (Nur Luft und Wasserdampf)

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    cp_fl : float
        Spezifische Wärmekapazität bei konstanten Druck [J/kg*K]
    """
    xs = FeuchteLuftSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", 1.0)

    if xs >= x:  # Ungesättigt
        cp_fl = HAPropsSI("C", "T", t + 273.15, "P", p * 10 ** 5, "W", x)

    else:  # Gesättigt
        cp_fl = HAPropsSI("C", "T", t + 273.15, "P", p * 10 ** 5, "R", 1)

    return cp_fl


def cv_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der spezifischen Wärmekapazität der feuchten Luft
    bei konstanten Volumen. (Ideales Gas, nur Luft und Wasserdampf)

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    cv_fl : float
        Spezifische Wärmekapazität bei konstanten Volumen [J/kg*K]
    """
    xs = FeuchteLuftSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", 1.0)

    if x <= xs:
        cv_fl = (1 - x / (1 + x)) * flideal.cv_l + (x / (1 + x)) * flideal.cv_w_dampf
    else:
        cv_fl = (1 - xs / (1 + xs)) * flideal.cv_l + (
            xs / (1 + xs)
        ) * flideal.cv_w_dampf

    return cv_fl


def R_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der spezifischen Gaskonstante der feuchten Luft.
    (Ideales Gas, nur Luft und Wasserdampf)

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    R : float
        Spezifische Gaskonstante [J/kg*K]
    """
    xs = FeuchteLuftSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", 1.0)

    if x <= xs:
        R_fl = (1 - x / (1 + x)) * flideal.R_l + (x / (1 + x)) * flideal.R_w
    else:
        R_fl = (1 - xs / (1 + xs)) * flideal.R_l + (xs / (1 + xs)) * flideal.R_w

    return R_fl


def kappaM_tpx(t1, t2, p1=1.01325, p2=1.01325, x1=0.0, x2=0.0):
    """
    Berechnung des mittleren Isentropenexponents der feuchte Luft
    berechnet an zwei Zustandspunkten.

    Parameters
    ----------
    t1 : float
        Temperatur Zustand 1 [°C]
    t2 : float
        Temperatur Zustand 2 [°C]
    p1 : float, optional
        Druck Zustand 1 (Standard: 1.01325) [bar]
    p2 : float, optional
        Druck Zustand 2 (Standard: 1.01325) [bar]
    x1 : float, optional
        Wasserbeladung Zustand 1 (Standard: 0) [kgW/kgTL]
    x2 : float, optional
        Wasserbeladung Zustand 2 (Standard: 0) [kgW/kgTL]

    Returns
    -------
    kappa : float
        Mittlerer Isentropenexponent [-]

    Notes
    -----
    Ideales Gas, Arithmetisches Mittel
    """
    kappa = (
        (cp_tpx(t1, p1, x1) / cv_tpx(t1, p1, x1))
        + (cp_tpx(t2, p2, x2) / cv_tpx(t2, p2, x2))
    ) / 2

    return kappa


def kappa_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung des Isentropenexponents der feuchte Luft an einem Zustandspunkt.

    Parameters
    ----------
    t : float
        Temperatur Zustand 1 [°C]
    p : float, optional
        Druck Zustand 1 (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung Zustand 1 (Standard: 0) [kgW/kgTL]

    Returns
    -------
    kappa : float
        Isentropenexponent [-]

    Notes
    -----
    Ideales Gas
    """
    return cp_tpx(t, p, x) / cv_tpx(t, p, x)


def h_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der spezifischen Enthalpie der feuchten Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    -------
    h : float
        Spezifische Enthalpie [J/kg]

    Notes
    -----
    Quelle:
        Baehr, H.-D.: Thermodynamik: Grundlagen und technische Anwendungen.
        Springer Berlin Heidelberg. 2013.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    h = 0
    xs = FeuchteLuftSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", 1.0)
    cp_w_fest = flideal.cp_w_fest_poly(t)

    if xs >= x:  # Ungesättigt
        h = HAPropsSI("H", "T", t + 273.15, "P", p * 10 ** 5, "W", x) - h_fl_0

    else:  # Gesättigt
        if t + 273.15 > flideal.T_tr:  # Gesättigt mit flüssigen Wasser
            h = (
                HAPropsSI("H", "T", t + 273.15, "P", p * 10 ** 5, "R", 1)
                - h_fl_0
                + (x - xs) * (PropsSI("H", "T", t + 273.15, "Q", 0, "Water") - h_w_f_0)
            )

        elif t + 273.15 < flideal.T_tr:  # Gesättigt mit festem Wasser (Eis)
            h = (
                HAPropsSI("H", "T", t + 273.15, "P", p * 10 ** 5, "R", 1)
                - h_fl_0
                + (x - xs)
                * (
                    (-flideal.delta_he + cp_w_fest * (t + 273.15 - flideal.T_tr))
                    - h_w_e_0
                )
            )

        elif t + 273.15 == flideal.T_tr:
            logger.debug("Fehler: Wassergehalt der Luft nicht genau spezifiziert")

    return h


def s_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der spezifischen Entropie der feuchten Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    s : float
        Spezifische Entropie [J/kg*K]

    Notes
    -----
    Quelle:
        Baehr, H.-D.: Thermodynamik: Grundlagen und technische Anwendungen.
        Springer Berlin Heidelberg. 2013.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    s = 0
    xs = FeuchteLuftSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", 1.0)
    cp_w_fest = flideal.cp_w_fest_poly(t)

    # Ideale, mittlere Mischungsentropie feuchter Luft [J/kg*K]
    # if x > 0:
    #     delta_ms = flideal.R_w * ((flideal.R_l / flideal.R_w + x) *
    #         math.log(flideal.R_l / flideal.R_w + x) -
    #         x * math.log(x) - (flideal.R_l / flideal.R_w) *
    #         math.log(flideal.R_l / flideal.R_w))
    # else:
    #     delta_ms = 0

    if xs >= x:  # Ungesättigt
        s = HAPropsSI("S", "T", t + 273.15, "P", p * 10 ** 5, "W", x) - s_fl_0

    else:  # Gesättigt
        if t + 273.15 > flideal.T_tr:  # Gesättigt mit flüssigen Wasser
            s = (
                HAPropsSI("S", "T", t + 273.15, "P", p * 10 ** 5, "R", 1)
                - s_fl_0
                + (x - xs) * (PropsSI("S", "T", t + 273.15, "Q", 0, "Water") - s_w_f_0)
            )

        elif t + 273.15 < flideal.T_tr:  # Gesättigt mit festem Wasser (Eis)
            s = (
                HAPropsSI("S", "T", t + 273.15, "P", p * 10 ** 5, "R", 1)
                - s_fl_0
                + (x - xs)
                * (
                    (
                        (-1.0) * (flideal.delta_he / flideal.T_tr)
                        + cp_w_fest * math.log((t + 273.15) / flideal.T_tr)
                    )
                    - s_w_e_0
                )
            )

        elif t + 273.15 == flideal.T_tr:
            logger.debug("Fehler: Wassergehalt der Luft nicht genau spezifiziert")

    return s


def t_hpx_fun(t, h, p, x):
    """
    Funktion für die Nutzung mit einem Optimierungsverfahren zur Bestimmung der Temperatur.
    Der Aufruf erfolgt über t_hpx.
    """
    return h - h_tpx(t, p, x)


def t_hpx(h, p=1.01325, x=0.0):
    """
    Berechnung der Temperatur der feuchten Luft.

    Parameters
    ----------
    h : float
        Spezifische Enthalpie [J/kg]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    t : float
        Temperatur [°C]

    Notes
    -----
    Quelle:
        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    t_start = flideal.t_hpx(h, p, x)
    t = opt.fsolve(t_hpx_fun, t_start, args=(h, p, x))[0]

    return t


def t_spx_fun(t, s, p, x):
    """
    Funktion für die Nutzung mit einem Optimierungsverfahren zur Bestimmung der Temperatur.
    Der Aufruf erfolgt über t_spx.
    """
    return s - s_tpx(t, p, x)


def t_spx(s, p=1.01325, x=0.0):
    """
    Berechnung der Temperatur der feuchten Luft.

    Parameters
    ----------
    s : float
        Spezifische Entropie [J/kg*K]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    t : float
        Temperatur [°C]

    Notes
    -----
    Quelle:
        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    t_start = flideal.t_spx(s, p, x)
    t = opt.fsolve(t_spx_fun, t_start, args=(s, p, x))[0]

    return t


def v_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung des spezifisches Volumens der feuchten Luft. Das spezifische Volumen des
    Wassers wird mit 1 m**3/kg angenommen. (Nur Luft und Wasserdampf)

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    v : float
        Spezifisches Volumen [m**3/kg]
    """
    xs = FeuchteLuftSI("W", "T", t + 273.15, "P", p * 10 ** 5, "R", 1.0)

    if xs >= x:  # Ungesättigt
        v = HAPropsSI("V", "T", t + 273.15, "P", p * 10 ** 5, "W", x)

    else:  # Gesättigt
        v = HAPropsSI("V", "T", t + 273.15, "P", p * 10 ** 5, "R", 1)

    return v


def rho_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der Dichte der feuchten Luft. Die Dichte des
    Wassers wird mit 1 kg/m**3 angenommen.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]
    x : float, optional
        Wasserbeladung (Standard: 0) [kgW/kgTL]

    Returns
    ----------
    rho : float
        Dichte [kg/m**3]
    """
    return 1 / v_tpx(t, p, x)

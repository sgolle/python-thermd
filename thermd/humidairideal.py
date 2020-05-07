# -*- coding: utf-8 -*-

"""
    Berechnungsprozeduren/ -funktionen für die Berechnung der
    Stoffeigenschaften von feuchter Luft.

    Nullpunkt-Festlegung:
        h_l(T_tr) = 0 für trockene Luft
        h_w(T_tr) = 0 für flüssiges Wasser
        s_l(T_tr, p_tr) = 0 für trockene Luft
        s_w(T_tr, p_tr) = 0 für flüssiges Wasser
"""

import logging
import math
import numpy as np
from scipy import optimize as opt

# Protokollinstanz definieren
logger = logging.getLogger(__name__)

# Konstanten und Definition Eigenschaften
R_l = 287.0474730938159  # Spezifische Gaskonstante trockene Luft[J/kg*K]
R_w = 461.5230869726723  # Spezifische Gaskonstante Wasser [J/kg*K]

cp_l_poly = np.poly1d(
    [-1.02982783e-07, 4.29730845e-04, 1.46305349e-02, 1.00562420e03]
)  # Spezifische Wärmekapazität trockene Luft bei konst. Druck [J/kg*K]
cp_w_dampf_poly = np.poly1d(
    [
        3.05228669e-11,
        -1.57712722e-08,
        1.04676045e-06,
        1.27256322e-03,
        1.82289816e-01,
        1.85835959e03,
    ]
)  # Spezifische Wärmekapazität Wasserdampf bei konst. Druck [J/kg*K]
cp_w_fluessig_poly = np.poly1d(
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
)  # Spezifische Wärmekapazität flüssiges Wasser bei konst. Druck [J/kg*K]
cp_w_fest_poly = np.poly1d(
    [-1.03052963e-04, -2.77224838e-02, 4.87648024e00, 2.05097273e03]
)  # Spezifische Wärmekapazität Wassereis bei konst. Druck [J/kg*K]
cv_l = 718  # Spezifische Wärmekapazität trockene Luft bei konst. Volumen [J/kg*K]
cv_w_dampf = (
    1435.9  # Spezifische Wärmekapazität Wasserdampf bei konst. Volumen [J/kg*K]
)

delta_hv = 2500900  # Verdampfungsenthalpie von Wasser am Tripelpunkt [J/kg]
delta_he = 333400  # Schmelzenthalpie von Wasser [J/kg]

T_tr = 273.16  # Tripelpunkttemperatur von Wasser [K]
p_tr = 611.657 / 10 ** 5  # Tripelpunktdruck von Wasser [bar]


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
    >>>  FeuchteLuftSI('H','T',34+273.15,'P',2.84*10**5,'R',1)
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
                + "143.15 <= %s <= 350 °C",
                str(eingangsWert1 - 273.15),
            )
            return 0.0
    if eingangsRef2 == "P":
        if not 10 <= eingangsWert2 <= 10 * 10 ** 6:
            logger.warning(
                "Der übergebene Druck ist außerhalb des Definitionsbereichs: "
                + "10 <= %s <= 10 * 10 ** 6 Pa",
                str(eingangsWert2),
            )
            return 0.0
    if eingangsRef3 == "R":
        if not 0 <= eingangsWert3 <= 1:
            logger.warning(
                "Die übergebene Luftfeuchtigkeit ist außerhalb des Definitionsbereichs: "
                + "0 <= %s <= 1",
                str(eingangsWert3),
            )
            return 0.0
    if eingangsRef3 == "W":
        if not 0 <= eingangsWert3 <= 10:
            logger.warning(
                "Die übergebene Wasserbeladung ist außerhalb des Definitionsbereichs: "
                + "0 <= %s <= 10 kg/kg",
                str(eingangsWert3),
            )
            return 0.0

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

            ausgangsWert = phi_hardy_tpx(
                eingangsWert1 - 273.15, eingangsWert2 * 10 ** (-5), eingangsWert3
            )

        elif (
            ausgangsRef == "W"
            and eingangsRef1 == "T"
            and eingangsRef2 == "P"
            and eingangsRef3 == "R"
        ):

            ausgangsWert = x_hardy_tpphi(
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

        else:
            logger.error(
                "Berechnung der Stoffwerte gescheitert! Die Referenzen sind fehlerhaft"
            )
            ausgangsWert = 0.0

    except BaseException as e:
        logger.error("Berechnung des Stoffwerts gescheitert.")
        logger.exception("Fehlercode: %s", str(e))
        ausgangsWert = 0.0

    return float(ausgangsWert)


def cp_l_f(t):
    """
    Berechnung der spezifische Wärmekapazität trockener Luft bei konst. Druck.

    Parameters
    ----------
    t : float
        Temperatur [°C]

    Returns
    -------
    cp_l : float
         Spezifische Wärmekapazität trockene Luft bei konst. Druck [J/kg*K]

    Notes
    -----
    Gültigkeitsbereich:
        Polynom cp_l_poly -100 < t < 250
        Festwerte t < -100 und t > 250
    """
    if t < -100:
        cp_l = cp_l_poly(-100)
    elif t > 250:
        cp_l = cp_l_poly(250)
    else:
        cp_l = cp_l_poly(t)

    return cp_l


def cp_w_dampf_f(t):
    """
    Berechnung der spezifische Wärmekapazität von Wasserdampf bei konst. Druck.

    Parameters
    ----------
    t : float
        Temperatur [°C]

    Returns
    -------
    cp_w_dampf : float
         Spezifische Wärmekapazität Wasserdampf bei konst. Druck [J/kg*K]

    Notes
    -----
    Gültigkeitsbereich:
        Polynom cp_w_dampf_poly -100 < t < 250
        Festwerte t < -100 und t > 250
    """
    if t < -100:
        cp_w_dampf = cp_w_dampf_poly(-100)
    elif t > 250:
        cp_w_dampf = cp_w_dampf_poly(250)
    else:
        cp_w_dampf = cp_w_dampf_poly(t)

    return cp_w_dampf


def cp_w_fluessig_f(t):
    """
    Berechnung der spezifische Wärmekapazität von Wasser bei konst. Druck.

    Parameters
    ----------
    t : float
        Temperatur [°C]

    Returns
    -------
    cp_w_fluessig : float
         Spezifische Wärmekapazität Wasser bei konst. Druck [J/kg*K]

    Notes
    -----
    Gültigkeitsbereich:
        Polynom cp_w_fluessig_poly -100 < t < 250
        Festwerte t < 0.01 und t > 250
    """
    if t < 0.01:
        cp_w_fluessig = cp_w_fluessig_poly(0.01)
    elif t > 250:
        cp_w_fluessig = cp_w_fluessig_poly(250)
    else:
        cp_w_fluessig = cp_w_fluessig_poly(t)

    return cp_w_fluessig


def cp_w_fest_f(t):
    """
    Berechnung der spezifische Wärmekapazität von Wassereis bei konst. Druck.

    Parameters
    ----------
    t : float
        Temperatur [°C]

    Returns
    -------
    cp_w_fest : float
         Spezifische Wärmekapazität Wassereis bei konst. Druck [J/kg*K]

    Notes
    -----
    Gültigkeitsbereich:
        Polynom cp_w_fest_poly -100 < t < 250
        Festwerte t < -100 und t > 0
    """
    if t < -100:
        cp_w_fest = cp_w_fest_poly(-100)
    elif t > 0:
        cp_w_fest = cp_w_fest_poly(0)
    else:
        cp_w_fest = cp_w_fest_poly(t)

    return cp_w_fest


def ps_magnus_t(t):
    """
    Berechnung des Sättigungsdampfdruckes von feuchter Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]

    Returns
    -------
    ps : float
        Sättigungsdampfdruck [bar]

    Notes
    -----
    Korrelation nach Magnus und Sonntag 1990, Ohne Verstärkungsfaktor f für feuchte Luft
    """
    if t >= 0:
        ps = 0.0061078 * math.exp((17.08085 * t) / (234.175 + t))
    else:
        ps = 0.0061078 * math.exp((17.84362 * t) / (245.425 + t))
    return ps


def ps_hyland_t(t):
    """
    Berechnung des Sättigungsdampfdruckes von feuchter Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]

    Returns
    -------
    ps : float
        Sättigungsdampfdruck [bar]

    Notes
    -----
    Korrelation nach Hyland und Wexler 1983, Ohne Verstärkungsfaktor f für feuchte Luft
    """
    if t >= 0:
        ps = math.exp(
            (-5.8002206) * 10 ** 3 * (t + 273.15) ** (-1)
            + 1.3914993
            + (-4.8640239) * 10 ** (-2) * (t + 273.15)
            + 4.1764768 * 10 ** (-5) * (t + 273.15) ** 2
            + (-1.4452093) * 10 ** (-8) * (t + 273.15) ** 3
            + 6.5459673 * math.log(t + 273.15)
        ) * 10 ** (-5)
    else:
        ps = math.exp(
            -5.6745359 * 10 ** 3 * (t + 273.15) ** (-1)
            + 6.3925247
            + (-9.677843) * 10 ** (-3) * (t + 273.15)
            + 6.2215701 * 10 ** (-7) * (t + 273.15) ** 2
            + 2.0747825 * 10 ** (-9) * (t + 273.15) ** 3
            + (-9.4840240) * 10 ** (-13) * (t + 273.15) ** 4
            + 4.1635019 * math.log(t + 273.15)
        ) * 10 ** (-5)
    return ps


def ps_hardy_tp(t, p=1.01325):
    """
    Berechnung des Sättigungsdampfdruckes von feuchter Luft über flüssigem Wasser.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]

    Returns
    -------
    ps : float
        Sättigungsdampfdruck [bar]

    Notes
    -----
    Korrelation nach Hardy 1998 auf Basis der Temperaturskala ITS-90,
    Mit Verstärkungsfaktor f für feuchte Luft über flüssigem Wasser
    """
    if t >= 0:
        ps = math.exp(
            (-2.8365744) * 10 ** 3 * (t + 273.15) ** (-2)
            + (-6.028076559) * 10 ** 3 * (t + 273.15) ** (-1)
            + 1.954263612 * 10 ** 1 * (t + 273.15) ** 0
            + (-2.737830188) * 10 ** (-2) * (t + 273.15) ** 1
            + 1.6261698 * 10 ** (-5) * (t + 273.15) ** 2
            + 7.0229056 * 10 ** (-10) * (t + 273.15) ** 3
            + (-1.8680009) * 10 ** (-13) * (t + 273.15) ** 4
            + 2.7150305 * math.log(t + 273.15)
        ) * 10 ** (-5)
        alpha = (
            3.53624 * 10 ** (-4) * t ** 0
            + 2.9328363 * 10 ** (-5) * t ** 1
            + 2.6168979 * 10 ** (-7) * t ** 2
            + 8.5813609 * 10 ** (-9) * t ** 3
        )
        beta = math.exp(
            (-1.07588) * 10 ** 1 * t ** 0
            + 6.3268134 * 10 ** (-2) * t ** 1
            + (-2.5368934) * 10 ** (-4) * t ** 2
            + 6.3405286 * 10 ** (-7) * t ** 3
        )
    else:
        ps = math.exp(
            (-5.8666426) * 10 ** 3 * (t + 273.15) ** (-1)
            + 2.232870244 * 10 ** 1 * (t + 273.15) ** 0
            + 1.39387003 * 10 ** (-2) * (t + 273.15) ** 1
            + (-3.4262402) * 10 ** (-5) * (t + 273.15) ** 2
            + 2.7040955 * 10 ** (-8) * (t + 273.15) ** 3
            + 6.7063522 * 10 ** (-1) * math.log(t + 273.15)
        ) * 10 ** (-5)
        alpha = (
            3.64449 * 10 ** (-4) * t ** 0
            + 2.9367585 * 10 ** (-5) * t ** 1
            + 4.8874766 * 10 ** (-7) * t ** 2
            + 4.3669918 * 10 ** (-9) * t ** 3
        )
        beta = math.exp(
            (-1.07271) * 10 ** 1 * t ** 0
            + 7.6215115 * 10 ** (-2) * t ** 1
            + (-1.7490155) * 10 ** (-4) * t ** 2
            + 2.4668279 * 10 ** (-6) * t ** 3
        )

    f = math.exp(alpha * (1 - (ps / p)) + beta * ((p / ps) - 1))
    ps *= f

    return ps


def xs_magnus_tp(t, p=1.01325):
    """
    Berechnung des Sättigungswasserbeladung von feuchter Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]

    Returns
    -------
    xs : float
        Sättigungswasserbeladung [kgW/kgTL]

    Notes
    -----
    Korrelation nach Magnus und Sonntag 1990 für Sättigungsdampfdruck,
    Ohne Verstärkungsfaktor f für feuchte Luft
    """
    ps = ps_magnus_t(t)

    xs = abs(0.622 * (ps / (p - ps)))
    return xs


def xs_hyland_tp(t, p=1.01325):
    """
    Berechnung des Sättigungswasserbeladung von feuchter Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]

    Returns
    -------
    xs : float
        Sättigungswasserbeladung [kgW/kgTL]

    Notes
    -----
    Korrelation nach Hyland und Wexler 1983 für Sättigungsdampfdruck,
    Ohne Verstärkungsfaktor f für feuchte Luft
    """
    ps = ps_hyland_t(t)

    xs = abs(0.622 * (ps / (p - ps)))
    return xs


def xs_hardy_tp(t, p=1.01325):
    """
    Berechnung des Sättigungswasserbeladung von feuchter Luft.

    Parameters
    ----------
    t : float
        Temperatur [°C]
    p : float, optional
        Druck (Standard: 1.01325) [bar]

    Returns
    -------
    xs : float
        Sättigungswasserbeladung [kgW/kgTL]

    Notes
    -----
    Korrelation nach Hardy 1998 für Sättigungsdampfdruck auf Basis der Temperaturskala ITS-90,
    Mit Verstärkungsfaktor f für feuchte Luft
    """
    ps = ps_hardy_tp(t, p)

    xs = abs(0.622 * (ps / (p - ps)))
    return xs


def x_hardy_tpphi(t, p=1.01325, phi=1.0):
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
    Korrelation nach Hardy 1998 für Sättigungsdampfdruck auf Basis der Temperaturskala ITS-90,
    Mit Verstärkungsfaktor f für feuchte Luft
    """
    ps = ps_hardy_tp(t, p)

    x = abs(0.622 * ((phi * ps) / (p - phi * ps)))
    return x


def phi_hardy_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der relativen Luftfeuchtigkeit von feuchter Luft.

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
    Korrelation nach Hardy 1998 für Sättigungsdampfdruck auf Basis der Temperaturskala ITS-90,
    Mit Verstärkungsfaktor f für feuchte Luft
    """
    phi = (p / ps_hardy_tp(t, p)) * (x / (0.622 + x))

    return phi


def cp_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung der spezifischen Wärmekapazität der feuchten Luft
    bei konstanten Druck. (Ideales Gas, nur Luft und Wasserdampf)

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
    xs = xs_hardy_tp(t, p)
    cp_l = cp_l_poly(t)
    cp_w_dampf = cp_w_dampf_poly(t)

    if x <= xs:
        cp_fl = (1 - x / (1 + x)) * cp_l + (x / (1 + x)) * cp_w_dampf
    else:
        cp_fl = (1 - xs / (1 + xs)) * cp_l + (xs / (1 + xs)) * cp_w_dampf

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
    xs = xs_hardy_tp(t, p)

    if x <= xs:
        cv_fl = (1 - x / (1 + x)) * cv_l + (x / (1 + x)) * cv_w_dampf
    else:
        cv_fl = (1 - xs / (1 + xs)) * cv_l + (xs / (1 + xs)) * cv_w_dampf

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
    xs = xs_hardy_tp(t, p)

    if x <= xs:
        R_fl = (1 - x / (1 + x)) * R_l + (x / (1 + x)) * R_w
    else:
        R_fl = (1 - xs / (1 + xs)) * R_l + (xs / (1 + xs)) * R_w

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

    xs = xs_hardy_tp(t, p)
    cp_l = cp_l_f(t)
    cp_w_dampf = cp_w_dampf_f(t)
    cp_w_fluessig = cp_w_fluessig_f(t)
    cp_w_fest = cp_w_fest_f(t)

    if xs >= x:  # Ungesättigt
        h = cp_l * (t + 273.15 - T_tr) + x * (
            delta_hv + cp_w_dampf * (t + 273.15 - T_tr)
        )

    else:  # Gesättigt
        if t + 273.15 > T_tr:  # Gesättigt mit flüssigen Wasser
            h = (
                cp_l * (t + 273.15 - T_tr)
                + xs * (delta_hv + cp_w_dampf * (t + 273.15 - T_tr))
                + (x - xs) * cp_w_fluessig * (t + 273.15 - T_tr)
            )

        elif t + 273.15 < T_tr:  # Gesättigt mit festem Wasser (Eis)
            h = (
                cp_l * (t + 273.15 - T_tr)
                + xs * (delta_hv + cp_w_dampf * (t + 273.15 - T_tr))
                + (x - xs) * (-delta_he + cp_w_fest * (t + 273.15 - T_tr))
            )

        elif t + 273.15 == T_tr:
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

    xs = xs_hardy_tp(t, p)
    cp_l = cp_l_f(t)
    cp_w_dampf = cp_w_dampf_f(t)
    cp_w_fluessig = cp_w_fluessig_f(t)
    cp_w_fest = cp_w_fest_f(t)

    # Ideale, mittlere Mischungsentropie feuchter Luft [J/kg*K]
    if x > 0:
        delta_ms = R_w * (
            (R_l / R_w + x) * math.log(R_l / R_w + x)
            - x * math.log(x)
            - (R_l / R_w) * math.log(R_l / R_w)
        )
    else:
        delta_ms = 0

    if xs >= x:  # Ungesättigt
        s = (
            cp_l * math.log((t + 273.15) / T_tr)
            - R_l * math.log(p / p_tr)
            + x
            * (
                (delta_hv / T_tr)
                + cp_w_dampf * math.log((t + 273.15) / T_tr)
                - R_w * math.log(p / p_tr)
            )
            + delta_ms
        )

    else:  # Gesättigt
        if t + 273.15 > T_tr:  # Gesättigt mit flüssigen Wasser
            s = (
                cp_l * math.log((t + 273.15) / T_tr)
                - R_l * math.log(p / p_tr)
                + xs
                * (
                    (delta_hv / T_tr)
                    + cp_w_dampf * math.log((t + 273.15) / T_tr)
                    - R_w * math.log(p / p_tr)
                )
                + (x - xs) * cp_w_fluessig * math.log((t + 273.15) / T_tr)
                + delta_ms
            )

        elif t + 273.15 < T_tr:  # Gesättigt mit festem Wasser (Eis)
            s = (
                cp_l * math.log((t + 273.15) / T_tr)
                - R_l * math.log(p / p_tr)
                + xs
                * (
                    (delta_hv / T_tr)
                    + cp_w_dampf * math.log((t + 273.15) / T_tr)
                    - R_w * math.log(p / p_tr)
                )
                + (x - xs)
                * (
                    (-1.0) * (delta_he / T_tr)
                    + cp_w_fest * math.log((t + 273.15) / T_tr)
                )
                + delta_ms
            )

        elif t + 273.15 == T_tr:
            logger.debug("Fehler: Wassergehalt der Luft nicht genau spezifiziert")

    return s


def t_hpx_interpol(t, h, p, x):
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
    t = opt.fsolve(t_hpx_interpol, 0.0, args=(h, p, x))[0]

    return t


def t_spx_interpol(t, s, p, x):
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
    t = opt.fsolve(t_spx_interpol, 0.0, args=(s, p, x))[0]

    return t


def v_tpx(t, p=1.01325, x=0.0):
    """
    Berechnung des spezifisches Volumens der feuchten Luft. Das spezifische Volumen des
    Wassers wird mit 1 m**3/kg angenommen.

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
    xs = xs_hardy_tp(t, p)

    v_w = 1.0

    if x <= xs:  # Ungesättigt
        v = ((R_w * (t + 273.15)) / (p * 10 ** 5)) * ((0.622 + x) / (1 + x))

    else:  # Gesättigt mit flüssigem Wasser
        v = (
            1
            / (1 + x)
            * (((R_w * (t + 273.15)) / (p * 10 ** 5)) * (0.622 + xs) + (x - xs) * v_w)
        )

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

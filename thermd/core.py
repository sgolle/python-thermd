# -*- coding: utf-8 -*-

"""
    Hilfsfunktionen für die Thermodynamik.
"""

from CoolProp.CoolProp import PropsSI


def fIsentrop_rho_T(T2_T1, kappa=1.4):
    """
    Bestimmung der Dichteänderung mit Temperaturänderung bei isentropen Zustandsänderungen.

    Parameters
    ----------
    T2_T1 : float
        Temperaturänderung [-]
    kappa : float, optional
        Isentropenexponent des Gases (Standard: 1,4 für Luft) [-]

    Returns
    -------
    rho2_rho1 : float
        Dichteänderung [-]
    """
    return (T2_T1) ** (1 / (kappa - 1))


def fIsentrop_rho_p(p2_p1, kappa=1.4):
    """
    Bestimmung der Dichteänderung mit Druckänderung bei isentropen Zustandsänderungen.

    Parameters
    ----------
    p2_p1 : float
        Druckänderung [-]
    kappa : float, optional
        Isentropenexponent des Gases (Standard: 1,4 für Luft) [-]

    Returns
    -------
    rho2_rho1 : float
        Dichteänderung [-]
    """
    return (p2_p1) ** (1 / kappa)


def fIsentrop_p_T(T1_T2, kappa=1.4):
    """
    Bestimmung der Druckänderung mit Temperaturänderung bei isentropen Zustandsänderungen.

    Parameters
    ----------
    T1_T2 : float
        Temperaturänderung [-]
    kappa : float, optional
        Isentropenexponent des Gases (Standard: 1,4 für Luft) [-]

    Returns
    -------
    p1_p2 : float
        Druckänderung [-]
    """
    return (T1_T2) ** (kappa / (kappa - 1))


def fIsentrop_p_rho(rho1_rho2, kappa=1.4):
    """
    Bestimmung der Druckänderung mit Dichteänderung bei isentropen Zustandsänderungen.

    Parameters
    ----------
    rho1_rho2 : float
        Dichteänderung [-]
    kappa : float, optional
        Isentropenexponent des Gases (Standard: 1,4 für Luft) [-]

    Returns
    -------
    p1_p2 : float
        Druckänderung [-]
    """
    return (rho1_rho2) ** kappa


def fIsentrop_T_p(p1_p2, kappa=1.4):
    """
    Bestimmung der Temperaturänderung mit Druckänderung bei isentropen Zustandsänderungen.

    Parameters
    ----------
    p1_p2 : float
        Druckänderung [-]
    kappa : float, optional
        Isentropenexponent des Gases (Standard: 1,4 für Luft) [-]

    Returns
    -------
    T1_T2 : float
        Temperaturänderung [-]
    """
    return (p1_p2) ** ((kappa - 1) / kappa)


def fIsentrop_T_rho(rho1_rho2, kappa=1.4):
    """
    Bestimmung der Temperaturänderung mit Dichteänderung bei isentropen Zustandsänderungen.

    Parameters
    ----------
    rho1_rho2 : float
        Dichteänderung [-]
    kappa : float, optional
        Isentropenexponent des Gases (Standard: 1,4 für Luft) [-]

    Returns
    -------
    T1_T2 : float
        Temperaturänderung [-]
    """
    return (rho1_rho2) ** (kappa - 1)

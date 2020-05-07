# -*- coding: utf-8 -*-

"""
    Berechnungsprozeduren/ -funktionen für die Berechnung von
    thermodynamischen Zustandsänderungen.
"""

from CoolProp.CoolProp import PropsSI


def Isentrop(
    eingangsRef1,
    eingangsWert1,
    eingangsRef2,
    eingangsWert2,
    ausgangsRef,
    ausgangsWert,
    fluid,
):
    """
    Berechnung der isentropen Zustandsänderung (s = const.) für einphasige
    reine Fluide und Gemische in CoolProp im Einphasengebiet
    am Ein- und Ausgang. Falls im Zweiphasengebiet gerechnet wird,
    muss Ein- und Ausgangsgröße die spez. Enthalpie sein.

    Parameters
    ----------
    eingangsRef1 : string
        Gültige Variablenreferenz:\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'H' -- Spez. Enthalpie [J/kg]\n
        'S' -- Spez. Entropie [J/kg*K]
    eingangsWert1 : float
        Eingangswert 1 entsprechend Referenz
    eingangsRef2 : string
        Gültige Variablenreferenz (andere Referenz als eingangsRef1):\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'H' -- Spez. Enthalpie [J/kg]\n
        'S' -- Spez. Entropie [J/kg*K]
    eingangsWert2 : float
        Eingangswert 2 Referenz
    ausgangsRef : string
        Gültige Variablenreferenz:\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'H' -- Spez. Enthalpie [J/kg]
    ausgangsWert : float
        Ausgangswert entsprechend Referenz
    fluid : string
        Referenzname des Fluids in CoolProp

    Returns
    -------
    T : float
        Temperatur [K]
    p : float
        Druck [Pa]
    d : float
        Dichte [kg/m**3]
    h : float
        Spez. Enthalpie [J/kg]
    s : float
        Spez. Entropie [J/kg*K]
    u : float
        Spez. innere Energie [J/kg]
    deltah : float
        Änderung der spez. Enthalpie [J/kg]

    Examples
    --------
        >>>  from thermodynamik import prozess
        >>>  prozess.Isentrop('T',300.,'P',100000.,'P',200000.,'R134a')
        (321.3816833953912, 200000.0, 7.881374209828377, 443232.1321293819,
        1907.0070720162264, 417855.84689341474, 17105.364905666444)

    Notes
    -----
    Gültigkeitsbereich:
        Beschränkungen siehe CoolProp-Dokumentation [1].

    Quelle:
        Bell, I. H.; Wronski, J.; Quoilin, S. und Lemort, V.: Pure and
        Pseudo-pure Fluid Thermophysical Property Evaluation and the
        Open-Source Thermophysical Property Library CoolProp. In: Industrial and
        Engineering Chemistry Research 53, S. 2498-2508. 2014.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    if (
        (
            eingangsRef1 == "T"
            or eingangsRef1 == "P"
            or eingangsRef1 == "H"
            or eingangsRef1 == "S"
        )
        and (
            eingangsRef1 == "T"
            or eingangsRef1 == "P"
            or eingangsRef1 == "H"
            or eingangsRef1 == "S"
        )
        and (ausgangsRef == "T" or ausgangsRef == "P" or ausgangsRef == "H")
        and (eingangsRef1 != eingangsRef2)
    ):
        if ausgangsRef == "T":
            if eingangsRef1 != "S" and eingangsRef2 != "S":
                s = PropsSI(
                    "S", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "S":
                s = eingangsWert1
            elif eingangsRef2 == "S":
                s = eingangsWert2
            else:
                return

            T = ausgangsWert
            p = PropsSI("P", "S", s, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "S", s, ausgangsRef, ausgangsWert, fluid)
            h = PropsSI("H", "S", s, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "S", s, ausgangsRef, ausgangsWert, fluid)
            deltah = h - PropsSI(
                "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
            )
        elif ausgangsRef == "P":
            if eingangsRef1 != "S" and eingangsRef2 != "S":
                s = PropsSI(
                    "S", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "S":
                s = eingangsWert1
            elif eingangsRef2 == "S":
                s = eingangsWert2
            else:
                return

            p = ausgangsWert
            T = PropsSI("T", "S", s, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "S", s, ausgangsRef, ausgangsWert, fluid)
            h = PropsSI("H", "S", s, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "S", s, ausgangsRef, ausgangsWert, fluid)
            deltah = h - PropsSI(
                "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
            )
        elif ausgangsRef == "H":
            if eingangsRef1 != "S" and eingangsRef2 != "S":
                s = PropsSI(
                    "S", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "S":
                s = eingangsWert1
            elif eingangsRef2 == "S":
                s = eingangsWert2
            else:
                return

            h = ausgangsWert
            p = PropsSI("P", "S", s, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "S", s, ausgangsRef, ausgangsWert, fluid)
            T = PropsSI("T", "S", s, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "S", s, ausgangsRef, ausgangsWert, fluid)
            deltah = h - PropsSI(
                "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
            )
        else:
            return
    else:
        print("Die eingegebene Variablenreferenz ist ungültig.")
        s = 0.0
        T = 0.0
        p = 0.0
        d = 0.0
        h = 0.0
        u = 0.0
        deltah = 0.0

    return T, p, d, h, s, u, deltah


def Isobar(
    eingangsRef1,
    eingangsWert1,
    eingangsRef2,
    eingangsWert2,
    ausgangsRef,
    ausgangsWert,
    fluid,
):
    """
    Berechnung der isobaren Zustandsänderung (p = const.) für einphasige
    reine Fluide und Gemische in CoolProp im Einphasengebiet am
    Ein- und Ausgang. Falls im Zweiphasengebiet gerechnet wird,
    muss Ein- und Ausgangsgröße die spez. Enthalpie sein.

    Parameters
    ----------
    eingangsRef1 : string
        Gültige Variablenreferenz:\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'H' -- Spez. Enthalpie [J/kg]\n
        'S' -- Spez. Entropie [J/kg*K]
    eingangsWert1 : float
        Eingangswert 1 entsprechend Referenz
    eingangsRef2 : string
        Gültige Variablenreferenz (andere Referenz als eingangsRef1):\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'H' -- Spez. Enthalpie [J/kg]\n
        'S' -- Spez. Entropie [J/kg*K]
    eingangsWert2 : float
        Eingangswert 2 Referenz
    ausgangsRef : string
        Gültige Variablenreferenz:\n
        'T' -- Temperatur [K]\n
        'H' -- Spez. Enthalpie [J/kg]\n
        'S' -- Spez. Entropie [J/kg*K]
    ausgangsWert : float
        Ausgangswert entsprechend Referenz
    fluid : string
        Referenzname des Fluids in CoolProp

    Returns
    -------
    T : float
        Temperatur [K]
    p : float
        Druck [Pa]
    d : float
        Dichte [kg/m**3]
    h : float
        Spez. Enthalpie [J/kg]
    s : float
        Spez. Entropie [J/kg*K]
    u : float
        Spez. innere Energie [J/kg]
    deltah : float
        Änderung der spez. Enthalpie [J/kg]

    Examples
    --------
        >>>  from thermodynamik import prozess
        >>>  prozess.Isobar('T',300.,'P',100000.,'T',200.,'R134a')
        (200.0, 100000.0, 1510.6174611314266, 107433.92596049618,
        607.2118551790679, 107367.72786430504, -318692.84126321925)

    Notes
    -----
    Gültigkeitsbereich:
        Beschränkungen siehe CoolProp-Dokumentation [1].

    Quelle:
        Bell, I. H.; Wronski, J.; Quoilin, S. und Lemort, V.: Pure and
        Pseudo-pure Fluid Thermophysical Property Evaluation and the
        Open-Source Thermophysical Property Library CoolProp. In: Industrial and
        Engineering Chemistry Research 53, S. 2498-2508. 2014.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    if (
        (
            eingangsRef1 == "T"
            or eingangsRef1 == "P"
            or eingangsRef1 == "H"
            or eingangsRef1 == "S"
        )
        and (
            eingangsRef1 == "T"
            or eingangsRef1 == "P"
            or eingangsRef1 == "H"
            or eingangsRef1 == "S"
        )
        and (ausgangsRef == "T" or ausgangsRef == "H" or ausgangsRef == "S")
        and (eingangsRef1 != eingangsRef2)
    ):
        if ausgangsRef == "T":
            if eingangsRef1 != "P" and eingangsRef2 != "P":
                p = PropsSI(
                    "P", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "P":
                p = eingangsWert1
            elif eingangsRef2 == "P":
                p = eingangsWert2
            else:
                return

            T = ausgangsWert
            s = PropsSI("S", "P", p, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "P", p, ausgangsRef, ausgangsWert, fluid)
            h = PropsSI("H", "P", p, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "P", p, ausgangsRef, ausgangsWert, fluid)
            deltah = h - PropsSI(
                "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
            )
        elif ausgangsRef == "H":
            if eingangsRef1 != "P" and eingangsRef2 != "P":
                p = PropsSI(
                    "P", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "P":
                p = eingangsWert1
            elif eingangsRef2 == "P":
                p = eingangsWert2
            else:
                return

            h = ausgangsWert
            T = PropsSI("T", "P", p, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "P", p, ausgangsRef, ausgangsWert, fluid)
            s = PropsSI("S", "P", p, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "P", p, ausgangsRef, ausgangsWert, fluid)
            deltah = h - PropsSI(
                "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
            )
        elif ausgangsRef == "S":
            if eingangsRef1 != "P" and eingangsRef2 != "P":
                p = PropsSI(
                    "P", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "P":
                p = eingangsWert1
            elif eingangsRef2 == "P":
                p = eingangsWert2
            else:
                return

            s = ausgangsWert
            h = PropsSI("H", "P", p, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "P", p, ausgangsRef, ausgangsWert, fluid)
            T = PropsSI("T", "P", p, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "P", p, ausgangsRef, ausgangsWert, fluid)
            deltah = h - PropsSI(
                "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
            )
        else:
            return
    else:
        print("Die eingegebene Variablenreferenz ist ungültig.")
        s = 0.0
        T = 0.0
        p = 0.0
        d = 0.0
        h = 0.0
        u = 0.0
        deltah = 0.0

    return T, p, d, h, s, u, deltah


def Isenthalp(
    eingangsRef1,
    eingangsWert1,
    eingangsRef2,
    eingangsWert2,
    ausgangsRef,
    ausgangsWert,
    fluid,
):
    """
    Berechnung der isenthalpen Zustandsänderung (h = const.)
    für reine Fluide und Gemische in CoolProp im Einphasengebiet am
    Ein- und Ausgang. Falls im Zweiphasengebiet gerechnet wird,
    muss Eingangsgröße die spez. Enthalpie sein.

    Parameters
    ----------
    eingangsRef1 : string
        Gültige Variablenreferenz:\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'H' -- Spez. Enthalpie [J/kg]\n
        'S' -- Spez. Entropie [J/kg*K]
    eingangsWert1 : float
        Eingangswert 1 entsprechend Referenz
    eingangsRef2 : string
        Gültige Variablenreferenz (andere Referenz als eingangsRef1):\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'H' -- Spez. Enthalpie [J/kg]\n
        'S' -- Spez. Entropie [J/kg*K]
    eingangsWert2 : float
        Eingangswert 2 Referenz
    ausgangsRef : string
        Gültige Variablenreferenz:\n
        'T' -- Temperatur [K]\n
        'P' -- Druck [Pa]\n
        'S' -- Spez. Entropie [J/kg]
    ausgangsWert : float
        Ausgangswert entsprechend Referenz
    fluid : string
        Referenzname des Fluids in CoolProp

    Returns
    -------
    T : float
        Temperatur [K]
    p : float
        Druck [Pa]
    d : float
        Dichte [kg/m**3]
    h : float
        Spez. Enthalpie [J/kg]
    s : float
        Spez. Entropie [J/kg*K]
    u : float
        Spez. innere Energie [J/kg]
    deltah : float
        Änderung der spez. Enthalpie [J/kg]

    Examples
    --------
        >>>  from thermodynamik import prozess
        >>>  prozess.Isenthalp('T',300.,'P',10000000.,'P',100000.,'R134a')
        (246.78881174998168, 100000.0, 15.371925151688105, 238262.0941280767,
        1162.6320979583938, 231756.7280783976, 0.0)

    Notes
    -----
    Gültigkeitsbereich:
        Beschränkungen siehe CoolProp-Dokumentation [1].

    Quelle:
        Bell, I. H.; Wronski, J.; Quoilin, S. und Lemort, V.: Pure and
        Pseudo-pure Fluid Thermophysical Property Evaluation and the
        Open-Source Thermophysical Property Library CoolProp. In: Industrial and
        Engineering Chemistry Research 53, S. 2498-2508. 2014.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.
    """
    if (
        (
            eingangsRef1 == "T"
            or eingangsRef1 == "P"
            or eingangsRef1 == "H"
            or eingangsRef1 == "S"
        )
        and (
            eingangsRef1 == "T"
            or eingangsRef1 == "P"
            or eingangsRef1 == "H"
            or eingangsRef1 == "S"
        )
        and (ausgangsRef == "T" or ausgangsRef == "P" or ausgangsRef == "S")
        and (eingangsRef1 != eingangsRef2)
    ):
        if ausgangsRef == "T":
            if eingangsRef1 != "H" and eingangsRef2 != "H":
                h = PropsSI(
                    "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "H":
                h = eingangsWert1
            elif eingangsRef2 == "H":
                h = eingangsWert2
            else:
                return

            T = ausgangsWert
            p = PropsSI("P", "H", h, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "H", h, ausgangsRef, ausgangsWert, fluid)
            s = PropsSI("S", "H", h, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "H", h, ausgangsRef, ausgangsWert, fluid)
            deltah = 0.0
        elif ausgangsRef == "P":
            if eingangsRef1 != "H" and eingangsRef2 != "H":
                h = PropsSI(
                    "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "H":
                h = eingangsWert1
            elif eingangsRef2 == "H":
                h = eingangsWert2
            else:
                return

            p = ausgangsWert
            T = PropsSI("T", "H", h, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "H", h, ausgangsRef, ausgangsWert, fluid)
            s = PropsSI("S", "H", h, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "H", h, ausgangsRef, ausgangsWert, fluid)
            deltah = 0.0
        elif ausgangsRef == "S":
            if eingangsRef1 != "H" and eingangsRef2 != "H":
                h = PropsSI(
                    "H", eingangsRef1, eingangsWert1, eingangsRef2, eingangsWert2, fluid
                )
            elif eingangsRef1 == "H":
                h = eingangsWert1
            elif eingangsRef2 == "H":
                h = eingangsWert2
            else:
                return

            s = ausgangsWert
            p = PropsSI("P", "H", h, ausgangsRef, ausgangsWert, fluid)
            d = PropsSI("D", "H", h, ausgangsRef, ausgangsWert, fluid)
            T = PropsSI("T", "H", h, ausgangsRef, ausgangsWert, fluid)
            u = PropsSI("U", "H", h, ausgangsRef, ausgangsWert, fluid)
            deltah = 0.0
        else:
            return
    else:
        print("Die eingegebene Variablenreferenz ist ungültig.")
        s = 0.0
        T = 0.0
        p = 0.0
        d = 0.0
        h = 0.0
        u = 0.0
        deltah = 0.0

    return T, p, d, h, s, u, deltah

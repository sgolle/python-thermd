# -*- coding: utf-8 -*-
"""
    Berechnungsprozeduren/ -funktionen für die Berechnung der
    Mischung zweier Fluide.
"""
import logging
from CoolProp.CoolProp import PhaseSI
from CoolProp.CoolProp import PropsSI

# from stoffwerte.feuchteluftideal import FeuchteLuftSI
from stoffwerte.feuchteluftreal import FeuchteLuftSI

# Protokollinstanz definieren
logger = logging.getLogger(__name__)


def Reinstoff(einZustand1, einZustand2):
    """
    Berechnung der Ausgangszustände bei der Mischung zweier Reinstoffströme.
    Der thermodynamische Prozess wird über die Energiebilanz ohne Verluste
    berechnet.

    Eingangswerte
    -------------
    einZustand1 : pandas.core.series.Series, float64
        Eingangszustand 1 des Reinstoffes; Elemente: Massenstrom, Temperatur,
        Druck, Enthalpie, Entropie, Volumen, Fluid
    einZustand2 : pandas.core.series.Series, float64
        Eingangszustand 2 des Reinstoffes; Elemente: Massenstrom, Temperatur,
        Druck, Enthalpie, Entropie, Volumen, Fluid

    Ausgangswerte
    -------------
    ausZustand : pandas.core.series.Series, float64
        Ausgangszustand des Reinstoffes; Elemente: Massenstrom,
        Temperatur, Druck, Enthalpie, Entropie, Volumen, Fluid

    Notes
    -----
    Gültigkeitsbereich:
        (siehe CoolProp)

    Quellen:
        Baehr, H. D., Kabelac, S.: Thermodynamik - Grundlagen und
        technische Anwendungen. Heidelberg, Springer Verlag. 2006.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.

        Bell, I. H.; Wronski, J.; Quoilin, S. und Lemort, V.: Pure and
        Pseudo-pure Fluid Thermophysical Property Evaluation and the
        Open-Source Thermophysical Property Library CoolProp. In: Industrial and
        Engineering Chemistry Research 53, S. 2498-2508. 2014.
    """
    # Ausgangszustände definieren
    ausZustand = einZustand1.copy()

    if einZustand1.at["Massenstrom"] > 0 and einZustand2.at["Massenstrom"] > 0:

        # Ausgangsmassenstrom
        ausZustand.at["Massenstrom"] = (
            einZustand1.at["Massenstrom"] + einZustand2.at["Massenstrom"]
        )

        # Sicherheitsabfrage, ob spezifische Enthalpie korrekt berechnet wurde
        phase_fluid1 = PhaseSI(
            "P",
            einZustand1.at["Druck"] * 10 ** 5,
            "H",
            einZustand1.at["spezEnthalpie"],
            einZustand1.at["Fluid"],
        )
        if phase_fluid1 != "twophase" and phase_fluid1 != "":
            zustand_ein_fluid1_spezEnthalpie = PropsSI(
                "H",
                "T",
                einZustand1.at["Temperatur"] + 273.15,
                "P",
                einZustand1.at["Druck"] * 10 ** 5,
                einZustand1.at["Fluid"],
            )

            if (
                abs(zustand_ein_fluid1_spezEnthalpie - einZustand1.at["spezEnthalpie"])
                >= 0.001
            ):
                logger.warning(
                    "Die Enthalpie des Fluids 1 ist nicht korrekt übergeben worden! (Differenz: "
                    + str(
                        zustand_ein_fluid1_spezEnthalpie
                        - einZustand1.at["spezEnthalpie"]
                    )
                    + ")"
                )

        elif phase_fluid1 == "":
            logger.warning("Die Phase des Fluids 1 wurde falsch berechnet!")

        phase_fluid2 = PhaseSI(
            "P",
            einZustand2.at["Druck"] * 10 ** 5,
            "H",
            einZustand2.at["spezEnthalpie"],
            einZustand2.at["Fluid"],
        )
        if phase_fluid2 != "twophase" and phase_fluid2 != "":
            zustand_ein_fluid2_spezEnthalpie = PropsSI(
                "H",
                "T",
                einZustand2.at["Temperatur"] + 273.15,
                "P",
                einZustand2.at["Druck"] * 10 ** 5,
                einZustand2.at["Fluid"],
            )

            if (
                abs(zustand_ein_fluid2_spezEnthalpie - einZustand2.at["spezEnthalpie"])
                >= 0.001
            ):
                logger.warning(
                    "Die Enthalpie des Fluids 2 ist nicht korrekt übergeben worden! (Differenz: "
                    + str(
                        zustand_ein_fluid2_spezEnthalpie
                        - einZustand2.at["spezEnthalpie"]
                    )
                    + ")"
                )

        elif phase_fluid2 == "":
            logger.warning("Die Phase des Fluids 2 wurde falsch berechnet!")

        # Mischungs-/Ausgangsenthalpie
        ausZustand.at["spezEnthalpie"] = (
            einZustand1.at["Massenstrom"] * einZustand1.at["spezEnthalpie"]
            + einZustand2.at["Massenstrom"] * einZustand2.at["spezEnthalpie"]
        ) / ausZustand.at["Massenstrom"]

        #        ausZustand.at['spezEnthalpie'] = \
        #            (einZustand1.at['Massenstrom'] *
        #             PropsSI('H',
        #                     'T', einZustand1.at['Temperatur'] + 273.15,
        #                     'P', einZustand1.at['Druck'] * 10 ** 5,
        #                     einZustand1.at['Fluid']) +
        #             einZustand2.at['Massenstrom'] *
        #             PropsSI('H',
        #                     'T', einZustand2.at['Temperatur'] + 273.15,
        #                     'P', einZustand2.at['Druck'] * 10 ** 5,
        #                     einZustand2.at['Fluid'])) / \
        #            ausZustand.at['Massenstrom']

        # Ausgangsdruck und Druckverluste (muss noch näher untersucht werden)
        if einZustand1.at["Druck"] <= einZustand2.at["Druck"]:
            ausZustand.at["Druck"] = einZustand1.at["Druck"]
        else:
            ausZustand.at["Druck"] = einZustand2.at["Druck"]

        # Ausgangstemperatur
        ausZustand.at["Temperatur"] = (
            PropsSI(
                "T",
                "H",
                ausZustand.at["spezEnthalpie"],
                "P",
                ausZustand.at["Druck"] * 10 ** 5,
                ausZustand.at["Fluid"],
            )
            - 273.15
        )

        # Ausgangsdampfmassegehalt
        ausZustand.at["Dampfmassegehalt"] = PropsSI(
            "Q",
            "H",
            ausZustand.at["spezEnthalpie"],
            "P",
            ausZustand.at["Druck"] * 10 ** 5,
            ausZustand.at["Fluid"],
        )

    elif einZustand2.at["Massenstrom"] <= 0 < einZustand1.at["Massenstrom"]:
        ausZustand = einZustand1.copy()

    elif einZustand1.at["Massenstrom"] <= 0 < einZustand2.at["Massenstrom"]:
        ausZustand = einZustand2.copy()

    return ausZustand


def BinaeresGemisch():
    pass


def TernaeresGemisch():
    pass


def FeuchteLuft(einZustand1, einZustand2):
    """
    Berechnung der Ausgangszustände bei der Mischung zweier feuchter
    Luftströme.
    Der thermodynamische Prozess wird über die Energiebilanz ohne Verluste
    berechnet.

    Eingangswerte
    -------------
    einZustand1 : pandas.core.series.Series, float64
        Eingangszustand 1 der feuchten Luft; Elemente: Massenstrom, Temperatur,
        Druck, Wassergehalt Dampf, Wassergehalt Flüssig-Fest, Enthalpie,
        Entropie, Volumen, Fluid
    einZustand2 : pandas.core.series.Series, float64
        Eingangszustand 2 der feuchten Luft; Elemente: Massenstrom, Temperatur,
        Druck, Wassergehalt Dampf, Wassergehalt Flüssig-Fest, Enthalpie,
        Entropie, Volumen, Fluid

    Ausgangswerte
    -------------
    ausZustand : pandas.core.series.Series, float64
        Ausgangszustand der feuchten Luft; Elemente: Massenstrom,
        Temperatur, Druck, Wassergehalt Dampf, Wassergehalt Flüssig-Fest,
        Enthalpie, Entropie, Volumen, Fluid

    Notes
    -----
    Gültigkeitsbereich:
        (siehe CoolProp)

    Quelle:
        Baehr, H. D., Kabelac, S.: Thermodynamik - Grundlagen und
        technische Anwendungen. Heidelberg, Springer Verlag. 2006.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.

        Bell, I. H.; Wronski, J.; Quoilin, S. und Lemort, V.: Pure and
        Pseudo-pure Fluid Thermophysical Property Evaluation and the
        Open-Source Thermophysical Property Library CoolProp. In: Industrial and
        Engineering Chemistry Research 53, S. 2498-2508. 2014.
    """
    # Ausgangszustände definieren
    ausZustand = einZustand1.copy()

    if einZustand1.at["Massenstrom"] > 0 and einZustand2.at["Massenstrom"] > 0:

        # Ausgangsmassenstrom
        ausZustand.at["Massenstrom"] = (
            einZustand1.at["Massenstrom"] + einZustand2.at["Massenstrom"]
        )

        # Ausgangswassergehalt
        x_aus = (
            ausZustand.at["Massenstrom"]
            / (
                einZustand1.at["Massenstrom"]
                / (
                    1
                    + einZustand1.at["Wassergehalt Dampf"]
                    + einZustand1.at["Wassergehalt Flüssig-Fest"]
                )
                + einZustand2.at["Massenstrom"]
                / (
                    1
                    + einZustand2.at["Wassergehalt Dampf"]
                    + einZustand2.at["Wassergehalt Flüssig-Fest"]
                )
            )
            - 1
        )

        # Ausgangsenthalpie
        ausZustand.at["spezEnthalpie"] = (
            (
                einZustand1.at["Massenstrom"]
                / (
                    1
                    + einZustand1.at["Wassergehalt Dampf"]
                    + einZustand1.at["Wassergehalt Flüssig-Fest"]
                )
            )
            * einZustand1.at["spezEnthalpie"]
            + (
                einZustand2.at["Massenstrom"]
                / (
                    1
                    + einZustand2.at["Wassergehalt Dampf"]
                    + einZustand2.at["Wassergehalt Flüssig-Fest"]
                )
            )
            * einZustand2.at["spezEnthalpie"]
        ) / (ausZustand.at["Massenstrom"] / (1 + x_aus))

        # Ausgangsdruck und Druckverluste (muss noch näher untersucht werden)
        if einZustand1.at["Druck"] <= einZustand2.at["Druck"]:
            ausZustand.at["Druck"] = einZustand1.at["Druck"]
        else:
            ausZustand.at["Druck"] = einZustand2.at["Druck"]

        # Ausgangstemperatur
        ausZustand.at["Temperatur"] = (
            FeuchteLuftSI(
                "T",
                "H",
                ausZustand.at["spezEnthalpie"],
                "P",
                ausZustand.at["Druck"] * 10 ** 5,
                "W",
                x_aus,
            )
            - 273.15
        )

        # Wassergehalt aufspalten (gasförmig, flüssig/fest)
        if (
            FeuchteLuftSI(
                "R",
                "T",
                ausZustand.at["Temperatur"] + 273.15,
                "P",
                ausZustand.at["Druck"] * 10 ** 5,
                "W",
                x_aus,
            )
            <= 1
        ):

            ausZustand.at["Wassergehalt Dampf"] = x_aus
            ausZustand.at["Wassergehalt Flüssig-Fest"] = 0
        else:
            ausZustand.at["Wassergehalt Dampf"] = FeuchteLuftSI(
                "W",
                "T",
                ausZustand.at["Temperatur"] + 273.15,
                "P",
                ausZustand.at["Druck"] * 10 ** 5,
                "R",
                1,
            )
            ausZustand.at["Wassergehalt Flüssig-Fest"] = (
                x_aus - ausZustand.at["Wassergehalt Dampf"]
            )

    elif einZustand2.at["Massenstrom"] <= 0 < einZustand1.at["Massenstrom"]:
        ausZustand = einZustand1.copy()

    elif einZustand1.at["Massenstrom"] <= 0 < einZustand2.at["Massenstrom"]:
        ausZustand = einZustand2.copy()

    return ausZustand


def FeuchteLuftWasser(einZustand1, einZustand2):
    """
    Berechnung der Ausgangszustände bei der Mischung eines feuchten
    Luftstroms mit einem Wasserstrom.
    Der thermodynamische Prozess wird über die Energiebilanz ohne Verluste
    berechnet.

    Eingangswerte
    -------------
    einZustand1 : pandas.core.series.Series, float64
        Eingangszustand der feuchten Luft; Elemente: Massenstrom, Temperatur,
        Druck, Wassergehalt Dampf, Wassergehalt Flüssig-Fest, Enthalpie,
        Entropie, Volumen, Fluid
    einZustand2 : pandas.core.series.Series, float64
        Eingangszustand des Wassers; Elemente: Massenstrom, Temperatur,
        Druck, Enthalpie, Entropie, Volumen, Fluid

    Ausgangswerte
    -------------
    ausZustand : pandas.core.series.Series, float64
        Ausgangszustand der feuchten Luft; Elemente: Massenstrom,
        Temperatur, Druck, Wassergehalt Dampf, Wassergehalt Flüssig-Fest,
        Enthalpie, Entropie, Volumen, Fluid

    Gültigkeitsbereich
    ---------
        (siehe CoolProp)

    Notes
    -----
    Quelle:
        Baehr, H. D., Kabelac, S.: Thermodynamik - Grundlagen und
        technische Anwendungen. Heidelberg, Springer Verlag. 2006.

        Huhn, J.: Lehrveranstaltung Technische Thermodynamik -
        Teil Energielehre. TU Dresden. 2006.

        Bell, I. H.; Wronski, J.; Quoilin, S. und Lemort, V.: Pure and
        Pseudo-pure Fluid Thermophysical Property Evaluation and the
        Open-Source Thermophysical Property Library CoolProp. In: Industrial and
        Engineering Chemistry Research 53, S. 2498-2508. 2014.
    """
    # Ausgangszustände definieren
    ausZustand = einZustand1.copy()

    # Ausgangsmassenstrom
    ausZustand.at["Massenstrom"] = (
        einZustand1.at["Massenstrom"] + einZustand2.at["Massenstrom"]
    )

    if einZustand1.at["Massenstrom"] > 0 and einZustand2.at["Massenstrom"] > 0:

        # Ausgangswassergehalt
        x_aus = (
            einZustand1.at["Wassergehalt Dampf"]
            + einZustand1.at["Wassergehalt Flüssig-Fest"]
        ) + einZustand2.at["Massenstrom"] / (
            einZustand1.at["Massenstrom"]
            / (
                1
                + einZustand1.at["Wassergehalt Dampf"]
                + einZustand1.at["Wassergehalt Flüssig-Fest"]
            )
        )

        # Ausgangsenthalpie
        ausZustand.at["spezEnthalpie"] = einZustand1.at["spezEnthalpie"] + (
            einZustand2.at["spezEnthalpie"] * einZustand2.at["Massenstrom"]
        ) / (
            einZustand1.at["Massenstrom"]
            / (
                1
                + einZustand1.at["Wassergehalt Dampf"]
                + einZustand1.at["Wassergehalt Flüssig-Fest"]
            )
        )

        # Ausgangstemperatur
        ausZustand.at["Temperatur"] = (
            FeuchteLuftSI(
                "T",
                "H",
                ausZustand.at["spezEnthalpie"],
                "P",
                ausZustand.at["Druck"] * 10 ** 5,
                "W",
                x_aus,
            )
            - 273.15
        )

        # Neuen Wassergehalt aufspalten (gasförmig, flüssig/fest)
        if (
            FeuchteLuftSI(
                "R",
                "T",
                ausZustand.at["Temperatur"] + 273.15,
                "P",
                ausZustand.at["Druck"] * 10 ** 5,
                "W",
                x_aus,
            )
            <= 1.0
        ):

            ausZustand.at["Wassergehalt Dampf"] = x_aus
            ausZustand.at["Wassergehalt Flüssig-Fest"] = 0
        else:
            ausZustand.at["Wassergehalt Dampf"] = FeuchteLuftSI(
                "W",
                "T",
                ausZustand.at["Temperatur"] + 273.15,
                "P",
                ausZustand.at["Druck"] * 10 ** 5,
                "R",
                1,
            )
            ausZustand.at["Wassergehalt Flüssig-Fest"] = (
                x_aus - ausZustand.at["Wassergehalt Dampf"]
            )

    return ausZustand

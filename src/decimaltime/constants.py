import datetime as _datetime
from enum import Enum

COMPLEMENTARY_DAYS = (
    "La Fête de la Vertu", "La Fête du Génie", "La Fête du Travail", "La Fête de l'Opinion",
    "La Fête des Récompenses", "La Fête de la Révolution"
)

WEEK_DAYS = (
    "Primidi", "Duodi",   "Tridi",  "Quartidi", "Quintidi",
    "Sextidi", "Septidi", "Octidi", "Nonidi",   "Décadi"
)

class Weekday(Enum):
    Primidi = 1
    Duodi = 2
    Tridi = 3
    Quartidi = 4
    Quintidi = 5
    Sextidi = 6
    Septidi = 7
    Octidi = 8
    Nonidi = 9 
    Décadi = 0

class ComplementaryWeekday(Enum):
    """La Fête..."""
    Vertu = 1
    Génie = 2
    Travail = 3
    Opinion = 4
    Récompenses = 5
    Révolution = 6

MONTHS = (
    "Vendémiaire", "Brumaire", "Frimaire",  # Autumn
    "Nivôse", "Pluviôse", "Ventôse",  # Winter
    "Germinal", "Floréal", "Prairial",  # Spring
    "Messidor", "Thermidor", "Fructidor"  # Summer
)

class Month(Enum):
    Vendémiaire = 1
    Brumaire = 2
    Frimaire = 3
    Nivôse = 4
    Pluviôse = 5
    Ventôse = 6
    Germinal = 7
    Floréal = 8
    Prairial = 9
    Messidor = 10
    Thermidor = 11
    Fructidor = 12

class LeapYearRule(Enum):
    Straight4 = 0
    Romme = 1 # 4/100/400
    Goucher = 2 # 4/128


SPECIAL_LEAPS = (3,7,11,15,20)


MINYEAR = 1
MAXYEAR = 9999
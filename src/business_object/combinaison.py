"""Implementation de la classe Combinaison."""

from carte import Carte
from enum import IntEnum

class Combinaison(IntEnum):
    CarteHaute = 1
    Paire = 2
    DoublePaire = 3
    Brelan = 4
    Quinte = 5  
    Flush = 6 
    Full = 7
    Carre = 8
    QuinteFlush = 9
    QuinteRoyale = 10

    


"""Implementation de la classe Carte."""

class Carte :
    """
    La classe Carte permet de modéliser une carte du jeu,
    avec sa valeur et sa couleur.

    Parameters
    ----------
    valeur : str
    Valeur de la carte.
    couleur : str
    Couleur de la carte.

    Attributes
    ----------
    __VALEURS : tuple
    Tuple de l'ensemble des valeurs possibles pour une carte.
    __COULEURS : tuple
    Tuple de l'ensemble des couleurs possibles pour une carte.
    __valeur : str
    Valeur de la carte.
    __couleur : str
    Couleur de la carte.
    """

    __VALEURS = (
        "As",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Valet",
        "Dame",
        "Roi",
    )
    __COULEURS = ("Pique", "Carreau", "Coeur", "Trêfle")


    def __init__(self, valeur: str, couleur: str):
        if valeur not in self.__VALEURS:
            raise ValueError(f"Valeur {valeur} non valide")
        if couleur not in self.__COULEURS:
            raise ValueError(f"Couleur {couleur} non valide")
        self.__valeur = valeur
        self.__couleur = couleur


    @classmethod
    def VALEURS(cls):
        return cls.__VALEURS

    @classmethod
    def COULEURS(cls):
        return cls.__COULEURS
    
    @property
    def valeur(self):
        return self.__valeur

    @property
    def couleur(self):
        return self.__couleur

    def __eq__(self, other):
        if isinstance(other, Carte):
            return (self.__valeur, self.__couleur) == (other.__valeur, other.__couleur)
        else:
            return False

    def __str__(self):
        return f"{self.__valeur} de {self.__couleur.lower()}"

    def __repr__(self):
        return f"Carte({self.__valeur!r}, {self.__couleur!r})"

    def __hash__(self):
        return hash(repr(self))
    
    @classmethod
    def from_str(cls, s: str) -> "Carte":
        """
        Reconstruit une carte à partir d'une chaîne de type "valeur de couleur", 
        ex: "As de coeur" ou "10 de pique".
        """
        try:
            valeur, couleur = s.split(" de ", 1)
            couleur = couleur.capitalize() #car stocké avec le format str en bdd
            return cls(valeur=valeur, couleur=couleur)
        except Exception as e:
            raise ValueError(f"Impossible de créer une Carte à partir de '{s}'") from e


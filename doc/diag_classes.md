
# Diagramme de classes des objets métiers

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/classDiagram.html) :

* avantage : facile à coder
* inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :

* à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
* rechercher `mermaid`
  * installer l'extension **Markdown Preview Mermaid Support**
* revenir sur ce fichier
  * faire **CTRL + K**, puis **V**

```mermaid
classDiagram
    class Joueurb {
        +id_joueur: int
        +pseudo: string
        +mdp: string
        +age: int
        +mail: string
        +fan_pokemon: bool
    }

    class Siege {
      - id_siege_ : int
    }

    class Table {
      - id_table_ : int
      - grosse_blinde : dict[siege : int, valeur : int]
    }

    class Partie {
      + id_partie : int
      + joueurs : list[JoueurPartie]
      + repartition_blinde()
      + calcul_gagnant(flop, dict[Joueur : Main])
    }

    class JoueurPartie {
        + main : Main
        + statut : str
        + miser()
        + se_coucher()
        + suivre()
    }
    
    class Joueur {
        + identifiant : str
        + pseudo : str
        + mot_de_passe : str
        + credit : int
        + jouer_partie()
        + augmenter_credit()

    }

    class Combinaison {
      - cartes : list[cartes]
      + combinaison() : int
    }

    class Flop {
      «Create» __init__(cartes : list[Carte] = [])
    }
    
    class Carte{
      VALEURS : tuple[str]
      COULEURS : tuple[str]
      - valeur : str
      - couleur : str
      «property» + valeur : str
      «property» + couleur : str
      «Create» __init__(valeur : str, couleur : str)
      «classmethod» + VALEURS() : tuple[str]
      «classmethod» + COULEURS() : tuple[str]
      __eq__(other) : bool
      __str__() : str
      __repr__() : str
      __hash__() : int
    }

    class Croupier {
      + melanger(cartes : ListeDeCartes)
      + ajouter_carte(cartes : ListeDeCartes,  carte : Carte)

    }

    class ListeDeCartes{
      - cartes : list[Carte]
      «Create» __init__(cartes : list[Carte] or None)
      - __str__() : str
      - __len__() : int
    }

    VueAbstraite <|-- AccueilVue
    VueAbstraite <|-- ConnexionVue
    VueAbstraite <|-- MenuJoueurVue
    MenuJoueurVue ..> JoueurService : appelle
    ConnexionVue ..> JoueurService : appelle
    JoueurService ..> JoueurDao : appelle
    Joueur <.. JoueurService: utilise
    Joueur <.. JoueurDao: utilise
    Carte "1" o-- "1..*" Combinaison : contient
```

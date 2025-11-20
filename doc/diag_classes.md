# Diagramme de classes des objets métiers

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/classDiagram.html) :

* avantage : facile à coder
* inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :
kv
* à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
* rechercher `mermaid`
  * installer l'extension **Markdown Preview Mermaid Support**
* revenir sur ce fichier
  * faire **CTRL + K**, puis **V**

```mermaid
classDiagram
    class Joueur {
      + id_joueur : str
      + pseudo : str
      - mot_de_passe : str
      - credit : int
      «Create» __init__(id_joueur : str, pseudo : str, mot_de_passe : str, credit : int = 0)
      + jouer_partie() void
      + augmenter_credit(montant : int)
    }

    class Admin {
      + crediter_joueur(joueur :  Joueur)
      + consulter_stat() dict
    }

    class Transaction {
      - id_transaction : int
      - id_joueur : int
      - solde : int
      - date : datetime
      «Create» __init__(id_transaction : int, joueur_id : str, solde : int, date : datetime)
    }

      class Pot {
      - montant_pot : Monnaie
      - joueurs_contributeurs : list[JoueurPartie]
      «Create» __init__(montant_pot : int = 0, joueurs_contributeurs : list[int] = [])
      + grouper_mise () void
      + affecter_pot () void
      + reinitialiser_pot () void

    }

    class Siege {
      + id_siege : int
      + est_occupe : bool
      «Create» __init__(id_siege : int)
      + occuper() void
      + liberer() void
    }

    class Monnaie {
      + valeur : int
      «Create» __init__(valeur : int)
      + __str__() str
      + __repr__() str
    }

    class Table {
      + id_table_ : int
      + nb_sieges : int
      + nb_joueurs: int
      + blind_initial : Monnaie
      «Create» __init__(id_table : int, nb_sieges : int, blind_initial : Monnaie)
    }

    class AccessPartie {
      + tables : list[Table]
      «Create» __init__()
      + rejoindre_table(joueur : Joueur) bool
      + creer_table(nb_sieges : int) Table
    }

    class Main {
      + id_partie : int
      + joueurs : list[JoueurPartie]
      «Create» __init__(id_partie : int, joueurs : list[JoueurPartie] = [])
      + calcul_gagnant(joueurs: Joueur, MainJoueurComplete): Joueur
    }


    class Partie {
      + id_partie : int
      + joueurs : list[JoueurPartie]
      + tour : int
      + pot : Pot
      «Create» __init__(id_partie : int, joueurs : list[JoueurPartie] = [])
      + repartition_blind() void
      + gerer_blind() void
      + finir_partie() bool
    }

    class JoueurPartie {
        + main : Main
        + statut : str
        + dealer : bool
        + siege : Siege
        «Create» __init__(joueur : Joueur, siege : Siege)
        + miser(montant : int)
        + se_coucher() void
        + suivre() void
    }
    
    class MainJoueurComplete {
      - cartes : list[cartes]
      «Create» __init__(cartes : list[Carte] = [])
      + combinaison() int
    }

    class MainJoueur {
      - cartes : tuple[Carte]
      «Create» __init__(cartes : tuple[Carte])
    }

    class Combinaison {
      - cartes : list[cartes]
      «Create» __init__(cartes : list[Carte] = [])
      + combinaison() int
      
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
      __eq__(other) bool
      __str__() str
      __repr__() str
      __hash__() int
    }

    class Croupier {
      + pioche : ListeDeCartes
      «Create» __init__(pioche : ListeDeCartes = None)
      + melanger(cartes : ListeDeCartes)
      + debarrasser (cartes: ListeDeCartes)
      + ajouter_carte(cartes : ListeDeCartes,  carte : Carte)

    }

    class ListeDeCartes{
      - cartes : list[Carte]
      «Create» __init__(cartes : list[Carte] or None)
      - __str__() str
      - __len__() int
      + ajouter_carte(carte : Carte)
    }

    class DeroulementPartie {
      + big_blind : Monnaie
      + small_blind : Monnaie
      + access_partie : AccessPartie
      + table : Table
      + pioche : ListeCartes
      + croupier : Croupier
      + pot : Pot
      + transactions : list[Transaction]
      + partie : Partie
      + joueurs_partie : list[JoueurPartie]
      «Create» __init__(joueurs : list[Joueur], big_blind : int, small_blind : int, logger=None)
      + lancer_partie() void
      - _collecter_blinds() void
      - _tour_de_table(phase : str) void
      - _showdown(cartes_communes : list[Carte]) void
    }

    Joueur <|-- JoueurPartie
    ListeDeCartes <|-- Flop
    ListeDeCartes <|-- Combinaison
    ListeDeCartes <|-- MainJoueurComplete
    Joueur "1" --> "1..*" AccessPartie : accède
    AccessPartie "1" o-- "1..*" Table : contient
    Partie "1" --> "0..*" JoueurPartie : contient
    Partie "1" o-- "1" Pot : possède
    Partie "1" --> "1" Table : se_joue_sur
    Croupier "1" o-- "1..*" Carte : gère
    JoueurPartie "1..8" o-- "1..*" Main : gère
    Main "1" o-- "1..8" MainJoueurComplete : compare
    MainJoueurComplete "1" o-- "0..1" MainJoueur : contient
    MainJoueurComplete "1" o-- "0..1" Flop : contient
    ListeDeCartes "1" o-- "1..*" Carte : contient
    Table "1" o-- "1..8" Siege : contient
    JoueurPartie "1" o-- "1" Siege : occupe
    MainJoueur "1" o-- "1..*" Carte: utilise
    Joueur "1" o-- "1..*" Monnaie : possède  
    Pot "1" o-- "1..*" Monnaie : possède  
    Admin "1" -- "0..*" Transaction: permet
    Transaction "1" o-- "1..*" Monnaie : contient
    Joueur "1" --> "1" Transaction : débite
    Transaction "1" --> "1" Joueur : crédite
    DeroulementPartie "1" o-- "1" Pot : possède
    DeroulementPartie "1" --> "0..*" JoueurPartie : interagit_avec
    DeroulementPartie "1" --> "1" Table : se_deroule_sur
    DeroulementPartie "1" o-- "1" Croupier : gère
```

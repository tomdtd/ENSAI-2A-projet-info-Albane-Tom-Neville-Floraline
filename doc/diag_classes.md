
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
    class Joueur {
      + id_joueur : str
      + pseudo : str
      + mot_de_passe : str
      + credit : int
      + jouer_partie(): void
      + augmenter_credit(montant : int)
    }

    class Admin {
      + crediter_joueur(joueur :  Joueur)
      + consulter_stat() : dict
    }

    class Transaction {
      - id_transaction : int
      - id_joueur : int
      - solde : int
      - date : datetime
    }

      class Pot {
      - montant_pot : int
      - joueurs_contributeurs : list[int]
      - grouper_mise (): void
      - affecter_pot (): void
      - reinitialiser_pot (): void

    }

    class Siege {
      - id_siege_ : int
      - est_occupe : bool
    }

    class Monnaie {
      - valeur : int
    }

    class Table {
      - id_table_ : int
      - nb_sieges : int
      - nb_joueurs: int
      - blind_initial : monnaie
    }

    class AccessPartie {
      + tables_ : int
      + id_partie : int
      + rejoindre_table(joueur : Joueur) : bool
      + creer_table(nb_sieges : int) : Table
    }

    class Main {
      + id_partie : int
      + joueurs : list[JoueurPartie]
      + calcul_gagnant(joueurs: Joueur, MainJoueurComplete):Joueur
    }


    class Partie {
      + id_partie : int
      + joueurs : list[JoueurPartie]
      + tour : int
      + pot : Pot
      + repartition_blind() : void
      + gerer_blind() : void
      + finir_partie() : bool
    }

    class JoueurPartie {
        + main : Main
        + statut : str
        + miser(montant : int)
        + se_coucher() : void
        + suivre() : void
    }
    
    class MainJoueurComplete {
      «Create» __init__(cartes : list[Carte] = [])
      - cartes : list[cartes]
      + combinaison() : int
    }

    class MainJoueur {
      «Create» __init__(cartes : tuple[Carte])
      - cartes : tuple[Carte]
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
      + debarrasser (cartes: ListeDeCartes)
      + ajouter_carte(cartes : ListeDeCartes,  carte : Carte)

    }

    class ListeDeCartes{
      - cartes : list[Carte]
      «Create» __init__(cartes : list[Carte] or None)
      - __str__() : str
      - __len__() : int
    }

    Joueur <|-- JoueurPartie
    ListeDeCartes <|-- Flop
    ListeDeCartes <|-- Combinaison
    ListeDeCartes <|-- MainJoueurComplete
    AccessPartie "1" o-- "1..*" Partie : ouvre
    Partie "1" --> "0..*" JoueurPartie : contient
    Partie "1" o-- "1" Pot : possède
    Partie "1" --> "1" Table : se_joue_sur
    Croupier "1" o-- "1..*" Carte : gère
    JoueurPartie "1..8" o-- "1..*" Main : gère
    JoueurPartie "1..8" o-- "1*" MainJoueurComplete : compare
    MainJoueur "1" o-- "2" ListeDeCartes : contient
    MainJoueurComplete "1" o-- "2" MainJoueur : contient
    ListeDeCartes "1" *-- "1..*" Carte : contient
    Table "1" o-- "1..8" Siege : contient
    JoueurPartie "0..1" o-- "1" Siege : occupe
    MainJoueur "1" o-- "1..*" ListeDeCartes: utilise
    Joueur "1" o-- "1" Monnaie : possède  
    Transaction "1" -- "0..*" Admin : permet
    Transaction "1" --> "1" Monnaie : utilise
    Transaction "1" --> "1" Joueur : débite
    Transaction "1" --> "1" Joueur : crédite
```

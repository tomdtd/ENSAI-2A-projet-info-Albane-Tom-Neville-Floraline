
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
      + identifiant : str
      + pseudo : str
      + mot_de_passe : str
      + credit : int
      + jouer_partie()
      + augmenter_credit()
    }

    class Admin {
      + crediter_joueur()
      + consulter_stat()
    }

    class Transaction {
      - id_transaction_ : int
      - id_joueur : int
      - solde : int
      - date : datetime
    }

      class Pot {
      - montant_pot : int
      - id_joueur : int
      - grouper_mise :list[int]
      - affecter_pot :list[int]
      - reinitialiser_pot :list[int]

    }

    class Siege {
      - id_siege_ : int
    }

    class Monnaie {
      - monnaie : int
    }

    class Table {
      - id_table_ : int
      - nb_siege : int
      - nb_joueur: int
      - grosse_blinde : monnaie
    }

    class AccessPartie {
      + tables_ : int
      + id_partie : int
      + rejoindre_table()
      + creer_table()
    }

    class Main {
      + id_partie : int
      + joueurs : list[JoueurPartie]
      + repartition_blinde()
      + calcul_gagnant(flop, dict[Joueur : Main])
    }


    class Partie {
      + id_partie : int
      + joueurs : list[JoueurPartie]
      + pot : list[monnaie]
      + finir_partie() : bool
    }

    class JoueurPartie {
        + main : Main
        + statut : str
        + miser()
        + se_coucher()
        + suivre()
    }
    
    class MainJoueur {
      «Create» __init__(cartes : list[Carte] = [])
      - cartes : list[cartes]
      + combinaison() : int
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

    Joueur <|-- JoueurPartie
    ListeDeCartes <|-- Flop
    Partie "1" o-- "1..*" JoueurPartie : participe
    Carte "1..*" o-- "1..5" Combinaison : contient
    Carte "1..*" o-- "1..*" ListeDeCartes : contient
    Siege "1..8" o-- "1" Table : contient
```

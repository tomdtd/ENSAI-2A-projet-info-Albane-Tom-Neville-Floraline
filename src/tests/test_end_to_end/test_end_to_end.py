"""Test qui simule plusieurs joueurs connectés au serveur
(Attention ces tests ne fonctionnent que si la base de donnée prod_poker est vide)"""

import pexpect
import sys
import os
import re
import random
import string


def random_pseudo(prefix="test_joueur"):
    """Génère un pseudo unique pour chaque test"""
    return prefix + "".join(random.choices(string.ascii_lowercase + string.digits, k=5))


# Regex pour ignorer les séquences ANSI (couleurs, curseur, etc.)
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def test_creation_et_connexion_joueur_ok():
    pseudo = random_pseudo()
    email = pseudo + "@gmail.com"
    mdp = "Test_joueur1"
    age = "22"

    main_path = os.path.abspath("src/main.py")

    # Création du joueur
    child = pexpect.spawn(sys.executable, [main_path], encoding='utf-8', timeout=30)
    child.setwinsize(40, 120)

    # Menu affiché
    child.expect("Se connecter")
    child.expect("Créer un compte")
    child.expect("Quitter")

    # Commande pour aller sur "Créer un compte" (flèche bas puis Entrer)
    child.send("\x1b[B\r")

    # Interaction avec prompts
    child.expect("Entrez votre pseudo")
    child.sendline(pseudo)

    child.expect("Entrez votre mot de passe")
    child.sendline(mdp)

    child.expect("Entrez votre age")
    child.sendline(age)

    child.expect("Entrez votre mail")
    child.sendline(email)

    # Vérifier le message de succès
    child.expect(f"Votre compte {pseudo} a été créé")

    child.terminate(force=True)

    # Connection du joueur
    child = pexpect.spawn(sys.executable, [main_path], encoding='utf-8', timeout=30)
    child.setwinsize(40, 120)

    # Menu principal
    child.expect("Se connecter")
    child.expect("Créer un compte")
    child.expect("Quitter")

    # Choisir "Se connecter" (option 1 : entrer -> \r)
    child.send("\r")

    # Interagir avec prompts de connexion
    child.expect("Entrez votre pseudo")
    child.sendline(pseudo)

    child.expect("Entrez votre mot de passe")
    child.sendline(mdp)

    # Vérifier message de connexion réussie
    child.expect(f"Vous êtes connecté sous le pseudo {pseudo}")

    child.terminate(force=True)


def creer_compte(child, pseudo, mdp="Test_joueur1", age="22", email=None):
    """Simule la création d'un compte joueur"""
    if email is None:
        email = f"{pseudo}@gmail.com"
    child.expect("Se connecter")
    child.expect("Créer un compte")
    child.expect("Quitter")
    child.send("\x1b[B\r")  # choisir "Créer un compte"
    child.expect("Entrez votre pseudo")
    child.sendline(pseudo)
    child.expect("Entrez votre mot de passe")
    child.sendline(mdp)
    child.expect("Entrez votre age")
    child.sendline(age)
    child.expect("Entrez votre mail")
    child.sendline(email)
    child.expect(f"Votre compte {pseudo} a été créé")


def se_connecter(child, pseudo, mdp="Test_joueur1"):
    """Simule la connexion d'un joueur"""
    child.expect("Se connecter")
    child.expect("Créer un compte")
    child.expect("Quitter")
    child.send("\r")  # choisir "Se connecter"
    child.expect("Entrez votre pseudo")
    child.sendline(pseudo)
    child.expect("Entrez votre mot de passe")
    child.sendline(mdp)
    child.expect(f"Vous êtes connecté sous le pseudo {pseudo}")
    child.expect("Rejoindre une partie")


def test_deux_joueurs_rejoignent_partie():
    main_path = os.path.abspath("src/main.py")

    # Générer des pseudos aléatoires
    pseudo1 = random_pseudo("joueur1_")
    pseudo2 = random_pseudo("joueur2_")
    mdp = "Test_joueur1"

    # Lancer deux sessions terminal simulées
    player1 = pexpect.spawn(sys.executable, [main_path], encoding="utf-8", timeout=30)
    player2 = pexpect.spawn(sys.executable, [main_path], encoding="utf-8", timeout=30)

    player1.setwinsize(40, 120)
    player2.setwinsize(40, 120)

    # Création des comptes
    creer_compte(player1, pseudo1, mdp)
    creer_compte(player2, pseudo2, mdp)

    # Connexion
    se_connecter(player1, pseudo1, mdp)
    se_connecter(player2, pseudo2, mdp)

    # Les deux joueurs choisissent "Rejoindre une partie"
    player1.expect("Faites votre choix")
    player1.send("\r")  # "Rejoindre une partie"
    player2.expect("Faites votre choix")
    player2.send("\r")

    # Les deux joueurs choisissent une table
    player1.expect("Que voulez-vous faire")
    player1.sendline("\r") # Créer une nouvelle table
    player2.expect("Que voulez-vous faire")
    player2.sendline("\r") # Attention ne fonctionnera que si la table table_poker est vide ! (pas de Table 1)
    
    # Attendre la confirmation que l'autre joueur a rejoint
    player1.expect(r".*Vous avez rejoint la Table.*")
    player2.expect(r".*Vous avez rejoint la Table.*")

    # Terminer les sessions
    player1.terminate(force=True)
    player2.terminate(force=True)

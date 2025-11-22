"""Test qui simule plusieurs joueurs connectés au serveur.

Ces tests end-to-end utilisent pexpect pour simuler des interactions
utilisateur avec l'application de poker via le terminal.

Prérequis:
- Base de données PostgreSQL fonctionnelle
- L'API FastAPI doit être lancée (automatiquement par la fixture)

Les pseudos sont générés aléatoirement pour éviter les conflits.
"""

import pexpect
import pytest
import sys
import os
import re
import random
import string
import time
import subprocess
import signal
import socket

# Regex pour nettoyer les séquences ANSI (couleurs, curseur, etc.)
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# Timeout par défaut pour les interactions pexpect
DEFAULT_TIMEOUT = 30

# Configuration de l'API
API_HOST = "127.0.0.1"
API_PORT = 9678


def get_project_root():
    """Retourne le chemin racine du projet."""
    # Remonte depuis src/tests/test_end_to_end jusqu'à la racine
    current = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(current)))


def is_port_in_use(port):
    """Vérifie si un port est déjà utilisé."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((API_HOST, port)) == 0


def wait_for_api(timeout=30):
    """Attend que l'API soit disponible."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(API_PORT):
            # Vérifier que l'API répond
            try:
                import requests
                response = requests.get(f"http://{API_HOST}:{API_PORT}/", timeout=2)
                if response.status_code == 200:
                    return True
            except Exception:
                pass
        time.sleep(0.5)
    return False


@pytest.fixture(scope="module")
def api_server():
    """Lance l'API FastAPI pour les tests E2E."""
    project_root = get_project_root()

    # Vérifier si l'API est déjà lancée
    if is_port_in_use(API_PORT):
        print(f"API déjà en cours d'exécution sur le port {API_PORT}")
        yield None
        return

    # Préparer l'environnement
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root

    # Lancer l'API en arrière-plan
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api:app",
         "--host", API_HOST, "--port", str(API_PORT)],
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Attendre que l'API soit prête
    if not wait_for_api(timeout=30):
        api_process.terminate()
        pytest.skip("Impossible de démarrer l'API")

    print(f"API démarrée sur http://{API_HOST}:{API_PORT}")

    yield api_process

    # Arrêter l'API après les tests
    if api_process:
        api_process.terminate()
        try:
            api_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
        print("API arrêtée")


def clean_ansi(text):
    """Nettoie les séquences ANSI d'un texte."""
    if text is None:
        return ""
    return ANSI_ESCAPE_PATTERN.sub('', text)


def random_pseudo(prefix="test_joueur"):
    """Génère un pseudo unique pour chaque test."""
    return prefix + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


@pytest.fixture
def main_path():
    """Retourne le chemin absolu vers main.py."""
    project_root = get_project_root()
    return os.path.join(project_root, "src", "main.py")


def spawn_app(main_path, timeout=DEFAULT_TIMEOUT):
    """Crée une nouvelle instance de l'application avec pexpect."""
    project_root = get_project_root()

    # Définir PYTHONPATH et API_URL pour que l'application fonctionne
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root
    env['API_URL'] = f"http://{API_HOST}:{API_PORT}"

    child = pexpect.spawn(
        sys.executable,
        [main_path],
        encoding='utf-8',
        timeout=timeout,
        cwd=project_root,
        env=env
    )
    child.setwinsize(40, 120)
    return child


def test_creation_et_connexion_joueur_ok(api_server, main_path):
    """Test la création d'un compte joueur puis sa connexion."""
    pseudo = random_pseudo()
    email = pseudo + "@gmail.com"
    mdp = "Test_joueur1"
    age = "22"

    child = None
    try:
        # Création du joueur
        child = spawn_app(main_path)

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

    finally:
        if child:
            child.terminate(force=True)

    # Connexion du joueur
    child = None
    try:
        child = spawn_app(main_path)

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

    finally:
        if child:
            child.terminate(force=True)


def creer_compte(child, pseudo, mdp="Test_joueur1", age="22", email=None):
    """Simule la création d'un compte joueur.

    Args:
        child: Instance pexpect de l'application
        pseudo: Pseudo du joueur à créer
        mdp: Mot de passe (défaut: Test_joueur1)
        age: Age du joueur (défaut: 22)
        email: Email du joueur (défaut: {pseudo}@gmail.com)
    """
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
    """Simule la connexion d'un joueur.

    Args:
        child: Instance pexpect de l'application
        pseudo: Pseudo du joueur
        mdp: Mot de passe (défaut: Test_joueur1)
    """
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


def test_deux_joueurs_rejoignent_partie(api_server, main_path):
    """Test que deux joueurs peuvent créer des comptes et rejoindre une partie."""
    # Générer des pseudos aléatoires
    pseudo1 = random_pseudo("joueur1_")
    pseudo2 = random_pseudo("joueur2_")
    mdp = "Test_joueur1"

    player1 = None
    player2 = None

    try:
        # Lancer deux sessions terminal simulées
        player1 = spawn_app(main_path)
        player2 = spawn_app(main_path)

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
        # Note: send("\r") au lieu de sendline("\r") pour éviter le double retour chariot
        player1.expect("Que voulez-vous faire")
        player1.send("\r")  # Créer une nouvelle table
        player2.expect("Que voulez-vous faire")
        player2.send("\r")  # Rejoindre la table existante

        # Attendre la confirmation que chaque joueur a rejoint une table
        player1.expect(r".*Vous avez rejoint la Table.*")
        player2.expect(r".*Vous avez rejoint la Table.*")

    finally:
        # Toujours terminer les sessions proprement
        if player1:
            player1.terminate(force=True)
        if player2:
            player2.terminate(force=True)

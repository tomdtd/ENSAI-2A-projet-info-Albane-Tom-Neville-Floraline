import dotenv

from view.accueil_vue import AccueilVue


"""
Classe de lancement de l'application
"""
if __name__ == "__main__":
    # On charge les variables d'envionnement
    dotenv.load_dotenv(override=True)

    vue_courante = AccueilVue("Bienvenue")
    nb_erreurs = 0

    while vue_courante:
        if nb_erreurs > 100:
            print("Le programme recense trop d'erreurs et va s'arrêter")
            break
        try:
            # Affichage du menu
            vue_courante.afficher()

            # Affichage des choix possibles
            vue_courante = vue_courante.choisir_menu()
        except Exception as e:
            print(e)
            nb_erreurs += 1
            vue_courante = AccueilVue(
                "Une erreur est survenue, retour au menu principal"
            )

    # Lorsque l on quitte l application
    print("----------------------------------")
    print("Au revoir")

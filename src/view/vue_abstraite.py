from abc import ABC, abstractmethod


class VueAbstraite(ABC):
    def __init__(self, message=""):
        self.message = message

    def nettoyer_console(self):
        for i in range(30):
            print("")

    def afficher(self) -> None:
        """Echappe un grand espace dans le terminal pour simuler le changement de page de l'application"""
        self.nettoyer_console()
        print(self.message)
        print()

    @abstractmethod
    def choisir_menu(self):
        pass

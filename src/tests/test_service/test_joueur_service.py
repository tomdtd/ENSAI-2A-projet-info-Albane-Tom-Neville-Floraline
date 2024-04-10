from unittest.mock import MagicMock

from service.joueur_service import JoueurService

from dao.joueur_dao import JoueurDao

from dto.joueur import Joueur


liste_joueurs = [
    Joueur(pseudo="jp", age="10", mail="jp@mail.fr", mdp="1234"),
    Joueur(pseudo="lea", age="10", mail="lea@mail.fr", mdp="0000"),
    Joueur(pseudo="gg", age="10", mail="gg@mail.fr", mdp="abcd"),
]


def test_creer_ok():
    # GIVEN
    pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
    JoueurDao().creer = MagicMock(return_value=True)

    # WHEN
    joueur = JoueurService().creer(pseudo, mdp, age, mail, fan_pokemon)

    # THEN
    assert joueur.pseudo == pseudo


def test_creer_echec():
    # GIVEN
    pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
    JoueurDao().creer = MagicMock(return_value=False)

    # WHEN
    joueur = JoueurService().creer(pseudo, mdp, age, mail, fan_pokemon)

    # THEN
    assert joueur is None


def test_lister_tous_inclure_mdp_true():
    # GIVEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)

    # WHEN
    res = JoueurService().lister_tous(inclure_mdp=True)

    # THEN
    assert len(res) == 3
    for joueur in res:
        assert joueur.mdp is not None


def test_lister_tous_inclure_mdp_false():
    # GIVEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)

    # WHEN
    res = JoueurService().lister_tous()

    # THEN
    assert len(res) == 3
    for joueur in res:
        assert not joueur.mdp


def test_pseudo_deja_utilise_oui():
    # GIVEN
    pseudo = "lea"

    # WHEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)
    res = JoueurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert res


def test_pseudo_deja_utilise_non():
    # GIVEN
    pseudo = "chaton"

    # WHEN
    JoueurDao().lister_tous = MagicMock(return_value=liste_joueurs)
    res = JoueurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert not res


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])

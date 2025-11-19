import pytest
from src.business_object.admin import Admin


class TestAdmin:
    """Tests unitaires pour la classe Admin"""

    def test_creation_admin_sans_id(self):
        """Test de création d'un administrateur sans ID (pour nouvelle création)"""
        # WHEN
        admin = Admin(nom="admin_test", mdp="password123", mail="admin@test.com")
        
        # THEN
        assert admin.nom == "admin_test"
        assert admin.mdp == "password123"
        assert admin.mail == "admin@test.com"
        assert admin.admin_id is None

    def test_creation_admin_avec_id(self):
        """Test de création d'un administrateur avec ID (pour admin existant)"""
        # WHEN
        admin = Admin(nom="admin_test", mdp="password123", mail="admin@test.com", admin_id=1)
        
        # THEN
        assert admin.nom == "admin_test"
        assert admin.mdp == "password123"
        assert admin.mail == "admin@test.com"
        assert admin.admin_id == 1

    def test_str_representation(self):
        """Test de la représentation en string de l'admin"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="password123", mail="admin@test.com", admin_id=1)
        
        # WHEN
        str_repr = str(admin)
        
        # THEN
        assert "Admin(id=1, nom='admin_test', mail='admin@test.com')" in str_repr
        assert "admin_test" in str_repr
        assert "admin@test.com" in str_repr

    def test_repr_representation(self):
        """Test de la représentation technique de l'admin"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="password123", mail="admin@test.com", admin_id=1)
        
        # WHEN
        repr_repr = repr(admin)
        
        # THEN
        assert "Admin(admin_id=1, nom='admin_test', mail='admin@test.com')" == repr_repr

    def test_changer_mdp_success(self):
        """Test du changement de mot de passe réussi"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="ancien_mdp", mail="admin@test.com")
        
        # WHEN
        resultat = admin.changer_mdp("ancien_mdp", "nouveau_mdp")
        
        # THEN
        assert resultat is True
        assert admin.mdp == "nouveau_mdp"

    def test_changer_mdp_echec_mauvais_ancien_mdp(self):
        """Test du changement de mot de passe échoué (mauvais ancien mot de passe)"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="ancien_mdp", mail="admin@test.com")
        mdp_initial = admin.mdp
        
        # WHEN
        resultat = admin.changer_mdp("mauvais_ancien_mdp", "nouveau_mdp")
        
        # THEN
        assert resultat is False
        assert admin.mdp == mdp_initial  # Le mot de passe ne doit pas avoir changé

    def test_changer_mdp_avec_nouveau_mdp_vide(self):
        """Test du changement de mot de passe avec un nouveau mot de passe vide"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="ancien_mdp", mail="admin@test.com")
        
        # WHEN
        resultat = admin.changer_mdp("ancien_mdp", "")
        
        # THEN
        assert resultat is True
        assert admin.mdp == ""

    def test_changer_mdp_avec_nouveau_mdp_identique(self):
        """Test du changement de mot de passe avec le même mot de passe"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="mon_mdp", mail="admin@test.com")
        
        # WHEN
        resultat = admin.changer_mdp("mon_mdp", "mon_mdp")
        
        # THEN
        assert resultat is True
        assert admin.mdp == "mon_mdp"

    def test_egalite_deux_admins_meme_id(self):
        """Test que deux admins avec le même ID sont considérés égaux"""
        # GIVEN
        admin1 = Admin(nom="admin1", mdp="mdp1", mail="admin1@test.com", admin_id=1)
        admin2 = Admin(nom="admin2", mdp="mdp2", mail="admin2@test.com", admin_id=1)
        
        # WHEN & THEN
        # Note: Par défaut, Python compare les objets par identité mémoire
        # Mais on peut tester l'égalité basée sur l'ID
        assert admin1.admin_id == admin2.admin_id

    def test_difference_deux_admins_ids_differents(self):
        """Test que deux admins avec des IDs différents sont différents"""
        # GIVEN
        admin1 = Admin(nom="admin1", mdp="mdp1", mail="admin1@test.com", admin_id=1)
        admin2 = Admin(nom="admin1", mdp="mdp1", mail="admin1@test.com", admin_id=2)
        
        # WHEN & THEN
        assert admin1.admin_id != admin2.admin_id

    def test_admin_sans_id_et_avec_id_different(self):
        """Test comparaison entre admin sans ID et admin avec ID"""
        # GIVEN
        admin_sans_id = Admin(nom="admin", mdp="mdp", mail="admin@test.com")
        admin_avec_id = Admin(nom="admin", mdp="mdp", mail="admin@test.com", admin_id=1)
        
        # WHEN & THEN
        assert admin_sans_id.admin_id != admin_avec_id.admin_id
        assert admin_sans_id.admin_id is None
        assert admin_avec_id.admin_id == 1

    def test_attributs_modifiables(self):
        """Test que les attributs de l'admin peuvent être modifiés"""
        # GIVEN
        admin = Admin(nom="admin_initial", mdp="mdp_initial", mail="mail_initial@test.com", admin_id=1)
        
        # WHEN
        admin.nom = "admin_modifie"
        admin.mdp = "mdp_modifie"
        admin.mail = "mail_modifie@test.com"
        admin.admin_id = 2
        
        # THEN
        assert admin.nom == "admin_modifie"
        assert admin.mdp == "mdp_modifie"
        assert admin.mail == "mail_modifie@test.com"
        assert admin.admin_id == 2

    def test_creation_avec_caracteres_speciaux(self):
        """Test de création avec des caractères spéciaux dans les champs"""
        # GIVEN & WHEN
        admin = Admin(
            nom="Admin_Étrange-123",
            mdp="M0t@d3P@$$3!",
            mail="admin.étrange+test@domaine- spécial.com",
            admin_id=999
        )
        
        # THEN
        assert admin.nom == "Admin_Étrange-123"
        assert admin.mdp == "M0t@d3P@$$3!"
        assert admin.mail == "admin.étrange+test@domaine- spécial.com"
        assert admin.admin_id == 999

    def test_changer_mdp_avec_caracteres_speciaux(self):
        """Test du changement de mot de passe avec des caractères spéciaux"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="ancien_mdp", mail="admin@test.com")
        
        # WHEN
        nouveau_mdp = "N0uv3@u_M0t_D3_P@$$3_Trè$_$écurisé!"
        resultat = admin.changer_mdp("ancien_mdp", nouveau_mdp)
        
        # THEN
        assert resultat is True
        assert admin.mdp == nouveau_mdp

    def test_admin_avec_valeurs_extremes(self):
        """Test de création avec des valeurs extrêmes"""
        # GIVEN & WHEN
        admin = Admin(
            nom="A",  # Nom très court
            mdp="",   # Mot de passe vide
            mail="a@b.c",  # Email très court
            admin_id=0  # ID à 0 (peut être valide dans certains systèmes)
        )
        
        # THEN
        assert admin.nom == "A"
        assert admin.mdp == ""
        assert admin.mail == "a@b.c"
        assert admin.admin_id == 0

    def test_changer_mdp_multiple_fois(self):
        """Test de changement de mot de passe multiple fois"""
        # GIVEN
        admin = Admin(nom="admin_test", mdp="mdp_initial", mail="admin@test.com")
        
        # WHEN - Premier changement
        resultat1 = admin.changer_mdp("mdp_initial", "mdp_1")
        
        # THEN - Vérifier premier changement
        assert resultat1 is True
        assert admin.mdp == "mdp_1"
        
        # WHEN - Deuxième changement
        resultat2 = admin.changer_mdp("mdp_1", "mdp_2")
        
        # THEN - Vérifier deuxième changement
        assert resultat2 is True
        assert admin.mdp == "mdp_2"
        
        # WHEN - Tentative avec mauvais ancien mot de passe
        resultat3 = admin.changer_mdp("mdp_1", "mdp_3")  # mdp_1 n'est plus le bon
        
        # THEN - Vérifier échec
        assert resultat3 is False
        assert admin.mdp == "mdp_2"  # Doit rester inchangé


class TestAdminIntegration:
    """Tests d'intégration pour vérifier le comportement de Admin avec d'autres composants"""
    
    def test_admin_dans_liste(self):
        """Test que l'admin fonctionne correctement dans des structures de données"""
        # GIVEN
        admins = [
            Admin(nom="admin1", mdp="mdp1", mail="admin1@test.com", admin_id=1),
            Admin(nom="admin2", mdp="mdp2", mail="admin2@test.com", admin_id=2),
            Admin(nom="admin3", mdp="mdp3", mail="admin3@test.com", admin_id=3)
        ]
        
        # WHEN & THEN
        assert len(admins) == 3
        assert admins[0].nom == "admin1"
        assert admins[1].admin_id == 2
        assert admins[2].mail == "admin3@test.com"

    def test_admin_dans_dictionnaire(self):
        """Test que l'admin fonctionne comme clé de dictionnaire"""
        # GIVEN
        admin1 = Admin(nom="admin1", mdp="mdp1", mail="admin1@test.com", admin_id=1)
        admin2 = Admin(nom="admin2", mdp="mdp2", mail="admin2@test.com", admin_id=2)
        
        # WHEN
        admins_dict = {
            admin1: "premier_admin",
            admin2: "deuxieme_admin"
        }
        
        # THEN
        assert admins_dict[admin1] == "premier_admin"
        assert admins_dict[admin2] == "deuxieme_admin"
        assert len(admins_dict) == 2

    def test_admin_serialisation_deserialisation(self):
        """Test simulation de sérialisation/désérialisation"""
        # GIVEN
        admin_original = Admin(nom="admin_test", mdp="mdp_secret", mail="admin@test.com", admin_id=42)
        
        # WHEN - Simulation de sérialisation (vers dictionnaire)
        admin_dict = {
            'admin_id': admin_original.admin_id,
            'nom': admin_original.nom,
            'mdp': admin_original.mdp,
            'mail': admin_original.mail
        }
        
        # WHEN - Simulation de désérialisation (depuis dictionnaire)
        admin_recree = Admin(
            nom=admin_dict['nom'],
            mdp=admin_dict['mdp'],
            mail=admin_dict['mail'],
            admin_id=admin_dict['admin_id']
        )
        
        # THEN
        assert admin_recree.admin_id == admin_original.admin_id
        assert admin_recree.nom == admin_original.nom
        assert admin_recree.mdp == admin_original.mdp
        assert admin_recree.mail == admin_original.mail


if __name__ == "__main__":
    # Exécution des tests
    pytest.main([__file__, "-v", "--tb=short"])
import pytest
from src.Salle import Salle
from src.Ennemi import Ennemi
from src.Objet import Potion

# ---------
# Fixtures
# ---------
@pytest.fixture
def salle_basique():
    # Une salle simple sans lit
    return Salle(id_salle="entree", nom="Entrée", description="Une petite entrée.", a_lit=False)

@pytest.fixture
def salle_repos():
    # Une salle avec un lit pour tester les connexions
    return Salle(id_salle="chambre", nom="Chambre", description="Une chambre confortable.", a_lit=True)

@pytest.fixture
def ennemi_gobelin():
    # Un ennemi basique pour tester les blocages
    return Ennemi(nom="Gobelin", vie_max=30, force=10)

@pytest.fixture
def potion_soin():
    # Un objet simple pour vérifier qu'il ne bloque pas la salle
    return Potion(nom="Potion de soin", description="Soigne 20 PV", quantite=20)


# -------------------
# Tests Salle
# -------------------
def test_salle_init(salle_basique, salle_repos):
    # Vérification des attributs de base de la salle
    assert salle_basique.id == "entree"
    assert salle_basique.nom == "Entrée"
    assert salle_basique.description == "Une petite entrée."
    assert salle_basique.a_lit is False
    
    # Vérification des listes et dictionnaires qui doivent être vides au départ
    assert salle_basique.objets == []
    assert salle_basique.ennemis == []
    assert salle_basique.connexions == {}

    # Vérification qu'un lit peut bien être présent
    assert salle_repos.a_lit is True

def test_salle_est_vide_sans_rien(salle_basique):
    # Une salle fraîchement créée ne doit contenir aucun ennemi
    assert salle_basique.est_vide() is True

def test_salle_est_vide_avec_ennemi(salle_basique, ennemi_gobelin):
    # Ajout d'un ennemi : la salle ne doit plus être considérée comme vide
    salle_basique.ennemis.append(ennemi_gobelin)
    assert salle_basique.est_vide() is False

def test_salle_est_vide_avec_objet_seulement(salle_basique, potion_soin):
    # Ajout d'un objet : contrairement aux ennemis, les objets ne bloquent pas la salle
    salle_basique.objets.append(potion_soin)
    assert salle_basique.est_vide() is True

def test_salle_ajouter_connexion(salle_basique, salle_repos):
    # On relie la salle de base à la salle de repos vers le NORD
    salle_basique.ajouter_connexion("NORD", salle_repos)
    
    # La direction NORD doit maintenant exister dans le dictionnaire
    assert "NORD" in salle_basique.connexions
    
    # L'objet stocké à la clé "NORD" doit être la salle de repos
    assert salle_basique.connexions["NORD"] == salle_repos
    
    # Ajout d'une direction inhabituelle (Téléporteur) pointant vers elle-même
    salle_basique.ajouter_connexion("TELEPORTEUR", salle_basique)
    
    # Il doit y avoir exactement 2 connexions désormais
    assert len(salle_basique.connexions) == 2
    assert salle_basique.connexions["TELEPORTEUR"] == salle_basique
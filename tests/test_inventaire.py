import pytest
from src.Inventaire import PileObjet, Inventaire
from src.Objet import Potion, Bombe

# ---------
# Fixtures
# ---------
@pytest.fixture
def potion():
    # Potion de base qui rendra 20 PV
    return Potion(nom="Potion Soin", description="Soin", quantite=20)

@pytest.fixture
def bombe():
    # Bombe de base qui infligera 30 dégâts
    return Bombe(nom="Bombe Feu", description="Dégâts", degats=30)


# -------------------
# Tests PileObjet
# -------------------
def test_pile_objet_init(potion):
    pile = PileObjet(potion, 2)
    assert pile.objet.nom == "Potion Soin"
    assert pile.quantite == 2

def test_pile_objet_ajouter_retirer(potion):
    pile = PileObjet(potion, 1)
    
    # Ajout classique
    pile.ajouter(3)
    assert pile.quantite == 4
    
    # Retrait classique
    pile.retirer(2)
    assert pile.quantite == 2
    
    # Retrait excessif : ne doit pas passer en négatif
    pile.retirer(5) 
    assert pile.quantite == 0
    assert pile.est_vide() is True


# -------------------
# Tests Inventaire
# -------------------
def test_inventaire_ajouter_nouveau(potion):
    inv = Inventaire()
    inv.ajouter(potion, 2)
    # L'objet doit maintenant être détecté dans l'inventaire
    assert inv.contient(potion) is True
    assert inv.quantite(potion) == 2

def test_inventaire_ajouter_existant(potion):
    inv = Inventaire()
    # Ajout en deux fois pour vérifier que les piles se cumulent
    inv.ajouter(potion, 1)
    inv.ajouter(potion, 3)
    assert inv.quantite(potion) == 4

def test_inventaire_retirer(potion, bombe):
    inv = Inventaire()
    inv.ajouter(potion, 3)
    inv.ajouter(bombe, 1)
    
    # Retrait partiel
    inv.retirer(potion, 1)
    assert inv.quantite(potion) == 2
    
    # Retrait total : l'objet doit disparaître du dictionnaire
    inv.retirer(bombe, 1)
    assert inv.contient(bombe) is False
    assert inv.quantite(bombe) == 0

def test_inventaire_lister(potion, bombe):
    inv = Inventaire()
    inv.ajouter(potion, 2)
    inv.ajouter(bombe, 1)
    
    liste = inv.lister()
    # On vérifie le formatage de la chaîne de caractères
    assert "2x Potion Soin" in liste
    assert "1x Bombe Feu" in liste
    
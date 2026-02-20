import pytest
from src.Inventaire import PileObjet, Inventaire
from src.Objet import Potion, Bombe

@pytest.fixture
def potion():
    return Potion(nom="Potion Soin", description="Soin", quantite=20)

@pytest.fixture
def bombe():
    return Bombe(nom="Bombe Feu", description="Dégâts", degats=30)

# --- Tests PileObjet ---
def test_pile_objet_init(potion):
    pile = PileObjet(potion, 2)
    assert pile.objet.nom == "Potion Soin"
    assert pile.quantite == 2

def test_pile_objet_ajouter_retirer(potion):
    pile = PileObjet(potion, 1)
    pile.ajouter(3)
    assert pile.quantite == 4
    pile.retirer(2)
    assert pile.quantite == 2
    pile.retirer(5) # Ne doit pas descendre sous 0
    assert pile.quantite == 0
    assert pile.est_vide() is True

# --- Tests Inventaire ---
def test_inventaire_ajouter_nouveau(potion):
    inv = Inventaire()
    inv.ajouter(potion, 2)
    assert inv.contient(potion) is True
    assert inv.quantite(potion) == 2

def test_inventaire_ajouter_existant(potion):
    inv = Inventaire()
    inv.ajouter(potion, 1)
    inv.ajouter(potion, 3)
    assert inv.quantite(potion) == 4

def test_inventaire_retirer(potion, bombe):
    inv = Inventaire()
    inv.ajouter(potion, 3)
    inv.ajouter(bombe, 1)
    
    inv.retirer(potion, 1)
    assert inv.quantite(potion) == 2
    
    # Retirer le dernier objet doit le supprimer du dictionnaire
    inv.retirer(bombe, 1)
    assert inv.contient(bombe) is False
    assert inv.quantite(bombe) == 0

def test_inventaire_lister(potion, bombe):
    inv = Inventaire()
    inv.ajouter(potion, 2)
    inv.ajouter(bombe, 1)
    liste = inv.lister()
    assert "2x Potion Soin" in liste
    assert "1x Bombe Feu" in liste
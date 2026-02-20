import pytest
from src.Ennemi import Ennemi
from src.Objet import Arme


# ----------------------
# Tests d'initialisation
# ----------------------
def test_ennemi_initialisation():
    ennemi = Ennemi("Gobelin", vie_max=30, force=5, exp=15)
    
    assert ennemi.nom == "Gobelin"
    assert ennemi.exp == 15
    # La liste des récompenses doit être initialisée à vide par défaut
    assert isinstance(ennemi.recompenses, list)
    assert len(ennemi.recompenses) == 0


# ----------------------
# Tests des Récompenses
# ----------------------
def test_ennemi_ajout_recompense():
    ennemi = Ennemi("Troll", vie_max=50, force=10)
    arme_loot = Arme("Massue", "Lourde", bonus=8)
    
    # On simule l'ajout d'un butin à l'ennemi
    ennemi.recompenses.append(arme_loot)
    
    assert len(ennemi.recompenses) == 1
    assert ennemi.recompenses[0].nom == "Massue"
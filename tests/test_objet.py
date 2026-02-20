import pytest
from src.Objet import Potion, Bombe, Arme, Armure
from src.Personnage import Personnage


# -----------------------
# Tests des Consommables
# -----------------------
def test_potion_soigne_personnage():
    cible = Personnage("Test", vie_max=50, force=5)
    cible.vie = 10 # On le blesse à 10 PV
    potion = Potion("Soin", "Rend 20 PV", quantite=20)
    
    potion.utiliser(cible)
    
    # La cible doit passer de 10 à 30 PV
    assert cible.vie == 30

def test_bombe_inflige_degats():
    cible = Personnage("Test", vie_max=50, force=5)
    bombe = Bombe("Explosif", "Fait 15 dégâts", degats=15)
    
    bombe.utiliser(cible)
    
    # La cible subit 15 dégâts purs : 50 - 15 = 35 PV
    assert cible.vie == 35 


# -----------------------
# Tests des Équipements
# -----------------------
def test_arme_bonus():
    arme = Arme("Épée", "Coupe", bonus=10)
    assert arme.bonus_arme() == 10

def test_armure_bonus():
    armure = Armure("Bouclier", "Protège", bonus=5)
    assert armure.bonus_armure() == 5
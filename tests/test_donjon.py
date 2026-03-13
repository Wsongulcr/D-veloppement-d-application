import pytest
from src.Salle import Salle
from src.Donjon import Donjon
from src.Ennemi import Ennemi

# ---------
# Fixtures
# ---------
@pytest.fixture
def mini_donjon():
    """
    Crée un mini donjon de 2 salles pour les tests.
    """
    entree = Salle("s_1", "Entrée", "Le début.")
    couloir = Salle("s_2", "Couloir", "La suite.")
    
    # On connecte les salles
    entree.ajouter_connexion("NORD", couloir)
    couloir.ajouter_connexion("SUD", entree)
    
    salles_dict = {
        entree.id: entree,
        couloir.id: couloir
    }
    
    donjon = Donjon(nom="Cave", salles=salles_dict, salle_actuelle=entree)
    return donjon, entree, couloir


# ----------------------
# Tests d'initialisation
# ----------------------
def test_donjon_initialisation(mini_donjon):
    donjon, entree, _ = mini_donjon
    
    assert donjon.nom == "Cave"
    assert len(donjon.salles) == 2
    assert donjon.salle_actuelle == entree


# ----------------------
# Tests de Déplacement
# ----------------------
def test_deplacer_heros_succes(mini_donjon):
    donjon, entree, couloir = mini_donjon
    
    # Le déplacement vers le NORD doit réussir
    resultat = donjon.deplacer_heros("NORD")
    
    assert resultat is True
    assert donjon.salle_actuelle == couloir # Le héros a bien changé de salle

def test_deplacer_heros_echec_direction_invalide(mini_donjon):
    donjon, entree, _ = mini_donjon
    
    # Il n'y a pas de porte à l'OUEST
    resultat = donjon.deplacer_heros("OUEST")
    
    assert resultat is False
    assert donjon.salle_actuelle == entree # Le héros est resté dans l'entrée

def test_deplacer_heros_echec_ennemi_bloquant(mini_donjon):
    donjon, entree, _ = mini_donjon
    
    # On place un monstre agressif dans la salle actuelle
    monstre = Ennemi("Orc", vie_max=50, force=5)
    entree.ennemis.append(monstre)
    
    # Le déplacement doit être bloqué même si la porte NORD existe
    resultat = donjon.deplacer_heros("NORD")
    
    assert resultat is False
    assert donjon.salle_actuelle == entree # Le héros n'a pas pu fuir
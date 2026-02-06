import math
from random import uniform
from src.Personnage import Personnage 

class Ennemi(Personnage):
    """
    Classe représentant un ennemi.
    
    Hérite de Personnage et possède une valeur d'expérience donnée au joueur
    en cas de défaite.
    """
    def __init__(self, nom: str, vie_max: int, force: int, arme: int = 0, armure: int = 0, exp: int = 10):
        """
        Initialise un nouvel ennemi.

        Args:
            nom (str): Le nom de l'ennemi.
            vie_max (int): Les points de vie maximums.
            force (int): La force d'attaque de base.
            arme (int, optional): Le bonus de l'arme. Par défaut 0.
            armure (int, optional): La valeur d'armure. Par défaut 0.
            exp (int, optional): L'expérience donnée au vainqueur. Par défaut 10.
        """
        super().__init__(nom, vie_max, force, arme, armure)

        self.exp = exp
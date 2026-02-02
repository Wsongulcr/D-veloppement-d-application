import math
from random import uniform
from src.Personnage import Personnage 

class Ennemi(Personnage):
    def __init__(self, nom: str, vie_max: int, force: int, arme: int = 0, armure: int = 0, exp: int = 10):
        super().__init__(nom, vie_max, force, arme, armure)

        self.exp = exp
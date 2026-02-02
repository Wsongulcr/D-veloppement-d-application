import math
from random import uniform
from src.Personnage import Personnage 

class Hero(Personnage):
    def __init__(self, nom:str, vie_max:int, force:int, arme:int=0, armure:int=0):

        super().__init__(nom, vie_max, force, arme, armure)

        self.niveau = 1
        self.exp = 0

    def exp_pour_prochain_niveau(self):
        return 100 * (self.niveau**2 + self.niveau)
    
    def monter_niveau(self):
        self.niveau += 1

        pourcentage = uniform(1, 10)
        facteur = 1 + (pourcentage / 100)
        self.vie_max = math.ceil(self.vie_max * facteur)

        pourcentage = uniform(1, 10)
        facteur = 1 + (pourcentage / 100)
        self.force = math.ceil(self.force * facteur)

        pourcentage = uniform(1, 10)
        facteur = 1 + (pourcentage / 100)
        self.arme = math.ceil(self.arme * facteur)

        pourcentage = uniform(1, 10)
        facteur = 1 + (pourcentage / 100)
        self.armure = math.ceil(self.armure * facteur)

        self.vie = self.vie_max

    def gagner_exp(self, quantite):

        if quantite<= 0:
            return
        
        self.exp += quantite

        while self.exp >= self.exp_pour_prochain_niveau():
            self.monter_niveau()


    
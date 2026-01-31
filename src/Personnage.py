import random
from random import uniform

class Personnage:
    def __init__(self, nom:str, vie_max:int, force:int, arme:int = 0, armure:int = 0):
        self.nom = nom
        self.vie_max = vie_max
        self.vie = vie_max
        self.force = force
        self.arme = arme
        self.armure = armure
    

    def est_vivant(self):
        return self.vie > 0
    

    def calcul_degats_sur(self, cible: "Personnage"):
        facteur = uniform(1.00, 1.10)
        degats = (self.force + self.arme) - cible.armure
        if degats <= 0:
            return 0
        else:
            return round(degats * facteur)
    
    def subir_degats(self, valeur:int):
        if valeur <= 0:
            return 0
        if self.vie < valeur :
            tmp = self.vie
            self.vie = 0
            return tmp
        else:
            self.vie = self.vie - valeur
        return valeur
    
    def attaquer(self,cible:"Personnage"):
        if self.vie == 0:
            return cible.subir_degats(0)
        else:
            degats = self.calcul_degats_sur(cible)
            print(self.nom + " inflige " + str(degats) + " dégâts à " + cible.nom + " (PV " + str(cible.vie) + "/" + str(cible.vie_max))
            return cible.subir_degats(degats)
        
    





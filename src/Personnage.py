import random

class Personnage:
    def __init__(self, nom:str, vie_max:int, vie:int, force:int, arme:int, armure:int):
        self.nom = nom
        self.vie_max = vie_max
        self.vie = vie
        self.force = force
        self.arme = arme
        self.armure = armure
    

    def est_vivant(self):
        return self.vie > 0
    

    def calcul_degats_sur(self, cible: Personnage):
        facteur = random.uniform(1.00, 1.10)
        degats = (self.force + self.arme - self.armure)
        return degats * facteur
    
    def subir_degats(self, valeur:int):
        return self.vie - valeur
    
    def attaquer(self,cible:Personnage):
        degats = self.calcul_degats_sur(cible)
        return cible.subir_degats(degats)
    
    
        
    



import math
from random import uniform
from src.Personnage import Personnage 

class Hero(Personnage):
    """
    Classe représentant le héros du jeu.
    
    Gère le système de niveaux, l'expérience et l'amélioration des statistiques.
    """
    def __init__(self, nom:str, vie_max:int, force:int, arme:int=0, armure:int=0):
        """
        Initialise le héros au niveau 1 avec 0 expérience.

        Args:
            nom (str): Le nom du héros.
            vie_max (int): Les points de vie maximums.
            force (int): La force d'attaque de base.
            arme (int, optional): Le bonus de l'arme. Par défaut 0.
            armure (int, optional): La valeur d'armure. Par défaut 0.
        """
        super().__init__(nom, vie_max, force, arme, armure)

        self.niveau = 1
        self.exp = 0

    def exp_pour_prochain_niveau(self):
        """
        Calcule l'expérience requise pour atteindre le niveau suivant.
        
        Formule : 100 * (niveau^2 + niveau).

        Returns:
            int: La quantité totale d'XP nécessaire.
        """
        return 100 * (self.niveau**2 + self.niveau)
    
    def monter_niveau(self):
        """
        Fait passer le héros au niveau supérieur.
        
        Augmente le niveau de 1 et améliore les statistiques (vie_max, force,
        arme, armure) d'un pourcentage aléatoire entre 1% et 10%.
        La vie est restaurée au maximum après l'amélioration.
        """
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
        """
        Ajoute de l'expérience au héros.
        
        Gère automatiquement la montée de niveau si l'expérience accumulée
        dépasse le seuil requis (boucle while pour multiples niveaux).

        Args:
            quantite (int): La quantité d'expérience gagnée.
        """
        if quantite<= 0:
            return
        
        self.exp += quantite

        while self.exp >= self.exp_pour_prochain_niveau():
            self.monter_niveau()
            
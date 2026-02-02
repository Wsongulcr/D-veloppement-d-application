import random
from random import uniform

class Personnage:
    """
    Classe de base représentant un personnage dans le système de combat.
    
    Cette classe gère les statistiques vitales, l'équipement défensif et offensif,
    ainsi que les mécanismes de calcul et d'application des dégâts.
    """

    def __init__(self, nom:str, vie_max:int, force:int, arme:int = 0, armure:int = 0):
        """
        Initialise un nouveau personnage avec ses attributs de base.

        Args:
            nom (str): Le nom du personnage.
            vie_max (int): La capacité maximale de points de vie.
            force (int): La puissance d'attaque naturelle du personnage.
            arme (int, optional): Le bonus de dégâts fourni par l'arme équipée. Par défaut 0.
            armure (int, optional): La valeur de réduction des dégâts subis. Par défaut 0.
        """
        self.nom = nom
        self.vie_max = vie_max
        self.vie = vie_max
        self.force = force
        self.arme = arme
        self.armure = armure

    def est_vivant(self):
        """
        Vérifie si le personnage possède encore des points de vie.

        Returns:
            bool: True si la vie est supérieure à 0, False sinon.
        """
        return self.vie > 0

    def calcul_degats_sur(self, cible: "Personnage"):
        """
        Calcule les dégâts potentiels infligés à un adversaire.
        
        La formule utilise la force et l'arme de l'attaquant moins l'armure de la cible,
        multiplié par un facteur aléatoire entre 1.00 et 1.10.

        Args:
            cible (Personnage): L'adversaire qui subit l'attaque.

        Returns:
            int: Le montant de dégâts calculé, arrondi à l'entier le plus proche.
        """
        facteur = uniform(1.00, 1.10)
        degats = (self.force + self.arme) - cible.armure
        if degats <= 0:
            return 0
        else:
            return round(degats * facteur)

    def subir_degats(self, valeur:int):
        """
        Applique une réduction de points de vie au personnage.

        Args:
            valeur (int): Le montant de dégâts à déduire.

        Returns:
            int: La quantité réelle de points de vie perdus (ne peut dépasser la vie actuelle).
        """
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
        """
        Gère le processus complet d'une attaque sur une cible.
        
        Vérifie l'état de l'attaquant, calcule les dégâts, affiche le résultat 
        dans la console et applique les dégâts à la cible.

        Args:
            cible (Personnage): L'adversaire visé par l'attaque.

        Returns:
            int: Le montant final de dégâts infligés à la cible.
        """
        if self.vie <= 0:
            return 0
        else:
            degats = self.calcul_degats_sur(cible)
            return cible.subir_degats(degats)
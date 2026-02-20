import random
from random import uniform
from src.Objet import Arme, Armure

class Personnage:
    """
    Classe de base représentant un personnage dans le système de combat.
    """
    def __init__(self, nom: str, vie_max: int, force: int, arme: Arme = None, armure: Armure = None):
        """
        Initialise un nouveau personnage.

        Args:
            nom (str): Le nom du personnage.
            vie_max (int): La capacité maximale de points de vie.
            force (int): La puissance d'attaque naturelle du personnage.
            arme (Arme, optional): L'objet Arme équipé. Par défaut None.
            armure (Armure, optional): L'objet Armure équipé. Par défaut None.
        """
        self.nom = nom
        self.vie_max = vie_max
        self.vie = vie_max
        self.force = force
        self.arme = arme      
        self.armure = armure  

    def est_vivant(self) -> bool:
        """
        Vérifie si le personnage possède encore des points de vie.

        Returns:
            bool: True si la vie est supérieure à 0, False sinon.
        """
        return self.vie > 0

    def calcul_degats_sur(self, cible: "Personnage") -> int:
        """
        Calcule les dégâts potentiels infligés à un adversaire en prenant en compte les équipements.

        Args:
            cible (Personnage): L'adversaire qui subit l'attaque.

        Returns:
            int: Le montant de dégâts calculé, arrondi à l'entier le plus proche.
        """
        facteur = uniform(1.00, 1.10)
        
        bonus_arme = self.arme.bonus_arme() if self.arme is not None else 0
        bonus_armure = cible.armure.bonus_armure() if cible.armure is not None else 0
        
        degats = (self.force + bonus_arme) - bonus_armure
        
        if degats <= 0:
            return 0
        else:
            return round(degats * facteur)

    def subir_degats(self, valeur: int) -> int:
        """
        Applique une réduction de points de vie au personnage.

        Args:
            valeur (int): Le montant de dégâts à déduire.

        Returns:
            int: La quantité réelle de points de vie perdus.
        """
        if valeur <= 0:
            return 0
        if self.vie < valeur:
            tmp = self.vie
            self.vie = 0
            return tmp
        else:
            self.vie -= valeur
        return valeur

    def attaquer(self, cible: "Personnage") -> int:
        """
        Gère le processus complet d'une attaque sur une cible.

        Args:
            cible (Personnage): L'adversaire visé par l'attaque.

        Returns:
            int: Le montant final de dégâts infligés à la cible.
        """
        if self.vie <= 0:
            return 0
        degats = self.calcul_degats_sur(cible)
        return cible.subir_degats(degats)

    def soigner(self, valeur: int) -> int:
        """
        Restaure des points de vie au personnage sans dépasser la vie maximale.

        Args:
            valeur (int): Le montant de points de vie à restaurer.

        Returns:
            int: La quantité réelle de points de vie restaurés.
        """
        if valeur <= 0 or not self.est_vivant():
            return 0
        soin_effectif = min(valeur, self.vie_max - self.vie)
        self.vie += soin_effectif
        return soin_effectif
import math
from random import uniform
from src.Personnage import Personnage
from src.Inventaire import Inventaire
from src.Objet import Consommable, Arme, Armure

class Hero(Personnage):
    """
    Classe représentant le héros du jeu avec son inventaire et son système de progression.
    """
    def __init__(self, nom: str, vie_max: int, force: int, arme: Arme = None, armure: Armure = None):
        """
        Initialise le héros au niveau 1 avec un inventaire vide.

        Args:
            nom (str): Le nom du héros.
            vie_max (int): Les points de vie maximums.
            force (int): La force d'attaque de base.
            arme (Arme, optional): L'objet Arme équipé. Par défaut None.
            armure (Armure, optional): L'objet Armure équipé. Par défaut None.
        """
        super().__init__(nom, vie_max, force, arme, armure)
        self.niveau = 1
        self.exp = 0
        self.inventaire = Inventaire()

    def exp_pour_prochain_niveau(self) -> int:
        """
        Calcule l'expérience requise pour atteindre le niveau suivant.

        Returns:
            int: La quantité totale d'XP nécessaire.
        """
        return 100 * (self.niveau**2 + self.niveau)
    
    def monter_niveau(self):
        """
        Fait passer le héros au niveau supérieur.
        Augmente les statistiques naturelles (vie_max, force) et restaure la vie.
        """
        self.niveau += 1

        pourcentage = uniform(1, 10)
        facteur = 1 + (pourcentage / 100)
        self.vie_max = math.ceil(self.vie_max * facteur)

        pourcentage = uniform(1, 10)
        facteur = 1 + (pourcentage / 100)
        self.force = math.ceil(self.force * facteur)
        
        self.vie = self.vie_max

    def gagner_exp(self, quantite: int):
        """
        Ajoute de l'expérience au héros et gère les montées de niveau.

        Args:
            quantite (int): La quantité d'expérience gagnée.
        """
        if quantite <= 0:
            return
        self.exp += quantite
        while self.exp >= self.exp_pour_prochain_niveau():
            self.monter_niveau()

    def utiliser_objet(self, objet: Consommable, cible: Personnage) -> None:
        """
        Utilise un objet consommable de l'inventaire sur une cible.

        Args:
            objet (Consommable): L'objet à utiliser.
            cible (Personnage): Le personnage sur lequel appliquer l'effet.
        """
        if self.inventaire.contient(objet):
            objet.utiliser(cible)
            self.inventaire.retirer(objet, 1)

    def ramasser_butin(self, objet: "Objet") -> str:
        """
        Traite un objet ramassé dans une salle ou sur un ennemi.
        Les consommables vont dans l'inventaire.
        Les équipements remplacent les anciens s'ils sont meilleurs.

        Args:
            objet (Objet): L'objet ramassé (Consommable, Arme ou Armure).

        Returns:
            str: Un message textuel décrivant ce qui s'est passé (pour affichage par l'UI).
        """
        # Gestion des consommables (Potions, Bombes...)
        if isinstance(objet, Consommable):
            self.inventaire.ajouter(objet, 1)
            return f"{self.nom} a ramassé : {objet.nom}."
            
        # Gestion des armes
        elif isinstance(objet, Arme):
            # On s'équipe si on n'a rien, ou si le bonus est strictement supérieur
            if self.arme is None or objet.bonus > self.arme.bonus:
                self.arme = objet
                return f"{self.nom} s'équipe de l'arme : {objet.nom}."
            return f"{self.nom} ignore {objet.nom} (son arme actuelle est meilleure)."
                
        # Gestion des armures
        elif isinstance(objet, Armure):
            # On s'équipe si on n'a rien, ou si le bonus est strictement supérieur
            if self.armure is None or objet.bonus > self.armure.bonus:
                self.armure = objet
                return f"{self.nom} s'équipe de l'armure : {objet.nom}."
            return f"{self.nom} ignore {objet.nom} (son armure actuelle est meilleure)."
            
        return ""
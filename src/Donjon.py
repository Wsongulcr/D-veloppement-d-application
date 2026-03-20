from typing import Dict
from src.Salle import Salle

class Donjon:
    """
    Classe gérant le donjon, l'ensemble de ses salles et la navigation du héros.
    """
    def __init__(self, nom: str, salles: Dict[str, Salle], salle_actuelle: Salle):
        self.nom = nom
        self.salles = salles
        self.salle_actuelle = salle_actuelle
        # NOUVEAU : On mémorise la salle d'où l'on vient pour pouvoir fuir
        self.salle_precedente: Salle = None 

    def deplacer_heros(self, direction: str) -> bool:
        # Règle 1 : Le héros ne peut se déplacer que s'il n'y a aucun ennemi
        if not self.salle_actuelle.est_vide():
            print("Impossible d'avancer, des ennemis vous bloquent le passage !")
            return False
            
        # Règle 2 : Vérifier si une salle est connectée dans cette direction
        if direction in self.salle_actuelle.connexions:
            nouvelle_salle = self.salle_actuelle.connexions[direction]
            
            # NOUVEAU : Avant de bouger, on sauvegarde la salle actuelle comme étant la précédente
            self.salle_precedente = self.salle_actuelle 
            self.salle_actuelle = nouvelle_salle
            
            print(f"Vous vous déplacez vers : {direction} ({self.salle_actuelle.nom})")
            return True
        else:
            print(f"Il n'y a pas de passage dans la direction : {direction}.")
            return False

    def fuir(self) -> bool:
        """
        Permet au héros de fuir dans la salle précédente s'il y en a une.
        """
        if self.salle_precedente is None:
            print("Vous ne pouvez pas fuir, vous n'avez nulle part où aller !")
            return False
            
        print(f"Vous fuyez lâchement vers : {self.salle_precedente.nom} !")
        # Le héros retourne dans la salle précédente, et on efface la trace (on ne peut fuir qu'une fois)
        self.salle_actuelle = self.salle_precedente
        self.salle_precedente = None
        return True
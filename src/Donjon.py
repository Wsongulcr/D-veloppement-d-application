from typing import Dict
from src.Salle import Salle

class Donjon:
    def __init__(self, nom: str, salles: Dict[str, Salle], salle_actuelle: Salle):
        self.nom = nom
        self.salles = salles
        self.salle_actuelle = salle_actuelle
        self.salle_precedente: Salle = None 

    def deplacer_heros(self, direction: str) -> bool:
        # Règle 1 : Pas de fuite si ennemi
        if not self.salle_actuelle.est_vide():
            return False
            
        # Règle 2 : Déplacement si la porte existe
        if direction in self.salle_actuelle.connexions:
            nouvelle_salle = self.salle_actuelle.connexions[direction]
            self.salle_precedente = self.salle_actuelle 
            self.salle_actuelle = nouvelle_salle
            return True
            
        return False

    def fuir(self) -> bool:
        if self.salle_precedente is None:
            return False
            
        self.salle_actuelle = self.salle_precedente
        self.salle_precedente = None
        return True
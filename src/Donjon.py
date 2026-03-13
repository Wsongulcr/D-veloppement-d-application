from typing import Dict
from src.Salle import Salle

class Donjon:
    """
    Classe gérant le donjon, l'ensemble de ses salles et la navigation du héros.
    """
    def __init__(self, nom: str, salles: Dict[str, Salle], salle_actuelle: Salle):
        """
        Initialise un nouveau donjon.

        Args:
            nom (str): Le nom du donjon.
            salles (Dict[str, Salle]): Un dictionnaire contenant toutes les salles (clé=id, valeur=Salle).
            salle_actuelle (Salle): La salle où le héros démarre.
        """
        self.nom = nom
        self.salles = salles
        self.salle_actuelle = salle_actuelle

    def deplacer_heros(self, direction: str) -> bool:
        """
        Tente de déplacer le héros dans une direction.
        Le déplacement est annulé si des ennemis sont présents ou si la direction n'existe pas.

        Args:
            direction (str): La direction dans laquelle se déplacer.

        Returns:
            bool: True si le déplacement a réussi, False sinon.
        """
        # Règle 1 : Le héros ne peut se déplacer que s'il n'y a aucun ennemi
        if not self.salle_actuelle.est_vide():
            print("Impossible de fuir, des ennemis vous bloquent le passage !")
            return False
            
        # Règle 2 : Vérifier si une salle est connectée dans cette direction
        if direction in self.salle_actuelle.connexions:
            nouvelle_salle = self.salle_actuelle.connexions[direction]
            self.salle_actuelle = nouvelle_salle
            print(f"Vous vous déplacez vers : {direction} ({self.salle_actuelle.nom})")
            return True
        else:
            print(f"Il n'y a pas de passage dans la direction : {direction}.")
            return False
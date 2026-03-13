from src.Personnage import Personnage
from src.Objet import Objet
from src.Ennemi import Ennemi

class Salle:
    def __init__(self, id_salle: str, nom: str, description: str, a_lit: bool = False):
        self.id = id_salle
        self.nom = nom
        self.description = description
        self.a_lit = a_lit
        
        # On initialise les contenus à vide pour le moment
        self.objets = []
        self.ennemis = []
        self.connexions = {}

    def est_vide(self) -> bool:
        """
        Vérifie si la salle est vide, c'est-à-dire sans ennemis.

        Returns:
            bool: True si la salle est vide, False sinon.
        """
        return len(self.ennemis) == 0
    
    def ajouter_connexion(self, direction: str, salle_destination: "Salle") -> None:
        """Ajoute une connexion vers une autre salle."""
        self.connexions[direction] = salle_destination
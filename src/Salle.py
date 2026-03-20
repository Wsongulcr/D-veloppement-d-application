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


    def utiliser_lit(self, hero: Hero) -> bool:
        """
        Permet au héros de se soigner entièrement s'il y a un lit et aucun ennemi.

        Args:
            hero (Hero): Le héros qui tente de dormir.

        Returns:
            bool: True si le héros s'est reposé, False sinon.
        """
        if self.a_lit and self.est_vide():
            hero.soigner(hero.vie_max)
            return True
        return False

    def recuperer_objets(self, hero: Hero) -> bool:
        """
        Transfère tous les objets de la salle vers le héros s'il n'y a aucun ennemi.

        Args:
            hero (Hero): Le héros qui ramasse les objets.

        Returns:
            bool: True si des objets ont été ramassés, False sinon.
        """
        if self.est_vide() and len(self.objets) > 0:
            for objet in self.objets:
                hero.ramasser_butin(objet)
            self.objets.clear()
            return True
        return False
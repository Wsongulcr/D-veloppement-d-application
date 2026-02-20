from src.Personnage import Personnage 
from src.Objet import Arme, Armure

class Ennemi(Personnage):
    """
    Classe représentant un ennemi lachant des récompenses à sa mort.
    """
    def __init__(self, nom: str, vie_max: int, force: int, arme: Arme = None, armure: Armure = None, exp: int = 10):
        """
        Initialise un nouvel ennemi.

        Args:
            nom (str): Le nom de l'ennemi.
            vie_max (int): Les points de vie maximums.
            force (int): La force d'attaque de base.
            arme (Arme, optional): L'objet Arme équipé. Par défaut None.
            armure (Armure, optional): L'objet Armure équipé. Par défaut None.
            exp (int, optional): L'expérience donnée au vainqueur. Par défaut 10.
        """
        super().__init__(nom, vie_max, force, arme, armure)
        self.exp = exp
        self.recompenses = []
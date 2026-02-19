from src import Personnage
class Objet:
    """Classe de base pour tous les objets du jeu."""
    def __init__(self, nom: str, description: str):
        self.nom = nom
        self.description = description


class Consommable(Objet):
    """Classe pour les objets à usage unique."""
    def utiliser(self, cible: "Personnage") -> None:
        pass

class Equipement(Objet):
    """Classe pour les objets d'équipement."""
    def __init__(self, nom: str, description: str, bonus: int):
        super().__init__(nom, description)
        self.bonus = bonus

class Potion(Consommable):
    """Restaure des points de vie à la cible."""
    def __init__(self, nom: str, description: str, quantite: int):
        super().__init__(nom, description)
        self.quantite = quantite

    def utiliser(self, cible: "Personnage") -> None:
        cible.soigner(self.quantite)

class Bombe(Consommable):
    """Inflige des dégâts à la cible."""
    def __init__(self, nom: str, description: str, degats: int):
        super().__init__(nom, description)
        self.degats = degats

    def utiliser(self, cible: "Personnage") -> None:
        cible.subir_degats(self.degats)

class Arme(Equipement):
    """Confère un bonus offensif."""
    def bonus_arme(self) -> int:
        return self.bonus

class Armure(Equipement):
    """Confère un bonus défensif."""
    def bonus_armure(self) -> int:
        return self.bonus
class Objet:
    """
    Classe de base pour tous les objets du jeu.
    """
    def __init__(self, nom: str, description: str):
        """
        Initialise un nouvel objet.

        Args:
            nom (str): Le nom de l'objet.
            description (str): La description détaillée de l'objet.
        """
        self.nom = nom
        self.description = description


class Consommable(Objet):
    """
    Classe représentant les objets à usage unique.
    """
    def utiliser(self, cible: "Personnage") -> None:
        """
        Applique l'effet du consommable sur une cible.

        Args:
            cible (Personnage): Le personnage sur lequel l'objet est utilisé.
        """
        pass


class Equipement(Objet):
    """
    Classe représentant les objets d'équipement (armes, armures).
    """
    def __init__(self, nom: str, description: str, bonus: int):
        """
        Initialise un nouvel équipement avec son bonus.

        Args:
            nom (str): Le nom de l'équipement.
            description (str): La description de l'équipement.
            bonus (int): La valeur du bonus accordé par l'équipement.
        """
        super().__init__(nom, description)
        self.bonus = bonus


class Potion(Consommable):
    """
    Objet consommable qui restaure des points de vie.
    """
    def __init__(self, nom: str, description: str, quantite: int):
        """
        Initialise une nouvelle potion.

        Args:
            nom (str): Le nom de la potion.
            description (str): La description de la potion.
            quantite (int): Le nombre de points de vie restaurés.
        """
        super().__init__(nom, description)
        self.quantite = quantite

    def utiliser(self, cible: "Personnage") -> None:
        """
        Restaure les points de vie de la cible.

        Args:
            cible (Personnage): Le personnage à soigner.
        """
        cible.soigner(self.quantite)


class Bombe(Consommable):
    """
    Objet consommable qui inflige des dégâts.
    """
    def __init__(self, nom: str, description: str, degats: int):
        """
        Initialise une nouvelle bombe.

        Args:
            nom (str): Le nom de la bombe.
            description (str): La description de la bombe.
            degats (int): Le nombre de dégâts infligés.
        """
        super().__init__(nom, description)
        self.degats = degats

    def utiliser(self, cible: "Personnage") -> None:
        """
        Inflige des dégâts à la cible.

        Args:
            cible (Personnage): Le personnage qui subit l'explosion.
        """
        cible.subir_degats(self.degats)


class Arme(Equipement):
    """
    Équipement conférant un bonus offensif.
    """
    def bonus_arme(self) -> int:
        """
        Renvoie la valeur du bonus d'attaque.

        Returns:
            int: Le bonus de l'arme.
        """
        return self.bonus


class Armure(Equipement):
    """
    Équipement conférant un bonus défensif.
    """
    def bonus_armure(self) -> int:
        """
        Renvoie la valeur du bonus de défense.

        Returns:
            int: Le bonus de l'armure.
        """
        return self.bonus
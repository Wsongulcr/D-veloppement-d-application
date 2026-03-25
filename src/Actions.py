from src.Hero import Hero
from src.Donjon import Donjon

class Action:
    """
    Classe de base pour toutes les actions.

    """
    def __init__(self, nom: str):
        self.nom = nom

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        """Indique si l'action est réalisable dans l'état actuel."""
        return False

    def executer(self, donjon: Donjon, heros: Hero, *args) -> str:
        """
        Exécute la logique de l'action et retourne un message à afficher par l'UI.
        """
        return ""


class ActionObserver(Action):
    def __init__(self):
        super().__init__("Observer")

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        # Possible uniquement si la salle ne contient pas d'ennemi
        return donjon.salle_actuelle.est_vide()

    def executer(self, donjon: Donjon, heros: Hero, *args) -> str:
        salle = donjon.salle_actuelle
        message = f"--- {salle.nom} ---\n{salle.description}\n"
        if salle.objets:
            noms_objets = [obj.nom for obj in salle.objets]
            message += f"Objets au sol : {', '.join(noms_objets)}"
        else:
            message += "Il n'y a rien de spécial au sol."
        return message


class ActionSeDeplacer(Action):
    def __init__(self):
        super().__init__("Se déplacer")

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        # Possible uniquement si la salle ne contient aucun ennemi
        return donjon.salle_actuelle.est_vide()

    def executer(self, donjon: Donjon, heros: Hero, direction: str = "") -> str:

        if donjon.deplacer_heros(direction):
            return f"Vous vous êtes déplacé vers : {direction}."
        return f"Impossible d'aller vers {direction}."


class ActionRamasser(Action):
    def __init__(self):
        super().__init__("Ramasser")

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        # Possible si pas d'ennemi ET s'il y a des objets
        salle = donjon.salle_actuelle
        return salle.est_vide() and len(salle.objets) > 0

    def executer(self, donjon: Donjon, heros: Hero, *args) -> str:

        if donjon.salle_actuelle.recuperer_objets(heros):
            return "Vous avez ramassé tous les objets de la salle."
        return "Il n'y a rien à ramasser."


class ActionSeReposer(Action):
    def __init__(self):
        super().__init__("Se reposer")

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        # Possible si pas d'ennemi ET si la salle possède un lit
        return donjon.salle_actuelle.est_vide() and donjon.salle_actuelle.a_lit

    def executer(self, donjon: Donjon, heros: Hero, *args) -> str:
        if donjon.salle_actuelle.utiliser_lit(heros):
            return "Vous vous reposez. Vos points de vie sont restaurés au maximum !"
        return "Vous ne pouvez pas vous reposer ici."


class ActionFuir(Action):
    def __init__(self):
        super().__init__("Fuir")

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        # Possible s'il y a un ennemi ET qu'on vient d'une salle précédente
        return not donjon.salle_actuelle.est_vide() and donjon.salle_precedente is not None

    def executer(self, donjon: Donjon, heros: Hero, *args) -> str:
        if donjon.fuir():
            return "Vous fuyez lâchement vers la salle précédente !"
        return "La fuite a échoué."


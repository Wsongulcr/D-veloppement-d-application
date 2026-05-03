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

class ActionAttaquer(Action):
    def __init__(self):
        super().__init__("Attaquer")

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        # Possible uniquement si la salle contient au moins un ennemi[cite: 19]
        return not donjon.salle_actuelle.est_vide()

    def executer(self, donjon: Donjon, heros: Hero, *args) -> str:
        salle = donjon.salle_actuelle
        # On cible le premier ennemi vivant de la salle
        cible = next((e for e in salle.ennemis if e.est_vivant()), None)
        
        if cible:
            degats = heros.attaquer(cible)
            message = f"Vous attaquez {cible.nom} et lui infligez {degats} dégâts ! (PV restants: {cible.vie}/{cible.vie_max})\n"
            
            # Si l'attaque tue l'ennemi
            if not cible.est_vivant():
                message += f"Bravo, vous avez vaincu {cible.nom} !\n"
                heros.gagner_exp(cible.exp)
                message += f"Vous gagnez {cible.exp} points d'expérience.\n"
                
                # Ramassage des récompenses de l'ennemi
                for butin in cible.recompenses:
                    msg_loot = heros.ramasser_butin(butin)
                    message += f"{msg_loot}\n"
                    
            return message.strip()
        return "Il n'y a personne à attaquer."
    

class ActionUtiliser(Action):
    def __init__(self):
        super().__init__("Utiliser")

    def est_possible(self, donjon: Donjon, heros: Hero) -> bool:
        # Possible si le héros possède au moins un objet dans son inventaire[cite: 19]
        return len(heros.inventaire._objets) > 0

    def executer(self, donjon: Donjon, heros: Hero, nom_objet: str = "") -> str:
        if not nom_objet:
            return "Vous devez préciser quel objet utiliser."

        # Vérifier si l'objet est dans l'inventaire
        if nom_objet in heros.inventaire._objets:
            pile = heros.inventaire._objets[nom_objet]
            objet = pile.objet
            
            # Déterminer la cible (le héros par défaut)
            salle = donjon.salle_actuelle
            cible = heros
            
            # Si c'est une bombe, la cible devient le monstre
            if "Bombe" in objet.__class__.__name__ or "Bombe" in objet.nom:
                ennemi = next((e for e in salle.ennemis if e.est_vivant()), None)
                if ennemi:
                    cible = ennemi
                else:
                    return "Il n'y a pas d'ennemi sur qui lancer cela !"

            heros.utiliser_objet(objet, cible)
            return f"Vous avez utilisé {objet.nom} sur {cible.nom}."
            
        return "Objet introuvable dans l'inventaire."
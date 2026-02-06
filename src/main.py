from random import seed
from src import Personnage
from src.Hero import Hero
from src.Ennemi import Ennemi

def combat_tour_par_tour(joueur: Hero, ennemi: Ennemi, log: bool = True) -> Personnage:
    """
    Simule un combat tour par tour entre le joueur et un ennemi.
    
    Le joueur attaque toujours en premier. Le combat s'arrête quand l'un
    des deux combattants n'a plus de vie.

    Args:
        joueur (Hero): Le héros contrôlé par le joueur.
        ennemi (Ennemi): L'adversaire à combattre.
        log (bool, optional): Si True, affiche le déroulement dans la console. Par défaut True.

    Returns:
        Personnage: L'objet représentant le vainqueur (joueur ou ennemi).
    """
    tour = 1
    
    while joueur.est_vivant() and ennemi.est_vivant():
        if log:
            print(f"--- Tour {tour} ---")
        
        degats_infliges = joueur.attaquer(ennemi) 
        
        if log:
            print(f"{joueur.nom} inflige {degats_infliges} dégâts à {ennemi.nom} (PV {ennemi.vie}/{ennemi.vie_max})")
        
        if not ennemi.est_vivant():
            if log:
                print(f"{ennemi.nom} est vaincu !")
                print(f"{joueur.nom} gagne {ennemi.exp} XP.")
            joueur.gagner_exp(ennemi.exp)
            return joueur
            
        degats_subis = ennemi.attaquer(joueur)
        
        if log:
            print(f"{ennemi.nom} inflige {degats_subis} dégâts à {joueur.nom} (PV {joueur.vie}/{joueur.vie_max})")
        
        if not joueur.est_vivant():
            if log:
                print(f"{joueur.nom} est vaincu")
            return ennemi
            
        tour += 1
        
    return joueur if joueur.est_vivant() else ennemi
    
if __name__ == "__main__":
    seed(44) # Pour des résultats reproductibles malgré l'aléatoire 
    hero = Hero(nom="Gustave", vie_max=300, force=60, arme=20, armure=10) 
    ennemi = Ennemi(nom="Dualliste", vie_max=200, force=40, arme=10, armure=0, exp=250) 
    vainqueur = combat_tour_par_tour(hero, ennemi, log=True) 
    print("Vainqueur :", vainqueur.nom) 
    print(f"{hero.nom}- Niveau {hero.niveau}, XP {hero.exp}/{hero.exp_pour_prochain_niveau()}")
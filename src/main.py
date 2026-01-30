from random import seed

def combat_tour_par_tour(joueur: Hero, ennemi: Ennemi, log: bool = True)-> Personnage:
    """Exécute un combat. Renvoie le vainqueur (joueur ou ennemi). 
    
    **Paramètres**
    - `joueur : Hero` : Personnage joueur.
    - `ennemi : Ennemi` : Personnage ennemi.
    - `log : bool` : Si `log == True`, affiche des messages pendant le combat, sinon aucun message. 
    """ 
    # CODE À COMPLÉTER 
    
if __name__ == "__main__":
    seed(44) # Pour des résultats reproductibles malgré l'aléatoire 
    hero = Hero(nom="Gustave", vie_max=300, force=60, arme=20, armure=10) 
    ennemi = Ennemi(nom="Dualliste", vie_max=200, force=40, arme=10, armure=0, exp=250) 
    vainqueur = combat_tour_par_tour(hero, ennemi, log=True) 
    print("Vainqueur :", vainqueur.nom) 
    print(f"{hero.nom}- Niveau {hero.niveau}, XP {hero.exp}/{hero.exp_pour_prochain_niveau()}")
from src.Hero import Hero
from src.chargement import charger_donjon
from src.Actions import (
    ActionObserver, ActionSeDeplacer, ActionAttaquer, 
    ActionRamasser, ActionSeReposer, ActionFuir, ActionUtiliser
)

def afficher_interface(heros: Hero, nom_salle: str):
    """Affiche l'en-tête de l'interface avec les stats du joueur."""
    print(f"\n{'='*40}")
    print(f"📍 Lieu : {nom_salle}")
    print(f"👤 {heros.nom} | Niveau {heros.niveau} | PV : {heros.vie}/{heros.vie_max} | XP : {heros.exp}/{heros.exp_pour_prochain_niveau()}")
    
    # On vérifie si l'inventaire a des objets en regardant la taille de sa liste
    if len(heros.inventaire.lister()) > 0:
        print(f"🎒 Inventaire : {', '.join(heros.inventaire.lister())}")
    print(f"{'='*40}")

def main():
    print("========================================")
    print("  LUMEN-UMBRA : AVENTURE 44 - PROTOTYPE ")
    print("========================================\n")

    # 1. Initialisation du Modèle (Création du héros et du donjon)
    heros = Hero(nom="Gustave", vie_max=100, force=20)
    
    try:
        donjon = charger_donjon("donjon.json")
    except FileNotFoundError:
        print("Erreur : Le fichier 'donjon.json' est introuvable.")
        return

    # 2. Initialisation des Actions (Les "télécommandes" du jeu)
    toutes_les_actions = [
        ActionObserver(),
        ActionSeDeplacer(),
        ActionAttaquer(),
        ActionRamasser(),
        ActionSeReposer(),
        ActionFuir(),
        ActionUtiliser()
    ]

    # 3. La Boucle de Jeu Principale
    while heros.est_vivant():
        salle_actuelle = donjon.salle_actuelle
        afficher_interface(heros, salle_actuelle.nom)

        # --- A. TOUR DU JOUEUR ---
        # On filtre la liste pour ne garder que les actions autorisées
        actions_possibles = [act for act in toutes_les_actions if act.est_possible(donjon, heros)]

        print("\nQue voulez-vous faire ?")
        for i, action in enumerate(actions_possibles):
            print(f"{i + 1}. {action.nom}")

        choix = input("\nVotre choix (numéro) : ")

        try:
            index_choix = int(choix) - 1
            if 0 <= index_choix < len(actions_possibles):
                action_choisie = actions_possibles[index_choix]

                print("\n" + "-"*40)
                # Cas particuliers où l'interface doit demander des détails
                if action_choisie.nom == "Se déplacer":
                    print(f"Directions possibles : {', '.join(salle_actuelle.connexions.keys())}")
                    direction = input("Dans quelle direction aller ? ").upper()
                    resultat = action_choisie.executer(donjon, heros, direction)
                    print(resultat)

                elif action_choisie.nom == "Utiliser":
                    nom_objet = input("Tapez le nom exact de l'objet à utiliser : ")
                    resultat = action_choisie.executer(donjon, heros, nom_objet)
                    print(resultat)

                # Cas standard
                else:
                    resultat = action_choisie.executer(donjon, heros)
                    print(resultat)
                print("-"*40)

            else:
                print("\n❌ Choix invalide, veuillez entrer un numéro de la liste.")
                continue # On recommence la boucle sans faire jouer les ennemis
        except ValueError:
            print("\n❌ Veuillez entrer un chiffre valide.")
            continue # On recommence la boucle

        # --- B. TOUR DES ENNEMIS ---
        # Les ennemis attaquent s'ils sont dans la salle et vivants
        if not salle_actuelle.est_vide():
            print("\n⚔️ --- Tour des ennemis ---")
            for ennemi in salle_actuelle.ennemis:
                if ennemi.est_vivant():
                    degats_subis = ennemi.attaquer(heros)
                    print(f"⚠️ {ennemi.nom} vous attaque et inflige {degats_subis} dégâts !")
                    
                    if not heros.est_vivant():
                        break # Le héros est mort, on arrête les attaques

    # 4. Fin de partie
    print("\n💀" + "="*36 + "💀")
    print("    VOUS AVEZ SUCCOMBÉ AUX TÉNÈBRES...")
    print("💀" + "="*36 + "💀")

if __name__ == "__main__":
    main()
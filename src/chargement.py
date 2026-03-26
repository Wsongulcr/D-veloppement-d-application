import json
from src.Salle import Salle
from src.Donjon import Donjon
from src.Ennemi import Ennemi
from src.Objet import Potion, Bombe, Arme, Armure

def creer_objet_depuis_dict(data: dict):
    """
    Fonction utilitaire pour recréer un objet Python à partir de son dictionnaire JSON.
    """
    if not data:
        return None
        
    type_obj = data.get("type")
    
    # On regarde si le JSON contient "type" pour créer le bon objet
    if type_obj == "Potion":
        return Potion(nom=data["nom"], description=data["description"], quantite=data["quantite"])
    elif type_obj == "Bombe":
        return Bombe(nom=data["nom"], description=data["description"], degats=data["degats"])
    elif type_obj == "Arme":
        return Arme(nom=data["nom"], description=data["description"], bonus=data["bonus"])
    elif type_obj == "Armure":
        return Armure(nom=data["nom"], description=data["description"], bonus=data["bonus"])
        
    # Cas spécial pour les armes/armures des ennemis qui n'ont parfois pas la clé "type" dans ton JSON
    elif "bonus" in data:
        # On devine que c'est une Arme si ça a un bonus et pas de type (simplification)
        # Mais dans l'idéal, ton JSON devrait toujours avoir la clé "type" !
        if "Armure" in data.get("nom", "") or "Cuir" in data.get("nom", ""):
             return Armure(nom=data["nom"], description=data["description"], bonus=data["bonus"])
        return Arme(nom=data["nom"], description=data["description"], bonus=data["bonus"])
        
    return None



def charger_donjon(chemin_fichier: str) -> Donjon:
    """
    Charge le donjon depuis un fichier JSON[cite: 87, 88].
    """
    # Ouverture et lecture du fichier JSON [cite: 89, 90]
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)

    salles_dict = {}

    # ==========================================
    # PASSAGE 1 : Création des salles isolées
    # ==========================================
    for id_salle, data_salle in data["salles"].items():
        # Création de la salle basique
        salle = Salle(
            id_salle=id_salle,
            nom=data_salle["nom"],
            description=data_salle["description"],
            a_lit=data_salle.get("a_lit", False)
        )

        # Ajout des objets sur le sol de la salle
        for obj_data in data_salle.get("objets", []):
            obj = creer_objet_depuis_dict(obj_data)
            if obj:
                salle.objets.append(obj)

        # Ajout des ennemis dans la salle
        for ennemi_data in data_salle.get("ennemis", []):
            arme_ennemi = creer_objet_depuis_dict(ennemi_data.get("arme"))
            armure_ennemi = creer_objet_depuis_dict(ennemi_data.get("armure"))

            ennemi = Ennemi(
                nom=ennemi_data["nom"],
                vie_max=ennemi_data["vie_max"],
                force=ennemi_data["force"],
                arme=arme_ennemi,
                armure=armure_ennemi,
                exp=ennemi_data.get("exp", 10)
            )

            # Ajout du butin (récompenses) que l'ennemi va lâcher
            for rec_data in ennemi_data.get("recompenses", []):
                recompense = creer_objet_depuis_dict(rec_data)
                if recompense:
                    ennemi.recompenses.append(recompense)

            salle.ennemis.append(ennemi)

        # On stocke la salle terminée dans notre dictionnaire
        salles_dict[id_salle] = salle

    # ==========================================
    # PASSAGE 2 : Création des portes (connexions)
    # ==========================================
    for id_salle, data_salle in data["salles"].items():
        salle = salles_dict[id_salle]
        connexions = data_salle.get("connexions", {})
        
        for direction, id_dest in connexions.items():
            if id_dest in salles_dict:
                salle.ajouter_connexion(direction, salles_dict[id_dest])

    # ==========================================
    # PASSAGE 3 : Finalisation du Donjon
    # ==========================================
    id_depart = data.get("salle_depart")
    salle_depart = salles_dict.get(id_depart)

    return Donjon(nom="Lumen-Umbra", salles=salles_dict, salle_actuelle=salle_depart)
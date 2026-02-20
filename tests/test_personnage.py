import math
import pytest

from src.Personnage import Personnage
from src.Objet import Arme, Armure


# ---------
# Fixtures
# ---------
@pytest.fixture
def hero():
    # force + arme = 7 ; armure = 1 ; vie_max = 30
    arme_hero = Arme(nom="Épée basique", description="", bonus=1)
    armure_hero = Armure(nom="Armure basique", description="", bonus=1)
    return Personnage(nom="Héros", vie_max=30, force=6, arme=arme_hero, armure=armure_hero)

@pytest.fixture
def mob():
    # force + arme = 5 ; armure = 2 ; vie_max = 20
    arme_mob = Arme(nom="Dague", description="", bonus=1)
    armure_mob = Armure(nom="Cuir épais", description="", bonus=2)
    return Personnage(nom="Mob", vie_max=20, force=4, arme=arme_mob, armure=armure_mob)


# ----------------------
# Tests d'initialisation
# ----------------------
def test_init_sets_vie_to_vie_max():
    p = Personnage("Test", 25, 5) # arme et armure valent None par défaut
    assert p.vie_max == 25
    assert p.vie == 25
    assert p.est_vivant() is True



# -------------------
# Tests subir_degats
# -------------------
def test_subir_degats_reduit_vie_et_retourne_perte():
    p = Personnage("Test", 10, 3)
    perdu = p.subir_degats(4)
    assert perdu == 4
    assert p.vie == 6

def test_subir_degats_ne_passe_jamais_sous_zero():
    p = Personnage("Test", 5, 3)
    _ = p.subir_degats(3)
    perdu = p.subir_degats(10)   # dépassement
    assert perdu == 2            # 2 restants -> tombe à 0
    assert p.vie == 0
    assert p.est_vivant() is False

def test_subir_degats_zero_ou_negatifs_aucun_effet():
    p = Personnage("Test", 8, 2)
    assert p.subir_degats(0) == 0
    assert p.subir_degats(-3) == 0
    assert p.vie == 8

def test_subir_degats_sur_personnage_deja_mort_aucun_effet():
    p = Personnage("Test", 5, 1)
    p.subir_degats(5)
    assert p.est_vivant() is False
    assert p.subir_degats(3) == 0
    assert p.vie == 0


# -----------------------
# Tests calcul_degats_sur
# -----------------------
def test_calcul_degats_sur_base_negative_donne_zero(monkeypatch, hero, mob):
    # Rendre la base <= 0 : armure cible > force+arme attaquant
    grosse_armure = Armure("Blindage", "", bonus=999)
    cible = Personnage("Tank", vie_max=50, force=1, arme=None, armure=grosse_armure)
    # Fixer l'aléatoire au max pour vérifier que ça reste 0
    monkeypatch.setattr("src.Personnage.uniform", lambda a,b: 1.9999999)
    assert hero.calcul_degats_sur(cible) == 0

def test_calcul_degats_sur_mult_1_00(monkeypatch):
    # base = (6+2) - 1 = 7
    arme_a = Arme("Hache", "", bonus=2)
    armure_b = Armure("Bouclier", "", bonus=1)
    a = Personnage("A", 10, force=6, arme=arme_a, armure=None)
    b = Personnage("B", 10, force=1, arme=None, armure=armure_b)
    monkeypatch.setattr("src.Personnage.uniform", lambda a,b: 1.0)
    assert a.calcul_degats_sur(b) == 7

def test_calcul_degats_sur_mult_proche_1_10(monkeypatch):
    # base = 10 ; mult ~ 1.0999999 = 11
    a = Personnage("A", 10, force=10, arme=None, armure=None)
    b = Personnage("B", 10, force=0, arme=None, armure=None)
    monkeypatch.setattr("src.Personnage.uniform", lambda a,b: 1.0999999)
    assert a.calcul_degats_sur(b) == 11

@pytest.mark.parametrize(
    "force,bonus_arme,bonus_armure_cible",
    [
        (5, 0, 0),
        (7, 1, 2),
        (3, 4, 1),
    ],
)
def test_calcul_degats_sur_dans_bornes(force, bonus_arme, bonus_armure_cible, monkeypatch):
    # Création des objets uniquement s'il y a un bonus
    arme_obj = Arme("Arme test", "", bonus=bonus_arme) if bonus_arme > 0 else None
    armure_obj = Armure("Armure test", "", bonus=bonus_armure_cible) if bonus_armure_cible > 0 else None
    
    attaquant = Personnage("A", 10, force=force, arme=arme_obj, armure=None)
    cible = Personnage("C", 10, force=0, arme=None, armure=armure_obj)
    base = max(0, (force + bonus_arme) - bonus_armure_cible)

    # Tester plusieurs valeurs pseudo-aléatoires
    for r in (1.0, 1.012, 1.05,1.087321):  # toutes dans [1.0,1.1)
        monkeypatch.setattr("src.Personnage.uniform", lambda a,b: r)
        dmg = attaquant.calcul_degats_sur(cible)
        assert dmg >= 0
        assert base <= dmg <= math.ceil(base * 1.1)


# -------------
# Tests attaquer
# -------------
def test_attaquer_applique_degats_et_retourne_valeur(monkeypatch, hero, mob):
    # Fixer mult = 1.0 pour rendre déterministe
    monkeypatch.setattr("src.Personnage.uniform", lambda a,b: 1.0)
    # base = (6+1) - 2 = 5 ; ceil(5 * 1.0) = 5
    inflige = hero.attaquer(mob)
    assert inflige == 5
    assert mob.vie == mob.vie_max - 5

def test_attaquer_sur_cible_morte_retourne_zero(monkeypatch, hero, mob):
    mob.subir_degats(mob.vie_max)  # tuer la cible
    assert mob.est_vivant() is False
    monkeypatch.setattr("src.Personnage.uniform", lambda a,b: 1.0)
    avant = mob.vie
    inflige = hero.attaquer(mob)
    assert inflige == 0
    assert mob.vie == avant  # pas d'effet

def test_attaquer_par_mort_retourne_zero(monkeypatch, hero, mob):
    hero.subir_degats(hero.vie_max)  # tuer l'attaquant
    assert hero.est_vivant() is False
    monkeypatch.setattr("src.Personnage.uniform", lambda a,b: 1.0)
    avant = mob.vie
    inflige = hero.attaquer(mob)
    assert inflige == 0
    assert mob.vie == avant  # pas d'effet


# --------------------------------------
# Tests de "non-régression" sur les bornes
# --------------------------------------
def test_degats_ne_peuvent_pas_etre_negatifs(monkeypatch):
    # armure de la cible supérieure à l'offense -> base <= 0
    grosse_armure = Armure("Mur", "", bonus=999)
    a = Personnage("A", 10, force=1, arme=None, armure=None)
    c = Personnage("C", 10, force=0, arme=None, armure=grosse_armure)
    # même avec boost quelconque, résultat attendu = 0
    for r in (1.0, 1.42, 1.9999):
        monkeypatch.setattr("src.Personnage.uniform", lambda a,b: r)
        assert a.calcul_degats_sur(c) == 0


# --------------------------
# Petit test d'intégration
# --------------------------
def test_mini_combat_deterministe(monkeypatch):
    """
    On force l'aléa à 1.0 pour simuler un mini "combat" de 2 tours :
    - A attaque B (base 4) -> 4 dégâts
    - B réplique (base 2)   -> 2 dégâts
    - A attaque B à nouveau -> 4 dégâts
    On vérifie seulement les effets cumulatifs.
    """
    monkeypatch.setattr("src.Personnage.uniform", lambda a,b: 1.0)

    arme_a = Arme("Arme A", "", bonus=1)
    armure_b = Armure("Armure B", "", bonus=1)

    A = Personnage("A", vie_max=12, force=3, arme=arme_a, armure=None)  # base vs B = (3+1)-1 = 3 (car armure B=1)
    B = Personnage("B", vie_max=10, force=2, arme=None, armure=armure_b)  # base vs A = (2+0)-0 = 2 (car armure A=0)

    # Tour 1 : A -> B
    assert A.attaquer(B) == 3
    assert B.vie == 7

    # Tour 1 : B -> A
    assert B.attaquer(A) == 2
    assert A.vie == 10

    # Tour 2 : A -> B
    assert A.attaquer(B) == 3
    assert B.vie == 4  # encore vivant

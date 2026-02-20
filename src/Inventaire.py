from src.Objet import Objet

class PileObjet:
    """
    Gère une quantité d'un même objet.
    """
    def __init__(self, objet: Objet, quantite: int = 1):
        """
        Initialise une pile avec un objet et une quantité de départ.

        Args:
            objet (Objet): L'objet contenu dans la pile.
            quantite (int, optional): La quantité initiale. Par défaut 1.
        """
        self.objet = objet
        self.quantite = quantite

    def ajouter(self, qte: int) -> None:
        """
        Ajoute une quantité d'objets à la pile.

        Args:
            qte (int): La quantité à ajouter.
        """
        if qte > 0:
            self.quantite += qte

    def retirer(self, qte: int) -> None:
        """
        Retire une quantité d'objets de la pile.

        Args:
            qte (int): La quantité à retirer.
        """
        if qte > 0:
            self.quantite -= qte
            if self.quantite < 0:
                self.quantite = 0

    def est_vide(self) -> bool:
        """
        Vérifie si la pile est vide.

        Returns:
            bool: True si la quantité est inférieure ou égale à 0, False sinon.
        """
        return self.quantite <= 0


class Inventaire:
    """
    Inventaire permettant de stocker et gérer les objets possédés.
    """
    def __init__(self):
        """
        Initialise un inventaire vide.
        """
        self._objets = {} 

    def ajouter(self, o: Objet, qte: int = 1) -> None:
        """
        Ajoute un objet à l'inventaire en gérant les piles.

        Args:
            o (Objet): L'objet à ajouter.
            qte (int, optional): La quantité à ajouter. Par défaut 1.
        """
        if qte <= 0:
            return
        if o.nom in self._objets:
            self._objets[o.nom].ajouter(qte)
        else:
            self._objets[o.nom] = PileObjet(o, qte)

    def retirer(self, o: Objet, qte: int = 1) -> None:
        """
        Retire une quantité d'un objet de l'inventaire.

        Args:
            o (Objet): L'objet à retirer.
            qte (int, optional): La quantité à retirer. Par défaut 1.
        """
        if qte <= 0:
            return
        if o.nom in self._objets:
            self._objets[o.nom].retirer(qte)
            if self._objets[o.nom].est_vide():
                del self._objets[o.nom]

    def contient(self, o: Objet) -> bool:
        """
        Vérifie si l'inventaire contient au moins un exemplaire de l'objet.

        Args:
            o (Objet): L'objet à vérifier.

        Returns:
            bool: True si l'objet est présent, False sinon.
        """
        return o.nom in self._objets and not self._objets[o.nom].est_vide()

    def quantite(self, o: Objet) -> int:
        """
        Renvoie la quantité possédée d'un objet spécifique.

        Args:
            o (Objet): L'objet dont on veut connaître la quantité.

        Returns:
            int: La quantité de l'objet dans l'inventaire.
        """
        if o.nom in self._objets:
            return self._objets[o.nom].quantite
        return 0

    def lister(self) -> list[str]:
        """
        Renvoie une liste formatée du contenu de l'inventaire.

        Returns:
            list[str]: Une liste de chaînes de caractères décrivant les objets et leurs quantités.
        """
        return [f"{pile.quantite}x {nom}" for nom, pile in self._objets.items()]
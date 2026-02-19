from src.Objet import Objet

class PileObjet:
    """Gère une quantité d'un même objet."""
    def __init__(self, objet: Objet, quantite: int = 1):
        self.objet = objet
        self.quantite = quantite

    def ajouter(self, qte: int) -> None:
        if qte > 0:
            self.quantite += qte

    def retirer(self, qte: int) -> None:
        if qte > 0:
            self.quantite -= qte
            if self.quantite < 0:
                self.quantite = 0

    def est_vide(self) -> bool:
        return self.quantite <= 0

class Inventaire:
    """Inventaire permettant de stocker et gérer les objets possédés."""
    def __init__(self):
        
        self._objets = {} # On y stock les piles d'objets

    def ajouter(self, o: Objet, qte: int = 1) -> None:
        if qte <= 0: 
            return
        if o.nom in self._objets:
            self._objets[o.nom].ajouter(qte)
        else:
            self._objets[o.nom] = PileObjet(o, qte)

    def retirer(self, o: Objet, qte: int = 1) -> None:
        if qte <= 0: 
            return
        if o.nom in self._objets:
            self._objets[o.nom].retirer(qte)
            if self._objets[o.nom].est_vide():
                del self._objets[o.nom]

    def contient(self, o: Objet) -> bool:
        return o.nom in self._objets and not self._objets[o.nom].est_vide()

    def quantite(self, o: Objet) -> int:
        if o.nom in self._objets:
            return self._objets[o.nom].quantite
        return 0

    def lister(self) -> list[str]:
        return [f"{pile.quantite}x {nom}" for nom, pile in self._objets.items()]
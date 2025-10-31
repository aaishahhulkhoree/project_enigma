from typing import Dict, Iterable, Optional, Tuple
from utils.nettoyage import assertionError
from utils.nettoyage import est_majuscule, est_liste_paires_valides

MAX_PAIRES = 10
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Plugboard:
    """Classe Plugboard pour gérer les connexions du plugboard."""
    def __init__(self, paires: Iterable[str] | None = None) -> None:
        self.plugboard : Dict[str, str] = {}
        if paires:
            self.configurer(paires)


    def configurer(self, paires: Iterable[str]) -> None:
        """List(str) paires: Liste de paires de lettres à connecter."""
        paires = list(paires)
        if len(paires) > MAX_PAIRES:
            assertionError(f"Le plugboard ne peut pas avoir plus de {MAX_PAIRES} paires de connexions.")

        est_liste_paires_valides(paires)
        
        lettres_utilisees = set()

        for paire in paires:
            a, b = paire[0].upper(), paire[1].upper()
            if a in lettres_utilisees or b in lettres_utilisees:
                assertionError(f"Les lettres '{a}' et/ou '{b}' sont déjà utilisées.")
            if not (est_majuscule(a) and est_majuscule(b)):
                assertionError("Seules les lettres A–Z sont autorisées.")
            if a == b:
                assertionError("Une paire ne peut pas relier une lettre à elle-même.")
            lettres_utilisees.update({a, b})
            self.plugboard[a] = b
            self.plugboard[b] = a

    
    def est_connectee(self, lettre: str) -> bool:
        """True si la lettre (A–Z) est connectée dans le plugboard, sinon False."""
        if not lettre or len(lettre) != 1:
            assertionError("est_majuscule attend un caractère unique.")
        L = lettre.upper()
        if not est_majuscule(L):
            assertionError("est_majuscule s'applique uniquement aux lettres A–Z.")
        return L in self.plugboard

    def permuter(self, lettre: str) -> str:
        """Permute une lettre via le plugboard si connectée, sinon retourne la lettre inchangée.
        Non-lettres renvoyées telles quelles (pratique pour laisser passer espaces/ponctuation)."""
        if not lettre or len(lettre) != 1:
            assertionError("permuter attend un caractère unique.")
        L = lettre.upper()
        if not est_majuscule(L):
            return lettre
        return self.plugboard.get(L, L)
    
    def connect(self, a: str, b: str) -> None:
        """Ajoute une connexion a<->b (lève si impossible)."""
        if self.nb_paires >= MAX_PAIRES:
            assertionError(f"Nombre maximal de paires atteint ({MAX_PAIRES}).")
        a, b = a.upper(), b.upper()
        if not (est_majuscule(a) and est_majuscule(b)):
            assertionError("Seules les lettres A–Z sont autorisées.")
        if a == b:
            assertionError("Impossible de connecter une lettre à elle-même.")
        if self.est_connectee(a) or self.est_connectee(b):
            assertionError("Une des lettres est déjà connectée.")
        self.plugboard[a] = b
        self.plugboard[b] = a

    def disconnect(self, lettre: str) -> Optional[Tuple[str, str]]:
        """Supprime la paire contenant `lettre`. Renvoie le tuple (x,y) supprimé ou None si non connectée."""
        if not lettre or len(lettre) != 1:
            assertionError("disconnect attend un caractère unique.")
        L = lettre.upper()
        if not est_majuscule(L):
            assertionError("disconnect s'applique uniquement aux lettres A–Z.")
        if L not in self.plugboard:
            return None
        autre = self.plugboard.pop(L)
        if self.plugboard.get(autre) == L:
            self.plugboard.pop(autre, None)
        return tuple(sorted((L, autre)))

    def reset(self):
        """Réinitialise le plugboard en supprimant toutes les connexions."""
        self.plugboard.clear()
    

    @property
    def nb_paires(self) -> int:
        """Renvoie le nombre de paires connectées dans le plugboard."""
        return len(self.plugboard) // 2
    

    def afficher(self):
        """Affiche les connexions du plugboard."""
        if not self.plugboard:
            print("Plugboard non configuré.")
            return
        
        connexions = []
        deja_affiche = set()

        for a, b in self.plugboard.items():
            if a not in deja_affiche and b not in deja_affiche:
                connexions.append(f"{a} <-> {b}")
                deja_affiche.add(a)
                deja_affiche.add(b)

        print("Connexions du Plugboard :")
        for connexion in connexions:
            print(connexion)

    def __repr__(self) -> str:
        pairs = []
        deja = set()
        for a in sorted(self.plugboard.keys()):
            if a in deja:
                continue
            b = self.plugboard[a]
            pairs.append(f"{a}{b}")
            deja.update({a, b})
        return f"Plugboard(paires={pairs})"
    
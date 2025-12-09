from typing import Iterable

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def assertionError(message: str) -> None:
    """Compat: reproduit l'appel que tu utilisais, mais lève une vraie AssertionError."""
    raise AssertionError(message)


def est_majuscule(ch: str) -> bool:
    return len(ch) == 1 and ch in ALPHABET


def est_liste_paires_valides(paires: Iterable[str]) -> None:
    """Valide une liste de paires 'AB' (A–Z), sans doublons et sans auto-connexion."""
    seen = set()
    for p in paires:
        if not isinstance(p, str):
            assertionError(f"Paire invalide (type): {p!r}")
        p = p.strip().upper()
        if len(p) != 2 or any(c not in ALPHABET for c in p):
            assertionError(f"Paire invalide (doit être 'AB' avec A–Z): {p!r}")
        a, b = p[0], p[1]
        if a == b:
            assertionError(f"Paire invalide (lettres identiques): {p!r}")
        if a in seen or b in seen:
            assertionError(f"Lettres déjà utilisées: {a!r} ou {b!r}")
        seen.update({a, b})

from configuration.configuration import ALPHABET

def est_caractere_autorise(ch: str) -> bool:
    """True si le caractère est autorisé dans le texte clair."""
    if not ch:
        return False
    if ch == " ":
        return True
    return ch.upper() in ALPHABET


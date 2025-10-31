from typing import Dict
from utils import assertionError

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Reflecteur:
    """Classe Reflecteur pour gérer la réflexion des lettres."""

    def __init__(self, mapping: Dict[str, str] | None = None, preset: str | None = None) -> None:
        """mapping ou preset ('B' ou 'C')."""
        if preset:
            preset = preset.upper()
            if preset not in REFLECTORS:
                assertionError(f"Reflecteur inconnu: {preset!r}. Choisir parmi: {', '.join(REFLECTORS)}")
            self.mapping = _str_to_bijective_map(REFLECTORS[preset])
        else:
            self.mapping = mapping or {}
            _validate_bijection(self.mapping)

    def allumer_lettre(self, lettre: str) -> str:
        """Réfléchit une lettre via le reflecteur."""
        if not lettre or len(lettre) != 1:
            assertionError("allumer_lettre attend un caractère unique.")
        L = lettre.upper()
        if L not in ALPHABET:
            return lettre
        return self.mapping.get(L, L)
        

def _str_to_bijective_map(s: str) -> Dict[str, str]:
    """Convertit une chaîne 26 lettres en dict bijectif A->s[0], etc., puis impose la réciproque."""
    if len(s) != 26:
        assertionError("Le mapping de réflecteur doit avoir 26 lettres.")
    s = s.upper()
    m: Dict[str, str] = {}
    for i, a in enumerate(ALPHABET):
        b = s[i]
        if a == b:
            assertionError("Un réflecteur ne peut pas connecter une lettre à elle-même.")
        m[a] = b
        m[b] = a
    _validate_bijection(m)
    return m


def _validate_bijection(m: Dict[str, str]) -> None:
    if not m:
        return
    # bijectif: a->b et b->a, pas d'auto-connexion
    for a, b in m.items():
        if a == b:
            assertionError("Auto-connexion détectée dans le réflecteur.")
        if m.get(b) != a:
            assertionError("Mapping de réflecteur non bijectif.")
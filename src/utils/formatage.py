import re

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def only_letters(text: str, keep_spaces: bool = False) -> str:
    """Conserve uniquement A–Z (option: espaces)."""
    text = text.upper()
    if keep_spaces:
        return re.sub(r"[^A-Z ]", "", text)
    return re.sub(r"[^A-Z]", "", text)


def group5(text: str) -> str:
    """Groupe le texte en blocs de 5 (classique radio)."""
    text = only_letters(text, keep_spaces=False)
    return " ".join(text[i:i+5] for i in range(0, len(text), 5))


def normalize_char(c: str) -> str:
    """Retourne la lettre majuscule si c appartien à A–Z, sinon c tel quel."""
    c = c.upper()
    return c if c in ALPHABET else c

import json
from typing import Dict, List, Tuple

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ROTORS: Dict[str, Tuple[str, str]] = {
    "I":   ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II":  ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV":  ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V":   ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}

REFLECTORS: Dict[str, str] = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}


def load_codebook(json_path: str, date_str: str) -> Dict:
    """Charge l'entrée complète du livre de code (rotors, positions, plugboard) pour une date."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if date_str not in data:
        raise KeyError(f"Aucune entrée pour la date {date_str!r} dans {json_path}.")
    entry = data[date_str]
    if not isinstance(entry, dict):
        raise ValueError(f"Entrée invalide pour {date_str!r}.")
    return entry


def parse_positions(pos3: str) -> List[int]:
    """Transforme 'DCA' -> [3, 2, 0] (A=0)."""
    pos3 = pos3.strip().upper()
    if len(pos3) != 3 or any(c not in ALPHABET for c in pos3):
        raise ValueError("Les positions doivent être 3 lettres A–Z (ex: 'DCA').")
    return [ALPHABET.index(c) for c in pos3]

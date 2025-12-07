import string
import os
import json
from datetime import date

from ui.ui import show_info,show_error,demander_rotors_gui,demander_positions_gui, demander_rings_gui,input_dialog
from configuration.configuration import load_codebook

# -------------------------------------------
# Fonctions pour demander les configurations MANUELLEMENT
# -------------------------------------------
def demander_rotors():
    valid_rotors = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

    # 1) Combien de rotors l'utilisateur veut-il ?
    while True:
        nb_str = input_dialog(
            "Nombre de rotors",
            "Combien de rotors souhaitez-vous utiliser ? (3 à 8)",
            allow_back=True
        )
        if nb_str is None:
            return None
        try:
            nb = int(nb_str.strip())
        except ValueError:
            show_error("Erreur", "Veuillez entrer un nombre entier entre 3 et 8.")
            continue
        if not (3 <= nb <= 8):
            show_error("Erreur", "Le nombre de rotors doit être compris entre 3 et 8.")
            continue
        break

    # 2) Choix des rotors eux-mêmes
    choix = demander_rotors_gui(n=nb, rotors_possibles=valid_rotors)
    return choix


def demander_positions(n=3):
    """
    Demande les positions initiales des rotors via la fenêtre demander_positions_gui.
    """
    while True:
        positions = demander_positions_gui(n=n)

        # Si l'utilisateur ferme la fenêtre --> on annule
        if positions is None:
            return None

        # Vérification (en théorie inutile)
        valid = True
        for p in positions:
            if not isinstance(p, str) or len(p) != 1 or p not in string.ascii_uppercase:
                valid = False
                break

        if not valid:
            show_error(
                "Erreur positions",
                f"Les positions doivent être {n} lettres majuscules entre A et Z."
            )
            continue

        return positions


def demander_ring_settings(n=3):
    """ Entrée : n (nombre de rotors)
    Sortie : liste d'entiers [0-25] ou None si Retour/annulation.
    Demande les Ring settings (Ringstellung) pour n rotors via une fenêtre graphique."""
    while True:
        lettres = demander_rings_gui(n=n)

        if lettres is None:
            return None

        if len(lettres) != n:
            show_error(
                "Erreur Ringstellung",
                f"Vous devez choisir exactement {n} lettres."
            )
            continue

        ok = True
        rings = []
        for c in lettres:
            c = (c or "").strip().upper()
            if len(c) != 1 or c < "A" or c > "Z":
                ok = False
                break
            rings.append(ord(c) - ord("A"))

        if not ok:
            show_error(
                "Erreur Ringstellung",
                "Les Ring settings doivent être des lettres A–Z."
            )
            continue

        return rings


def demander_plugboard(max_paires=10, allow_back=True):
    alphabet = set(string.ascii_uppercase)

    # 1) Demander si on veut max_paires ou non
    while True:
        saisie = input_dialog(
            "Plugboard",
            f"Souhaitez-vous {max_paires} connexions de plugboard (complexité max) ?\n"
            "Répondez O (oui) ou N (non).",
            allow_back=allow_back
        )
        if saisie is None:
            return None

        choix = saisie.strip().lower()
        if choix in ("o", "oui"):
            target_pairs = max_paires
            break
        if choix in ("n", "non"):
            nb = input_dialog(
                "Plugboard",
                f"Combien de connexions souhaitez-vous ? (0 à {max_paires}) :",
                allow_back=allow_back
            )
            if nb is None:
                return None
            try:
                target_pairs = int(nb.strip())
                if 0 <= target_pairs <= max_paires:
                    break
                else:
                    show_error("Erreur plugboard", f"Entrez un entier entre 0 et {max_paires}.")
            except ValueError:
                show_error("Erreur plugboard", "Entrez un entier valide.")
        else:
            show_error("Erreur plugboard", "Répondez par O (oui) ou N (non).")

    if target_pairs == 0:
        return []

    # 2) Demander les paires en une seule fois
    while True:
        saisie = input_dialog(
            "Plugboard",
            f"Saisissez {target_pairs} paires sous forme AB CD EF ...\n"
            "Sans chevauchement de lettres.\n"
            "Exemple : AQ WS ED RF...",
            allow_back=allow_back
        )
        if saisie is None:
            return None

        tokens = saisie.strip().upper().split()
        if len(tokens) != target_pairs:
            show_error(
                "Erreur plugboard",
                f"Vous devez entrer exactement {target_pairs} paires séparées par des espaces."
            )
            continue

        used_letters = set()
        pairs = []
        ok = True
        for token in tokens:
            if len(token) != 2:
                show_error("Erreur plugboard", f"'{token}' n'est pas une paire de 2 lettres.")
                ok = False
                break
            a, b = token[0], token[1]
            if a not in alphabet or b not in alphabet:
                show_error("Erreur plugboard", f"'{token}' contient des caractères non A-Z.")
                ok = False
                break
            if a == b:
                show_error("Erreur plugboard", f"'{token}' doit relier deux lettres différentes.")
                ok = False
                break
            if a in used_letters or b in used_letters:
                show_error(
                    "Erreur plugboard",
                    f"'{token}' chevauche une lettre déjà utilisée ({a} ou {b})."
                )
                ok = False
                break
            used_letters.update([a, b])
            pairs.append(token)

        if ok:
            return pairs


# -------------------------------------------
# Fonctions spécifiques au LIVRE DE CODE
# -------------------------------------------

def demander_nb_rotors_livre():
    """
    Demande combien de rotors utiliser AVEC le livre de code (3 à 8).
    """
    while True:
        nb_str = input_dialog(
            "Nombre de rotors",
            "Combien de rotors souhaitez-vous utiliser avec le livre de code ? (3 à 8)",
            allow_back=True
        )
        if nb_str is None:
            return None
        try:
            nb = int(nb_str.strip())
        except ValueError:
            show_error("Erreur", "Veuillez entrer un nombre entier entre 3 et 8.")
            continue
        if not (3 <= nb <= 8):
            show_error("Erreur", "Le nombre de rotors doit être compris entre 3 et 8.")
            continue
        return nb


def charger_config_livre_code(nb_rotors: int | None = None):
    """
    Charge la config du jour depuis data/livre_code.json.
    Si nb_rotors est fourni, on tronque rotors/positions à nb_rotors.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__)) 
    codebook_path = os.path.join(base_dir, "data", "livre_code.json")

    with open(codebook_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    today = date.today().isoformat()
    if today in data:
        date_str = today
    else:
        date_str = sorted(data.keys())[-1]

    entry = load_codebook(codebook_path, date_str)

    rotors = entry["rotors"]
    positions = entry["positions"]
    plugboard = entry["plugboard"]
    
    rings_raw = entry.get("rings") # peut être absent car optionnel
    if rings_raw is None:
        rings = [0] * len(rotors)
    else:
        rings_raw = rings_raw.strip().upper()
        if len(rings_raw) != len(rotors):
            show_error(
                "Livre de code",
                f"Le champ 'rings' ({rings_raw}) ne contient pas autant de lettres "
                f"que de rotors ({len(rotors)})."
            )
            return None
        rings = [ord(c) - ord("A") for c in rings_raw]



    if nb_rotors is not None:
        if len(rotors) < nb_rotors or len(positions) < nb_rotors:
            show_error(
                "Livre de code",
                f"Le livre de code pour la date {date_str} ne définit que {len(rotors)} rotors, "
                f"vous en avez demandé {nb_rotors}."
            )
            return None
        rotors = rotors[:nb_rotors]
        positions = positions[:nb_rotors]
        rings = rings[:nb_rotors]
    else:
        nb_rotors = len(rotors)

    show_info(
        "Livre de code",
        f"Configuration du livre de code pour la date : {date_str}\n"
        f"Nombre de rotors utilisés : {nb_rotors}"
    )

    return {
        "rotors": rotors,
        "positions": positions,
        "rings": rings, 
        "plugboard": plugboard,
    }
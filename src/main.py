"""
Point d'entrée automatique de la machine Enigma.
- Si aucun argument fourni, on charge la configuration du jour depuis data/livre_code.json
- Sinon, on accepte les options (--date, --rotors, etc.)
"""

import sys
import os
from datetime import date
import argparse

# --- forcer src/ dans sys.path pour éviter conflits de "utils" ---
sys.path.insert(0, os.path.dirname(__file__))

from components.machineEnigma import MachineEnigma
from configuration.configuration import load_codebook


def charger_config_auto(codebook_path: str):
    """Charge automatiquement la config du jour ou la dernière date disponible."""
    import json
    from datetime import date

    with open(codebook_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    today = date.today().isoformat()
    if today in data:
        date_str = today
    else:
        # si la date du jour n'existe pas, on prend la dernière date triée
        date_str = sorted(data.keys())[-1]

    print(f"Configuration chargée pour la date : {date_str}")
    return load_codebook(codebook_path, date_str)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--date", type=str, help="Date du livre de code (YYYY-MM-DD)")
    parser.add_argument("--msg", type=str, default="ENIGMA DEMO", help="Message à chiffrer")
    parser.add_argument("--group5", action="store_true", help="Afficher le résultat en groupes de 5")
    args, _ = parser.parse_known_args()

    # chemin du livre de code
    codebook_path = os.path.join(os.path.dirname(__file__), "data", "livre_code.json")

    # Charger la config : soit date donnée, soit auto
    if args.date:
        entry = load_codebook(codebook_path, args.date)
    else:
        entry = charger_config_auto(codebook_path)

    rotor_names = entry["rotors"]
    positions = entry["positions"]
    plug_pairs = entry["plugboard"]

    # Initialiser la machine
    machine = MachineEnigma(
        rotors_names=rotor_names,
        positions=positions,
        plug_pairs=plug_pairs,
        reflector_preset="B",
    )

    print("Machine Enigma initialisée :")
    print(f"  Rotors     : {rotor_names}")
    print(f"  Positions  : {positions}")
    print(f"  Plugboard  : {', '.join(plug_pairs)}\n")

    message = args.msg.upper()
    print(f"Message clair : {message}\n")

    cipher = machine.encrypt(message, keep_spaces=True, group_5=args.group5)
    print(f"Message chiffré : {cipher}")

if __name__ == "__main__":
    main()

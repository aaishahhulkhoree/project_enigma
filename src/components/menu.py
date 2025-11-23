import string 
import os 
import json
from datetime import date

from components.ui import demander_choix, demander_texte
from components.machineEnigma import MachineEnigma
from configuration.configuration import load_codebook #recupère la fonction load_codebook

class Menu:

    @staticmethod
    def choix_prompt(prompt, valid_choices, allow_back=False, allow_quit=False):
        """
        Affiche un prompt texte + éventuellement:
        - R: Retour
        - Q: Quitter
        et renvoie le choix validé.
        """
        extra = []
        if allow_back:
            extra.append("R: Retour")
        if allow_quit:
            extra.append("Q: Quitter")
        if extra:
            prompt += "\n" + " / ".join(extra)
        else :
            prompt += "\n"

        while True:
            #choix = input(f"{prompt}\n> ").strip().upper()

            choix = demander_texte("Menu Enigma", prompt)
            if choix is None:
            # utilisateur a fermé la fenêtre → on peut décider de quitter
                return "Q" if allow_quit else None

            choix = choix.strip().upper()

            if allow_back and choix == "R":
                return "R"
            if allow_quit and choix == "Q":
                return "Q"
            if choix in valid_choices:
                return choix
            print("Choix invalide. Réessayez.")

    # -------------------------------------------
    # Fonctions pour demander les configurations MANUELLEMENT 
    # -------------------------------------------
    @staticmethod
    def demander_rotors(n=3):
        while True:
            rotors_input = input(f"Entrez les {n} rotors (ex: I II III): ").strip()
            rotors = rotors_input.split()
            if len(rotors) != n:
                print(f"Veuillez entrer exactement {n} rotors. Recommencez.")
                continue
            valid_rotors = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII"}
            if all(rotor in valid_rotors for rotor in rotors):
                break
            else:
                print("Rotors invalides. Choisissez parmi I, II, III, IV, V, VI, VII, VIII.")
        return rotors

    @staticmethod
    def demander_positions(n=3):
        while True:
            positions_input = input(f"Entrez les {n} positions initiales des rotors (ex: A B C): ").strip()
            positions = positions_input.split()
            if len(positions) != n:
                print(f"Veuillez entrer exactement {n} positions. Recommencez.")
                continue
            if all(pos in string.ascii_uppercase for pos in positions):
                break
            else:
                print("Positions invalides. Utilisez des lettres majuscules A-Z.")
        return positions


    @staticmethod
    def demander_plugboard(max_paires=10, allow_back=True):
        alphabet = set(string.ascii_uppercase)
        while True:
            choix = input(f"Souhaitez-vous {max_paires} connexions de plugboard pour complexité max ? (o/n): — ou R pour retour:\n").strip().lower()
            if allow_back and choix == "r":
                return None
            if choix in ("o", "oui"):
                target_pairs = max_paires
                break
            if choix in ("n", "non"):
                try:
                    nb = input("Combien de connexions souhaitez-vous ? (0 à 10): — ou R pour retour:\n").strip()
                    if allow_back and nb == 'r':
                        return None
                    target_pairs = int(nb)
                    if 0 <= target_pairs <= max_paires:
                        break
                    print("Entrez un entier entre 0 et 10.")
                except ValueError:
                    print("Entrez un entier valide.")
            else:
                print("Répondez par 'o' ou 'n'.")

        if target_pairs == 0:
            return []

        print(f"\nSaisissez {target_pairs} paires sous forme AB (ex: AQ), sans chevauchement de lettres.")
        print("Astuce: vous pouvez aussi les entrer en une seule ligne séparées par des espaces (ex: AB CD EF...).")
        print("Tapez R pour revenir en arrière.")

        used_letters = set()
        pairs = []

        while len(pairs) < target_pairs:
            rest = target_pairs - len(pairs)
            ligne = input(f"Entrez {rest} paire(s): ").strip().upper()

            if allow_back and ligne == "R":
                return None
            
            candidats = ligne.split()
            for token in candidats:
                if len(pairs) >= target_pairs:
                    break
                if len(token) != 2:
                    print(f"'{token}' n'est pas une paire de 2 lettres.")
                    continue
                a, b = token[0], token[1]
                if a not in alphabet or b not in alphabet:
                    print(f"'{token}' contient des caractères non A-Z.")
                    continue
                if a == b:
                    print(f"'{token}' doit relier deux lettres différentes.")
                    continue
                if a in used_letters or b in used_letters:
                    print(f"'{token}' chevauche une lettre déjà utilisée ({a} ou {b}).")
                    continue
                used_letters.update([a, b])
                pairs.append(token)
        return pairs
    
    #-------------------------------------------
    # Fonction pour charger la config du jour depuis le livre de code AUTOMATIQUEMENT
    #-------------------------------------------
    
    def charger_config_livre_code():
        """Charge la config du jour depuis data/livre_code.json."""

        # on remonte de components/ vers src/, puis on va dans data/
        base_dir = os.path.dirname(os.path.dirname(__file__))
        codebook_path = os.path.join(base_dir, "data", "livre_code.json")

        with open(codebook_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        today = date.today().isoformat()
        if today in data:
            date_str = today
        else:
            date_str = sorted(data.keys())[-1]

        print(f"Configuration du livre de code pour la date : {date_str}")
        return load_codebook(codebook_path, date_str)



    #-------------------------------------------
    # Menu principal et navigation
    #-------------------------------------------
    @staticmethod   
    def afficher_menu():
        print("****** Menu Enigma Simulator ******")
        print("Veuillez choisir une option :")
        print("1. Chiffrer un message")
        print("2. Déchiffrer un message")
        print("3. Quitter")
        return Menu.choix_prompt("Sélectionnez une option (1/2/3):", {"1", "2", "3"})
    
    @staticmethod
    def configurer_manuellement():
        rotors = Menu.demander_rotors()
        if rotors is None:
            return None

        positions = Menu.demander_positions()
        if positions is None:
            return None

        plugboard = Menu.demander_plugboard()
        if plugboard is None:
            return None
        return {"mode": "manuel", "rotors": rotors, "positions": positions, "plugboard": plugboard}

    def menu_chiffrement():
        while True:
            print("\n--- Chiffrement ---")
            print("1. Utiliser les configurations du jour (livre de code)")
            print("2. Entrer manuellement les rotors, positions et plugboard")
            print("R. Retour au menu principal")
            choix = Menu.choix_prompt("Votre choix (1/2/R):", {"1", "2"}, allow_back=True)

            if choix == "R":
                return None
            if choix == "1":
                #print("Configuration du jour sélectionnée.")
                entry = Menu.charger_config_livre_code()
                return {
                    "mode": "livre_de_code",
                    "rotors": entry["rotors"],
                    "positions": list(entry["positions"]), 
                    "plugboard": entry["plugboard"],
                }
            if choix == "2":
                cfg = Menu.configurer_manuellement()
                if cfg is None:
                    continue
                return cfg

    @staticmethod
    def menu_dechiffrement():
        while True:
            print("\n--- Déchiffrement ---")
            print("1. Utiliser les configurations du jour (livre de code)")
            print("2. Entrer manuellement les rotors, positions et plugboard")
            print("R. Retour")
            choix = Menu.choix_prompt("Votre choix (1/2) ?", {"1", "2"}, allow_back=True)

            if choix == "R":
                return None
            if choix == "1":
                #print("Configuration du jour sélectionnée.")
                entry = Menu.charger_config_livre_code()
                return {
                    "mode": "livre_de_code",
                    "rotors": entry["rotors"],
                    "positions": list(entry["positions"]), 
                    "plugboard": entry["plugboard"],
                }
            if choix == "2":
                cfg = Menu.configurer_manuellement()
                if cfg is None:
                    continue
                return cfg
            
    #-------------------------------------------
    # Fonction pour lancer la machine Enigma avec la config donnée
    #-------------------------------------------
    @staticmethod
    def lancer_machine(config, mode: str):
        """Crée la machine Enigma avec la config et chiffre/déchiffre un message."""
        rotors = config["rotors"]
        positions = "".join(config["positions"])
        plugboard = config["plugboard"]

        machine = MachineEnigma(
            rotors_names=rotors,
            positions=positions,
            plug_pairs=plugboard,
            reflector_preset="B",
        )

        texte = input(f"Entrez le message à {mode} : ").strip()
        if not texte:
            print("Aucun texte saisi.")
            return

        # Enigma est symétrique : même fonction pour chiffrer et déchiffrer
        resultat = machine.encrypt(texte, keep_spaces=True, group_5=True)
        print(f"\nTexte {mode} : {resultat}\n")

    
    @staticmethod
    def quitter():
        print("Merci d'avoir utilisé le simulateur Enigma. Au revoir!")
        print("Fermeture du programme.")
        exit(0)

    @staticmethod
    def main_menu():
        while True:
            choix = Menu.afficher_menu()

            if choix == "1":
                config = Menu.menu_chiffrement()
                if config is None:
                    continue
                print("Configuration sélectionnée:", config)
                Menu.lancer_machine(config, mode="chiffrer") 
                    
            elif choix == "2":
                config = Menu.menu_dechiffrement()
                if config is None:
                    continue
                print("Configuration sélectionnée:", config)
                Menu.lancer_machine(config, mode="déchiffrer")

            elif choix == "3":
                Menu.quitter()
            
            else:
                print("Choix invalide. Réessayez.")


if __name__ == "__main__":
    Menu.main_menu()
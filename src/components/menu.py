import string 
import os 
import json
from datetime import date

from components.ui import demander_texte, show_info, show_error, demander_rotors_gui, popup_menu
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
            #print("Choix invalide. Réessayez.")
            show_error("Choix invalide", "Choix invalide. Réessayez.")

    # -------------------------------------------
    # Fonctions pour demander les configurations MANUELLEMENT 
    # -------------------------------------------
    @staticmethod
    def demander_rotors(n=3):
        valid_rotors = ["I", "II", "III", "IV", "V"]

        choix = demander_rotors_gui(n=n, rotors_possibles=valid_rotors)
        return choix 

    @staticmethod
    def demander_positions(n=3):
        while True:
            #positions_input = input(f"Entrez les {n} positions initiales des rotors (ex: A B C): ").strip()
            saisie = demander_texte(
                "Positions des rotors",
                f"Entrez les {n} positions initiales (ex: A B C ou ABC):"
            )
            if saisie is None:
                return None
            
            positions = saisie.strip().upper().replace(" ", "")
            if len(positions) != n or any(c not in string.ascii_uppercase for c in positions):
                show_error(
                    "Erreur positions",
                    f"Vous devez entrer exactement {n} lettres A-Z (ex: A B C ou ABC)."
                )
                continue
            #la suite du code attend une liste, donc on met bien une liste:
            return list(positions)


    @staticmethod
    def demander_plugboard(max_paires=10, allow_back=True):
        alphabet = set(string.ascii_uppercase)

        #Soit 1)Demander si on veut max paires ou non
        while True:
            saisie = demander_texte(
                "Plugboard",
                f"Souhaitez-vous {max_paires} connexions de plugboard (complexité max) ?\n"
                "Répondez O (oui), N (non) ou R (retour)."
            )
            if saisie is None:
                return None

            choix = saisie.strip().lower()
            if allow_back and choix == "r":
                return None
            if choix in ("o", "oui"):
                target_pairs = max_paires
                break
            if choix in ("n", "non"):
                nb = demander_texte(
                    "Plugboard",
                    f"Combien de connexions souhaitez-vous ? (0 à {max_paires})\n"
                    "Ou R pour retour."
                )
                if nb is None:
                    return None
                nb = nb.strip().lower()
                if allow_back and nb == "r":
                    return None
                try:
                    target_pairs = int(nb)
                    if 0 <= target_pairs <= max_paires:
                        break
                    else:
                        show_error("Erreur plugboard", f"Entrez un entier entre 0 et {max_paires}.")
                except ValueError:
                    show_error("Erreur plugboard", "Entrez un entier valide.")
            else:
                show_error("Erreur plugboard", "Répondez par O, N ou R.")

        if target_pairs == 0:
            return []

        #Soit 2)Demander les paires en une seule fois
        while True:
            saisie = demander_texte(
                "Plugboard",
                f"Saisissez {target_pairs} paires sous forme AB CD EF ...\n"
                "Sans chevauchement de lettres.\n"
                "Exemple : AQ WS ED RF..."
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

    
    #-------------------------------------------
    # Fonction pour charger la config du jour depuis le livre de code AUTOMATIQUEMENT
    #-------------------------------------------
    @staticmethod
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

        #print(f"Configuration du livre de code pour la date : {date_str}")
        show_info("Livre de code", f"Configuration du livre de code pour la date : {date_str}")
        return load_codebook(codebook_path, date_str)



    #-------------------------------------------
    # Menu principal et navigation
    #-------------------------------------------
    @staticmethod
    def afficher_menu():
        choix = popup_menu(
            "Menu principal",
            "Que souhaitez-vous faire sur la machine Enigma ?",
            {
                "1": "Chiffrer un message",
                "2": "Déchiffrer un message",
                "3": "Quitter"
            },
            include_back=False 
        )
        if choix is None:
            return "3"
        return choix


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


    @staticmethod
    def menu_chiffrement():
        while True:
            choix = popup_menu(
                "Chiffrement",
                "Avec quelle méthode souhaitez-vous chiffrer votre message ?",
                {
                    "1": "Utiliser les configurations du jour (livre de code)",
                    "2": "Entrer manuellement les rotors, positions et plugboard"
                },
                include_back=True 
            )

            if choix == "R" or choix is None:
                return None
            if choix == "1":
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
            choix = popup_menu(
                "Déchiffrement",
                "Avec quelle méthode souhaitez-vous déchiffrer votre message ?",
                {
                    "1": "Utiliser les configurations du jour (livre de code)",
                    "2": "Entrer manuellement les rotors, positions et plugboard"
                },
                include_back=True
            )

            if choix == "R" or choix is None:
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

        texte = demander_texte("Message", f"Entrez le message à {mode} :")
        if texte is None or not texte.strip():
            show_error("Erreur", "Aucun texte saisi.")
            return

        # Enigma est symétrique : même fonction pour chiffrer et déchiffrer
        resultat = machine.encrypt(texte, keep_spaces=True, group_5=True)
        #print(f"\nTexte {mode} : {resultat}\n")
        show_info("Résultat", f"Texte {mode} :\n\n{resultat}")

    
    @staticmethod
    def quitter():
        # print("Merci d'avoir utilisé le simulateur Enigma. Au revoir!")
        # print("Fermeture du programme.")
        exit(0)

    @staticmethod
    def main_menu():
        while True:
            choix = Menu.afficher_menu()

            if choix == "1":
                config = Menu.menu_chiffrement()
                if config is None:
                    continue
                # print("Configuration sélectionnée:", config)
                Menu.lancer_machine(config, mode="chiffrer") 
                    
            elif choix == "2":
                config = Menu.menu_dechiffrement()
                if config is None:
                    continue
                # print("Configuration sélectionnée:", config)
                Menu.lancer_machine(config, mode="déchiffrer")

            elif choix == "3":
                Menu.quitter()
            
            else:
                # print("Choix invalide. Réessayez.")
                show_error("Choix invalide", "Choix invalide. Réessayez.")


if __name__ == "__main__":
    Menu.main_menu()
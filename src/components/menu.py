import string 
import os 
import json
import math
from datetime import date

from components.ui import show_info, show_error, demander_rotors_gui, demander_positions_gui, popup_menu, input_dialog
from components.machineEnigma import MachineEnigma
from configuration.configuration import load_codebook #recupère la fonction load_codebook

class Menu:

    # -------------------------------------------
    # Fonctions pour demander les configurations MANUELLEMENT 
    # -------------------------------------------
    @staticmethod
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


    @staticmethod
    def demander_positions(n=3):
        """
        Demande les positions initiales des rotors via une boucle while True,
        mais en utilisant une fenêtre graphique (demander_positions_gui).
        """
        while True:

            # Ouvre la fenêtre avec menus déroulants
            positions = demander_positions_gui(n=n)

            # Si l'utilisateur ferme la fenêtre --> on annule
            if positions is None:
                return None

            # Vérification (normalement inutile car la GUI empêche d'autres valeurs)
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
                continue  # On relance la demande

            # OK → on renvoie
            return positions




    @staticmethod
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
    @staticmethod
    def demander_nb_rotors_livre():
        """
        Demande combien de rotors utiliser AVEC le livre de code (3 à 8).
        On ne choisit pas les noms ici, ils viennent du livre.
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

    @staticmethod
    def charger_config_livre_code(nb_rotors: int | None = None):
        """
        Charge la config du jour depuis data/livre_code.json.
        Si nb_rotors est fourni, on tronque la liste des rotors/positions
        aux nb_rotors premiers (si le livre en définit assez).
        """
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

        entry = load_codebook(codebook_path, date_str)

        rotors = entry["rotors"]
        positions = entry["positions"]
        plugboard = entry["plugboard"]

        # Si l'utilisateur demande un nombre précis de rotors
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
            "plugboard": plugboard,
        }


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
        
        n= len(rotors)
        positions = Menu.demander_positions(n=n)
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
                #entry = Menu.charger_config_livre_code()
                # 1) Demander d'abord le nombre de rotors
                nb = Menu.demander_nb_rotors_livre()
                if nb is None:
                    continue

                # 2) Charger la config du livre de code en coupant à nb rotors
                entry = Menu.charger_config_livre_code(nb_rotors=nb)
                if entry is None:
                    # erreur (ex: le livre n'a que 3 rotors) -> on revient au menu
                    continue

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
                #entry = Menu.charger_config_livre_code()
                
                # 1) Demander le nombre de rotors
                nb = Menu.demander_nb_rotors_livre()
                if nb is None:
                    continue

                # 2) Charger la config du livre de code coupée à nb rotors
                entry = Menu.charger_config_livre_code(nb_rotors=nb)
                if entry is None:
                    continue


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

        texte = input_dialog("Message", f"Entrez le message à {mode} :", allow_back=True)
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
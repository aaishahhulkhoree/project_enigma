import math  # si tu en as encore besoin

from components.ui import show_error, popup_menu, input_dialog
from components.machineEnigma import MachineEnigma

from components.configEnigma import (demander_rotors,demander_positions,demander_plugboard,demander_nb_rotors_livre,charger_config_livre_code)


class Menu:

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
        """
        Enchaîne 3 étapes :
        1) Choix du nombre de rotors + des rotors
        2) Choix des positions initiales
        3) Choix du plugboard

        Comportement des boutons Retour :
        - Retour dans la fenêtre des ROTORS  → retour au menu précédent (chiffrement/déchiffrement)
        - Retour dans la fenêtre des POSITIONS → retour à l'étape 1 (choix des rotors)
        - Retour dans la fenêtre du PLUGBOARD → retour à l'étape 2 (positions)
        """
        while True:  # boucle "globale" = on peut revenir jusqu'au choix des rotors
            # --- Étape 1 : rotors (nombre + noms) ---
            rotors = demander_rotors()
            if rotors is None:
                # Retour demandé à cette étape -> on sort vers le menu chiffrement/déchiffrement
                return None

            n = len(rotors)

            # --- Étape 2 & 3 : positions puis plugboard ---
            while True:
                # Étape 2 : positions
                positions = demander_positions(n)
                if positions is None:
                    # Retour demandé depuis la fenêtre des positions :
                    # on sort de la boucle interne et on revient au choix des rotors
                    break

                # Étape 3 : plugboard
                plugboard = demander_plugboard()
                if plugboard is None:
                    # Retour demandé dans le plugboard :
                    # on reste avec les mêmes rotors, mais on retourne à l'étape positions
                    continue

                # Si on arrive ici, tout est correctement renseigné
                return {
                    "mode": "manuel",
                    "rotors": rotors,
                    "positions": positions,
                    "plugboard": plugboard,
                }


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
                nb = demander_nb_rotors_livre()
                if nb is None:
                    continue

                entry = charger_config_livre_code(nb_rotors=nb)
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
                nb = demander_nb_rotors_livre()
                if nb is None:
                    continue

                entry = charger_config_livre_code(nb_rotors=nb)
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
    # Lancer la machine avec une config
    #-------------------------------------------
    @staticmethod
    def lancer_machine(config, mode: str):
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

        resultat = machine.encrypt(texte, keep_spaces=True, group_5=True)

        from components.ui import show_info  # import local pour éviter un import circulaire
        show_info("Résultat", f"Texte {mode} :\n\n{resultat}")

    @staticmethod
    def quitter():
        exit(0)

    @staticmethod
    def main_menu():
        while True:
            choix = Menu.afficher_menu()

            if choix == "1":
                config = Menu.menu_chiffrement()
                if config is None:
                    continue
                Menu.lancer_machine(config, mode="chiffrer")

            elif choix == "2":
                config = Menu.menu_dechiffrement()
                if config is None:
                    continue
                Menu.lancer_machine(config, mode="déchiffrer")

            elif choix == "3":
                Menu.quitter()
            else:
                show_error("Choix invalide", "Choix invalide. Réessayez.")


if __name__ == "__main__":
    Menu.main_menu()

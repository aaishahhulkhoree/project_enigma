import math 

from ui.ui import show_error, popup_menu, input_dialog, afficher_resultat_avec_complexite
from core.machineEnigma import MachineEnigma
from configuration.configEnigma import (demander_rotors,demander_positions, demander_ring_settings,demander_plugboard,demander_nb_rotors_livre,charger_config_livre_code)
from components.realtime import lancer_mode_temps_reel


class Menu:

    @staticmethod
    def evaluer_complexite(config) -> str:
        """
        Calcule une estimation de la complexité de la configuration Enigma
        (nombre de clés possibles) en fonction :
        - de l'ordre des rotors,
        - des positions initiales,
        - ring setting, 
        - du plugboard.
        Retourne un texte explicatif.
        """
        n_rotors = len(config["rotors"])
        nb_paires = len(config["plugboard"])

        # 1) permutations d'ordre des rotors parmi 8 disponibles
        total_rotors_disponibles = 8
        perm_rotors = 1
        for i in range(total_rotors_disponibles, total_rotors_disponibles - n_rotors, -1):
            perm_rotors *= i

        # 2) positions initiales possibles : 26^n
        positions_factor = 26 ** n_rotors

        # 3) ring settings possibles : 26^n
        ring_factor = 26 ** n_rotors

        # 4) combinaisons de plugboard (formule classique Enigma)
        p = nb_paires
        if p == 0:
            plugboard_configs = 1
        else:
            plugboard_configs = math.factorial(26) // (
                (2 ** p) * math.factorial(p) * math.factorial(26 - 2 * p)
            )

        espace_cles = perm_rotors * positions_factor * ring_factor * plugboard_configs

        # Logs pour avoir des exposants lisibles
        log10_k = math.log10(espace_cles)
        log2_k = math.log2(espace_cles)

        if log2_k < 40:
            niveau = "faible"
        elif log2_k < 80:
            niveau = "moyenne"
        else:
            niveau = "élevée"

        texte = (
            f"Nombre de rotors utilisés : {n_rotors}\n"
            f"Nombre de paires de plugboard : {nb_paires}\n\n"
            f"Ring settings possibles : 26^{n_rotors} possibilités \n"
            "Espace de clés approximatif (nombre de configurations possibles) :\n"
            f"- ≈ 10^{log10_k:.1f} configurations différentes\n"
            f"- soit ≈ 2^{log2_k:.1f} possibilités\n\n"
            f"Niveau global de complexité : {niveau.upper()}."
        )
        return texte

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
                "3": "Mode temps réel",
                "4": "Quitter",
            },
            include_back=False
        )
        if choix is None:
            return "4"  # Considérer comme quitter si la fenêtre est fermée
        return choix

    @staticmethod
    def configurer_manuellement():
        """
        Enchaîne 4 étapes :
        1) Choix du nombre de rotors + des rotors
        2) Choix des positions initiales
        3) Choix des Ring settings (Ringstellung)
        4) Choix du plugboard

        Boutons Retour :
        - Retour dans ROTORS  → retour au menu précédent (chiffrement/déchiffrement)
        - Retour dans POSITIONS → retour à l'étape 1 (choix des rotors)
        - Retour dans RING SETTINGS → retour à l'étape 2 (positions)
        - Retour dans le PLUGBOARD → retour à l'étape 3 (ring settings)
        """
        while True:  # boucle globale = on peut revenir jusqu'au choix des rotors
            # --- Étape 1 : rotors (nombre + noms) ---
            rotors = demander_rotors()
            if rotors is None:
                # Retour demandé à cette étape -> on sort vers le menu chiffrement/déchiffrement
                return None

            n = len(rotors)

            # --- Étapes 2, 3, 4 : positions, ring settings, plugboard ---
            while True:
                # Étape 2 : positions
                positions = demander_positions(n)
                if positions is None:
                    # Retour demandé depuis la fenêtre des positions :
                    # on sort de la boucle interne et on revient au choix des rotors
                    break

                # Étape 3 : Ring settings
                ring_settings = demander_ring_settings(n)
                if ring_settings is None:
                    # Retour demandé -> revenir à l'étape 2 (positions)
                    continue

                # Étape 4 : plugboard
                plugboard = demander_plugboard()
                if plugboard is None:
                    # Retour demandé dans le plugboard :
                    # on garde rotors + positions + ring_settings,
                    # mais on revient à l'étape 3 (ring settings)
                    continue

                # Si on arrive ici, tout est correctement renseigné
                return {
                    "mode": "manuel",
                    "rotors": rotors,
                    "positions": positions,       # liste de lettres
                    "plugboard": plugboard,
                    "rings": ring_settings,       # liste d'entiers 0-25
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
                    "rings": entry["rings"],
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
                    "rings": entry["rings"],
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
        ring_settings = config.get("rings")
        if ring_settings is None:
            ring_settings = [0] * len(rotors)
        plugboard = config["plugboard"]


        machine = MachineEnigma(rotors_names=rotors,positions=positions,ring_settings=ring_settings,plug_pairs=plugboard,reflector_preset="B")

        texte = input_dialog("Message", f"Entrez le message à {mode} :", allow_back=True)
        if texte is None or not texte.strip():
            show_error("Erreur", "Aucun texte saisi.")
            return

        # Enigma est symétrique : même fonction pour chiffrer et déchiffrer
        resultat = machine.encrypt(texte, keep_spaces=True, group_5=False) # Sans groupage 5 ici, plus besoin 

        # Calcul du texte d'évaluation de la complexité à partir de la config
        texte_complexite = Menu.evaluer_complexite(config)

        # Affiche une fenêtre avec le résultat + bouton "Voir l'évaluation de la complexité"
        afficher_resultat_avec_complexite(mode, resultat, texte_complexite)

        #show_info("Résultat", f"Texte {mode} :\n\n{resultat}")

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
                #show_info("Mode temps réel", "Cette fonctionnalité n'est pas encore implémentée.")
                config = Menu.menu_chiffrement() # on réutilise le menu de chiffrement 
                if config is None:
                    continue
                lancer_mode_temps_reel(config)

            elif choix == "4":
                Menu.quitter()
            else:
                show_error("Choix invalide", "Choix invalide. Réessayez.")


if __name__ == "__main__":
    Menu.main_menu()

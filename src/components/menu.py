import string 

class Menu:

    @staticmethod
    def choix_prompt(prompt, valid_choices, allow_back=False, allow_quit=False):
        extra = []
        if allow_back:
            extra.append("R: Retour")
        if allow_quit:
            extra.append("Q: Quitter")
        if extra:
            prompt += "\n" + " / ".join(extra)

        while True:
            choix = input(f"{prompt}\n> ").strip().upper()
            if allow_back and choix == "R":
                return "R"
            if allow_quit and choix == "Q":
                return "Q"
            if choix in valid_choices:
                return choix
            print("Choix invalide. Réessayez.")

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

    #***MENU***
    @staticmethod   
    def afficher_menu():
        print("****** Menu Enigma Simulator ******")
        print("Veuillez choisir une option :")
        print("1. Chiffrer un message")
        print("2. Déchiffrer un message")
        print("Q. Quitter")
        #choix = input("Votre choix: ").strip()
        return Menu.choix_prompt("Sélectionnez une option (1/2/Q):", {"1", "2", "Q"}, allow_quit=True)
    
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
                print("Configuration du jour sélectionnée.")
                return {"mode": "livre_de_code"}
            if choix == "2":
                cfg = Menu._config_manuel()
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
            choix = Menu._prompt_choice("Votre choix (1/2) ?", {"1", "2"}, allow_back=True)

            if choix == "R":
                return None
            if choix == "1":
                print("Configuration du jour sélectionnée.")
                return {"mode": "livre_de_code"}
            if choix == "2":
                cfg = Menu._config_manuel()
                if cfg is None:
                    continue
                return cfg
    
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
                # TODO : oublies pas d'ajouter la suite pour chiffrer le message, 
                    
            elif choix == "2":
                config = Menu.menu_dechiffrement()
                if config is None:
                    continue
                print("Configuration sélectionnée:", config)
                #TODO:  oublies pas d'ajouter la suite pour déchiffrer le message,

            elif choix == "3":
                Menu.quitter()
            
            else:
                print("Choix invalide. Réessayez.")


if __name__ == "__main__":
    Menu.main_menu()
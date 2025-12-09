import tkinter as tk

from ui.ui import root, center_window, show_info, show_error, input_dialog, popup_menu
from core.machineEnigma import MachineEnigma
from configuration.configuration import ALPHABET
from utils.nettoyage import est_caractere_autorise


""" Entrée : None 
    Sortie : str | None
    Demande à l'utilisateur de saisir un code secret via une boîte de dialogue.
    """
def demander_code_secret() -> str | None:
    secret_code = input_dialog(
        "Création du code secret",
        "Créez un code secret qui sera nécessaire pour afficher la configuration :",
        allow_back=True
    )

    if secret_code is None:
        return None
    
    secret_code = secret_code.strip()
    if not secret_code:
        # si le code vide, on considère que l'utilisateur annule
        return None
    return secret_code

""" Entrée : None
    Sortie : bool | None
    Demande à l'utilisateur quel mode temps réel il veut utiliser.
    Retourne:
        - True  -> mode historique (stateful)
        - False -> mode classique (recalcul complet, éditable)
        - None  -> si l'utilisateur annule
    """
def demander_mode_temps_reel() -> bool | None:
    
    choix = popup_menu(
        "Mode temps réel",
        "Choisissez le mode de chiffrement temps réel :",
        {
            "1": "Mode classique (texte éditable, recalcul complet)",
            "2": "Mode historique (stateful, rotors persistants)",
        },
        include_back=True,
    )

    if choix is None or choix == "R":
        return None
    if choix == "2":
        return True
    return False

""" Entrée : 
        rotors : liste des noms de rotors
        positions : chaîne des positions initiales
        plugboard : liste des paires de connexions du plugboard
        secret_code : str
    Sortie : (tk.Toplevel, tk.Text, tk.Text)
    Crée la fenêtre Tkinter du mode temps réel et tous les widgets.
    """
def creer_fenetre_mode_reel(rotors, positions, ring_settings, plugboard, secret_code: str, stateful: bool):
    win = tk.Toplevel(root)
    win.title("Enigma - Mode temps réel")
    win.resizable(True, True)
    win.grab_set()

    win.minsize(800, 400)
    win.update_idletasks()
    center_window(win)

    main_frame = tk.Frame(win, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    title_label = tk.Label(
        main_frame,
        text="Mode temps réel - chiffrement Enigma",
        font=("Segoe UI", 12, "bold")
    )
    title_label.pack(anchor="w", pady=(0, 5))

    mode_label = tk.Label(
        main_frame,
        text="Mode : historique (stateful, rotors persistants)" if stateful
             else "Mode : classique (texte éditable, recalcul complet)",
        font=("Segoe UI", 9, "italic")
    )
    mode_label.pack(anchor="w", pady=(0, 8))

    positions_str = " ".join(list(positions))
    lbl_positions = tk.Label(
        main_frame,
        text=f"Positions des rotors : {positions_str}",
        font=("Segoe UI", 9)
    )
    lbl_positions.pack(anchor="w", pady=(0, 8))

    def afficher_config():
        saisie = input_dialog(
            "Code requis",
            "Entrez le code secret pour afficher la configuration :",
            allow_back=True
        )
        if saisie is None:
            return # utilisateur a annulé
        if saisie.strip() != secret_code:
            show_error("Accès refusé", "Code incorrect. Vous ne pouvez pas voir la configuration.")
            return

        texte_cfg = (
            f"Rotors : {', '.join(rotors)}\n"
            f"Positions : {positions}\n"
            f"Ringstellung : {''.join(chr(ord('A') + r) for r in ring_settings)}\n"
            f"Plugboard : {' '.join(plugboard) if plugboard else 'aucune'}"
        )
        show_info("Configuration Enigma", texte_cfg)

    btn_cfg = tk.Button(
        main_frame,
        text="Afficher la configuration complète",
        command=afficher_config
    )
    btn_cfg.pack(anchor="w", pady=(0, 10))

    # Encadrement pour le texte clair et chiffré
    text_frame = tk.Frame(main_frame)
    text_frame.pack(fill="both", expand=True)

    text_frame.columnconfigure(0, weight=1)
    text_frame.columnconfigure(1, weight=1)
    text_frame.rowconfigure(0, weight=1)

    # Texte clair
    frame_plain = tk.Frame(text_frame)
    frame_plain.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    lbl_plain = tk.Label(frame_plain, text="Texte clair :", font=("Segoe UI", 10, "bold"))
    lbl_plain.pack(anchor="w")

    txt_plain = tk.Text(frame_plain, height=10, wrap="word")
    txt_plain.pack(fill="both", expand=True)

    # Texte chiffré
    frame_cipher = tk.Frame(text_frame)
    frame_cipher.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    lbl_cipher = tk.Label(frame_cipher, text="Texte chiffré :", font=("Segoe UI", 10, "bold"))
    lbl_cipher.pack(anchor="w")

    txt_cipher = tk.Text(frame_cipher, height=10, wrap="word", state="disabled")
    txt_cipher.pack(fill="both", expand=True)

    # Boutons
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill="x", pady=(10, 0))

    def reset():
        txt_plain.delete("1.0", "end")
        txt_cipher.config(state="normal")
        txt_cipher.delete("1.0", "end")
        txt_cipher.config(state="disabled")

    btn_reset = tk.Button(button_frame, text="Réinitialiser", command=reset)
    btn_reset.pack(side="left")

    btn_close = tk.Button(button_frame, text="Retour", command=win.destroy)
    btn_close.pack(side="right")

    return win, txt_plain, txt_cipher, lbl_positions

""" Entrée : 
        txt_plain : tk.Text
        txt_cipher : tk.Text
        rotors : liste des noms de rotors
        positions : chaîne des positions initiales
        plugboard : liste des paires de connexions du plugboard
    Sortie : None
    Connecte la logique de chiffrement temps réel.
    - stateful=False : mode classique (recalcul complet, texte éditable)
    - stateful=True  : mode historique (rotors persistants, saisie append-only)
"""
def connecter_logique_chiffrement(txt_plain: tk.Text,
                                  txt_cipher: tk.Text,
                                  rotors,
                                  positions: str,
                                  plugboard,
                                  ring_settings,
                                  stateful: bool,
                                  lbl_positions=None):
    
    if not stateful:
        # MODE CLASSIQUE (RECALCUL COMPLET, EDITABLE)
        def update_cipher(event=None):
            text = txt_plain.get("1.0", "end-1c")

            clean_chars = []
            invalid = set()
            for ch in text:
                if ch in ("\n", "\r", "\t"):
                    clean_chars.append(" ")
                    continue
                if est_caractere_autorise(ch):
                    clean_chars.append(ch)
                else:
                    invalid.add(ch)

            if invalid:
                txt_plain.delete("1.0", "end")
                txt_plain.insert("1.0", "".join(clean_chars))
                chars = " ".join(sorted(repr(c) for c in invalid))
                show_error(
                    "Caractères non autorisés",
                    "Certains caractères ont été retirés car interdits :\n"
                    f"{chars}\n\nSeules les lettres A–Z et les espaces sont autorisés."
                )

            text = "".join(clean_chars)


            machine = MachineEnigma(
                rotors_names=rotors,
                positions=positions,
                plug_pairs=plugboard,
                reflector_preset="B",
                ring_settings=ring_settings
            )

            cipher = machine.encrypt(text, keep_spaces=True, group_5=False)

            txt_cipher.config(state="normal")
            txt_cipher.delete("1.0", "end")
            txt_cipher.insert("1.0", cipher)
            txt_cipher.config(state="disabled")

        txt_plain.bind("<KeyRelease>", update_cipher)
        return

    # MODE HISTORIQUE (STATEFUL, APPEND-ONLY)
    machine_initial_args = {
        "rotors_names": rotors,
        "positions": positions,
        "plug_pairs": plugboard,
        "reflector_preset": "B",
        "ring_settings": ring_settings,
    }
    machine = MachineEnigma(**machine_initial_args)

    internal_plain = ""

    def maj_label_positions():
        """Met à jour le label avec la position actuelle des rotors (lettres)."""
        if lbl_positions is None:
            return
        pos_str = " ".join(
            chr(ord("A") + r.position) for r in machine.rotors
        )
        lbl_positions.config(text=f"Positions des rotors : {pos_str}")


    def recompute_from_scratch():
        """Recrée la machine et rechiffre tout caractère par caractère."""
        nonlocal machine
        machine = MachineEnigma(**machine_initial_args)
        cipher = []
        for ch in internal_plain:
            if ch.upper() in ALPHABET:
                cipher.append(machine.encrypt_char(ch.upper()))
            else:
                cipher.append(ch)

        txt_cipher.config(state="normal")
        txt_cipher.delete("1.0", "end")
        txt_cipher.insert("1.0", "".join(cipher))
        txt_cipher.config(state="disabled")

    def on_key(event: tk.Event):
        nonlocal internal_plain

        if event.keysym in ("Left", "Right", "Up", "Down", "Home", "End"):
            return "break"

        if event.keysym == "BackSpace":
            if internal_plain:
                internal_plain = internal_plain[:-1]
                txt_plain.delete("end-1c", "end")
                recompute_from_scratch()
            return "break"

        if event.keysym in ("Return", "Tab"):
            return "break"

        ch = event.char
        if not ch:
            return "break"
        
        if not est_caractere_autorise(ch):
            return "break"

        upper = ch.upper()

        txt_plain.insert("end", ch)
        internal_plain += ch

        if upper in ALPHABET:
            enc = machine.encrypt_char(upper)
            positions_str = " ".join(chr(ord("A") + r.position) for r in machine.rotors)
        else:
            enc = ch

        txt_cipher.config(state="normal")
        txt_cipher.insert("end", enc)
        txt_cipher.config(state="disabled")

        # On force le scroll tout en bas
        txt_plain.see("end")
        txt_cipher.see("end")

        maj_label_positions()

        return "break"
    
    maj_label_positions()
    txt_plain.bind("<KeyPress>", on_key)

""" Entrée : config : dictionnaire de configuration Enigma
    Sortie : None
    Ouvre une fenêtre permettant d'obtenir le chiffrement Enigma en temps réel.
    Le texte peut être soit :
      - en mode classique (éditable, recalcul complet)
      - en mode historique (stateful, rotors persistants).
    """
def lancer_mode_temps_reel(config):
    rotors = config["rotors"]
    positions = "".join(config["positions"])
    ring_settings = config.get("rings")
    plugboard = config["plugboard"]

    # 1) Choix du mode
    stateful = demander_mode_temps_reel()
    if stateful is None:
        return  # utilisateur a annulé

    # 2) Demander le code secret
    secret_code = demander_code_secret()
    if secret_code is None:
        return  # utilisateur a annulé ou rien saisi

    # 3) Créer la fenêtre et les widgets
    win, txt_plain, txt_cipher, lbl_positions = creer_fenetre_mode_reel(
        rotors=rotors,
        positions=positions,
        ring_settings=ring_settings,
        plugboard=plugboard,
        secret_code=secret_code,
        stateful=stateful,
    )

    # 4) Connecter la logique de chiffrement temps réel
    connecter_logique_chiffrement(
        txt_plain=txt_plain,
        txt_cipher=txt_cipher,
        rotors=rotors,
        positions=positions,
        ring_settings=ring_settings,
        plugboard=plugboard,
        stateful=stateful,
        lbl_positions=lbl_positions
    )
    txt_plain.focus_set()
    root.wait_window(win)
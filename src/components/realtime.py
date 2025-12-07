import tkinter as tk

from ui.ui import root, center_window, show_info, show_error, input_dialog
from core.machineEnigma import MachineEnigma


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

""" Entrée : 
        rotors : liste des noms de rotors
        positions : chaîne des positions initiales
        plugboard : liste des paires de connexions du plugboard
        secret_code : str
    Sortie : (tk.Toplevel, tk.Text, tk.Text)
    Crée la fenêtre Tkinter du mode temps réel et tous les widgets.
    """
def creer_fenetre_mode_reel(rotors, positions, plugboard, secret_code: str):
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
            f"Plugboard : {' '.join(plugboard) if plugboard else 'aucune'}"
        )
        show_info("Configuration Enigma", texte_cfg)

    btn_cfg = tk.Button(
        main_frame,
        text="Afficher la configuration",
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

    return win, txt_plain, txt_cipher

""" Entrée : 
        txt_plain : tk.Text
        txt_cipher : tk.Text
        rotors : liste des noms de rotors
        positions : chaîne des positions initiales
        plugboard : liste des paires de connexions du plugboard
    Sortie : None
    Connecte la logique de chiffrement temps réel au champ txt_plain. À chaque frappe, le texte est rechiffré et affiché dans txt_cipher.
"""
def connecter_logique_chiffrement(txt_plain: tk.Text,
                                  txt_cipher: tk.Text,
                                  rotors,
                                  positions: str,
                                  plugboard):
    

    def update_cipher(event=None):
        text = txt_plain.get("1.0", "end-1c")

        machine = MachineEnigma(
            rotors_names=rotors,
            positions=positions,
            plug_pairs=plugboard,
            reflector_preset="B"
        )

        cipher = machine.encrypt(text, keep_spaces=True, group_5=False)

        txt_cipher.config(state="normal")
        txt_cipher.delete("1.0", "end")
        txt_cipher.insert("1.0", cipher)
        txt_cipher.config(state="disabled")

    txt_plain.bind("<KeyRelease>", update_cipher)

"""
    Entrée : config : dictionnaire de configuration Enigma
    Sortie : None
    Ouvre une fenêtre permettant d'obtenir le chiffrement Enigma en temps réel.
    Le texte est rechiffré depuis les positions initiales à chaque frappe.
    """
def lancer_mode_temps_reel(config):
    rotors = config["rotors"]
    positions = "".join(config["positions"])
    plugboard = config["plugboard"]

    # 1) Demander le code secret
    secret_code = demander_code_secret()
    if secret_code is None:
        return  # utilisateur a annulé ou rien saisi

    # 2) Créer la fenêtre et les widgets
    win, txt_plain, txt_cipher = creer_fenetre_mode_reel(
        rotors=rotors,
        positions=positions,
        plugboard=plugboard,
        secret_code=secret_code
    )

    # 3) Connecter la logique de chiffrement temps réel
    connecter_logique_chiffrement(
        txt_plain=txt_plain,
        txt_cipher=txt_cipher,
        rotors=rotors,
        positions=positions,
        plugboard=plugboard
    )

    # Focus dans le texte clair et attente de fermeture
    txt_plain.focus_set()
    root.wait_window(win)
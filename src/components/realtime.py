import tkinter as tk

from components.ui import root, center_window
from components.machineEnigma import MachineEnigma

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

    # Fenêtre principale du mode temps réel
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
    title_label.pack(anchor="w")

    cfg_label = tk.Label(
        main_frame,
        text=(
            f"Rotors : {', '.join(rotors)}     "
            f"Positions : {positions}     "
            f"Plugboard : {' '.join(plugboard) if plugboard else 'aucune'}"
        ),
        font=("Segoe UI", 9),
        fg="#555"
    )
    cfg_label.pack(anchor="w", pady=(0, 10))

    text_frame = tk.Frame(main_frame)
    text_frame.pack(fill="both", expand=True)

    text_frame.columnconfigure(0, weight=1)
    text_frame.columnconfigure(1, weight=1)
    text_frame.rowconfigure(0, weight=1)


    # Zone : texte clair
    frame_plain = tk.Frame(text_frame)
    frame_plain.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    lbl_plain = tk.Label(frame_plain, text="Texte clair :", font=("Segoe UI", 10, "bold"))
    lbl_plain.pack(anchor="w")

    txt_plain = tk.Text(frame_plain, height=10, wrap="word")
    txt_plain.pack(fill="both", expand=True)

    # Zone : texte chiffré 
    frame_cipher = tk.Frame(text_frame)
    frame_cipher.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    lbl_cipher = tk.Label(frame_cipher, text="Texte chiffré :", font=("Segoe UI", 10, "bold"))
    lbl_cipher.pack(anchor="w")

    txt_cipher = tk.Text(frame_cipher, height=10, wrap="word", state="disabled")
    txt_cipher.pack(fill="both", expand=True)

    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill="x", pady=(10, 0))

    # Boutons : Réinitialiser / Fermer
    def reset():
        txt_plain.delete("1.0", "end")
        txt_cipher.config(state="normal")
        txt_cipher.delete("1.0", "end")
        txt_cipher.config(state="disabled")

    btn_reset = tk.Button(button_frame, text="Réinitialiser", command=reset)
    btn_reset.pack(side="left")

    btn_close = tk.Button(button_frame, text="Fermer", command=win.destroy)
    btn_close.pack(side="right")

    # Mise à jour du chiffrement à chaque frappe
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

    txt_plain.focus_set()
    root.wait_window(win)

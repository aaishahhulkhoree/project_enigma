import tkinter as tk 
from tkinter import messagebox, simpledialog, ttk

root = tk.Tk()
root.withdraw() 

def center_window(win):
    win.update_idletasks()  # met à jour la taille réelle de la fenêtre
    w = win.winfo_width()
    h = win.winfo_height()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()

    x = int((sw - w) / 2)
    y = int((sh - h) / 2)

    win.geometry(f"{w}x{h}+{x}+{y}")


def demander_texte(title: str, prompt: str) -> str | None:
    """Demande une chaîne à l'utilisateur via une pop-up."""
    return simpledialog.askstring(title, prompt, parent=root)

def show_info(title: str, message: str):
    messagebox.showinfo(title, message, parent=root)


def show_error(title: str, message: str):
    messagebox.showerror(title, message, parent=root)

def demander_rotors_gui(n=3, rotors_possibles=None):
    """
    Ouvre une fenêtre avec n menus déroulants pour choisir les rotors.
    La hauteur de la fenêtre s'adapte automatiquement au nombre de rotors.
    Retourne une liste de noms de rotors, ou None si l'utilisateur clique sur Retour
    ou ferme la fenêtre.
    """
    if rotors_possibles is None:
        rotors_possibles = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

    win = tk.Toplevel(root)
    win.title("Choix des rotors")
    win.resizable(False, False)
    win.grab_set()

    base_height = 180
    per_rotor = 45
    dynamic_height = base_height + n * per_rotor
    win.minsize(450, dynamic_height)

    win.update_idletasks()
    center_window(win)

    style = ttk.Style(win)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Menu.TButton",
        padding=6,
        font=("Segoe UI", 10)
    )
    style.configure(
        "Return.TButton",
        padding=6,
        font=("Segoe UI", 10, "bold")
    )

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    lbl = ttk.Label(
        frame,
        text="Choisissez les rotors à utiliser :",
        justify="center",
        wraplength=400
    )
    lbl.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    combos = []
    for i in range(n):
        l = ttk.Label(frame, text=f"Rotor {i+1} :")
        l.grid(row=i+1, column=0, padx=10, pady=5, sticky="e")

        combo = ttk.Combobox(frame, values=rotors_possibles, state="readonly", width=8)
        combo.current(0)
        combo.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
        combos.append(combo)

    result = {"values": None}

    def valider():
        result["values"] = [c.get() for c in combos]
        win.destroy()

    def retour():
        result["values"] = None
        win.destroy()

    def on_close():
        result["values"] = None
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    # Ligne de boutons : Valider / Retour
    btn_valider = ttk.Button(frame, text="Valider", style="Menu.TButton", command=valider)
    btn_valider.grid(row=n+1, column=0, pady=(10, 0), padx=5, sticky="e")

    btn_retour = ttk.Button(frame, text="Retour", style="Return.TButton", command=retour)
    btn_retour.grid(row=n+1, column=1, pady=(10, 0), padx=5, sticky="w")

    root.wait_window(win)

    return result["values"]


def demander_positions_gui(n=3):
    """
    Ouvre une fenêtre adaptée automatiquement au nombre de rotors.
    Retourne une liste de lettres (positions) ou None si l'utilisateur clique sur Retour
    ou ferme la fenêtre.
    """
    letters = [chr(ord('A') + i) for i in range(26)]

    win = tk.Toplevel(root)
    win.title("Positions initiales des rotors")
    win.resizable(False, False)
    win.grab_set()

    base_height = 180
    per_rotor = 45
    dynamic_height = base_height + n * per_rotor
    win.minsize(450, dynamic_height)

    win.update_idletasks()
    center_window(win)

    style = ttk.Style(win)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("Menu.TButton", padding=6, font=("Segoe UI", 10))
    style.configure("Return.TButton", padding=6, font=("Segoe UI", 10, "bold"))

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    lbl = ttk.Label(
        frame,
        text="Choisissez la position initiale de chaque rotor :",
        justify="center",
        wraplength=400
    )
    lbl.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    combos = []
    for i in range(n):
        l = ttk.Label(frame, text=f"Rotor {i+1} :")
        l.grid(row=i+1, column=0, padx=10, pady=5, sticky="e")

        combo = ttk.Combobox(frame, values=letters, state="readonly", width=5)
        combo.current(0)
        combo.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
        combos.append(combo)

    result = {"values": None}

    def valider():
        result["values"] = [c.get() for c in combos]
        win.destroy()

    def retour():
        result["values"] = None
        win.destroy()

    def on_close():
        result["values"] = None
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    btn_valider = ttk.Button(frame, text="Valider", style="Menu.TButton", command=valider)
    btn_valider.grid(row=n+1, column=0, pady=(10, 0), padx=5, sticky="e")

    btn_retour = ttk.Button(frame, text="Retour", style="Return.TButton", command=retour)
    btn_retour.grid(row=n+1, column=1, pady=(10, 0), padx=5, sticky="w")

    root.wait_window(win)

    return result["values"]

"""Entrées : 
        title (str) : Titre de la fenêtre
        message (str) : Message à afficher en haut
        options (dict) : Dictionnaire clé->texte des options (ex: {"1": "Option 1", "2": "Option 2"})
        include_back (bool) : Si True, ajoute un bouton Retour
    Sortie : clé choisie (str) ou "R" si Retour, ou None si la fenêtre est fermée
    Affiche une fenêtre avec un message et des boutons pour chaque option"""
def popup_menu(title, message, options, include_back=False):

    win = tk.Toplevel(root)
    win.title(title)
    win.resizable(False, False)
    win.grab_set()

    win.minsize(800, 100)

    win.update_idletasks()
    center_window(win)

    style = ttk.Style(win)
    try: 
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Menu.TButton",
        padding=6,
        font=("Segoe UI", 10)
    )
    style.configure(
        "Return.TButton",
        padding=6,
        font=("Segoe UI", 10, "bold")
    )

    lbl = tk.Label(win, text=message, justify="center", wraplength=400)
    lbl.pack(padx=20, pady=(20, 10))

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    result = {"choice": None}

    # Sous-fonction appelée lors du clic sur un bouton
    def make_choice(k):
        result["choice"] = k
        win.destroy()

    for key, text in options.items():
        btn = ttk.Button(frame, text=text, style="Menu.TButton", command=lambda k=key: make_choice(k))
        btn.pack(fill="x", pady=5)

    if include_back:
        btn_back = ttk.Button(win, text="Retour", style="Return.TButton", command=lambda: make_choice("R"))
        btn_back.pack(pady=(0, 15))

    # Sous-fonction appelée lors de la fermeture de la fenêtre
    def on_close():
        if messagebox.askokcancel("Quitter", "Etes-vous sur de vouloir quitter ?", parent=win):
            result["choice"] = None
            win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_close)

    root.wait_window(win)
    return result["choice"]


def input_dialog(title, message, initial_value: str = "", allow_back: bool = False) -> str | None:
    """
    Affiche une fenêtre centrée avec un texte (message), un champ de saisie, 
    bouton 'Valider', bouton 'Retour' (si allow_back=True)
    Retourne la chaîne saisie, ou None si l'utilisateur clique sur Retour ou ferme la fenêtre.
    """
    win = tk.Toplevel(root)
    win.title(title)
    win.resizable(False, False)
    win.grab_set()

    win.minsize(450, 200)
    win.update_idletasks()
    center_window(win)

    style = ttk.Style(win)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Menu.TButton",
        padding=6,
        font=("Segoe UI", 10)
    )
    style.configure(
        "Return.TButton",
        padding=6,
        font=("Segoe UI", 10, "bold")
    )

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    lbl = ttk.Label(frame, text=message, justify="center", wraplength=400)
    lbl.pack(pady=(0, 10))

    var = tk.StringVar(value=initial_value)
    entry = ttk.Entry(frame, textvariable=var, width=40)
    entry.pack(pady=(0, 15))
    entry.focus_set()

    result = {"text": None}

    def on_ok():
        result["text"] = var.get()
        win.destroy()

    def on_back():
        result["text"] = None
        win.destroy()

    btn_frame = ttk.Frame(frame)
    btn_frame.pack()

    btn_ok = ttk.Button(btn_frame, text="Valider", style="Menu.TButton", command=on_ok)
    btn_ok.grid(row=0, column=0, padx=5)

    if allow_back:
        btn_back = ttk.Button(btn_frame, text="Retour", style="Return.TButton", command=on_back)
        btn_back.grid(row=0, column=1, padx=5)

    win.bind("<Return>", lambda e: on_ok())
    win.bind("<Escape>", lambda e: on_back())

    root.wait_window(win)
    return result["text"]


def afficher_resultat_avec_complexite(mode: str, texte_resultat: str, texte_complexite: str):
    """
    Affiche une fenêtre avec le texte chiffré/déchiffré
    et un bouton pour voir l'évaluation de la complexité.
    """
    win = tk.Toplevel(root)
    win.title("Résultat")
    win.resizable(False, False)
    win.grab_set()

    win.minsize(600, 300)
    win.update_idletasks()
    center_window(win)

    style = ttk.Style(win)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Menu.TButton", padding=6, font=("Segoe UI", 10))
    style.configure("Return.TButton", padding=6, font=("Segoe UI", 10, "bold"))

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    # Titre
    lbl = ttk.Label(
        frame,
        text=f"Texte {mode} :",
        justify="left",
        font=("Segoe UI", 11, "bold")
    )
    lbl.pack(anchor="w", pady=(0, 5))

    # Zone de texte en lecture seule
    txt = tk.Text(frame, height=8, wrap="word")
    txt.insert("1.0", texte_resultat)
    txt.config(state="disabled")
    txt.pack(fill="both", expand=True, pady=(0, 15))

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=(0, 5))

    def voir_complexite():
        messagebox.showinfo(
            "Évaluation de la complexité",
            texte_complexite,
            parent=win
        )

    btn_complex = ttk.Button(
        btn_frame,
        text="Voir l'évaluation de la complexité",
        style="Menu.TButton",
        command=voir_complexite
    )
    btn_complex.grid(row=0, column=0, padx=5)

    btn_close = ttk.Button(
        btn_frame,
        text="Fermer",
        style="Return.TButton",
        command=win.destroy
    )
    btn_close.grid(row=0, column=1, padx=5)

    root.wait_window(win)


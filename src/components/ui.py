import tkinter as tk 
from tkinter import messagebox, simpledialog, ttk

root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale

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

    result = []

    def valider():
        nonlocal result
        result = [c.get() for c in combos]
        win.destroy()

    def on_close():
        result.clear()
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    btn = ttk.Button(frame, text="Valider", style="Menu.TButton", command=valider)
    btn.grid(row=n+1, column=0, columnspan=2, pady=(10, 0))

    root.wait_window(win)

    return result if result else None


def demander_positions_gui(n=3):
    """
    Ouvre une fenêtre adaptée automatiquement au nombre de rotors.
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

    result = []

    def valider():
        nonlocal result
        result = [c.get() for c in combos]
        win.destroy()

    def on_close():
        result.clear()
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    btn = ttk.Button(frame, text="Valider", style="Menu.TButton", command=valider)
    btn.grid(row=n+1, column=0, columnspan=2, pady=(10, 0))

    root.wait_window(win)

    return result if result else None


def popup_menu(title, message, options, include_back=False):
    """
    Affiche une fenêtre avec plusieurs boutons. 
    Retourne la clé de l'option choisie (ex: "1", "2").
    Retourne "R" si le bouton Retour est cliqué.
    """
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

    def make_choice(k):
        result["choice"] = k
        win.destroy()

    for key, text in options.items():
        btn = ttk.Button(frame, text=text, style="Menu.TButton", command=lambda k=key: make_choice(k))
        btn.pack(fill="x", pady=5)

    if include_back:
        btn_back = ttk.Button(win, text="Retour", style="Return.TButton", command=lambda: make_choice("R"))
        btn_back.pack(pady=(0, 15))

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

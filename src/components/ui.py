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
    if rotors_possibles is None:
        rotors_possibles = ["I", "II", "III", "IV", "V"]

    # Fenêtre enfant de root (PAS un nouveau Tk)
    win = tk.Toplevel(root)
    win.title("Choix des rotors")
    win.resizable(False, False)

    # Empêcher l'utilisateur de cliquer ailleurs
    win.grab_set()

    combos = []

    for i in range(n):
        lbl = tk.Label(win, text=f"Rotor {i+1} :")
        lbl.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        combo = ttk.Combobox(win, values=rotors_possibles, state="readonly")
        combo.current(0)
        combo.grid(row=i, column=1, padx=10, pady=5)
        combos.append(combo)

    result = []

    def valider():
        nonlocal result
        result = [c.get() for c in combos]
        win.destroy()  # ferme seulement cette fenêtre

    btn = tk.Button(win, text="OK", command=valider)
    btn.grid(row=n, column=0, columnspan=2, pady=15)

    # Attendre que la fenêtre soit fermée (bloque seulement cette fonction)
    root.wait_window(win)

    # Si l'utilisateur a cliqué sur la croix sans valider → result == []
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
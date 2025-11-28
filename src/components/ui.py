import tkinter as tk 
from tkinter import messagebox, simpledialog, ttk

root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale

def demander_texte(title: str, prompt: str) -> str | None:
    """Demande une chaîne à l'utilisateur via une pop-up."""
    return simpledialog.askstring(title, prompt, parent=root)


# def demander_choix(title: str, prompt: str, choices: list[str]) -> str | None:
#     """
#     Demande un choix parmi une liste (1,2,3...). 
#     Retourne la chaîne choisie ou None si annulé.
#     """
#     texte = prompt + "\n\n" + "\n".join(choices)
#     return simpledialog.askstring(title, texte, parent=root)

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
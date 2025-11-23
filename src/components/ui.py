import tkinter as tk 
from tkinter import messagebox, simpledialog

root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale

def demander_texte(title: str, prompt: str) -> str | None:
    """Demande une chaîne à l'utilisateur via une pop-up."""
    return simpledialog.askstring(title, prompt, parent=root)


def demander_choix(title: str, prompt: str, choices: list[str]) -> str | None:
    """
    Demande un choix parmi une liste (1,2,3...). 
    Retourne la chaîne choisie ou None si annulé.
    """
    texte = prompt + "\n\n" + "\n".join(choices)
    return simpledialog.askstring(title, texte, parent=root)

def show_info(title: str, message: str):
    messagebox.showinfo(title, message, parent=root)


def show_error(title: str, message: str):
    messagebox.showerror(title, message, parent=root)
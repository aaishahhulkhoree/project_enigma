from configuration.configuration import ROTORS
from utils.nettoyage import assertionError
from dataclasses import dataclass

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A_IDX = {c: i for i, c in enumerate(ALPHABET)}


def _mod26(x: int) -> int:
    return x % 26

@dataclass
class Rotor:
    name: str
    wiring: str         # 26 lettres e.g. "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    notch: str          # lettre de cran e.g. "Q"
    position: int = 0   # 0..25 (A=0, B=1, ...)
    ring_setting: int = 0  # 0..25 (Ringstellung ; A=0)

    def __post_init__(self) -> None:
        self.wiring = self.wiring.upper()
        if len(self.wiring) != 26:
            assertionError("Le wiring du rotor doit comporter 26 lettres.")
        self.notch = self.notch.upper()
        if len(self.notch) != 1 or self.notch not in ALPHABET:
            assertionError("Le notch doit être une lettre A–Z.")
        self.position = _mod26(self.position)
        self.ring_setting = _mod26(self.ring_setting)

        # Pré-calcul des mappings indexés
        self.forward = [A_IDX[c] for c in self.wiring]                 # entrée -> sortie (index)
        # reverse: pour chaque sortie, où est l'entrée
        self.reverse = [0] * 26
        for i, out_idx in enumerate(self.forward):
            self.reverse[out_idx] = i

    # --- mécanique ---
    @property
    def at_notch(self) -> bool:
        """Vrai si le rotor est sur sa/son (ses) cran(s)."""
        return self.position == A_IDX[self.notch]

    def step(self) -> None:
        """Fait tourner le rotor d'une position (A->B)."""
        self.position = _mod26(self.position + 1)

    # --- signal ---
    def map_forward(self, idx: int) -> int:
        """Passage aller (gauche <- droite) avec offset de position et ring setting."""
        # appliquer le décalage (position - ring)
        shifted = _mod26(idx + self.position - self.ring_setting)
        wired = self.forward[shifted]
        # revenir au repère original
        out = _mod26(wired - self.position + self.ring_setting)
        return out

    def map_reverse(self, idx: int) -> int:
        """Passage retour (droite -> gauche)."""
        shifted = _mod26(idx + self.position - self.ring_setting)
        wired = self.reverse[shifted]
        out = _mod26(wired - self.position + self.ring_setting)
        return out


def create_rotor(name: str, position: str = "A", ring_setting: int = 0) -> Rotor:
    """Crée un rotor depuis son nom ('I'..'V'), position lettre (ex: 'D') et ring_setting (0..25)."""
    name = name.upper()
    if name not in ROTORS:
        assertionError(f"Rotor inconnu: {name!r}. Choisir parmi: {', '.join(ROTORS)}")
    wiring, notch = ROTORS[name]
    pos_idx = A_IDX.get(position.upper(), None)
    if pos_idx is None:
        assertionError("La position doit être une lettre A–Z.")
    return Rotor(name=name, wiring=wiring, notch=notch, position=pos_idx, ring_setting=ring_setting)


def step_triple_rotors(r1: Rotor, r2: Rotor, r3: Rotor) -> None:
    """Double-stepping simplifié (M3) :
    - r1 (droite) tourne à chaque frappe,
    - r2 avance si r1 est sur son notch,
    - r3 avance si r2 est sur son notch (double-step quand r1 arrive au notch de r2).
    """
    # double step: si le rotor milieu est au notch, il avancera lui-même ET fera avancer le gauche
    middle_will_step = r2.at_notch
    right_will_step = True  # le plus à droite avance toujours

    if right_will_step:
        r1.step()
    if middle_will_step:
        r2.step()
        r3.step()
    else:
        # avance le milieu si le droit vient d'atteindre son notch
        if r1.at_notch:
            r2.step()

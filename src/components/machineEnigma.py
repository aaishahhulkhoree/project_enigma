from typing import List

from components.plugboard import Plugboard
from components.reflecteur import Reflecteur
from components.rotors import create_rotor, Rotor
from configuration.configuration import ALPHABET
from utils.formatage import only_letters, group5

A_IDX = {c: i for i, c in enumerate(ALPHABET)}
IDX_A = {i: c for c, i in A_IDX.items()}


class MachineEnigma:
    def __init__(
        self,
        rotors_names: List[str],
        positions: str,
        plug_pairs: List[str] | None = None,
        reflector_preset: str = "B",
        ring_settings: List[int] | None = None,
    ) -> None:
        """
        rotors_names: ["LEFT", "MIDDLE", "RIGHT"]
        positions:    "LMR" (ex: "DCA")
        ring_settings: [L, M, R] en 0..25 (par défaut [0,0,0])
        """
        if len(rotors_names) != 3:
            raise ValueError("Il faut exactement 3 rotors: [LEFT, MIDDLE, RIGHT].")
        if len(positions) != 3:
            raise ValueError("positions doit être une chaîne de 3 lettres (LEFT,MIDDLE,RIGHT).")

        self.left_name, self.mid_name, self.right_name = [x.upper() for x in rotors_names]
        L_pos, M_pos, R_pos = positions.upper()

        ring_settings = ring_settings or [0, 0, 0]
        if len(ring_settings) != 3:
            raise ValueError("ring_settings doit être de longueur 3 (LEFT,MIDDLE,RIGHT).")

        # Composants
        self.plugboard = Plugboard(plug_pairs or [])
        self.reflector = Reflecteur(preset=reflector_preset)

        # Rotors (instanciés gauche→milieu→droite)
        self.left: Rotor = create_rotor(self.left_name, position=L_pos, ring_setting=ring_settings[0])
        self.middle: Rotor = create_rotor(self.mid_name, position=M_pos, ring_setting=ring_settings[1])
        self.right: Rotor = create_rotor(self.right_name, position=R_pos, ring_setting=ring_settings[2])

    # ---------------- Stepping (double-step correct) ----------------
    def _step_rotors(self) -> None:
        """
        Règle M3:
        - Right avance à chaque frappe.
        - Middle avance si Right est au notch OU si Middle est au notch.
        - Left avance si Middle est au notch (double-stepping).
        """
        advance_left = self.middle.at_notch
        advance_middle = self.right.at_notch or self.middle.at_notch

        # ordre de mouvement : Right, puis Middle (si), puis Left (si)
        self.right.step()
        if advance_middle:
            self.middle.step()
        if advance_left:
            self.left.step()

    # ---------------- Chiffrement d'une lettre ----------------
    def _enc_idx(self, idx: int) -> int:
        # Aller
        idx = self.right.map_forward(idx)
        idx = self.middle.map_forward(idx)
        idx = self.left.map_forward(idx)

        # Réflecteur
        ch = IDX_A[idx]
        ch_ref = self.reflector.allumer_lettre(ch)
        idx = A_IDX[ch_ref]

        # Retour
        idx = self.left.map_reverse(idx)
        idx = self.middle.map_reverse(idx)
        idx = self.right.map_reverse(idx)

        return idx

    def encrypt_char(self, ch: str) -> str:
        """Chiffre un caractère. Non-A–Z renvoyé tel quel (pratique pour garder espaces/ponctuation si souhaité)."""
        if ch.upper() not in ALPHABET:
            return ch
        self._step_rotors()  # la machine step AVANT le trajet
        # Plugboard IN
        x = self.plugboard.permuter(ch)
        idx = A_IDX[x.upper()]

        # Rotors + Reflecteur + Rotors
        idx_out = self._enc_idx(idx)
        y = IDX_A[idx_out]

        # Plugboard OUT
        y2 = self.plugboard.permuter(y)
        return y2

    def encrypt(self, text: str, keep_spaces: bool = False, group_5: bool = False) -> str:
        """
        Chiffre un texte.
        - keep_spaces: si False, on nettoie en A–Z uniquement ; sinon, on garde les espaces.
        - group_5: regroupe la sortie en blocs de 5.
        """
        if keep_spaces:
            # On enlève tout sauf A–Z et espaces, mais la machine ignore les espaces dans le stepping:
            clean = "".join(c if c == " " or c.upper() in ALPHABET else "" for c in text.upper())
        else:
            clean = only_letters(text, keep_spaces=False)

        out = []
        for ch in clean:
            if ch == " ":
                out.append(" ")  # n'affecte pas les rotors (choix pédagogique)
                continue
            out.append(self.encrypt_char(ch))

        cipher = "".join(out)
        if group_5:
            return group5(cipher.replace(" ", ""))
        return cipher

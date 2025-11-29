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
        rotors_names: liste de nom de rotors, de gauche à droite 
                        ex: ["I", "II", "III"] pour 3 rotors
                        ex : ["I", "II", "IV", "V"] pour 4 rotors ...
        positions:    chaine des positions initiales, meme longueur que rotor_names attention
        ring_settings: liste des ring settings(0-25) pour chaque rotor, meme longueur que rotor_names
        """
        n = len(rotors_names)
        if n < 3 or n > 8:
            raise ValueError("Le nombre de rotors doit être entre 3 et 8.")
        if len(positions) != n:
            raise ValueError("positions doit être une chaîne de 3 lettres (LEFT,MIDDLE,RIGHT).")

        if ring_settings is None:
            ring_settings = [0] * n  # par défaut, tous à 0
        if len(ring_settings) != n:
            raise ValueError("ring_settings doit être une liste de même longueur que rotors_names.")

        # Composants
        self.plugboard = Plugboard(plug_pairs or [])
        self.reflector = Reflecteur(preset=reflector_preset)

        # Rotors : liste de gauche -> droite
        self.rotor_names = [name.upper() for name in rotors_names]
        self.rotors: List[Rotor] = []
        for name, pos_letter, ring in zip(self.rotor_names, positions, ring_settings):
            self.rotors.append(create_rotor(name, position=pos_letter, ring_setting=ring))

    # ---------------- Stepping (double-step correct) ----------------
    def _step_rotors(self) -> None:
        """ Règle:
        -Le rotor le plus à droite avance à chaque frappe
        -Tout rotor qui est sur son cran (at_notch) avance
        -Le rotor immédiatement à gauche d'un rotor sur son cran avance aussi
          (double-stepping)
        Cela reproduit le comportement classique à 3 rotors, et l'étend
        naturellement pour 4..8 rotors
        """
        n = len(self.rotors)
        will_step = [False] * n

        # Le rotor le plus à droite avance toujours
        will_step[-1] = True

        # Double-step
        for i in range(n - 1, -1, -1):
            if self.rotors[i].at_notch:
                will_step[i] = True
                if i > 0:
                    will_step[i - 1] = True

        for i, rotor in enumerate(self.rotors):
            if will_step[i]:
                rotor.step()

    # ---------------- Chiffrement d'un index ----------------
    def _enc_idx(self, idx: int) -> int:
        # Aller : du rotor le plus à droite vers le plus à gauche
        for rotor in reversed(self.rotors):
            idx = rotor.map_forward(idx)

        # Réflecteur
        ch = IDX_A[idx]
        ch_ref = self.reflector.allumer_lettre(ch)
        idx = A_IDX[ch_ref]

        # Retour : du rotor le plus à gauche vers le plus à droite
        for rotor in self.rotors:
            idx = rotor.map_reverse(idx)

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
                out.append(" ")  # n'affecte pas les rotors, pour m'aider à la lisibilité...
                continue
            out.append(self.encrypt_char(ch))

        cipher = "".join(out)
        if group_5:
            return group5(cipher.replace(" ", ""))
        return cipher

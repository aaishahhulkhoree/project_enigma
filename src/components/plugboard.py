from utils import assertionError

"""Classe Plugboard pour gérer les connexions du plugboard."""

class Plugboard:

    def __init__(self, paires=None):
        self.plugboard = {}

        if paires:
            self.configurer(paires)


    def configurer(self, paires):
        """List(str) paires: Liste de paires de lettres à connecter."""
        if len(paires) > 10:
            assertionError("Le plugboard ne peut pas avoir plus de 10 paires de connexions.")
        
        lettres_utilisees = set()

        for paire in paires:
            if len(paire) !=2 :
                assertionError(f"La paire '{paire}' doit contenir exactement deux lettres.")
            
            a, b = paire[0], paire[1]

            if a in lettres_utilisees or b in lettres_utilisees:
                assertionError(f"Les lettres '{a}' et '{b}' ne peuvent pas être utilisées dans plusieurs paires.")

            self.plugboard[a] = b
            self.plugboard[b] = a

    
    def is_connected(self, lettre):
        """Str : retourne True si la lettre est connectée dans le plugboard, sinon False."""
        return lettre in self.plugboard


    def permuter(self, lettre):
        """ Str : permute une lettre via le plugboard si connectée, sinon retourne la lettre inchangée."""
        if lettre.isconnected():
            return self.plugboard[lettre]
        return lettre
    

    def afficher(self):
        """Affiche les connexions du plugboard."""
        if not self.plugboard:
            print("Plugboard non configuré.")
            return
        
        connexions = []
        deja_affiche = set()

        for a, b in self.plugboard.items():
            if a not in deja_affiche and b not in deja_affiche:
                connexions.append(f"{a} <-> {b}")
                deja_affiche.add(a)
                deja_affiche.add(b)

        print("Connexions du Plugboard :")
        for connexion in connexions:
            print(connexion)

    
    def reset(self):
        """Réinitialise le plugboard en supprimant toutes les connexions."""
        self.plugboard.clear()
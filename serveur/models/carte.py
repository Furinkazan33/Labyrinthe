# -*-coding:Utf-8 -*

""" Ce fichier contient la classe Carte.

"""

class Carte:
    """ Classe représentant une carte sous forme d'une chaîne de caractères."""

    nom = ""
    chaine = ""
    content = []

    def _strToLab (self, chaine):
        """ Convertit une chaîne en carte (liste de liste)."""
        c = i = j = 0
        ligne = []
        lab = []

        while c < len(chaine):
            if chaine[c] == '\r':
                pass
            elif chaine[c] == '\n':
                lab.append(ligne)
                ligne = []
                j+=1
                i=0
            else:
                ligne.append(chaine[c])
                i+=1
            c+=1

        if ligne != []:
            lab.append(ligne)

        #print(lab)

        return lab

    def __init__(self, nom, chaine):
        self.nom = nom
        self.chaine = chaine
        self.content = self._strToLab(chaine)

    def to_dic(self):
        return {'nom': self.nom, 'chaine': self.chaine, 'content': self.content}

    def __repr__(self):
        """Retourne le labyrinthe (carte) sous forme de chaîne."""
        return str(self.to_dic())

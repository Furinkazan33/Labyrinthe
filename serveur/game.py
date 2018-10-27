#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu - classe Game.
Il est utilisé par le serveur."""

import os
import sys
import const
from models import *

class Game():

    maps = []
    labyrinthe = None

    def __init__(self):
        # On charge les cartes existantes
        for nom_fichier in os.listdir(const.MAPS_FOLDER):
            if nom_fichier.endswith(".txt"):
                chemin = os.path.join(const.MAPS_FOLDER, nom_fichier)
                nom_carte = nom_fichier[:-4].lower()

                with open(chemin, "r") as fichier:
                    chaine = fichier.read()
                    self.maps.append((nom_carte, chaine))

        self.labyrinthe = Labyrinthe()

    def get_maps (self):
        """ Retourne une chaîne contenant la liste des cartes.
            \"  {indice} - {repr(carte)}\"
        """

        affichage = ""

        for i, (nom_carte, chaine) in enumerate(self.maps):
            affichage += "  {} - {}\n".format(i + 1, nom_carte)
            affichage += chaine

        return affichage

    def set_map(self, n):
        (nom_carte, chaine) = self.maps[n-1]
        self.labyrinthe.set_carte(nom_carte, chaine)

    # Boucle principale d'affichage du labyrinthe
    def move(self, name, direction, occurence):
        # Déplacement du robot
        (name, returncode, x, y) = self.labyrinthe.move(name, direction, occurence)

        return (name, returncode, x, y)

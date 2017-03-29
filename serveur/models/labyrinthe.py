# -*-coding:Utf-8 -*

""" Ce fichier contient la classe Labyrinthe.

"""
import const
from .robot import Robot
from .carte import Carte

class Labyrinthe:
    """ Classe représentant un labyrinthe. Un labyrinthe est définit par une carte et un robot"""
    robots = {}
    carte = None

    def set_carte(self, nom, chaine):
        self.carte = Carte(nom, chaine)

    def get_carte(self):
        return self.carte

    def add_robot (self, name):
        self.robots[name] = Robot(name)

    def get_robot (self, name):
        return self.robots[name]

    def get_robots(self):
        return self.robots


    def move (self, name, direction, occurence):
        """ Bouge le robot si pas d'obstacle."""

        if direction == const.CHAR_UP:
            dx = 0
            dy = -1
        elif direction == const.CHAR_DOWN:
            dx = 0
            dy = 1
        elif direction == const.CHAR_LEFT:
            dx = -1
            dy = 0
        elif direction == const.CHAR_RIGHT:
            dx = 1
            dy = 0
        else:
            dx = 0
            dy = 0

        while occurence > 0:
            x = self.robots[name].posX + dx
            y = self.robots[name].posY + dy

            if self.carte.content[y][x] == const.CHAR_EXIT:
                self.robots[name].posX = x
                self.robots[name].posY = y
                return (name, const.RC_LAB_MOVE_ENDGAME, self.robots[name].posX, self.robots[name].posY)

            elif self.carte.content[y][x] == const.CHAR_OBSTACLE:
                return (name, const.RC_LAB_MOVE_OBSTACLE, self.robots[name].posX, self.robots[name].posY)

            elif self.carte.content[y][x] != const.CHAR_OBSTACLE:
                self.robots[name].posX = x
                self.robots[name].posY = y
                occurence -= 1

        return (name, const.RC_LAB_MOVE_FREE, self.robots[name].posX, self.robots[name].posY)


    def to_dic(self):
        """Retourne le labyrinthe (carte) sous forme de dictionnaire.
        """
        robots = {}
        for name, robot in self.robots.items():
            robots[name] = robot.to_dic()
        return {'carte': self.carte.to_dic(), 'robots': robots}

    def __repr__(self):
        """Retourne le labyrinthe (carte) sous forme de chaîne.
        """
        return str(self.to_dic())

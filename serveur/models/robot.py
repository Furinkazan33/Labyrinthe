# -*-coding:Utf-8 -*

""" Ce fichier contient la classe Robot.

"""
#import const

class Robot:
    """ Classe représentant un Robot."""
    #status = None
    name = ""
    posX = 1
    posY = 1

    def __init__(self, name):
        #self.status = const.PLAYER_CONNECTED
        self.name = name

    # def disconnect(self):
    #     self.status = const.PLAYER_DISCONNECTED


    def to_dic(self):
        """ Retourne le robot sous forme de dictionnaire.
            {'name': self.name, 'posX': self.posX, 'posY': self.posY}
        """
        return {'name': self.name, 'posX': self.posX, 'posY': self.posY}

    def __repr__(self):
        """ Retourne le robot sous forme de chaîne.
            {'name': {name} 'posX': {posX}, 'posY': {posY}}
        """
        return str(self.to_dic())

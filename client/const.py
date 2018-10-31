# -*-coding:Utf-8 -*

"""
    Ce fichier contient les constantes du jeu.
"""
##################################################
# Diverses constantes
##################################################
PROMPT = "  >>"

##################################################
# Les différents types de messages échangés
##################################################
SOCKET_CLIENT_NAME = "SOCKET_CLIENT_NAME"
SOCKET_CLIENT_DISCONNECT = "SOCKET_CLIENT_DISCONNECT"
SOCKET_CLIENT_MOVE = "SOCKET_CLIENT_MOVE"

SOCKET_SERVER_ASK_NAME = "SOCKET_SERVER_ASK_NAME"
SOCKET_SERVER_ASK_DISCONNECT = "SOCKET_SERVER_ASK_DISCONNECT"
SOCKET_SERVER_ASK_MOVE = "SOCKET_SERVER_ASK_MOVE"
SOCKET_SERVER_MESSAGE = "SOCKET_SERVER_MESSAGE"

SOCKET_SERVER_ANSWER_NAME = "SOCKET_SERVER_ANSWER_NAME"
SOCKET_SERVER_ANSWER_DISCONNECT = "SOCKET_SERVER_ANSWER_DISCONNECT"
SOCKET_SERVER_ANSWER_MOVE = "SOCKET_SERVER_ANSWER_MOVE"

##################################################
# Messages affichés
##################################################
STRING_LOAD = "Charger partie"
STRING_NEW = "Nouvelle partie"
STRING_BYE = "Au revoir !"
STRING_FREE = "On se balade"
STRING_OUCH = "Ouch !"
STRING_CONGRATS = "Félicitations ! Vous avez gagné !"

##################################################
# Status possibles des joueurs
##################################################
PLAYER_DISCONNECTED = 0
PLAYER_CONNECTED = 1

##################################################
# Saisies possibles du joueur
##################################################
CHAR_QUIT = 'q'
CHAR_UP = 'n'
CHAR_DOWN = 's'
CHAR_LEFT = 'o'
CHAR_RIGHT = 'e'

##################################################
# Les symboles du labyrinthe
##################################################
CHAR_OBSTACLE = 'O'
CHAR_EXIT = 'U'
CHAR_ROBOT = 'X'
# TODO: à utiliser ?
CHAR_DOOR = '.'

##################################################
# Codes retours
##################################################
# De la classe Labyrinthe, fonction move
RC_LAB_MOVE_FREE = 0
RC_LAB_MOVE_OBSTACLE = 1
RC_LAB_MOVE_ENDGAME = 2

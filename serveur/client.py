# -*-coding:Utf-8 -*

""" Ce fichier contient la classe Client.

"""
import socket
import json
import sys

class Client:
    _socket = None
    _name = ""
    _id = None

    def __init__(self, socket):
        self._socket = socket
        self._id = socket.fileno()

    def set_name(self, name):
        self._name = name

    def get_socket(self):
        return self._socket

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def disconnect(self):
        self._socket.close()
        del(self._socket)

    def send (self, m_type, infos, message):
        dictionnaire = {'type': m_type, 'infos': infos, 'message': message}
        msg = json.dumps(dictionnaire)
        msg_a_envoyer = msg.encode()

        print("Envoyé {}".format(msg_a_envoyer), file=sys.stdout)

        self._socket.send(msg_a_envoyer)

    def get (self):
        msg_recu = self._socket.recv(1024)
        # Peut planter si le message contient des caractères spéciaux
        dictionnaire = json.loads(msg_recu.decode())

        print("Reçu {}".format(dictionnaire), file=sys.stdout)

        return dictionnaire

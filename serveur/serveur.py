#!/usr/bin/python3
# -*-coding:utf-8 -*

"""module multipli contenant la fonction table"""

class Client():
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


if __name__ == "__main__":
    import const
    import socket
    import json
    import select
    import sys
    #import modules.th_read
    from game import Game

    #sys.stdout = open('write2game', 'w')
    #sys.stdin = open('write2server', 'r')

    #fd = open('write2server', 'r')
    #th_read = modules.th_read.ReadFromPipe(fd)
    #th_read.run()

    game = Game()

    hote = ''
    port = 12800

    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(port), file=sys.stdout)

    serveur_lance = True
    connexions_demandees = []
    clients_connectes = []

    while serveur_lance:
        # Gestion des nouvelles connexions
        # On attend 50ms maximum
        connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)

        for connexion in connexions_demandees:
            socket, infos = connexion.accept()
            #print("socket:", socket) #print("infos:", infos)

            # Ajout du client à la liste
            client = Client(socket)
            clients_connectes.append(client)

            # Demande le nom du joueur connecté
            client.send(const.SOCKET_SERVER_ASK_NAME, {}, "Votre nom:")

        # On attend 50ms maximum
        # Si la liste de clients connectés est vide, une exception peut être levée
        #TODO: est-il possible de récupérer directement les clients à lire ?
        sockets_a_lire = []
        clients_a_lire = []
        try:
            sockets = [client.get_socket() for client in clients_connectes]
            sockets_a_lire, wlist, xlist = select.select(sockets, [], [], 0.05)

            for socket in sockets_a_lire:
                for client in clients_connectes:
                    if client.get_socket()==socket:
                        clients_a_lire.append(client)

        except select.error:
            pass
        else:
            for client in clients_a_lire:
                #print("Client:", client)
                #print(client.fileno())

                ##################################
                # Les réponses du client
                ##################################
                reponse = client.get()

                if reponse["type"] == const.SOCKET_CLIENT_NAME:
                    name = reponse["infos"]
                    client.set_name(name)
                    client.send(const.SOCKET_SERVER_ANSWER_NAME, {}, "Bienvenue " + name)
                    client.send(const.SOCKET_SERVER_ASK_CHOOSE_MAP, "Veuillez choisir une carte", game.get_maps())

                elif reponse["type"] == const.SOCKET_CLIENT_CHOOSE_MAP:
                    #client.send(const.SOCKET_SERVER_ANSWER_CHOOSE_MAP, {}, "Vous avez choisi " + reponse["infos"])
                    #TODO: cela écrase le choix du précédent joueur
                    game.set_map(int(reponse["infos"]))
                    game.labyrinthe.add_robot(client.get_name())

                    client.send(const.SOCKET_SERVER_ASK_MOVE, game.labyrinthe.to_dic(), "")

                elif reponse["type"] == const.SOCKET_CLIENT_MOVE:
                    (direction, occurence) = reponse["infos"]
                    (name, returncode, x, y) = game.move(client.get_name(), direction, int(occurence))

                    if returncode == const.RC_LAB_MOVE_ENDGAME:
                        client.send(const.SOCKET_SERVER_ASK_DISCONNECT, game.labyrinthe.to_dic(), const.STRING_CONGRATS)
                    #     exit(0)

                    # On s'est prit un mur !
                    elif returncode == const.RC_LAB_MOVE_OBSTACLE:
                        client.send(const.SOCKET_SERVER_ANSWER_MOVE, game.labyrinthe.to_dic(), const.STRING_OUCH)

                    # Pas d'obstacle rencontré
                    elif returncode == const.RC_LAB_MOVE_FREE:
                        client.send(const.SOCKET_SERVER_ANSWER_MOVE, game.labyrinthe.to_dic(), const.STRING_FREE)

                elif reponse["type"] == const.SOCKET_CLIENT_DISCONNECT:
                    print("Le client", client.get_name(), "nous a quitté")
                    client.send(const.SOCKET_SERVER_ANSWER_DISCONNECT, {}, "Au revoir")
                    clients_a_lire.remove(client)
                    clients_connectes.remove(client)
                    client.disconnect()
                    del(client)

                    if not clients_connectes:
                        serveur_lance = False

    print("Fermeture des connexions", file=sys.stdout)
    for client in clients_connectes:
        client.disconnect()

    connexion_principale.close()
    exit(0)

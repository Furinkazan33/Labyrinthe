#!/usr/bin/python3
# -*-coding:utf-8 -*

"""module multipli contenant la fonction table"""

if __name__ == "__main__":
    import sys
    import socket
    import json
    import const

    hote = "localhost"
    port = 12800
    name = ""

    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur.connect((hote, port))
    print("Connexion établie avec le serveur {} sur le port {}".format(hote, port))

    def send (m_type, infos):
        dictionnaire = {'type': m_type, 'infos': infos}
        msg = json.dumps(dictionnaire)
        msg_a_envoyer = msg.encode()

        print("Envoyé {}".format(msg_a_envoyer), file=sys.stdout)

        connexion_avec_serveur.send(msg_a_envoyer)

    def get ():
        msg_recu = connexion_avec_serveur.recv(1024)
        dictionnaire = json.loads(msg_recu.decode())

        print("Reçu {}".format(dictionnaire), file=sys.stdout)

        return dictionnaire

    def close():
        print("Fermeture de la connexion")
        #connexion_avec_serveur.close()
        exit(0)

    def is_robot(robots, x, y):
        for name, robot in robots.items():
            if robot["posX"]==x and robot["posY"]==y:
                return True
        return False

    def chaine_robot(chaine, robots):
        """Retourne le labyrinthe sous forme de chaîne avec les robots."""
        client_robot = robots.pop(name)

        lab = ""
        i = 0
        l = c = 0
        while i < len(chaine):
            if chaine[i] == '\n':
                lab += '\n'
                c = -1
                l += 1
            elif client_robot["posX"]==c and client_robot["posY"]==l:
                lab += 'X'
            elif is_robot(robots, c, l):
                lab += 'x'
            else:
                lab += chaine[i]
            c += 1
            i += 1

        return lab


    reponse = {'type': None, 'infos': None, 'message': ""}
    while reponse["type"] != const.SOCKET_SERVER_ASK_DISCONNECT and reponse["type"] != const.SOCKET_SERVER_ANSWER_DISCONNECT:
        reponse = get()
        #
        # Les questions du serveur
        #
        if reponse["type"] == const.SOCKET_SERVER_ASK_DISCONNECT:
            print(reponse["message"])

        elif reponse["type"] == const.SOCKET_SERVER_ASK_NAME:
            print(reponse["message"])
            name = input(const.PROMPT)
            send(const.SOCKET_CLIENT_NAME, name)

        elif reponse["type"] == const.SOCKET_SERVER_ASK_CHOOSE_MAP:
            print(reponse["message"])
            print(reponse["infos"])
            choix = input(const.PROMPT)
            send(const.SOCKET_CLIENT_CHOOSE_MAP, choix)

        elif reponse["type"] == const.SOCKET_SERVER_ASK_MOVE or reponse["type"] == const.SOCKET_SERVER_ANSWER_MOVE:
            print(chaine_robot(reponse["infos"]["carte"]["chaine"], reponse["infos"]["robots"]))
            print(reponse["message"])

            # Commande joueur, le premier caractère est la direction, le second le nombre de déplacement
            saisie = ""
            while len(saisie) != 1 and len(saisie) != 2:
                saisie = input(const.PROMPT)

            if (saisie[0] == const.CHAR_QUIT):
                send(const.SOCKET_CLIENT_DISCONNECT, "Je me casse")

            else:
                direction = saisie[0]

                if len(saisie) == 1:
                    occurence = "1"
                else:
                    occurence = saisie[1]

                send(const.SOCKET_CLIENT_MOVE, direction+occurence)

        #
        # Les réponses du serveur
        #
        elif reponse["type"] == const.SOCKET_SERVER_ANSWER_NAME:
            print(reponse["message"])

        elif reponse["type"] == const.SOCKET_SERVER_ANSWER_CHOOSE_MAP:
            print(reponse["message"])

        elif reponse["type"] == const.SOCKET_SERVER_ANSWER_MOVE:
            print(reponse["message"])

        elif reponse["type"] == const.SOCKET_SERVER_ANSWER_DISCONNECT:
            print(reponse["message"])


    close()

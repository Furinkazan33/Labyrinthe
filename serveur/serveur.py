#!/usr/bin/python3
# -*-coding:utf-8 -*

"""Fichier a exécuter pour lancer le serveur"""

if __name__ == "__main__":
    import const
    import socket
    import select
    import sys
    from client import Client
    from game import Game

    # On créer la partie
    game = Game()

    # Choix de la carte
    print("Labyrinthes existants :\n", game.get_maps())
    choix = input("Entrez un numéro de labyrinthe pour commencer à jouer : ")
    game.set_map(int(choix))

    hote = ''
    port = 12800

    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    #print("Le serveur écoute à présent sur le port {}".format(port), file=sys.stdout)
    print("On attend les clients.")

    serveur_lance = True
    connexions_demandees = []
    clients_connectes = []

    while serveur_lance:
        # Gestion des nouvelles connexions
        # On attend 50ms maximum
        connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)

        for connexion in connexions_demandees:
            socket, infos = connexion.accept()
            
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
                ##################################
                # Les réponses du client
                ##################################
                reponse = client.get()

                if reponse["type"] == const.SOCKET_CLIENT_NAME:
                    name = reponse["infos"]
                    client.set_name(name)
                    game.labyrinthe.add_robot(name)
                    client.send(const.SOCKET_SERVER_MESSAGE, {}, "Bienvenue " + name)
                    client.send_others(clients_connectes, const.SOCKET_SERVER_MESSAGE, {}, name + " vient de se connecter.")

                elif reponse["type"] == const.SOCKET_CLIENT_MOVE:
                    (direction, occurence) = reponse["infos"]
                    (name, returncode, x, y) = game.move(client.get_name(), direction, int(occurence))

                    if returncode == const.RC_LAB_MOVE_ENDGAME:
                        client.send(const.SOCKET_SERVER_ASK_DISCONNECT, game.labyrinthe.to_dic(), const.STRING_CONGRATS)
                        client.send_others(clients_connectes, const.SOCKET_SERVER_ASK_DISCONNECT, game.labyrinthe.to_dic(), client.get_name() + " a gagné !")
                    #     exit(0)

                    # On s'est prit un mur !
                    elif returncode == const.RC_LAB_MOVE_OBSTACLE:
                        client.send(const.SOCKET_SERVER_ANSWER_MOVE, game.labyrinthe.to_dic(), const.STRING_OUCH)

                    # Pas d'obstacle rencontré
                    elif returncode == const.RC_LAB_MOVE_FREE:
                        client.send(const.SOCKET_SERVER_ANSWER_MOVE, game.labyrinthe.to_dic(), const.STRING_FREE)

                elif reponse["type"] == const.SOCKET_CLIENT_DISCONNECT:
                    print("Le client", client.get_name(), "nous a quitté")
                    client.send(const.SOCKET_SERVER_ANSWER_DISCONNECT, {}, "Au revoir "+client.get_name())
                    client.send_others(clients_connectes, const.SOCKET_SERVER_MESSAGE, {}, client.get_name() + " nous a quitté.")
                    clients_a_lire.remove(client)
                    clients_connectes.remove(client)
                    client.disconnect()
                    del(client)

                    if not clients_connectes:
                        serveur_lance = False

                if client.ready():
                    current = clients_connectes.pop()
                    clients_connectes.insert(0, current)
                    current.send(const.SOCKET_SERVER_ASK_MOVE, game.labyrinthe.to_dic(), "")

    print("Fermeture des connexions", file=sys.stdout)
    for client in clients_connectes:
        client.disconnect()

    connexion_principale.close()
    exit(0)

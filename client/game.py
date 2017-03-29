

class Game():
    self.grille = None
    self.robots = []

    

    def __repr__(self):
        """ Retourne le labyrinthe (grille + robots) sous forme de chaîne."""

        lab = ""
        l = c = 0
        while l < len(self.grille):
            while c < len(self.grille[0]):
                if l == self.robot.posY and c == self.robot.posX:
                    lab += const.CHAR_ROBOT
                else:
                    lab += self.grille[l][c]
                c+=1
            lab += '\n'
            c=0
            l+=1

        return lab

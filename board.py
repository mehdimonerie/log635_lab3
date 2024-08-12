import keyboard

class Board:
    def __init__(self, game_data):
        self.pieces = game_data["pieces"]
        self.personnages = game_data["personnages"]
        self.armes = game_data["armes"]
        self.position_actuelle = 0  # Index de la pièce actuelle dans la liste
        self.largeur = 3  # Supposons que les pièces sont organisées en grille 3x2 (ajustable selon vos besoins)

    def afficher_position(self):
        print(f"Vous êtes actuellement dans {self.pieces[self.position_actuelle]}.")

    def deplacer_haut(self):
        if self.position_actuelle >= self.largeur:
            self.position_actuelle -= self.largeur
            self.afficher_position()

    def deplacer_bas(self):
        if self.position_actuelle < len(self.pieces) - self.largeur:
            self.position_actuelle += self.largeur
            self.afficher_position()

    def deplacer_gauche(self):
        if self.position_actuelle % self.largeur > 0:
            self.position_actuelle -= 1
            self.afficher_position()

    def deplacer_droite(self):
        if self.position_actuelle % self.largeur < self.largeur - 1:
            self.position_actuelle += 1
            self.afficher_position()

    def deplacer_agent(self):
        self.afficher_position()
        print("Utilisez les touches directionnelles pour vous déplacer. Appuyez sur 'q' pour quitter.")

        while True:
            if keyboard.is_pressed('up'):
                self.deplacer_haut()
            elif keyboard.is_pressed('down'):
                self.deplacer_bas()
            elif keyboard.is_pressed('left'):
                self.deplacer_gauche()
            elif keyboard.is_pressed('right'):
                self.deplacer_droite()
            elif keyboard.is_pressed('q'):
                print("Vous avez quitté le déplacement.")
                break

import json

class Board:
    def __init__(self, game_data):
        self.pieces = game_data["pieces"]  # Utilisez la clé "pieces" du JSON
        self.position_actuelle = game_data["salle_depart"]  # Commencer dans la pièce de départ
        self.personnages = {piece: data["personnage"] for piece, data in self.pieces.items()}  # Associez personnages aux pièces
        self.armes = {piece: data["arme"] for piece, data in self.pieces.items()}  # Associez armes aux pièces

    def afficher_position(self):
        print(f"Vous êtes actuellement dans {self.position_actuelle}. Il y a {self.personnages[self.position_actuelle]} et {self.armes[self.position_actuelle]}.")

    def deplacer_haut(self):
        piece_actuelle = self.pieces[self.position_actuelle]
        if piece_actuelle["nord"]:
            self.position_actuelle = piece_actuelle["nord"]
            self.afficher_position()
        else:
            print("Vous ne pouvez pas vous déplacer au nord.")

    def deplacer_bas(self):
        piece_actuelle = self.pieces[self.position_actuelle]
        if piece_actuelle["sud"]:
            self.position_actuelle = piece_actuelle["sud"]
            self.afficher_position()
        else:
            print("Vous ne pouvez pas vous déplacer au sud.")

    def deplacer_gauche(self):
        piece_actuelle = self.pieces[self.position_actuelle]
        if piece_actuelle["ouest"]:
            self.position_actuelle = piece_actuelle["ouest"]
            self.afficher_position()
        else:
            print("Vous ne pouvez pas vous déplacer à l'ouest.")

    def deplacer_droite(self):
        piece_actuelle = self.pieces[self.position_actuelle]
        if piece_actuelle["est"]:
            self.position_actuelle = piece_actuelle["est"]
            self.afficher_position()
        else:
            print("Vous ne pouvez pas vous déplacer à l'est.")

    @staticmethod
    def charger_tableau(filepath='data/state_board.json'):
        """Charge le plateau de jeu à partir d'un fichier JSON."""
        with open(filepath, 'r') as f:
            return json.load(f)
        
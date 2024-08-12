import json

class Board:
    def __init__(self, game_data):
        self.pieces = game_data["pieces"]
        self.position_actuelle = game_data["salle_depart"]  # Commencer dans la pièce de départ
        self.personnages = {piece: data["personnage"] for piece, data in self.pieces.items()}
        self.armes = {piece: data["arme"] for piece, data in self.pieces.items()}

    def afficher_position(self):
        print(f"Vous êtes actuellement dans {self.position_actuelle}. Il y a {self.personnages[self.position_actuelle]} et {self.armes[self.position_actuelle]}.")

    def go_to_first_room(self):
        self.position_actuelle = list(self.pieces.keys())[0]
        self.afficher_position()

    def go_to_last_room(self):
        self.position_actuelle = list(self.pieces.keys())[-1]
        self.afficher_position()

    def deplacer_droite(self):
        current_index = list(self.pieces.keys()).index(self.position_actuelle)
        if current_index < len(self.pieces) - 1:
            self.position_actuelle = list(self.pieces.keys())[current_index + 1]
            self.afficher_position()
        else:
            print("Vous êtes dans la dernière pièce.")

    def deplacer_gauche(self):
        current_index = list(self.pieces.keys()).index(self.position_actuelle)
        if current_index > 0:
            self.position_actuelle = list(self.pieces.keys())[current_index - 1]
            self.afficher_position()
        else:
            print("Vous êtes dans la première pièce.")

    def yes_answer(self):
        #todo: implement
        print("Oui")
    
    def no_answer(self):
        #todo: implement
        print("Non")

    @staticmethod
    def charger_tableau(filepath='data/state_board.json'):
        """Charge le plateau de jeu à partir d'un fichier JSON."""
        with open(filepath, 'r') as f:
            return json.load(f)
        
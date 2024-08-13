import json

class Board:
    def __init__(self, game_data):
        self.pieces = game_data["pieces"]
        self.position_actuelle = game_data["salle_depart"]  # Commencer dans la piece de départ
        self.personnages = {piece: data["personnage"] for piece, data in self.pieces.items()}
        self.armes = {piece: data["arme"] for piece, data in self.pieces.items()}
        self.victime = game_data["victime"]
        self.positionsVisites = []

    def afficher_position(self, agent):
        print(self.victime)
        print(f"Vous êtes actuellement dans {self.position_actuelle}. Il y a {self.personnages[self.position_actuelle]} et {self.armes[self.position_actuelle]}.")
        if not self.positionsVisites.__contains__(self.position_actuelle):
            self.positionsVisites.append(self.position_actuelle)
            if self.personnages[self.position_actuelle] == self.victime:
                retourMort = agent.process_input(f"{self.victime} est mort")
            else :
                retourVivant = agent.process_input(f"{self.personnages[self.position_actuelle]} est vivant")
            retourPersonnage = agent.process_input(f"{self.personnages[self.position_actuelle]} est dans la {self.position_actuelle}")
            retourArme = agent.process_input(f"Le {self.armes[self.position_actuelle]} est dans la {self.position_actuelle}")
        

    def askQuestion(self, agent): 
        questionType = agent.getQuestion(self.position_actuelle, self.personnages[self.position_actuelle])
        if not questionType:
            return False
        else:
            return questionType


    def go_to_first_room(self, agent):
        self.position_actuelle = list(self.pieces.keys())[0]
        self.afficher_position(agent)

    def go_to_last_room(self, agent):
        self.position_actuelle = list(self.pieces.keys())[-1]
        self.afficher_position(agent)

    def deplacer_droite(self, agent):
        current_index = list(self.pieces.keys()).index(self.position_actuelle)
        if current_index < len(self.pieces) - 1:
            self.position_actuelle = list(self.pieces.keys())[current_index + 1]
            self.afficher_position(agent)
        else:
            print("Vous êtes déjà dans la derniere piece.")

    def deplacer_gauche(self, agent):
        current_index = list(self.pieces.keys()).index(self.position_actuelle)
        if current_index > 0:
            self.position_actuelle = list(self.pieces.keys())[current_index - 1]
            self.afficher_position(agent)
        else:
            print("Vous êtes déjà dans la premiere piece.")

    def yes_answer(self, agent):
        return agent.answerYes()
    
    def no_answer(self, agent):
        agent.answerNo()

    @staticmethod
    def charger_tableau(filepath='data/state_board.json'):
        """Charge le plateau de jeu à partir d'un fichier JSON."""
        with open(filepath, 'r') as f:
            return json.load(f)
        
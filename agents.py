import json

class Agent:
    def __init__(self, inference_engine):
        self.inference_engine = inference_engine
        self.state_board = self.load_state_board()

    def load_state_board(self):
        with open('data/state_board.json', 'r') as file:
            return json.load(file)

    def save_state_board(self):
        with open('data/state_board.json', 'w') as file:
            json.dump(self.state_board, file, indent=4)
    
    def start_investigation(self):
        return "Démarrage de l'enquête..."
    
    def process_input(self, input_text):
        # Logique pour traiter l'entrée et répondre
        return "Réponse de l'agent à : " + input_text

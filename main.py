from agents import Agent
from inference_engine import InferenceEngine
from communication import RandomInteraction
import game
from utils import load_facts, load_rules

def main():
    # Charger les faits et les règles
    rules = load_rules('data/rules.txt')
    
    #Initialiser le board
    board = game.generate_virtual_board()
    
    facts = game.generate_facts(board)

    # Initialiser le moteur d'inférence
    inference_engine = InferenceEngine(facts, rules)
    
    # Initialiser l'agent
    agent = Agent(inference_engine)
    
    # Démarrer les interactions aléatoires
    random_interaction = RandomInteraction(agent)
    random_interaction.start()

if __name__ == "__main__":
    main()

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
    
    for fact in facts:
        print(fact)
        inference_engine.add_clause(fact)
    


    # victime = inference_engine.get_victim()
    # print(f"Victime déduite : {victime}")
    # piece_du_crime = inference_engine.get_crime_room()
    # print(f"Pièce du crime déduite : {piece_du_crime}")
    # arme_du_crime = inference_engine.get_crime_weapon()
    # print(f"Arme du crime déduite : {arme_du_crime}")

    # Initialiser l'agent
    agent = Agent(inference_engine)
    
    # Démarrer les interactions aléatoires
    random_interaction = RandomInteraction(agent)
    random_interaction.start()

if __name__ == "__main__":
    main()

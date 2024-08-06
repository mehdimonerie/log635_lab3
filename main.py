from agents import Agent
from inference_engine import InferenceEngine
from communication import RandomInteraction
from utils import load_facts, load_rules

def main():
    # Charger les faits et les règles
    facts = load_facts('data/facts.txt')
    rules = load_rules('data/rules.txt')
    
    # Initialiser le moteur d'inférence
    inference_engine = InferenceEngine(facts, rules)
    
    # Initialiser l'agent
    agent = Agent(inference_engine)
    
    # Démarrer les interactions aléatoires
    random_interaction = RandomInteraction(agent)
    random_interaction.start()

if __name__ == "__main__":
    main()

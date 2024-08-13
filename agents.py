import json
import nltk

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
        print(input_text)
        pieces = ["cuisine", "salon", "bureau", "bibliotheque", "toilette", "garage"]
        personnages = ["Moutarde", "Rose", "Violet", "Olive", "Leblanc", "Pervenche"]
        armes = ["couteau", "chandelier", "revolver", "corde", "poison", "stylet"]
        
        # Initialize keyword lists
        found_pieces = [room for room in pieces if room in input_text]
        found_personnages = [character for character in personnages if character in input_text]
        found_armes = [weapon for weapon in armes if weapon in input_text]

        if (any(char.isdigit() for char in input_text) or 'minuit' in input_text or 'midi' in input_text) \
                and any(sub in input_text for sub in ['se trouvait', 'était', 'etait']) \
                and found_pieces \
                and found_personnages:
            grammar = 'grammars/personne_piece_heure.fcfg'
        elif (any(char.isdigit() for char in input_text) or 'minuit' in input_text or 'midi' in input_text) \
                and any(sub in input_text for sub in ['mort', 'morte']) \
                and found_personnages:
            grammar = 'grammars/personne_morte_heure.fcfg'
        elif any(sub in input_text for sub in ['se trouvait', 'était', 'etait', 'trouve', 'est']) \
                and found_armes \
                and found_pieces:
            grammar = 'grammars/arme_piece.fcfg'
        elif any(sub in input_text for sub in ['trouve', 'est']) \
                and found_personnages \
                and found_pieces:
            grammar = 'grammars/personne_piece.fcfg'
        elif any(sub in input_text for sub in ['est mort', 'est morte']) \
                and found_personnages:
            grammar = 'grammars/personne_morte.fcfg'
        elif any(sub in input_text for sub in ['est vivant', 'est vivante']) \
                and found_personnages:
            grammar = 'grammars/personne_vivant.fcfg'
        elif any(sub in input_text for sub in ['marque ', 'marques']) \
                and found_personnages:
            grammar = 'grammars/personne_marque.fcfg'
        elif any(sub in input_text for sub in ['blessure ', 'blessures']) \
                and found_personnages:
            grammar = 'grammars/personne_blessure.fcfg'
        elif any(sub in input_text for sub in ['eclats']) \
                and found_personnages:
            grammar = 'grammars/personne_debris.fcfg'
        elif any(sub in input_text for sub in ['discoloration ', 'discolorations']) \
                and found_personnages:
            grammar = 'grammars/personne_discoloration.fcfg'
        elif any(sub in input_text for sub in ['trou ', 'trous']) \
                and found_personnages:
            grammar = 'grammars/personne_trou.fcfg'
        else:
            return "L'entrée n'est pas reconnue."
        
        # Collect the found keywords
        keywords = found_pieces + found_personnages + found_armes
        
        # Add the clause to the inference engine using only the keywords
        self.inference_engine.add_clause(self.to_fol(' '.join(keywords), grammar))
        self.deduce_new_facts()
        suspect = self.inference_engine.get_suspect()
        if suspect:
            return f"Le coupable est: {suspect}"
        else:
            return "Je n'ai toujours pas assez d'informations pour résoudre ce crime"



    def to_fol(self, fact, grammar):
        t = self.fol_to_string(nltk.interpret_sents(fact, grammar))
        print(t)
        return t
    
    
    def fol_to_string(self, results):
        res = ''
        for result in results:
            for (synrep, semrep) in result:
                res += str(semrep)
        return res
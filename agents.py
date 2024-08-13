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
        pieces = ["cuisine", "salon", "bureau", "bibliotheque", "toilette", "garage"]
        personnages = ["Moutarde", "Rose", "Violet", "Olive", "Leblanc", "Pervenche"]
        armes = ["couteau", "chandelier", "revolver", "corde", "poison", "stylet"]

        # Detect which grammar to use based on input
        pieces = ["cuisine", "salon", "bureau", "bibliotheque", "toilette", "garage"]
        personnages = ["Moutarde", "Rose", "Violet", "Olive", "Leblanc", "Pervenche"]
        armes = ["couteau", "chandelier", "revolver", "corde", "poison", "stylet"]

        if (any(char.isdigit() for char in input_text) or 'minuit' in input_text or 'midi' in input_text) \
                and any(sub in input_text for sub in ['se trouvait', 'était', 'etait']) \
                and any(room in input_text for room in pieces) \
                and any(character in input_text for character in personnages):
            grammar = 'grammars/personne_piece_heure.fcfg'
        elif (any(char.isdigit() for char in input_text) or 'minuit' in input_text or 'midi' in input_text) \
                and any(sub in input_text for sub in ['mort', 'morte']) \
                and any(character in input_text for character in personnages):
            grammar = 'grammars/personne_morte_heure.fcfg'
        elif any(sub in input_text for sub in ['se trouvait', 'était', 'etait', 'trouve', 'est']) \
                and any(weapon in input_text for weapon in armes) \
                and any(room in input_text for room in pieces):
            grammar = 'grammars/arme_piece.fcfg'
        elif any(sub in input_text for sub in ['trouve', 'est']) \
                and any(character in input_text for character in personnages) \
                and any(room in input_text for room in pieces):
            grammar = 'grammars/personne_piece.fcfg'
        elif any(sub in input_text for sub in ['est mort', 'est morte']) \
                and any(character in input_text for character in personnages):
            grammar = 'grammars/personne_morte.fcfg'
        elif any(sub in input_text for sub in ['est vivant', 'est vivante']) \
                and any(character in input_text for character in personnages):
            grammar = 'grammars/personne_vivant.fcfg'
        elif any(sub in input_text for sub in ['marque ', 'marques']) \
                and any(character in input_text for character in personnages):
            grammar = 'grammars/personne_marque.fcfg'
        else:
            return "L'entrée n'est pas reconnue."

        self.inference_engine.add_clause(self.to_fol([input_text], grammar))
        self.deduce_new_facts()


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
    

    def deduce_new_facts(self):
        deduction_rules = [ #Pas tous utile, phrase que l'engine pourrait renvoyer
            ("{} avait acces a {} dans le {} à {}h", ['personnage', 'arme', 'piece', 'heure']),
            ("{} était dans le même lieu que {} à {}h", ['suspect', 'victime', 'heure']),
            ("{} est suspect car il était dans {} quand {} est mort", ['suspect', 'piece', 'victime']),
            ("{} pouvait utiliser {} dans le {}", ['personnage', 'arme', 'piece']),
            ("{} est suspect car {} a été tué avec {}", ['suspect', 'victime', 'arme']),
            ("{} est suspect car il était dans le {} peu avant ou apres la mort de {}", ['suspect', 'piece', 'victime']),
            ("{} et {} pourraient être complices car ils étaient dans le {} avec {}", ['suspect1', 'suspect2', 'piece', 'arme']),
            ("{} est suspect car il était la derniere personne vue avec {}", ['suspect', 'victime']),
            ("{} est suspect car il ne peut pas expliquer pourquoi il était dans le {} où {} est mort", ['suspect', 'piece', 'victime']),
        ]

        for rule, placeholders in deduction_rules:
            self.inference_engine.add_clause(self.to_fol(rule, 'grammars/deduction_rules.fcfg'))

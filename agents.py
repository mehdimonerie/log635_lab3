import json
import nltk

class Agent:
    def __init__(self, inference_engine):
        self.inference_engine = inference_engine
        self.state_board = self.load_state_board()
        self.askedClauses = []
        self.currentQuestion = None
        self.currentQuestionResponseType = None
        self.weaponMarks = [
            { "question": "La victime a tu des marques au cou ?", "clause" : self.inference_engine.body_mark_clauses[0]},
            { "question": "La victime a tu des trous à la poitrine ?", "clause" : self.inference_engine.body_mark_clauses[1]},
            { "question": "La victime a tu des éclats au corps ?", "clause" : self.inference_engine.body_mark_clauses[2]},
            { "question": "La victime a tu des blessures à la poitrine ?", "clause" : self.inference_engine.body_mark_clauses[3]},
            { "question": "La victime a tu de la discoloration au visage ?", "clause" : self.inference_engine.body_mark_clauses[4]},
            { "question": "La victime a tu un trou au crane ?", "clause" : self.inference_engine.body_mark_clauses[5]},
        ]

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
        crimeSolved = self.inference_engine.get_is_crime_solved()
        if(crimeSolved):
            suspect = self.inference_engine.get_suspect()
            victim = self.inference_engine.get_victim()
            weapon = self.inference_engine.get_crime_weapon()
            room = self.inference_engine.get_crime_room()
            heure = self.inference_engine.get_crime_hour()
            return f"{suspect} à tuer {victim} avec {weapon} dans la piece {room} à {heure}"
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
    

    def getQuestion(self, room, character): 
        self.currentQuestion = None
        self.currentQuestionResponseType = None
        victim = self.inference_engine.get_victim()
        crime_room = self.inference_engine.get_crime_room()
        crime_hour = self.inference_engine.get_crime_hour()
        if not victim:
            return False
        elif victim == character : 
            if not crime_hour: 
                self.currentQuestion = "A quel heure la victime est elle morte ?"
                self.currentQuestionResponseType = self.inference_engine.crime_hour_clause
                return "number"
            if not self.inference_engine.get_crime_weapon():
                for (question, clause) in self.weaponMarks :
                    personClause = clause.format(f"{victim}")
                    if not self.askedClauses.__contains__(personClause):
                        self.currentQuestion = question
                        self.currentQuestionResponseType = personClause
                        return "yes/no"
        elif not crime_hour or not crime_room:
            return False
        
        if not self.inference_engine.get_innocent().__contains__(character):
            person_room_hour_clause = self.inference_engine.person_room_hour_clause.format(character, crime_room, crime_hour)
            if not self.askedClauses.__contains__(person_room_hour_clause ):
                self.currentQuestion = f"{character}, était tu dans la pièce {crime_room} à {crime_hour}h ?"
                self.currentQuestionResponseType = person_room_hour_clause
                return "yes/no"
        
        return False


    def answerYes(self): 
        self.inference_engine.add_clause(f"{self.currentQuestionResponseType}")
        # ajouter à la liste de questions déjà posés et retirer la currentQuestion
        self.askedClauses.append(self.currentQuestionResponseType)
        self.currentQuestion = None
        self.currentQuestionResponseType = None
        crimeSolved = self.inference_engine.get_is_crime_solved()
        if(crimeSolved):
            suspect = self.inference_engine.get_suspect()
            victim = self.inference_engine.get_victim()
            weapon = self.inference_engine.get_crime_weapon()
            room = self.inference_engine.get_crime_room()
            heure = self.inference_engine.get_crime_hour()
            return f"{suspect} à tuer {victim} avec {weapon} dans la piece {room} à {heure}"
        else:
            return "Je n'ai toujours pas assez d'informations pour résoudre ce crime"

    def answerNo(self): 
        # ajouter à la liste de questions déjà posés et retirer la currentQuestion
        self.askedClauses.append(self.currentQuestionResponseType)
        self.currentQuestion = None
        self.currentQuestionResponseType = None

    def answerNumber(self, number): 
        self.inference_engine.add_clause(f"{self.currentQuestionResponseType.format(number)}")
        self.currentQuestion = None
        self.currentQuestionResponseType = None
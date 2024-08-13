import json
import nltk

class Agent:
    def __init__(self, inference_engine):
        self.inference_engine = inference_engine
        self.state_board = self.load_state_board()
        self.askedClauses = []
        self.currentQuestion = None
        self.currentQuestionResponse = None
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
        
        self.inference_engine.add_clause(self.to_fol([input_text], grammar))
        crimeSolved = self.inference_engine.get_is_crime_solved()
        if(crimeSolved):
            suspect = self.inference_engine.get_suspect()
            victim = self.inference_engine.get_victim()
            weapon = self.inference_engine.get_crime_weapon()
            room = self.inference_engine.get_crime_room()
            heure = self.inference_engine.get_crime_hour()
            return f"{suspect} à tuer {victim} avec {weapon} dans la piece {room} à {heure}h"
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
    
    # retourne le type de question et set currentQuestion au string de question et currentQuestionResponse au FOL que la réponse sera
    def getQuestion(self, room, character): 
        # vider si jamais la dernière question n'a pas été répondu 
        self.currentQuestion = None
        self.currentQuestionResponse = None
        victim = self.inference_engine.get_victim()
        crime_room = self.inference_engine.get_crime_room()
        crime_hour = self.inference_engine.get_crime_hour()
        # si on ne connait pas encore la victime, il n'y a pas de crime à investiguer
        if not victim:
            return False
        elif str(victim) == str(character) : 
            # si on est dans la salle avec la victime, on investigue la scene de crime pour de l'évidence
            if not crime_hour: 
                self.currentQuestion = "A quel heure la victime est elle morte ?"
                self.currentQuestionResponse = self.inference_engine.crime_hour_clause
                return "number"
            if not self.inference_engine.get_crime_weapon():
                for question in self.weaponMarks :
                    personClause = question["clause"].format(f"{victim}")
                    # on garde les questions posés pour ne pas répéter la même plusieurs fois
                    if not self.askedClauses.__contains__(personClause):
                        self.currentQuestion = question["question"]
                        self.currentQuestionResponse = personClause
                        return "yes/no"
        elif not crime_hour or not crime_room:
            return False
        
        elif not self.inference_engine.get_innocent().__contains__(str(character)):
            person_room_hour_clause = self.inference_engine.person_room_hour_clause.format(character, crime_room, crime_hour)
            # on garde les questions posés pour ne pas répéter la même question à la même personne plusieurs fois
            if not self.askedClauses.__contains__(person_room_hour_clause ):
                self.currentQuestion = f"{character}, était tu dans la pièce {crime_room} à {crime_hour}h ?"
                self.currentQuestionResponse = person_room_hour_clause
                return "yes/no"
        
        return False


    def answerYes(self): 
        self.inference_engine.add_clause(f"{self.currentQuestionResponse}")
        # ajouter à la liste de questions déjà posés et retirer la currentQuestion
        self.askedClauses.append(self.currentQuestionResponse)
        self.currentQuestion = None
        self.currentQuestionResponse = None
        # répondre à une question oui pourrait mener à résoudre le crime, on fait donc une vérification
        crimeSolved = self.inference_engine.get_is_crime_solved()
        if(crimeSolved):
            suspect = self.inference_engine.get_suspect()
            victim = self.inference_engine.get_victim()
            weapon = self.inference_engine.get_crime_weapon()
            room = self.inference_engine.get_crime_room()
            heure = self.inference_engine.get_crime_hour()
            return f"{suspect} à tuer {victim} avec {weapon} dans la piece {room} à {heure}h"
        else:
            return "Je n'ai toujours pas assez d'informations pour résoudre ce crime"

    def answerNo(self): 
        # ajouter à la liste de questions déjà posés et retirer la currentQuestion
        self.askedClauses.append(self.currentQuestionResponse)
        self.currentQuestion = None
        self.currentQuestionResponse = None

    def answerNumber(self, number): 
        self.inference_engine.add_clause(f"{self.currentQuestionResponse.format(number)}")
        self.currentQuestion = None
        self.currentQuestionResponse = None

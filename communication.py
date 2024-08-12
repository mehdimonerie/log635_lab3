import os
import sys , tty
import random
import time
from board import Board
import speech_recognition as sr
from text_to_speech import speak

class RandomInteraction:
    def __init__(self, agent):
        self.agent = agent
        self.recognizer = sr.Recognizer()
        game_data = Board.charger_tableau()
        self.board = Board(game_data)  
        
    def start(self):
        while True:
            mode = random.choice(['keyboard'])
            print(f"Mode d'entrée choisi: {mode}")
            
            if mode == 'text':
                self.text_interaction('data/input.txt', 'data/output.txt')
            elif mode == 'terminal':
                self.terminal_interaction()
            elif mode == 'speech':
                self.speech_interaction()
            elif mode == 'keyboard':
                self.keyboard_interaction()

            input_text = input()
            if input_text.lower() == 'exit':
                break
    
    def text_interaction(self, input_filepath, output_filepath):
        print('Text interaction')
        last_modified_time = os.path.getmtime(input_filepath)
        
        while True:
            current_modified_time = os.path.getmtime(input_filepath)
            if current_modified_time != last_modified_time:
                break
            time.sleep(0.1)
            
        with open(input_filepath, 'r') as infile, open(output_filepath, 'w') as outfile:
            user_input = infile.readline().strip()
            if user_input:
                response = self.agent.process_input(user_input)
                outfile.write(response + '\n')
                print("Agent: " + response)
                speak(response)
    
    def terminal_interaction(self):
        print("Terminal interaction")
        user_input = input()
        response = self.agent.process_input(user_input)
        print("Agent: " + response)
    
    def speech_interaction(self):
        print("Speech interaction")
        with sr.Microphone() as source:
            print("Parlez...")
            audio = self.recognizer.listen(source)
            try:
                user_input = self.recognizer.recognize_google(audio, language="fr-FR")
                response = self.agent.process_input(user_input)
                print("Agent: " + response)
                speak(response)
            except sr.UnknownValueError:
                print("Je n'ai pas compris. Réessayez.")
                speak("Je n'ai pas compris. Réessayez.")
            except sr.RequestError as e:
                print(f"Erreur de service; {e}")
                speak(f"Erreur de service; {e}")
                    
    def get_key(self):
        fd = sys.stdin.fileno()
        #old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch1 = sys.stdin.read(1)  # Lire le premier caractère
            
            if ch1 == '\x1b':  # C'est le début d'une séquence d'échappement (flèche directionnelle)
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
                return ch1 + ch2 + ch3
            else:
                return ch1  # C'est une touche simple (comme 'q')
        finally:
            print()
            #termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def keyboard_interaction(self):
        print("Keyboard interaction")
        print("Utilisez les touches directionnelles pour déplacer l'agent (appuyez sur 'q' pour quitter).")
        while True:
            key = self.get_key()
            if key == 'q':
                print("Vous avez quitté l'interaction au clavier.")
                break
            elif key == '\x1b[A':  # Flèche haut
                self.board.go_to_first_room()
            elif key == '\x1b[B':  # Flèche bas
                self.board.go_to_last_room()
            elif key == '\x1b[D':  # Flèche gauche
                self.board.deplacer_gauche()
            elif key == '\x1b[C':  # Flèche droite
                self.board.deplacer_droite()
            elif key == '1': # Touche 1
                self.board.yes_answer()
            elif key == '2': # Touche 2
                self.board.no_answer()
            else:
                print("Touche non reconnue.")
import os
import random
import time
import speech_recognition as sr
from text_to_speech import speak

class RandomInteraction:
    def __init__(self, agent):
        self.agent = agent
        self.recognizer = sr.Recognizer()
    
    def start(self):
        while True:
            mode = random.choice(['text', 'terminal', 'speech'])
            print(f"Mode d'entrée choisi: {mode}")
            speak(f"Mode d'entrée choisi: {mode}")
            
            if mode == 'text':
                self.text_interaction('data/input.txt', 'data/output.txt')
            elif mode == 'terminal':
                self.terminal_interaction()
            elif mode == 'speech':
                self.speech_interaction()

            input_text = input()
            if input_text.lower() == 'exit':
                break
    
    def text_interaction(self, input_filepath, output_filepath):
        speak("Question de l'agent")
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
        speak("Question de l'agent")
        user_input = input()
        response = self.agent.process_input(user_input)
        print("Agent: " + response)
        speak(response)
    
    def speech_interaction(self):
        with sr.Microphone() as source:
            speak("Question de l'agent")
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

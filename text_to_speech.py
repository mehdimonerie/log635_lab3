from gtts import gTTS
import os
from playsound import playsound

def speak(text):
    try:
        # Utiliser gtts pour convertir le texte en parole
        tts = gTTS(text=text, lang='fr')
        filename = "temp_audio.mp3"
        tts.save(filename)
        # Jouer le fichier audio
        playsound(filename)
        # Supprimer le fichier audio après utilisation
        os.remove(filename)
    except Exception as e:
        print(f"Erreur lors de l'utilisation de gtts: {e}")

# Test simple pour vérifier l'importation de gtts

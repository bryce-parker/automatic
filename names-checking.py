#!/usr/bin/env python
import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a name...")
        speak("Please say a name.")
        audio = recognizer.listen(source)
        try:
            name = recognizer.recognize_google(audio)
            print(f"Recognized name: {name}")
            return name
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

def main():
    name = recognize_speech()
    if name:
        print(f"You said: {name}")
        speak(f"You said {name}.")
    else:
        speak("Sorry, I couldn't hear you.")

if __name__ == "__main__":
    main()

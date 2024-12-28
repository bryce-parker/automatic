#!/usr/bin/env python
import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import pyautogui
import time

# Dictionary with contact names and numbers
contacts = {
    "101": "+92 326 9742096",
    "102": "+92 307 7319778",
    "Ahmed": "+92 308 7738282"
}

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command.lower()
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

# Function to call a contact via WhatsApp
def call_contact(contact_name):
    contact_number = contacts.get(contact_name)
    if contact_number:
        webbrowser.open(f"whatsapp://send?phone={contact_number}")
        time.sleep(3)
        pyautogui.click(1286, 55)
    else:
        speak("Contact not found. Whom to call?")
        new_contact_name = recognize_speech()
        if new_contact_name:
            call_contact(new_contact_name)
        else:
            speak("Sorry, I couldn't hear your command.")

def main():
    speak("whom to call.")
    subprocess.Popen(["start", "whatsapp://"], shell=True)
    contact_name = recognize_speech()
    
    if contact_name:
        call_contact(contact_name)
    else:
        speak("Sorry, I couldn't hear your command.")

if __name__ == "__main__":
    import sys
    if getattr(sys, 'frozen', False):
        # If the script is running as an executable
        import os
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    main()

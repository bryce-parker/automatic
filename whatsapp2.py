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
    "Ahmed": "+92 308 7738282",
    "Ahmad brother": "+92 300 2649238"
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
            return command.lower()  # Return lowercase for easier matching
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

# Function to call a contact via WhatsApp
def call_contact(contact_name):
    # Normalize contact name for case-insensitive matching
    normalized_name = contact_name.lower()
    found_contact = next((name for name in contacts if name.lower() == normalized_name), None)

    if found_contact:
        contact_number = contacts[found_contact]
        webbrowser.open(f"whatsapp://send?phone={contact_number}")
        time.sleep(3)
        pyautogui.click(1286, 55)
        time.sleep(2)
        pyautogui.click(936, 90)
        time.sleep(1)
        pyautogui.click(1249, 18)
    else:
        speak("Contact not found. Please try again.")
        new_contact_name = recognize_speech()
        if new_contact_name:
            call_contact(new_contact_name)
        else:
            speak("Sorry, I couldn't hear your command.")

def main():
    subprocess.Popen(["start", "whatsapp://"], shell=True)
    speak("Contact")
    contact_name = recognize_speech()
    
    if contact_name:
        call_contact(contact_name)
    else:
        speak("Sorry, I couldn't hear your command.")

if __name__ == "__main__":
    main()

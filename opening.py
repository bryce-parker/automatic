import keyboard
import os
import speech_recognition as sr
import pyttsx3
import tkinter as tk

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def activate_assistant():
    speak("active")

def deactivate_assistant():
    speak("deactivated.")

def open_directory(name):
    directories = {
        "whatsapp": r"C:\Users\Muhammad Mubashir\Desktop\automatic\run_whatsapp.bat",
        "timer": r"C:\Users\Muhammad Mubashir\Desktop\automatic\timer.bat",
        # ...add more mappings as needed...
    }
    if name in directories:
        os.startfile(directories[name])
    else:
        speak(f"No directory found for {name}.")

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Could not request results; check your network connection.")
    return ""

def create_indicator():
    root = tk.Tk()
    root.geometry("100x100+0+900")  # Position at bottom left
    root.overrideredirect(True)  # Remove window decorations
    frame = tk.Frame(root, bg="green")
    frame.pack(fill=tk.BOTH, expand=True)
    return root, frame

def start_glowing_effect(frame):
    def glow():
        current_color = frame.cget("bg")
        next_color = "yellow" if current_color == "green" else "green"
        frame.config(bg=next_color)
        frame.after(500, glow)
    glow()

def main():
    assistant_active = False
    root, frame = create_indicator()
    while True:
        if keyboard.is_pressed('F10'):
            if not assistant_active:
                activate_assistant()
                assistant_active = True
                frame.pack(fill=tk.BOTH, expand=True)  # Show the frame when listening
                start_glowing_effect(frame)  # Start glowing effect
                while assistant_active:
                    command = listen_for_command()
                    if command:
                        if command == "deactivate":
                            deactivate_assistant()
                            assistant_active = False
                        elif command == "close":
                            deactivate_assistant()
                            speak("Terminating.")
                            root.destroy()
                            exit(0)  # Completely exit the assistant
                        else:
                            open_directory(command)
                            assistant_active = False  # Immediately deactivate without saying "Assistant deactivated"
                    if keyboard.is_pressed('F10'):
                        deactivate_assistant()
                        assistant_active = False
                        while keyboard.is_pressed('F10'):
                            pass  # Wait until the F10 key is released
                frame.pack_forget()  # Hide the frame when not listening
            else:
                deactivate_assistant()
                assistant_active = False
                while keyboard.is_pressed('F10'):
                    pass  # Wait until the F10 key is released
        root.update_idletasks()
        root.update()

if __name__ == "__main__":
    main()

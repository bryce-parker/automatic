import os
import subprocess
import tkinter as tk
from tkinter import ttk
from threading import Thread
import keyboard
import speech_recognition as sr

def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        keyboard.wait('insert')  # Wait for Insert key press
        activate_ui()
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for command...")
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            execute_command(command)
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        deactivate_ui()

# Command execution
commands = {
    "timer": r"C:\Users\Muhammad Mubashir\Desktop\automatic\timer\timer.exe",
    "open downloads": r"C:\\Users\\YourUsername\\Downloads",
}

def execute_command(command):
    for key, path in commands.items():
        if key in command:
            if os.path.exists(path):
                if os.path.isfile(path):
                    subprocess.run(["start", "", path], shell=True)
                else:
                    os.startfile(path)
            else:
                print(f"Path does not exist: {path}")
            break
    else:
        print(f"Command not recognized: {command}")

def execute_command(command):
    for key, path in commands.items():
        if key in command:
            if os.path.exists(path):
                if os.path.isfile(path):
                    subprocess.run(["start", path], shell=True)
                else:
                    os.startfile(path)
            else:
                print(f"Path does not exist: {path}")
            break
    else:
        print(f"Command not recognized: {command}")

# UI Initialization
jarvis_ui = tk.Tk()
jarvis_ui.title("Jarvis")
jarvis_ui.geometry("200x200")
jarvis_ui.overrideredirect(True)
jarvis_ui.withdraw()

# Add UI elements
jarvis_canvas = tk.Canvas(jarvis_ui, width=200, height=200, bg="darkblue")
jarvis_canvas.pack()

# UI Components
def activate_ui():
    jarvis_ui.deiconify()
    jarvis_ui.after(0, glow_effect, True)

def deactivate_ui():
    jarvis_ui.after(0, glow_effect, False)
    jarvis_ui.withdraw()

def glow_effect(active):
    if active:
        jarvis_canvas.config(bg="blue")
    else:
        jarvis_canvas.config(bg="darkblue")

def main():
    Thread(target=listen_for_commands, daemon=True).start()
    jarvis_ui.mainloop()

if __name__ == "__main__":
    main()

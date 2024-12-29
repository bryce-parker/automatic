import speech_recognition as sr
import pyttsx3
import time
import tkinter as tk
from tkinter import messagebox
import threading

# Initialize the speech engine
engine = pyttsx3.init()

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry.")
        return None
    except sr.RequestError:
        speak("Sorry.")
        return None

# Function to update the timer label
def update_timer_label(hours, minutes, seconds):
    if root.winfo_exists():
        timer_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        root.update_idletasks()

# Function to set a timer based on user input
def set_timer():
    while True:
        speak("Focus.")
        focus_command = recognize_speech()
        if focus_command:
            focus_seconds = extract_seconds(focus_command)
            if focus_seconds is not None:
                break
        speak("Sorry.")

    while True:
        speak("Break.")
        break_command = recognize_speech()
        if break_command:
            break_seconds = extract_seconds(break_command)
            if break_seconds is not None:
                break
        speak("Sorry.")

    start_timers(focus_seconds, break_seconds)

# Function to extract seconds from the speech command
def extract_seconds(command):
    words = command.split()
    for word in words:
        if word.isdigit():
            if 'second' in command:
                return int(word)
            elif 'minute' in command:
                return int(word) * 60
    speak("Sorry.")
    return None

# Global variable to control skipping timers
skip_timer = False

# Global variable to control pausing timers
pause_timer = False

# Function to skip the current timer
def skip_current_timer():
    global skip_timer
    skip_timer = True
    root.quit()  # Exit the current Tkinter event loop

# Function to pause the current timer
def pause_current_timer():
    global pause_timer
    pause_timer = not pause_timer
    if pause_timer:
        pause_button.config(text="Unpause")
    else:
        pause_button.config(text="Pause")

# Function to reset the timer
def reset_timer():
    set_timer()

# Function to close the timer
def close_timer():
    speak("It is a pleasure to be working for you, my lord.")
    root.destroy()

# Function to start the focus and break timers
def start_timers(focus_seconds, break_seconds):
    while True:
        run_timer(focus_seconds, "Focus")
        run_timer(break_seconds, "Break")

# Function to run a single timer
def run_timer(seconds, timer_type):
    global skip_timer, pause_timer
    skip_timer = False
    speak(f"Starting the {timer_type}.")
    total_seconds = seconds
    while total_seconds > 0 and not skip_timer:
        if not pause_timer:
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            update_timer_label(hours, minutes, seconds)
            if root.winfo_exists():
                root.update()  # Update the Tkinter event loop
            time.sleep(1)
            total_seconds -= 1
        else:
            if root.winfo_exists():
                root.update()  # Keep the Tkinter event loop running while paused
            time.sleep(1)
    if not skip_timer:
        speak(f"Time's up! The {timer_type} timer has ended.")
        if root.winfo_exists():
            messagebox.showinfo("Timer", f"Time's up! The {timer_type} timer has ended.")
    else:
        speak(f"The {timer_type} timer was skipped.")

# Function to handle the button click
def on_button_click():
    set_timer()

# Function to handle the initial setup
def initial_setup():
    set_timer()

# Function to create a gradient background
def create_gradient(canvas, color1, color2):
    width = root.winfo_width()
    height = root.winfo_height()
    limit = height
    (r1, g1, b1) = root.winfo_rgb(color1)
    (r2, g2, b2) = root.winfo_rgb(color2)
    r_ratio = float(r2 - r1) / limit
    g_ratio = float(g2 - g1) / limit
    b_ratio = float(b2 - b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr:04x}{ng:04x}{nb:04x}'
        canvas.create_line(0, i, width, i, fill=color, tags=("gradient",))
    canvas.lower("gradient")

# Function to handle button hover effect
def on_enter(e):
    e.widget['background'] = '#c0392b'

def on_leave(e):
    e.widget['background'] = '#e74c3c'

# Define a stylish font
stylish_font = ("Helvetica", 12, "bold")

# Create the main window
root = tk.Tk()
root.title("Voice Assistant Timer")
root.geometry("300x200")
root.configure(bg="#2c3e50")

# Create and place the timer label
timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48, "bold"), bg="#2c3e50", fg="#ecf0f1")
timer_label.place(relx=0.5, rely=0.3, anchor="center")

# Create and place the skip button
skip_button = tk.Button(root, text="Skip", command=skip_current_timer, font=stylish_font, bg="#e74c3c", fg="#ecf0f1", activebackground="#c0392b", activeforeground="#ecf0f1", relief="flat", bd=0)
skip_button.place(relx=0.2, rely=0.7, anchor="center")
skip_button.bind("<Enter>", on_enter)
skip_button.bind("<Leave>", on_leave)

# Create and place the pause button
pause_button = tk.Button(root, text="Pause", command=pause_current_timer, font=stylish_font, bg="#f39c12", fg="#ecf0f1", activebackground="#e67e22", activeforeground="#ecf0f1", relief="flat", bd=0)
pause_button.place(relx=0.4, rely=0.7, anchor="center")
pause_button.bind("<Enter>", lambda e: e.widget.config(bg="#e67e22"))
pause_button.bind("<Leave>", lambda e: e.widget.config(bg="#f39c12"))

# Create and place the reset button
reset_button = tk.Button(root, text="Reset", command=reset_timer, font=stylish_font, bg="#3498db", fg="#ecf0f1", activebackground="#2980b9", activeforeground="#ecf0f1", relief="flat", bd=0)
reset_button.place(relx=0.6, rely=0.7, anchor="center")
reset_button.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
reset_button.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))

# Create and place the close button
close_button = tk.Button(root, text="Close", command=close_timer, font=stylish_font, bg="#2ecc71", fg="#ecf0f1", activebackground="#27ae60", activeforeground="#ecf0f1", relief="flat", bd=0)
close_button.place(relx=0.8, rely=0.7, anchor="center")
close_button.bind("<Enter>", lambda e: e.widget.config(bg="#27ae60"))
close_button.bind("<Leave>", lambda e: e.widget.config(bg="#2ecc71"))

# Run the initial setup
root.after(1000, initial_setup)

# Run the Tkinter event loop
root.mainloop()


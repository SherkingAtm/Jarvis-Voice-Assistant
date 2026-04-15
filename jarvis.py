import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import webbrowser
import keyboard
import subprocess
import pygetwindow as gw
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import requests
import playsound
import os
import time
from config import SOUND_FILE, SCREENSHOT_FOLDER

# -------------------- TTS Setup --------------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# -------------------- Voice Input --------------------
def take_command(timeout=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=6)
            command = recognizer.recognize_google(audio, language='en-IN')
            print(f"You said: {command}")
            return command.lower()
    except:
        return ""

# -------------------- Volume Control --------------------
def set_volume(target_volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    normalized_volume = target_volume / 100.0
    volume.SetMasterVolumeLevelScalar(normalized_volume, None)

    speak(f"Volume set to {target_volume} percent")

# -------------------- Weather --------------------
def weather():
    webbrowser.open('https://www.google.com/search?q=weather')
    speak("Showing weather")

# -------------------- Main Assistant --------------------
def run_jarvis():
    commandold = take_command()
    command = commandold.replace('jarvis', '').strip()

    if not command:
        return

    # -------- Basic Info --------
    if 'who are you' in command:
        speak("I am Jarvis, your virtual assistant.")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {current_time}")

    elif 'date' in command:
        current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        speak(f"Today is {current_date}")

    elif 'play' in command:
        song = command.replace('play', '').strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'weather' in command:
        weather()

    elif 'search' in command:
        query = command.replace('search', '').strip()
        webbrowser.open(f'https://google.com/search?q={query}')
        speak(f"Searching for {query}")

    elif 'volume up' in command:
        pyautogui.press('volumeup')
        speak("Volume increased")

    elif 'volume down' in command:
        pyautogui.press('volumedown')
        speak("Volume decreased")

    elif 'set volume' in command:
        try:
            volume = int(''.join(filter(str.isdigit, command)))
            if 0 <= volume <= 100:
                set_volume(volume)
            else:
                speak("Volume must be between 0 and 100")
        except:
            speak("Invalid volume level")

    elif 'mute' in command:
        pyautogui.press('volumemute')
        speak("Muted")

    elif 'screenshot' in command:
        screenshot = pyautogui.screenshot()
        name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(SCREENSHOT_FOLDER, f"{name}.png")
        screenshot.save(file_path)
        speak("Screenshot saved")

    elif 'open' in command:
        app = command.replace('open', '').strip().lower()

        app_paths = {
            "calculator": "calc.exe",
            "notepad": "notepad.exe",
            "command prompt": "cmd.exe",
            "file manager": "explorer.exe",
        }

        if app in app_paths:
            subprocess.Popen(app_paths[app], shell=True)
            speak(f"Opening {app}")
        else:
            webbrowser.open(f'https://{app}.com')
            speak(f"Opening {app}")

    elif 'close window' in command:
        pyautogui.hotkey('alt', 'f4')
        speak("Window closed")

    elif 'desktop' in command:
        pyautogui.hotkey('win', 'd')
        speak("Showing desktop")

    elif 'type' in command:
        text = command.replace('type', '').strip()
        pyautogui.typewrite(text)
        speak("Typing")

    elif 'joke' in command:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke = response.json()
            speak(joke['setup'])
            speak(joke['punchline'])

    elif 'exit' in command or 'stop assistant' in command:
        speak("Goodbye!")
        return "exit"

    else:
        speak("Sorry, I didn't understand that")

# -------------------- Wake Word Loop --------------------
if __name__ == "__main__":
    while True:
        print("System online!")
        wake_command = take_command(timeout=8)

        if 'jarvis' in wake_command:
            playsound.playsound(SOUND_FILE)
            speak("Your wish is my command")

            while True:
                if run_jarvis() == "exit":
                    break
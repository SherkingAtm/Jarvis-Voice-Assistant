import os

BASE_DIR = os.getcwd()

SOUND_FILE = os.path.join(BASE_DIR, "jarvis.mp3")
SCREENSHOT_FOLDER = os.path.join(BASE_DIR, "Screenshots")

if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)
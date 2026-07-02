"""
LEGEND AI - Text to Speech Tool
-----------------------------------------
What this file does:
Gives Legend AI a voice. After every response, it can
speak the reply out loud using your Windows built-in
voice engine. Completely free, works offline.

This completes the voice loop:
  You speak → Legend AI hears → Legend AI thinks → Legend AI speaks back
"""

import pyttsx3
import threading

def speak(text):
    """
    Speaks the given text out loud.
    Runs in a separate thread so it doesn't freeze the UI
    while talking.
    """
    def run():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)  # speed (words per minute)
            engine.setProperty('volume', 1.0)  # volume 0-1

            # Use the first available voice
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)

            # Limit to first 500 chars so it doesn't read out
            # a massive research report word by word
            short_text = text[:500]
            engine.say(short_text)
            engine.runAndWait()
        except Exception as e:
            print(f"[TTS] Error: {e}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
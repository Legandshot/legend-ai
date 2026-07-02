"""
LEGEND AI - Voice Tool
-----------------------------------------
What this file does:
Gives Legend AI the ability to listen to your microphone
and convert your speech to text, which then gets sent
to the Mission Engine just like typed text would.

Uses sounddevice to capture audio and Google's free
speech recognition API to convert it to text.
"""

import speech_recognition as sr
import sounddevice
import tempfile
import os
import wave
import numpy as np

SAMPLE_RATE = 16000
DURATION = 5  # seconds to listen


def listen_once():
    """
    Records audio from the microphone for DURATION seconds,
    then converts it to text using Google's free speech API.
    Returns the text, or None if nothing was understood.
    """
    try:
        print("[Voice] Listening...")
        audio_data = sounddevice.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='int16'
        )
        sounddevice.wait()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            tmp_path = f.name

        with wave.open(tmp_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_data.tobytes())

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio = recognizer.record(source)

        os.unlink(tmp_path)

        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None
    except Exception as e:
        return None
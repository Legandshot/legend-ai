"""
LEGEND AI - Model Router
-----------------------------------------
What this file does:
Routes all AI calls through one central function.
Tries Groq first, falls back to Gemini if Groq fails.

FIX: Clients are now created INSIDE ask_ai() instead of at
import time, so the .env keys are always loaded first.
"""

import os
from groq import Groq
from google import genai


def ask_ai(messages, temperature=0.7):
    """
    The ONE function everything calls to talk to an AI model.
    Tries Groq first. Falls back to Gemini if Groq fails.
    """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # --- Try Groq first ---
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content

    except Exception as groq_error:
        print(f"\n[Model Router] Groq failed ({groq_error}). Trying Gemini...")

        # --- Fall back to Gemini ---
        try:
            gemini_client = genai.Client(api_key=GEMINI_API_KEY)

            parts = []
            for m in messages:
                role = m["role"]
                content = m["content"]
                if role == "system":
                    parts.append(f"Instructions: {content}")
                elif role == "user":
                    parts.append(f"User: {content}")
                elif role == "assistant":
                    parts.append(f"Assistant: {content}")
            prompt = "\n\n".join(parts)

            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text

        except Exception as gemini_error:
            print(f"\n[Model Router] Gemini also failed ({gemini_error}).")
            return "I'm having trouble connecting to my AI brain right now. Please try again shortly."
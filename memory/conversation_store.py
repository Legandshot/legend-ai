"""
LEGEND AI - Conversation Store
-----------------------------------------
What this file does:
Saves and loads the FULL conversation history, separate from
the "facts" memory (memory_store.py). This is what makes Legend AI
feel continuous across sessions - it doesn't just remember isolated
facts about you, it remembers the actual conversation.

This matches "Conversation Memory" from the architecture -
session-oriented, but here we persist it so you can resume
naturally instead of starting blank every time.
"""

import json
import os

CONVERSATION_FILE = "conversation.json"

# Keep only the last N exchanges to avoid the conversation growing
# forever and becoming too expensive/slow to send to the AI each time.
MAX_MESSAGES = 40


def load_conversation():
    """Loads the saved conversation. Returns None if none exists yet."""
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_conversation(conversation):
    """
    Saves the conversation to disk, trimming it if it's gotten
    too long. The system message (first one) is always kept.
    """
    if len(conversation) > MAX_MESSAGES:
        system_msg = conversation[0]
        recent = conversation[-(MAX_MESSAGES - 1):]
        conversation = [system_msg] + recent

    with open(CONVERSATION_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation, f, indent=2)

    return conversation
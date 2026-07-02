"""
LEGEND AI - Memory Store
-----------------------------------------
What this file does:
Handles everything related to remembering things between sessions.
This is its own file because Memory is a "first-class service" -
it should be separate from chat logic, separate from tools, etc.
Any other part of Legend AI can import this file and use memory
without needing to know HOW it's stored.
"""

import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    """Loads saved memories from disk. Returns empty list if none exist yet."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memory(memories):
    """Writes the current memory list to disk permanently."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2)


def add_memory(memories, fact):
    """Adds a new fact to memory and saves immediately."""
    memories.append(fact)
    save_memory(memories)
    return memories


def memory_as_text(memories):
    """Formats memories as readable text for the AI's context."""
    if not memories:
        return "Nothing yet."
    return "\n".join(f"- {m}" for m in memories)
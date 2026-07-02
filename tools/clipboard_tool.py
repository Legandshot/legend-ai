"""
LEGEND AI - Clipboard Tool
-----------------------------------------
What this file does:
Gives Legend AI the ability to read and write your clipboard.

This means you can copy anything (code, text, an error message,
a paragraph) and then just say "explain this" or "fix this" -
Legend AI will read what you copied without you needing to
paste it into the chat manually.

This matches the "Clipboard Access" tool from the architecture.
"""

import pyperclip


def read_clipboard():
    """
    Reads whatever is currently on the clipboard.
    Returns the text, or None if clipboard is empty.
    """
    try:
        content = pyperclip.paste()
        return content if content.strip() else None
    except Exception as e:
        return None


def write_clipboard(text):
    """
    Writes text to the clipboard so the user can paste it anywhere.
    """
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        return False
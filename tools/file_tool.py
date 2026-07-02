"""
LEGEND AI - File Tool
-----------------------------------------
What this file does:
Handles all file-related actions Legend AI can take:
  - Creating files
  - Listing what files exist
  - Reading a file's content back
  - Renaming a file
  - Deleting a file (requires confirmation)
"""

import os
import re

OUTPUT_FOLDER = "legend_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def safe_filename(name):
    """Cleans up a filename so it's safe to save on Windows."""
    name = re.sub(r'[^a-zA-Z0-9\-_]', '-', name)
    return name.strip('-')[:50] or "legend-output"


def save_file(filename_hint, content):
    """Saves content to a real .txt file inside legend_files/."""
    filename = safe_filename(filename_hint)
    filepath = os.path.join(OUTPUT_FOLDER, f"{filename}.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def list_files():
    """Returns a list of all files currently saved in legend_files/."""
    files = os.listdir(OUTPUT_FOLDER)
    return [f for f in files if f.endswith(".txt")]


def find_matching_file(filename):
    """
    Finds the closest matching file to what the user typed.
    Returns None if nothing matches.
    """
    files = list_files()

    if filename in files:
        return filename

    cleaned = filename.lower().replace(".txt", "")
    matches = [f for f in files if cleaned in f.lower()]
    return matches[0] if matches else None


def read_file(filename):
    """Reads a file's content back."""
    target = find_matching_file(filename)
    if not target:
        return None

    filepath = os.path.join(OUTPUT_FOLDER, target)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    return {"filename": target, "content": content}


def delete_file(filename):
    """Permanently deletes a file."""
    target = find_matching_file(filename)
    if not target:
        return None

    filepath = os.path.join(OUTPUT_FOLDER, target)
    os.remove(filepath)
    return target


def rename_file(old_name, new_name):
    """
    Renames a file. Returns a dict with old and new names,
    or None if the original file couldn't be found.
    """
    target = find_matching_file(old_name)
    if not target:
        return None

    old_path = os.path.join(OUTPUT_FOLDER, target)
    new_filename = safe_filename(new_name) + ".txt"
    new_path = os.path.join(OUTPUT_FOLDER, new_filename)

    os.rename(old_path, new_path)
    return {"old_name": target, "new_name": new_filename}
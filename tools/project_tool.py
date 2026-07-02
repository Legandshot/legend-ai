"""
LEGEND AI - Project Tool
-----------------------------------------
What this file does:
This is the real beginning of "Goal-Oriented Automation" from
your original vision - the "continue my AI project" example.

Instead of you manually opening VS Code, navigating to a folder,
etc., you define a Project ONCE, and Legend AI can open everything
needed for it with one sentence.

Projects are saved to disk so they persist across sessions.
"""

import json
import os
import subprocess

PROJECTS_FILE = "projects.json"


def load_projects():
    """Loads saved projects from disk."""
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_projects(projects):
    """Saves projects to disk."""
    with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2)


def add_project(name, folder_path):
    """
    Registers a new project: a name and the folder it lives in.
    Example: add_project("AI project", "C:/Users/Lenovo/legend-ai")
    """
    projects = load_projects()
    projects[name.lower()] = {"folder": folder_path}
    save_projects(projects)
    return projects


def find_project(name):
    """Finds the closest matching project by name."""
    projects = load_projects()
    cleaned = name.lower()

    if cleaned in projects:
        return cleaned, projects[cleaned]

    for proj_name, data in projects.items():
        if cleaned in proj_name or proj_name in cleaned:
            return proj_name, data

    return None, None


def open_project(name):
    """
    Opens a project: launches VS Code directly inside that
    project's folder. This is the "continue my AI project" mission.
    """
    proj_name, data = find_project(name)

    if not data:
        return {"success": False, "message": f"I don't know a project called '{name}'. You can add one first."}

    folder = data["folder"]

    if not os.path.exists(folder):
        return {"success": False, "message": f"The folder for '{proj_name}' doesn't exist anymore: {folder}"}

    try:
        subprocess.Popen(f'code "{folder}"', shell=True)
        return {"success": True, "message": f"Opened your '{proj_name}' project in VS Code ({folder})."}
    except Exception as e:
        return {"success": False, "message": f"Failed to open project: {e}"}
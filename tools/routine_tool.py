"""
LEGEND AI - Routine Tool
"""

import json
import os
import subprocess
import time

ROUTINES_FILE = "routines.json"


def load_routines():
    if os.path.exists(ROUTINES_FILE):
        with open(ROUTINES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_routines(routines):
    with open(ROUTINES_FILE, "w", encoding="utf-8") as f:
        json.dump(routines, f, indent=2)


def add_routine(name, actions):
    routines = load_routines()
    routines[name.lower()] = {"actions": actions}
    save_routines(routines)
    return routines


def find_routine(name):
    routines = load_routines()
    cleaned = name.lower()
    if cleaned in routines:
        return cleaned, routines[cleaned]
    for routine_name, data in routines.items():
        if cleaned in routine_name or routine_name in cleaned:
            return routine_name, data
    return None, None


def run_routine(name, projects):
    routine_name, data = find_routine(name)
    if not data:
        return {"success": False, "message": "I don't know a routine called '" + name + "'."}

    actions = data.get("actions", [])
    results = []

    for action in actions:
        action_type = action.get("type")
        value = action.get("value", "")

        if action_type == "open_app":
            try:
                subprocess.Popen(value, shell=True)
                results.append("Opened " + value)
            except Exception as e:
                results.append("Failed to open " + value + ": " + str(e))
            time.sleep(1)

        elif action_type == "open_project":
            proj_name = value.lower()
            if proj_name in projects:
                folder = projects[proj_name]["folder"]
                try:
                    subprocess.Popen("code \"" + folder + "\"", shell=True)
                    results.append("Opened project '" + proj_name + "' in VS Code")
                except Exception as e:
                    results.append("Failed to open project: " + str(e))
                time.sleep(1)
            else:
                results.append("Project '" + proj_name + "' not found")

        elif action_type == "message":
            results.append(value)

    return {
        "success": True,
        "routine_name": routine_name,
        "results": results
    }
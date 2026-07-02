"""
LEGEND AI - System Tool
"""

import subprocess

KNOWN_APPS = {
    "vs code": "code",
    "vscode": "code",
    "visual studio code": "code",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad",
    "calculator": "calc",
    "file explorer": "explorer",
    "explorer": "explorer",
    "terminal": "wt",
    "command prompt": "cmd",
    "cmd": "cmd",
    "spotify": "spotify",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
}


def open_app(app_name):
    cleaned = app_name.lower().strip()
    command = KNOWN_APPS.get(cleaned)

    if not command:
        for known_name, cmd in KNOWN_APPS.items():
            if cleaned in known_name or known_name in cleaned:
                command = cmd
                break

    if not command:
        return {"success": False, "app": app_name, "message": "I don't know how to open '" + app_name + "' yet."}

    try:
        subprocess.Popen(command, shell=False)
        return {"success": True, "app": app_name, "message": "Opened " + app_name + "."}
    except Exception as e:
        return {"success": False, "app": app_name, "message": "Failed to open " + app_name + ": " + str(e)}
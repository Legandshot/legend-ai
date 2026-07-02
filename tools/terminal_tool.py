"""
LEGEND AI - Terminal Tool
-----------------------------------------
What this file does:
Gives Legend AI the ability to run terminal commands
on your computer.

SAFETY: Every command is shown to you BEFORE it runs.
Legend AI never executes anything without your approval.
This matches "Level 2: Explicit confirmation required"
from the architecture's permission system.
"""

import subprocess
import os


def run_command(command, working_dir=None):
    """
    Runs a terminal command and returns the output.
    working_dir: optional folder to run the command in.
    """
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_dir or os.getcwd()
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:
            return {
                "success": True,
                "output": output or "Command completed with no output.",
                "error": None
            }
        else:
            return {
                "success": False,
                "output": output,
                "error": error or "Command failed."
            }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Command timed out after 30 seconds."
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def suggest_command(goal, ask_ai_fn):
    """
    Takes a natural language goal and asks the AI to suggest
    the right terminal command to accomplish it.
    Returns the suggested command as a string.
    """
    prompt = f"""
The user wants to run a terminal command on Windows PowerShell to accomplish this goal:
"{goal}"

Suggest ONE specific PowerShell/Windows command that would accomplish this.
Respond with ONLY the command itself, nothing else. No explanation, no markdown.
Keep it safe - no destructive commands like format, rm -rf, del /f /s, etc.
"""
    return ask_ai_fn([{"role": "user", "content": prompt}], temperature=0).strip()
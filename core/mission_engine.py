"""
LEGEND AI - Mission Engine
"""

import json
from core.model_router import ask_ai


def classify_mission(user_message):
    classification_prompt = f"""
Classify the following user message into ONE mission type.

Mission types:
- QUESTION: user wants information Legend AI likely already knows
- WEB_SEARCH: user wants a QUICK answer using current/live internet info
- RESEARCH: user wants a THOROUGH investigation of a topic
- TASK_FILE: user wants something written AND saved as a new file
- LIST_FILES: user wants to see what files Legend AI has already created
- READ_FILE: user wants to read back/open/see a previously created file
- RENAME_FILE: user wants to rename a previously created file
- DELETE_FILE: user wants to delete/remove a previously created file
- OPEN_APP: user wants to open a generic application
- ADD_PROJECT: user wants to register a new project with a name and folder path
- OPEN_PROJECT: user wants to open/continue a previously registered project
- CREATE_ROUTINE: user wants to CREATE/DEFINE a new routine
- RUN_ROUTINE: user wants to RUN/START an existing routine
- CLIPBOARD_READ: user wants Legend AI to read/use/act on what is currently on their clipboard (e.g. "explain this", "fix this", "what is this", "summarize what I copied", "translate this")
- CLIPBOARD_WRITE: user wants Legend AI to copy something TO their clipboard (e.g. "copy that to clipboard", "put that in my clipboard")
- TASK_OTHER: user wants something done but doesn't fit the above
- CONVERSATION: small talk, greetings, casual chat

Respond ONLY with valid JSON in this exact format, nothing else:
{{"mission_type": "TASK_FILE", "goal": "short summary", "suggested_filename": null, "target_filename": null, "new_filename": null, "app_name": null, "project_name": null, "project_folder": null, "routine_name": null}}

Rules:
- If TASK_FILE: set suggested_filename
- If READ_FILE or DELETE_FILE: set target_filename
- If RENAME_FILE: set target_filename and new_filename
- If OPEN_APP: set app_name
- If ADD_PROJECT: set project_name and project_folder
- If OPEN_PROJECT: set project_name
- If CREATE_ROUTINE or RUN_ROUTINE: set routine_name
- Otherwise all null

User message: "{user_message}"
"""

    raw = ask_ai([{"role": "user", "content": classification_prompt}], temperature=0).strip()

    try:
        mission = json.loads(raw)
    except json.JSONDecodeError:
        mission = {
            "mission_type": "CONVERSATION",
            "goal": user_message,
            "suggested_filename": None,
            "target_filename": None,
            "new_filename": None,
            "app_name": None,
            "project_name": None,
            "project_folder": None,
            "routine_name": None
        }

    return mission


def should_remember(user_message):
    prompt = f"""
Does this message contain a LASTING fact worth remembering about the user
long-term - their name, preferences, ongoing project details, or goals?

Do NOT count one-time actions or commands as facts.

Respond ONLY with valid JSON:
{{"should_remember": true, "fact": "short factual summary"}}
or
{{"should_remember": false, "fact": null}}

Message: "{user_message}"
"""
    raw = ask_ai([{"role": "user", "content": prompt}], temperature=0).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"should_remember": False, "fact": None}


def parse_routine_actions(user_message, routine_name):
    prompt = f"""
The user wants to create a routine called "{routine_name}".
Their description: "{user_message}"

Extract the actions they want this routine to perform.
Each action must be one of these types:
- open_app: open an application (chrome, notepad, vs code, etc.)
- open_project: open a registered Legend AI project by name

Respond ONLY with valid JSON:
{{"actions": [
    {{"type": "open_app", "value": "chrome"}},
    {{"type": "open_project", "value": "ai project"}}
]}}

Only include actions explicitly mentioned. Keep values lowercase.
"""
    raw = ask_ai([{"role": "user", "content": prompt}], temperature=0).strip()
    try:
        parsed = json.loads(raw)
        return parsed.get("actions", [])
    except json.JSONDecodeError:
        return []
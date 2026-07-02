import sys
sys.path.insert(0, r"C:\Users\Lenovo\legend-ai")

import os
import streamlit as st
from dotenv import load_dotenv

from core.model_router import ask_ai
from core.mission_engine import classify_mission, should_remember, parse_routine_actions
from core.research_engine import run_research
from tools.file_tool import save_file, list_files, read_file, find_matching_file, delete_file, rename_file
from tools.search_tool import web_search
from tools.system_tool import open_app
from tools.project_tool import add_project, open_project, load_projects
from tools.routine_tool import add_routine, run_routine, load_routines
from tools.clipboard_tool import read_clipboard, write_clipboard
from tools.voice_tool import listen_once
from tools.tts_tool import speak
from tools.terminal_tool import run_command, suggest_command
from memory.memory_store import load_memory, add_memory, memory_as_text
from memory.conversation_store import load_conversation, save_conversation

load_dotenv()

st.set_page_config(page_title="Legend AI", page_icon="🧠", layout="centered")

if "memories" not in st.session_state:
    st.session_state.memories = load_memory()

if "conversation" not in st.session_state:
    saved = load_conversation()
    system_message = {
        "role": "system",
        "content": (
            "You are Legend AI, a personal AI operating system assistant. "
            f"Here is what you remember about the user so far:\n{memory_as_text(st.session_state.memories)}"
        )
    }
    if saved:
        st.session_state.conversation = [system_message] + saved[1:]
    else:
        st.session_state.conversation = [system_message]

if "pending_command" not in st.session_state:
    st.session_state.pending_command = None

with st.sidebar:
    st.title("🧠 Legend AI")
    st.caption("Your personal AI operating system")
    st.subheader("Memory")
    if st.session_state.memories:
        for m in st.session_state.memories:
            st.write("• " + m)
    else:
        st.write("Nothing remembered yet.")
    st.subheader("Files")
    files = list_files()
    if files:
        for f in files:
            st.write("📄 " + f)
    else:
        st.write("No files yet.")
    st.subheader("Projects")
    projects = load_projects()
    if projects:
        for name in projects:
            st.write("📁 " + name)
    else:
        st.write("No projects yet.")
    st.subheader("Routines")
    routines = load_routines()
    if routines:
        for name in routines:
            st.write("⚡ " + name)
    else:
        st.write("No routines yet.")

st.title("Legend AI")

for msg in st.session_state.conversation[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if st.session_state.pending_command:
    cmd = st.session_state.pending_command
    st.warning("Legend AI wants to run this command:")
    st.code(cmd, language="bash")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Approve and Run"):
            result = run_command(cmd)
            if result["success"]:
                reply = "Command ran successfully:\n\n```\n" + result["output"] + "\n```"
            else:
                reply = "Command failed:\n\n```\n" + result["error"] + "\n```"
            st.session_state.conversation.append({"role": "assistant", "content": reply})
            save_conversation(st.session_state.conversation)
            speak(reply[:200])
            st.session_state.pending_command = None
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.session_state.pending_command = None
            st.session_state.conversation.append({"role": "assistant", "content": "Command cancelled."})
            st.rerun()

col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.chat_input("Type your message...")
with col2:
    if st.button("🎤"):
        with st.spinner("Listening..."):
            spoken = listen_once()
        if spoken:
            st.success("Heard: " + spoken)
            user_input = spoken
        else:
            st.warning("Didn't catch that.")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.conversation.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Working on it..."):

            mission = classify_mission(user_input)
            fact_check = should_remember(user_input)

            if fact_check.get("should_remember") and fact_check.get("fact"):
                st.session_state.memories = add_memory(
                    st.session_state.memories, fact_check["fact"]
                )

            if mission["mission_type"] == "TASK_FILE":
                content = ask_ai([
                    {"role": "system", "content": "You are Legend AI. Write complete, well-formatted content for the user's request."},
                    {"role": "user", "content": user_input}
                ])
                filepath = save_file(mission.get("suggested_filename") or mission["goal"], content)
                reply = "File created: " + filepath + "\n\n" + content

            elif mission["mission_type"] == "WEB_SEARCH":
                result = web_search(user_input)
                sources = "\n".join("- [" + s["title"] + "](" + s["url"] + ")" for s in result["sources"])
                reply = result["answer"] + "\n\n**Sources:**\n" + sources

            elif mission["mission_type"] == "RESEARCH":
                result = run_research(user_input)
                seen = set()
                source_lines = []
                for s in result["sources"]:
                    if s["url"] not in seen:
                        source_lines.append("- [" + s["title"] + "](" + s["url"] + ")")
                        seen.add(s["url"])
                reply = result["report"] + "\n\n**Sources:**\n" + "\n".join(source_lines)

            elif mission["mission_type"] == "LIST_FILES":
                files = list_files()
                if files:
                    reply = "Here are the files I've created:\n" + "\n".join("- " + f for f in files)
                else:
                    reply = "I haven't created any files yet."

            elif mission["mission_type"] == "READ_FILE":
                target = mission.get("target_filename") or ""
                result = read_file(target)
                if result:
                    reply = "**" + result["filename"] + "**\n\n" + result["content"]
                else:
                    reply = "I couldn't find a file matching '" + target + "'."

            elif mission["mission_type"] == "RENAME_FILE":
                old_target = mission.get("target_filename") or ""
                new_target = mission.get("new_filename") or ""
                result = rename_file(old_target, new_target)
                if result:
                    reply = "Renamed '" + result["old_name"] + "' to '" + result["new_name"] + "'"
                else:
                    reply = "I couldn't find '" + old_target + "'."

            elif mission["mission_type"] == "DELETE_FILE":
                target_input = mission.get("target_filename") or ""
                matched = find_matching_file(target_input)
                if matched:
                    deleted = delete_file(matched)
                    reply = "Deleted: " + deleted
                else:
                    reply = "I couldn't find a file matching '" + target_input + "'."

            elif mission["mission_type"] == "OPEN_APP":
                app_name = mission.get("app_name") or ""
                result = open_app(app_name)
                reply = result["message"]

            elif mission["mission_type"] == "ADD_PROJECT":
                proj_name = mission.get("project_name") or ""
                proj_folder = mission.get("project_folder") or ""
                if proj_name and proj_folder:
                    add_project(proj_name, proj_folder)
                    reply = "Registered project '" + proj_name + "' at " + proj_folder
                else:
                    reply = "I need both a project name and folder path."

            elif mission["mission_type"] == "OPEN_PROJECT":
                proj_name = mission.get("project_name") or ""
                result = open_project(proj_name)
                reply = result["message"]

            elif mission["mission_type"] == "CREATE_ROUTINE":
                routine_name = mission.get("routine_name") or ""
                if routine_name:
                    actions = parse_routine_actions(user_input, routine_name)
                    if actions:
                        add_routine(routine_name, actions)
                        action_list = "\n".join("- " + a["type"] + ": " + a["value"] for a in actions)
                        reply = "Created routine '" + routine_name + "':\n" + action_list + "\n\nSay 'run " + routine_name + "' to execute it."
                    else:
                        reply = "I couldn't figure out the actions. Try describing it more clearly."
                else:
                    reply = "I need a name for the routine."

            elif mission["mission_type"] == "RUN_ROUTINE":
                routine_name = mission.get("routine_name") or ""
                projects = load_projects()
                result = run_routine(routine_name, projects)
                if result["success"]:
                    steps = "\n".join(result["results"])
                    reply = "Ran routine '" + result["routine_name"] + "':\n\n" + steps
                else:
                    reply = result["message"]

            elif mission["mission_type"] == "CLIPBOARD_READ":
                clipboard_content = read_clipboard()
                last_ai_reply = ""
                for msg in reversed(st.session_state.conversation):
                    if msg["role"] == "assistant":
                        last_ai_reply = msg["content"]
                        break
                if clipboard_content and last_ai_reply:
                    combined = (
                        "The user said: '" + user_input + "'\n\n"
                        "Option A - Clipboard:\n" + clipboard_content[:500] + "\n\n"
                        "Option B - Last reply:\n" + last_ai_reply[:500] + "\n\n"
                        "Figure out which one they mean, act on it, briefly mention which you used."
                    )
                    reply = ask_ai([
                        {"role": "system", "content": "You are Legend AI."},
                        {"role": "user", "content": combined}
                    ])
                elif clipboard_content:
                    combined = "The user copied:\n\n" + clipboard_content + "\n\nRequest: " + user_input
                    reply = ask_ai([
                        {"role": "system", "content": "You are Legend AI."},
                        {"role": "user", "content": combined}
                    ])
                else:
                    reply = "Your clipboard is empty."

            elif mission["mission_type"] == "CLIPBOARD_WRITE":
                last_reply = ""
                for msg in reversed(st.session_state.conversation):
                    if msg["role"] == "assistant":
                        last_reply = msg["content"]
                        break
                if last_reply:
                    success = write_clipboard(last_reply)
                    reply = "Copied to clipboard." if success else "Failed to copy."
                else:
                    reply = "Nothing to copy yet."

            elif mission["mission_type"] == "TERMINAL":
                suggested_cmd = suggest_command(user_input, ask_ai)
                st.session_state.pending_command = suggested_cmd
                reply = "I'll run this command - please review and approve it above."

            else:
                reply = ask_ai(st.session_state.conversation)

        st.write(reply)

    st.session_state.conversation.append({"role": "assistant", "content": reply})
    save_conversation(st.session_state.conversation)
    speak(reply)
    st.rerun()
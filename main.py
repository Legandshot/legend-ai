"""
LEGEND AI - Main Program
-----------------------------------------
What this file does:
This is the ONE file you run. It ties everything together.
"""

import os
from dotenv import load_dotenv
from groq import Groq

from core.mission_engine import classify_mission, should_remember
from core.research_engine import run_research
from tools.file_tool import save_file, list_files, read_file, find_matching_file, delete_file, rename_file
from tools.search_tool import web_search
from memory.memory_store import load_memory, add_memory, memory_as_text
from memory.conversation_store import load_conversation, save_conversation

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

memories = load_memory()
saved_conversation = load_conversation()

print("=" * 50)
print("LEGEND AI")
if memories:
    print(f"(Loaded {len(memories)} memories from previous sessions)")
else:
    print("(No previous memories found - starting fresh)")

if saved_conversation:
    print(f"(Resuming previous conversation - {len(saved_conversation)} messages)")
else:
    print("(Starting a new conversation)")

print("Type your message. Type 'exit' to quit.")
print("=" * 50)

system_message = {
    "role": "system",
    "content": (
        "You are Legend AI, a personal AI operating system assistant. "
        f"Here is what you remember about the user so far:\n{memory_as_text(memories)}"
    )
}

if saved_conversation:
    conversation = [system_message] + saved_conversation[1:]
else:
    conversation = [system_message]

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("\nLegend AI: Goodbye. I'll remember what we talked about.")
        break

    check = should_remember(client, user_input)
    if check.get("should_remember") and check.get("fact"):
        memories = add_memory(memories, check["fact"])
        print(f"\n[Memory Saved] {check['fact']}")

    mission = classify_mission(client, user_input)
    print(f"\n[Mission Detected] Type: {mission['mission_type']} | Goal: {mission['goal']}")

    conversation.append({"role": "user", "content": user_input})

    if mission["mission_type"] == "TASK_FILE":
        print("\n[Legend AI is creating your file...]")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Legend AI. Write complete, well-formatted content for the user's request."},
                {"role": "user", "content": user_input}
            ]
        )
        content = response.choices[0].message.content
        filepath = save_file(mission.get("suggested_filename") or mission["goal"], content)

        print(f"\n✅ File created: {filepath}")
        print("\n--- Preview ---")
        print(content[:300] + ("..." if len(content) > 300 else ""))

        conversation.append({"role": "assistant", "content": f"I created the file: {filepath}"})

    elif mission["mission_type"] == "WEB_SEARCH":
        print("\n[Legend AI is searching the web...]")
        result = web_search(user_input)

        print(f"\nLegend AI: {result['answer']}")
        if result["sources"]:
            print("\nSources:")
            for s in result["sources"]:
                print(f"   - {s['title']}: {s['url']}")

        conversation.append({"role": "assistant", "content": result["answer"]})

    elif mission["mission_type"] == "RESEARCH":
        print("\n[Legend AI is researching this from multiple angles...]")
        result = run_research(client, user_input)

        print(f"\n[Searched]: {', '.join(result['queries_used'])}")
        print(f"\nLegend AI:\n{result['report']}")

        if result["sources"]:
            print("\nSources:")
            seen = set()
            for s in result["sources"]:
                if s["url"] not in seen:
                    print(f"   - {s['title']}: {s['url']}")
                    seen.add(s["url"])

        conversation.append({"role": "assistant", "content": result["report"]})

    elif mission["mission_type"] == "LIST_FILES":
        files = list_files()
        if files:
            print(f"\nLegend AI: Here are the files I've created:")
            for f in files:
                print(f"   - {f}")
        else:
            print("\nLegend AI: I haven't created any files yet.")

        conversation.append({"role": "assistant", "content": f"Files found: {files}"})

    elif mission["mission_type"] == "READ_FILE":
        target = mission.get("target_filename") or ""
        result = read_file(target)

        if result:
            print(f"\nLegend AI: Here's '{result['filename']}':\n")
            print(result["content"])
            conversation.append({"role": "assistant", "content": f"Read file {result['filename']} aloud."})
        else:
            print(f"\nLegend AI: I couldn't find a file matching '{target}'. Try 'list my files' to see what exists.")
            conversation.append({"role": "assistant", "content": f"Could not find file matching {target}."})

    elif mission["mission_type"] == "RENAME_FILE":
        old_target = mission.get("target_filename") or ""
        new_target = mission.get("new_filename") or ""

        result = rename_file(old_target, new_target)
        if result:
            print(f"\n✏️  Renamed '{result['old_name']}' -> '{result['new_name']}'")
            conversation.append({"role": "assistant", "content": f"Renamed {result['old_name']} to {result['new_name']}."})
        else:
            print(f"\nLegend AI: I couldn't find a file matching '{old_target}' to rename.")
            conversation.append({"role": "assistant", "content": f"Could not find file matching {old_target} to rename."})

    elif mission["mission_type"] == "DELETE_FILE":
        target_input = mission.get("target_filename") or ""
        matched = find_matching_file(target_input)

        if not matched:
            print(f"\nLegend AI: I couldn't find a file matching '{target_input}'. Try 'list my files' first.")
            conversation.append({"role": "assistant", "content": f"Could not find file matching {target_input} to delete."})
        else:
            confirm = input(f"\n⚠️  Legend AI: Are you sure you want to permanently delete '{matched}'? (yes/no): ")
            if confirm.lower() in ["yes", "y"]:
                deleted = delete_file(matched)
                print(f"\n🗑️  Deleted: {deleted}")
                conversation.append({"role": "assistant", "content": f"Deleted file {deleted}."})
            else:
                print("\nLegend AI: Okay, I won't delete it.")
                conversation.append({"role": "assistant", "content": "User cancelled deletion."})

    else:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation
        )
        reply = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": reply})
        print(f"\nLegend AI: {reply}")

    conversation = save_conversation(conversation)
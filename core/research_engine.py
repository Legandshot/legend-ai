"""
LEGEND AI - Research Engine
-----------------------------------------
What this file does:
Implements the Research Pipeline: break topic into angles,
search each, synthesize. Now uses the Model Router.
"""

import json
from core.model_router import ask_ai
from tools.search_tool import multi_angle_search


def plan_research_angles(topic):
    prompt = f"""
The user wants research on this topic: "{topic}"

Break this into 2-4 specific search queries that together would
give a well-rounded understanding of the topic.

Respond ONLY with valid JSON in this exact format:
{{"queries": ["query 1", "query 2", "query 3"]}}
"""
    raw = ask_ai([{"role": "user", "content": prompt}], temperature=0.3).strip()
    try:
        parsed = json.loads(raw)
        return parsed.get("queries", [topic])
    except json.JSONDecodeError:
        return [topic]


def synthesize_research(topic, findings):
    findings_text = ""
    for f in findings:
        findings_text += f"\n--- Findings for: {f['query']} ---\n{f['answer']}\n"

    prompt = f"""
You are Legend AI's Research Engine. You researched the topic
"{topic}" from multiple angles. Here are the raw findings:

{findings_text}

Write a clear, well-organized research summary with:
- A brief overview
- Key findings (organized by theme)
- Any notable disagreements or different perspectives
"""
    return ask_ai([{"role": "user", "content": prompt}])


def run_research(topic):
    queries = plan_research_angles(topic)
    findings = multi_angle_search(queries)
    report = synthesize_research(topic, findings)

    all_sources = []
    for f in findings:
        all_sources.extend(f["sources"])

    return {"report": report, "queries_used": queries, "sources": all_sources}
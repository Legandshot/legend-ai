"""
LEGEND AI - Web Search Tool
-----------------------------------------
What this file does:
Gives Legend AI two ways to use the internet:

  web_search()      -> one quick search, fast answer
  deep_research()   -> multiple searches from different angles,
                        cross-checked into one structured report
                        (matches the "Research Pipeline" concept
                        from the architecture)
"""

import os
from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
search_client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query):
    """One quick search. Returns a summarized answer plus sources."""
    result = search_client.search(
        query=query,
        search_depth="basic",
        include_answer=True,
        max_results=4
    )

    answer = result.get("answer", "")
    sources = [
        {"title": r.get("title", ""), "url": r.get("url", "")}
        for r in result.get("results", [])
    ]

    return {"answer": answer, "sources": sources}


def multi_angle_search(queries):
    """
    Runs several searches (one per angle/sub-question) and
    collects all the raw findings together before they get
    summarized by the AI.
    """
    all_findings = []

    for q in queries:
        result = search_client.search(
            query=q,
            search_depth="advanced",
            include_answer=True,
            max_results=3
        )
        all_findings.append({
            "query": q,
            "answer": result.get("answer", ""),
            "sources": [
                {"title": r.get("title", ""), "url": r.get("url", "")}
                for r in result.get("results", [])
            ]
        })

    return all_findings
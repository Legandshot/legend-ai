# 🧠 Legend AI

A personal AI Operating System built from scratch.

Instead of opening apps manually, you talk to Legend AI and it gets things done.

> "Continue my AI project" → Opens VS Code in the right folder
> "Research X" → Searches the web from multiple angles and summarizes
> "Write a blog post and save it" → Creates a real file on your computer
> "Run morning routine" → Opens Chrome, VS Code, anything you set up

---

## What it can do

- 💬 AI chat with memory across sessions
- 🔍 Quick web search + deep multi-angle research
- 📄 Create, read, rename, delete files
- 🖥️ Open applications by name
- 📁 Open projects in VS Code instantly
- ⚡ Run multi-step routines with one phrase
- 📋 Read and act on your clipboard content
- 🎤 Voice input — speak instead of type
- 🧠 Remembers facts about you across sessions
- 🔄 Groq AI with automatic Gemini fallback

---

## Setup

### 1. Install Python, Git, VS Code

### 2. Clone the repo
git clone https://github.com/Legandshot/legend-ai.git
cd legend-ai

### 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 4. Install dependencies
pip install groq tavily-python streamlit python-dotenv google-genai pyperclip SpeechRecognition sounddevice scipy

### 5. Create your `.env` file
Create a file called `.env` in the root folder:
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
GEMINI_API_KEY=your_gemini_key_here

**Free API keys:**
- Groq: https://console.groq.com
- Tavily: https://tavily.com
- Gemini: https://aistudio.google.com/apikey

### 6. Run
streamlit run app.py

---

## Project Structure
legend-ai/
├── app.py                  # Main desktop UI
├── core/
│   ├── model_router.py     # AI provider with fallback
│   ├── mission_engine.py   # Intent classification
│   └── research_engine.py  # Multi-angle research
├── tools/
│   ├── file_tool.py        # File management
│   ├── search_tool.py      # Web search
│   ├── system_tool.py      # Open applications
│   ├── project_tool.py     # Project management
│   ├── routine_tool.py     # Workflow automation
│   ├── clipboard_tool.py   # Clipboard access
│   └── voice_tool.py       # Voice input
└── memory/
├── memory_store.py     # Persistent fact memory
└── conversation_store.py # Session continuity

---

## Built by

Mayur ([@Legandshot](https://github.com/Legandshot))

Built from scratch in one day with zero prior coding experience.

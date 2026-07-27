<div align="center">

<h1>⚡ InsightForge AI</h1>
<h3>Autonomous Multi-Agent Strategic Research Platform</h3>

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-Orchestration-FF6B6B?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Gemini_AI-2.0_Flash_%7C_2.5_Pro-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector_Store-6B46C1?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p><em>An end-to-end, production-grade AI research pipeline that autonomously plans, searches, analyzes, critiques, visualizes, and writes structured intelligence reports — powered by Google Gemini and orchestrated with LangGraph.</em></p>

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Agent Pipeline](#-agent-pipeline)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Docker Deployment](#-docker-deployment)
- [How It Works — Deep Dive](#-how-it-works--deep-dive)
- [API Keys & Models](#-api-keys--models)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

**InsightForge AI** is a fully autonomous, multi-agent AI research system built with **LangGraph**, **Google Gemini**, and **Streamlit**. It replaces manual research workflows with a self-correcting, graph-based agent pipeline.

Given any research topic, the system:

1. 🧠 **Plans** — A Supervisor agent decomposes the topic into structured research sub-goals.
2. 🔎 **Searches** — A Researcher agent runs live DuckDuckGo web searches and stores findings in a ChromaDB vector store.
3. 🔬 **Analyzes** — An Analyzer agent retrieves relevant context from vector memory and synthesizes key insights.
4. ⚖️ **Critiques** — A Critic agent evaluates the analysis for bias, hallucinations, and gaps. If it fails, the loop runs again.
5. 📊 **Visualizes** — A Visualizer agent generates AI-written Plotly Python code that is dynamically executed to produce interactive charts.
6. 📄 **Writes** — A Writer agent compiles everything into a professional, structured intelligence report.

All runs are persisted to SQLite, accessible from the History panel, and exportable as `.docx`.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        InsightForge AI — System Architecture                    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     STREAMLIT FRONTEND  (app.py)                        │   │
│  │  ┌────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │   │
│  │  │ Research   │  │   History    │  │   Settings   │  │   Report    │  │   │
│  │  │ Workspace  │  │    Panel     │  │    Panel     │  │   Viewer    │  │   │
│  │  └────────────┘  └──────────────┘  └──────────────┘  └─────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                   LANGGRAPH ORCHESTRATION ENGINE                        │   │
│  │                       (src/graph/workflow.py)                           │   │
│  │                                                                         │   │
│  │  ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────────┐    │   │
│  │  │Supervisor│───▶│Researcher │───▶│ Analyzer │───▶│    Critic    │    │   │
│  │  │  Agent   │    │  Agent    │    │  Agent   │    │    Agent     │    │   │
│  │  └──────────┘    └───────────┘    └──────────┘    └──────┬───────┘    │   │
│  │                                                           │            │   │
│  │                             ┌───── PASS ─────────────────┘            │   │
│  │                             │      FAIL → loops back to Analyzer       │   │
│  │                             ▼                                          │   │
│  │                    ┌─────────────┐     ┌──────────┐                   │   │
│  │                    │  Visualizer │────▶│  Writer  │────▶  END         │   │
│  │                    │    Agent    │     │  Agent   │                   │   │
│  │                    └─────────────┘     └──────────┘                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌──────────────────────────┐    ┌──────────────────────────────────────────┐  │
│  │     STORAGE LAYER        │    │           LLM / TOOLS LAYER              │  │
│  │                          │    │                                          │  │
│  │  ChromaDB (Vector Store) │    │  Google Gemini API                       │  │
│  │  • Gemini Embeddings     │    │  • gemini-2.0-flash  (primary)           │  │
│  │  • Persistent local DB   │    │  • gemini-2.5-flash  (fallback)          │  │
│  │  • Semantic retrieval    │    │  • gemini-2.5-pro    (fallback)          │  │
│  │                          │    │  • Auto-retry + quota-aware switching    │  │
│  │  SQLite3                 │    │                                          │  │
│  │  • research_history.db   │    │  DuckDuckGo Search (DDGS)                │  │
│  │  • Full CRUD history     │    │  Plotly Code Execution Sandbox           │  │
│  └──────────────────────────┘    └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Pipeline

The pipeline is a **directed state graph** powered by LangGraph. Every node is a pure function that receives and mutates the shared `AgentState` TypedDict object.

```
                ┌──────────────────────────────────────────────────────┐
                │              AgentState  (Shared Context)             │
                │                                                        │
                │  topic             → User's research query             │
                │  plan              → Supervisor's research outline     │
                │  research_data     → Raw DuckDuckGo search results     │
                │  analysis          → Synthesized key insights          │
                │  critique_feedback → "PASS" or specific corrections    │
                │  iterations        → Critic self-correction counter    │
                │  max_iterations    → Configured from UI settings       │
                │  visuals           → Plotly chart JSON string          │
                │  report            → Final structured markdown report  │
                │  current_agent     → Live agent tracking for UI        │
                │  error             → Failure capture field             │
                └──────────────────────────────────────────────────────┘
                                         │
   ┌─────────────────────────────────────┼────────────────────────────────────┐
   ▼                                     ▼                                    ▼

┌───────────────────┐   ┌────────────────────────────┐   ┌─────────────────────┐
│  1. SUPERVISOR    │   │  2. RESEARCHER              │   │  3. ANALYZER        │
│───────────────────│   │────────────────────────────│   │─────────────────────│
│ • Receives topic  │──▶│ • Generates search queries  │──▶│ • Queries ChromaDB  │
│ • Prompts Gemini  │   │   via Gemini                │   │   top-5 semantic    │
│ • Breaks topic    │   │ • Executes DuckDuckGo DDGS  │   │   matches           │
│   into 4 focused  │   │ • Stores results in ChromaDB│   │ • Synthesizes docs  │
│   sub-goals       │   │   with Gemini embeddings    │   │   into structured   │
│ • Writes plan     │   │ • Stores raw data in state  │   │   analysis          │
└───────────────────┘   └────────────────────────────┘   └────────────┬────────┘
                                                                        │
                                                                        ▼
                                                          ┌─────────────────────────┐
                                                          │  4. CRITIC              │
                                                          │─────────────────────────│
                                                          │ • Reviews analysis for: │
                                                          │   - Bias / skew         │
                                                          │   - Hallucinations      │
                                                          │   - Missing context     │
                                                          │ • Returns "PASS"        │
                                                          │   or specific feedback  │
                                                          └────────────┬────────────┘
                                                                       │
                                              ┌─── PASS ──────────────┘
                                              │
                       ┌──────────────────────┴─────────────────────────┐
                       │   FAIL  (and iterations < max_iterations)       │
                       │        → loop back to Analyzer to improve       │
                       └─────────────────────────────────────────────────┘
                                              │ PASS
                                              ▼
                                  ┌──────────────────────────┐
                                  │  5. VISUALIZER           │
                                  │──────────────────────────│
                                  │ • Prompts Gemini to      │
                                  │   write Plotly Express   │
                                  │   Python code            │
                                  │ • Sandboxed exec()       │
                                  │   with pd/px/go injected │
                                  │ • 2 retry attempts       │
                                  │ • Falls back gracefully  │
                                  └────────────┬─────────────┘
                                               │
                                               ▼
                                  ┌──────────────────────────┐
                                  │  6. WRITER               │
                                  │──────────────────────────│
                                  │ • Generates full 8-      │
                                  │   section professional   │
                                  │   intelligence report    │
                                  │ • Exportable as .docx    │
                                  └──────────────────────────┘
```

---

## 📂 Project Structure

```
insightforge-ai/
│
├── app.py                          # Main Streamlit application & UI entry point
│
├── src/
│   ├── __init__.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py                # AgentState TypedDict — shared pipeline schema
│   │   └── workflow.py             # LangGraph StateGraph builder & conditional edges
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── supervisor.py           # Plan generation + NativeGeminiLLM resilience wrapper
│   │   ├── researcher.py           # Live web search + ChromaDB document ingestion
│   │   ├── analyzer.py             # Vector retrieval + insight synthesis
│   │   ├── critic.py               # Quality control + self-correction loop trigger
│   │   ├── visualizer.py           # AI-generated Plotly chart code + execution
│   │   └── writer.py               # Final structured 8-section report generation
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── code_execution.py       # Sandboxed Python exec() environment for charts
│   │   └── pdf_reader.py           # PDF text extraction with PyMuPDF
│   │
│   └── utils/
│       ├── __init__.py
│       ├── db.py                   # SQLite3 CRUD layer for research run history
│       └── memory.py               # ChromaDB MemoryStore + Gemini EmbeddingFunction
│
├── assets/
│   └── style.css                   # Custom Streamlit CSS design system (dark theme)
│
├── chroma_db/                      # Persistent ChromaDB vector store (auto-created)
├── reports/                        # Exported .docx report files
├── research_history.db             # SQLite run history database (auto-created)
│
├── Dockerfile                      # Production Docker image definition
├── requirements.txt                # Python package dependencies
├── pyproject.toml                  # Pyright/Pylance type-checking configuration
├── .env.example                    # Environment variable template (safe to commit)
├── .env                            # Local secrets — NEVER commit this file
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Orchestration** | [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful multi-agent directed graph with conditional edges |
| **LLM** | [Google Gemini](https://ai.google.dev/) 2.0 Flash / 2.5 Pro | Reasoning, planning, writing, code generation |
| **Embeddings** | `models/embedding-001` (Gemini) | Semantic vector encoding of web search results |
| **Vector Store** | [ChromaDB](https://www.trychroma.com/) | Persistent local semantic search memory |
| **Web Search** | DuckDuckGo Search (`ddgs`) | Live, no-API-key-needed internet research |
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive dashboard & report UI |
| **Charts** | [Plotly Express](https://plotly.com/python/) | AI-generated dynamic interactive visualizations |
| **Database** | SQLite3 (stdlib) | Lightweight research history persistence |
| **Document Export** | `python-docx` | Word `.docx` formatted report export |
| **Containerization** | Docker | Portable, reproducible production deployment |
| **PDF Parsing** | PyMuPDF (`fitz`) | PDF document ingestion as research input |
| **Type Safety** | Pyright + Pylance | Static type analysis across the codebase |

---

## ✨ Features

### 🔄 Self-Correcting Agent Loop
The Critic agent evaluates every analysis before passing it to the report writer. If quality checks fail (hallucinations, missing context, bias detected), the pipeline automatically loops back to the Analyzer for refinement — up to a configurable maximum iteration count set from the UI.

### 🧠 Intelligent Model Fallback (`NativeGeminiLLM`)
The custom `NativeGeminiLLM` wrapper in `supervisor.py` builds resilience directly into the LLM layer:
- Prioritized model pool: `gemini-2.0-flash → gemini-flash-latest → gemini-2.5-flash → gemini-2.5-pro`
- On `429 / Quota Exceeded`: waits briefly and retries the same model once, then cascades to next
- On `404 / Model Not Found`: immediately skips to next model in pool
- Zero user intervention required — fully automatic

### 🔗 Persistent Vector Memory (RAG)
Every DuckDuckGo web search result is stored as a document in ChromaDB using Gemini embeddings. The Analyzer performs semantic retrieval (`top_k=5`) so its analysis is always grounded in real retrieved information — not parametric hallucination.

### 📊 Executable AI-Generated Charts
The Visualizer prompts Gemini to write valid Plotly Express Python code, then executes it in a sandboxed `exec()` environment with `pandas`, `plotly.express`, and `plotly.graph_objects` pre-injected. The resulting `plotly.Figure` is serialized to JSON and rendered as a fully interactive chart in Streamlit.

### 🕒 Full Research History
Every research run is stored in SQLite with topic, full markdown report, and chart JSON. The History panel enables loading, re-reading, and deleting any past session.

### 📤 Export to DOCX
Reports can be exported as formatted Microsoft Word `.docx` documents with proper heading hierarchy (H1/H2/H3), ready for sharing or printing.

### ⚙️ Runtime-Configurable Settings
Configure everything from the UI without touching code:
- **Gemini Model**: Select from available model variants
- **Max Critique Iterations**: Balance quality vs. speed
- **Web Search Toggle**: Enable/disable live DuckDuckGo access
- **Vision Core Toggle**: Enable/disable vision-based processing

---

## 📋 Prerequisites

- **Python** `3.11+`
- **pip** or `uv`
- A **Google AI Studio API Key** — get one free at [aistudio.google.com](https://aistudio.google.com)
- *(Optional)* **Docker** for containerized deployment

> **Windows users:** `chromadb` requires C++ build tools. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) if you encounter compilation errors during `pip install`.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/insightforge-ai.git
cd insightforge-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Copy the environment template:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# ── Required ──────────────────────────────────────────────────────────────────
GOOGLE_API_KEY="your_google_ai_studio_api_key_here"

# ── Model Selection (can also be changed from the UI at runtime) ───────────────
GEMINI_MODEL_VERSION="gemini-2.0-flash"

# ── Optional: LangSmith Agent Tracing ─────────────────────────────────────────
LANGCHAIN_TRACING_V2="false"
LANGCHAIN_API_KEY="your_langchain_api_key_here"
LANGCHAIN_PROJECT="InsightForge_Agent"

# ── Optional: Ollama Local Model Fallback ──────────────────────────────────────
OLLAMA_BASE_URL="http://localhost:11434"
```

> ⚠️ **Never commit your `.env` file.** The `.gitignore` already excludes it.

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**.

---

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t insightforge-ai .
```

### Run the Container

```bash
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY="your_api_key_here" \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/research_history.db:/app/research_history.db \
  insightforge-ai
```

> `-v` volume mounts preserve ChromaDB and SQLite data across container restarts.

### Docker Compose (Recommended for Production)

```yaml
version: "3.9"

services:
  insightforge:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - GEMINI_MODEL_VERSION=gemini-2.0-flash
    volumes:
      - ./chroma_db:/app/chroma_db
      - ./research_history.db:/app/research_history.db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
docker compose up --build -d
```

---

## 🔬 How It Works — Deep Dive

### LangGraph State Machine

The orchestration core is in [`src/graph/workflow.py`](src/graph/workflow.py). The graph is compiled from a `StateGraph(AgentState)` where every agent node is a function `(AgentState) -> AgentState`.

The critical design is the **conditional edge** from the Critic:

```python
def should_continue(state: AgentState):
    # PASS: proceed to visualization and report generation
    if state.get("critique_feedback") == "PASS":
        return "visualizer"

    # Check if we've hit the max retry limit
    iters = state.get("iterations", 0)
    max_iters = state.get("max_iterations", 1)

    if iters >= max_iters:
        return "visualizer"     # Force-proceed even on partial failure
    else:
        return "analyzer"       # Loop back to Analyzer for improvement

workflow.add_conditional_edges(
    "critic",
    should_continue,
    {"visualizer": "visualizer", "analyzer": "analyzer"}
)
```

This creates a **self-correcting feedback loop** bounded by `max_iterations` — configurable from the UI.

---

### NativeGeminiLLM — Resilient API Wrapper

Rather than using LangChain's built-in Gemini wrappers (which lack fine-grained quota handling), the project implements a custom `NativeGeminiLLM` class in [`src/agents/supervisor.py`](src/agents/supervisor.py):

```python
class NativeGeminiLLM:
    def __init__(self, model_name=None):
        self.model_pool = [
            "gemini-2.0-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ]
        self.primary_model = model_name or os.getenv("GEMINI_MODEL_VERSION", "gemini-2.0-flash")
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def invoke(self, prompt: str, retries=2):
        # Try primary model first, then fallback through pool
        models_to_try = [self.primary_model] + [m for m in self.model_pool if m != self.primary_model]

        for model in models_to_try:
            for attempt in range(retries):
                try:
                    response = self.client.models.generate_content(model=model, contents=prompt)
                    if response and response.text:
                        return MockLangChainResponse(content=response.text)
                except Exception as e:
                    if "404" in str(e):
                        break            # Skip to next model immediately
                    if "429" in str(e) or "quota" in str(e).lower():
                        time.sleep(2)    # Brief backoff then retry / cascade
                        if attempt < retries - 1:
                            continue
                        break
                    break
```

This provides **zero-downtime quota resilience** — critical for agentic workloads where multiple LLM calls happen in sequence within the same pipeline run.

---

### ChromaDB Vector Memory (RAG Layer)

The `MemoryStore` class in [`src/utils/memory.py`](src/utils/memory.py) wraps ChromaDB with Gemini's embedding model:

```python
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.encoder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def __call__(self, input: Documents) -> Embeddings:
        return cast(Embeddings, self.encoder.embed_documents(input))
```

**Ingestion** (in Researcher agent):
```python
memory.add_documents(
    documents=[search_result_text],
    metadata=[{"query": q, "topic": topic}],
    ids=[str(uuid.uuid4())]
)
```

**Retrieval** (in Analyzer agent):
```python
docs = memory.query(query_text=topic, n_results=5)
# Returns top-5 semantically similar documents
```

This implements a classic **Retrieval-Augmented Generation (RAG)** pattern: search → embed → store → retrieve → synthesize.

---

### AI-Generated & Executed Plotly Code

The Visualizer is the most technically advanced component. The flow is:

1. Gemini is prompted to write valid `plotly.express` Python code
2. Code is extracted from the markdown response with regex
3. Code is passed to [`execute_chart_code()`](src/tools/code_execution.py)
4. The function runs the code via `exec()` in an isolated namespace with `pd`, `px`, `go` pre-injected
5. The resulting `fig` variable is serialized with `fig.to_json()`
6. Streamlit renders the JSON as a fully interactive Plotly chart

```python
exec_globals = {
    "pd": importlib.import_module("pandas"),
    "px": importlib.import_module("plotly.express"),
    "go": importlib.import_module("plotly.graph_objects")
}
exec(python_code, exec_globals, local_vars)

if "fig" in local_vars and hasattr(local_vars["fig"], "to_json"):
    return {"success": True, "data": local_vars["fig"].to_json()}
```

If execution fails after 2 attempts, a graceful hardcoded fallback chart is used — ensuring the pipeline always completes.

---

## 📊 API Keys & Models

### Gemini Model Comparison

| Model | Speed | Intelligence | Free Quota |
|---|---|---|---|
| `gemini-2.0-flash` | ⚡⚡⚡ Fastest | Good | Very generous |
| `gemini-2.5-flash` | ⚡⚡ Fast | Very Good | Moderate |
| `gemini-2.5-pro` | ⚡ Slower | Best | Limited |

> Get your free API key at **[aistudio.google.com](https://aistudio.google.com)**. The free tier is sufficient for development and testing.

---

## 🗄️ Database Schema

### SQLite — `research_history.db`

```sql
CREATE TABLE IF NOT EXISTS research_runs (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    topic       TEXT     NOT NULL,  -- Original user research topic
    query       TEXT     NOT NULL,  -- Structured sub-query used in the run
    report      TEXT     NOT NULL,  -- Full markdown report output
    visuals     TEXT     NOT NULL,  -- Plotly chart JSON (JSON-stringified)
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**CRUD Functions:**
| Function | Description |
|---|---|
| `init_db()` | Creates table if it doesn't exist (called on startup) |
| `save_run(topic, query, report, visuals)` | Persists a completed research run |
| `get_all_runs()` | Fetches all runs (metadata only, no heavy fields) |
| `get_run_by_id(id)` | Fetches full run with report and visuals |
| `delete_run(id)` | Removes a specific run by ID |
| `clear_all_runs()` | Wipes all history |

### ChromaDB — `chroma_db/`

| Property | Value |
|---|---|
| Collection Name | `tnra_research` |
| Embedding Model | `models/embedding-001` (Gemini) |
| Client Type | `PersistentClient` (disk-backed) |
| Metadata per Document | `{ "query": "...", "topic": "..." }` |
| Retrieval Method | Semantic nearest-neighbor (`query_texts`, `n_results=5`) |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** your feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Write** your code following the conventions below
4. **Test** your changes manually
5. **Commit** using conventional commits:
   ```bash
   git commit -m "feat: add PDF upload as research input"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open** a Pull Request with a clear description

### Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use for |
|---|---|
| `feat:` | A new feature or capability |
| `fix:` | A bug fix |
| `docs:` | Documentation changes only |
| `refactor:` | Code restructuring without feature/fix |
| `chore:` | Dependencies, config, tooling |
| `test:` | Adding or updating tests |

### Code Style Guidelines

- Follow **PEP 8** for Python code formatting
- **Type-hint all function signatures** — the codebase is fully typed
- Keep agents **pure functions**: `(AgentState) -> AgentState` — no hidden side-effects outside their designated storage layer
- Use `print()` with clear prefixes for agent logging: `[AgentName] message`

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

See the [LICENSE](LICENSE) file for the full license text.

---

## 🙏 Acknowledgements

- **[LangGraph](https://github.com/langchain-ai/langgraph)** by LangChain — for the elegant stateful agent graph framework
- **[Google Gemini](https://ai.google.dev/)** — for the powerful LLM and embedding models powering every agent
- **[ChromaDB](https://www.trychroma.com/)** — for the fast, embedded vector database
- **[Streamlit](https://streamlit.io/)** — for making production-quality data apps simple to build
- **[Plotly](https://plotly.com/)** — for the interactive charting library

---

<div align="center">
  <p>Built with ❤️ — <strong>InsightForge AI</strong></p>
  <p><em>Autonomous Intelligence. Structured Insight.</em></p>
  <br/>
  <a href="https://github.com/YOUR_USERNAME/insightforge-ai/issues">Report Bug</a> ·
  <a href="https://github.com/YOUR_USERNAME/insightforge-ai/issues">Request Feature</a>
</div>

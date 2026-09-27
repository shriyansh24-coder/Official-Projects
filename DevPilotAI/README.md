# ◈ DevPilot AI

**DevPilot AI** is a desktop AI development command center built with Python and PyQt5. It helps developers inspect projects, review code, debug problems, analyze project structure, generate tests, scan for security issues, and inspect Git changes from one dark developer-focused interface.

## Features

- **Command Center** — project-aware AI assistant.
- **Project Explorer** — open a local project, browse files, and inspect source code.
- **Project Memory / RAG** — retrieves relevant project code before sending a question to Gemini.
- **AI Code Review** — reviews project code and reports findings.
- **AI Debugger** — helps investigate code and runtime issues.
- **Project Analysis** — analyzes the selected project.
- **Test Generator** — generates test suggestions for project code.
- **Security Scanner** — checks project code for security concerns.
- **Git Integration** — branch, working-tree status, changed files, diffs, and recent commits.
- **Repository-aware Git handling** — correctly handles projects nested inside a larger Git repository.
- **Dark AI Command Center UI** — built around an Obsidian + Electric Cyan visual style.

## Tech Stack

- Python
- PyQt5
- Google Gemini API via `google-genai`
- `python-dotenv`
- Git / Git CLI
- Qt `QThread` workers for long-running AI operations
- Local keyword-based project retrieval for lightweight RAG

## Architecture

```text
DevPilotAI/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── ai/
│   ├── client.py
│   ├── rag.py
│   └── __init__.py
├── pages/
│   ├── dashboard.py
│   ├── project_explorer.py
│   ├── code_review.py
│   ├── debugger.py
│   ├── project_analysis.py
│   ├── test_generator.py
│   ├── security.py
│   ├── git_page.py
│   └── __init__.py
├── services/
│   ├── file_service.py
│   ├── project_context.py
│   ├── project_memory.py
│   ├── git_service.py
│   └── __init__.py
└── ui/
    ├── main_window.py
    ├── sidebar.py
    ├── theme.py
    └── __init__.py
```

## How Project-Aware AI Works

```text
Open Project
     ↓
Project Scanner
     ↓
Project Memory
     ↓
Keyword Retrieval
     ↓
Relevant Code Context
     ↓
Gemini API
     ↓
DevPilot Response
```

The application does not send the entire project for every question. It first searches locally indexed project chunks and uses the most relevant results as AI context.

## Supported Source Files

Project memory currently supports common source/configuration formats including:

`.py` `.c` `.cpp` `.h` `.hpp` `.java` `.js` `.jsx` `.ts` `.tsx` `.html` `.css` `.sql` `.json` `.xml` `.md`

## Requirements

- Python 3.10+ recommended
- Git installed and available on `PATH`
- A Gemini API key
- Windows/Linux/macOS with a working PyQt5 environment

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd DevPilotAI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env` and add your API key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

**Never commit `.env` or your real API key.** `.env` is already excluded by `.gitignore`.

### 5. Run DevPilot

```bash
python main.py
```

## Usage

1. Launch DevPilot AI.
2. Open a local project from **Project Explorer**.
3. Use **Command Center** to ask project-aware questions.
4. Run Code Review, Debugger, Project Analysis, Test Generator, or Security Scanner as needed.
5. Use **Git** to inspect the selected project's branch, changes, diffs, and recent commits.

## Security Notes

- API credentials are loaded from environment variables.
- Real `.env` files should never be committed.
- The application reads local project files selected by the user.
- AI-generated analysis should be reviewed by the developer before applying changes.

## Project Status

DevPilot AI's core portfolio features are implemented and manually tested, including project-aware AI, RAG/project memory, code review, debugging, project analysis, test generation, security scanning, and Git integration.

## Future Improvements

Possible future work includes stronger semantic/vector retrieval, richer Git actions, automated test execution, configurable model settings, and additional language support.

## Author

**Shriyansh**

Built as a portfolio project focused on practical AI-assisted software development.
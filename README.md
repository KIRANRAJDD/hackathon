# AI Test Generator System

An intelligent, full-stack application that analyzes source code and automatically generates Unit, Integration, and Edge Case tests using AI.

## Features
- **FastAPI Backend:** Blazing fast Python API that extracts code ASTs and orchestrates prompt generation.
- **Premium Frontend:** A beautifully designed Vanilla HTML/JS/CSS interface featuring dark mode and glassmorphism. Works instantly without Node.js.
- **Auto-Formatting:** Generates separate code blocks for unit tests, integration tests, and edge cases, and saves them locally.

## Getting Started

### 1. Setup the Backend
The backend is written in Python. Ensure you have Python 3.9+ installed.

```bash
cd backend
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure the LLM
By default, the application runs in **Mock Mode**, meaning it returns static simulated responses so you can test the UI functionality immediately.

To use a real AI like OpenAI or Gemini, edit `backend/core/config.py`:
- Set `USE_MOCK_LLM = False`
- Set your `OPENAI_API_KEY` or `GEMINI_API_KEY`.
- Also update `backend/core/llm_engine.py` to uncomment the actual provider integrations.

### 3. Run the Backend Server
```bash
python main.py
```
*The server will start on http://localhost:8000.*

### 4. Open the UI
Since the frontend uses pure HTML/CSS/JS without Node.js tooling:
Simply double click `frontend/index.html` to open it in your browser!

Paste your source code in the left pane, click "**Generate Test Suite**", and enjoy the results!

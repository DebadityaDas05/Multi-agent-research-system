# ResearchMind 🔬 — Multi-Agent AI Research Assistant

ResearchMind is an advanced multi-agent research system powered by LangChain, Google Gemini, and Streamlit. It automates the process of researching any topic by orchestrating four specialized agents and chains (Search, Reader, Writer, and Critic) working in a collaborative pipeline to produce detailed, fact-checked, and critic-scored reports.

---

## 🚀 Key Features

- **Multi-Agent Orchestration:** Specialized agents execute tasks sequentially with dedicated tools.
- **Premium User Interface:** A modern, sleek glassmorphism Streamlit UI with dark mode, custom typography (Syne, DM Sans, DM Mono), and real-time step visualization.
- **Dynamic Research Pipeline:**
  1. **Search Agent:** Conducts a web search (via Tavily) to retrieve titles, URLs, and summaries.
  2. **Reader Agent:** Dynamically scrapes the most relevant URL for deep, context-rich extraction.
  3. **Writer Chain:** Synthesizes gathered data into a structured Markdown research report.
  4. **Critic Chain:** Performs a rigorous evaluation, scoring, and providing actionable feedback.
- **Dual Interface:** Run it as a web app using Streamlit or run the CLI research pipeline.
- **Export Formats:** One-click download of the generated report in Markdown format.

---

## 🛠️ Architecture & Agent Flow

The system runs a structured pipeline where each step feeds its state into the next:

![ResearchMind Architecture Diagram](assets/architecture_diagram.png)

### Agent Flow
```mermaid
graph TD
    User([User Prompt / Topic]) --> SearchAgent[01. Search Agent <br><i>Tavily Web Search</i>]
    SearchAgent -->|Top Results & snippets| ReaderAgent[02. Reader Agent <br><i>Web Scraper</i>]
    ReaderAgent -->|Full page text| Writer[03. Writer Chain <br><i>Report Drafting</i>]
    Writer -->|Draft Report| Critic[04. Critic Chain <br><i>Review & Scoring</i>]
    Critic -->|Score, Feedback, Verdict| Done([Final Output & Download])
```

---

## ⚙️ Installation & Setup

### 1. Clone & Navigate to Project Directory
```bash
git clone https://github.com/DebadityaDas05/Multi-agent-research-system.git
cd Multi-agent-research-system
```

### 2. Set Up a Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (CMD):
.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Tavily Search API Key
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## 🖥️ Usage

### Option A: Web Application (Recommended)
Launch the interactive Streamlit dashboard:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to experience the premium dark-themed UI.

### Option B: CLI Pipeline
Run the research pipeline directly from the command line:
```bash
python pipeline.py
```
You will be prompted to enter a topic, and the progress/results will be printed directly in the terminal.

---

## 📂 Project Structure

- `app.py`: The entry point for the Streamlit web app, containing layout, styles, and dashboard logic.
- `pipeline.py`: Defines `run_research_pipeline()` and acts as the CLI entry point.
- `agents.py`: Configures the Google Gemini LLM (`gemini-3.1-flash-lite`), agents, prompts, and chains.
- `tools.py`: Contains custom LangChain tools:
  - `web_search`: Uses Tavily API to gather relevant information.
  - `scrape_url`: Uses `requests` and `BeautifulSoup4` to clean and extract web pages.
- `requirements.txt`: Project dependencies list.
- `pyrightconfig.json`: Configuration for the Python type checker (Pyright).
- `.env`: Environment variables container (ignored by Git).

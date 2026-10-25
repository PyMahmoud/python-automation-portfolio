# Python Automation Portfolio

Python scripts, web tools, APIs, and AI agents for automating Excel, CSV, and web data tasks — cleaning, merging, analyzing, reporting, and delivering — plus hands-on LLM work: tool-calling assistants, document Q&A (RAG), and agents with long-term memory.

Drop a messy spreadsheet in. Get a clean, professional report out — or have it emailed automatically. Ask questions about a document and get answers grounded in its actual content.

---

## 🚀 Live Demos

**Try the apps instantly — no installation needed:**

👉 [Data Cleaner Pro](https://mahmoud-data-cleaner.streamlit.app) — Upload messy CSV/Excel → get a clean formatted report

👉 [Web Scraper Pro](https://mahmoud-web-scraper.streamlit.app) — Enter a URL → scrape data → download as Excel

👉 [Multi-Page Scraper Pro](https://mahmoud-multi-scraper.streamlit.app) — Scrape multiple pages automatically → download as Excel

---

## Before & After

![Before](screenshots/before.png)
![After](screenshots/after.png)

---

## App Screenshot

![App Screenshot](screenshots/app_screenshot.png)

---

## What These Scripts Do

Every script here solves a real business problem: messy data comes in, clean results go out — automatically, without touching the original files. The AI scripts apply the same idea to unstructured input: messy text and documents in, structured answers and actions out.

---

## Contents

- [Data & Reporting Tools](#data--reporting-tools)
- [Web Scraping](#web-scraping)
- [AI & LLM Automation](#ai--llm-automation)
- [How to Run](#how-to-run)
- [Requirements](#requirements)

---

# Data & Reporting Tools

### `data_cleaner_app.py` — Data Cleaner Pro (Live Web App)

A full web application that cleans messy CSV and Excel files through a browser — no Python knowledge required.

**🔗 Live demo: [mahmoud-data-cleaner.streamlit.app](https://mahmoud-data-cleaner.streamlit.app)**

**How to use:**
1. Upload one or multiple CSV or Excel files using the upload button
2. Choose your mode — Clean Only or Clean + Summary Report
3. Optionally sort the data by any column
4. In Summary mode, pick the numeric column to analyze — totals, averages, and highest values are calculated automatically
5. Optionally highlight any row with a custom color
6. Click Download to get your clean, formatted Excel file

**What it does:**
- Removes duplicate rows automatically
- Fixes text casing and strips extra spaces across all columns
- Fills empty numeric cells with 0 and empty text cells with N/A
- Generates a Summary sheet with groupby analysis when requested
- Applies bold headers to all sheets
- Highlights any row in any color the user chooses
- Outputs a multi-sheet formatted Excel file ready to deliver to clients

Built with Streamlit — runs in any browser, no Python knowledge needed.

---

### `fastapi_cleaner.py` — CSV Cleaning API

A backend API that accepts a CSV upload and returns a cleaned Excel file — built for integrating into other apps and client systems, not just browser use.

**How to use:**
1. Run the server locally with uvicorn
2. Open the interactive docs at `/docs`
3. Upload a CSV file to the `/clean` endpoint and execute
4. Receive a cleaned, formatted Excel file back in the response

**What it does:**
- Accepts any CSV file via a POST request
- Strips whitespace and standardizes text casing across all columns
- Removes duplicate rows
- Fills empty numeric cells with 0 and empty text cells with N/A
- Returns a downloadable Excel file directly in the response — nothing is saved to disk
- Returns a proper 400 error if no data remains after cleaning

Built with FastAPI and pandas.

---

### `email_sender.py` — Automated Report Delivery

Sends a cleaned report as an email attachment automatically — no manual downloading or attaching required.

**What it does:**
- Logs in securely using a Gmail App Password, never a real account password
- Builds a complete email with subject, body, and attachment
- Attaches the cleaned Excel file directly
- Sends and closes the connection automatically

**Setup:**
Create a `.env` file in the same folder (never committed to this repo):
```
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIEVER_EMAIL=recipient_email@gmail.com
```

Built with smtplib and python-dotenv.

---

### `sales_report_generator.py` — Multi-File Sales Report

Takes a folder of raw CSV sales files and outputs a single clean Excel report.

- Reads all CSV files in the folder automatically — no manual file selection
- Removes duplicates, fixes text casing, strips extra spaces, fills empty cells
- Calculates total sales, average sale, and highest sale per salesperson
- Highlights the top salesperson row in green
- Outputs `final_report.xlsx` with bold headers and frozen top row
- Never modifies the original CSV files

---

### `pandas_cleaner.py` — One-Command CSV Cleaner

Cleans any messy CSV file automatically.

- Removes duplicate rows
- Fixes inconsistent text casing and strips extra spaces across all text columns
- Fills empty cells with "N/A"
- Reports exactly how many duplicates were removed and how many empty cells were filled
- Saves cleaned output to Excel without touching the original file

---

### `pandas_report.py` — Multi-CSV Merge & Summary

Merges multiple CSV files and generates a grouped sales summary report.

- Reads and merges all CSV files in the folder automatically
- Validates data before analysis
- Calculates total, average, and highest sale per salesperson using groupby
- Sorts results by total sales, highlights top salesperson in green
- Outputs a professional Excel report with bold headers

---

### `cleaner.py` — Excel File Cleaner

Takes any messy Excel file and returns a clean version automatically.

- Removes duplicate rows
- Strips extra spaces from all text fields
- Fixes inconsistent text casing
- Fills empty cells with "N/A"
- Never overwrites the original file

---

### `merge.py` — Multi-File Excel Merger

Merges multiple Excel files from a folder into one master report.

- Automatically finds all `.xlsx` files in the folder
- Validates that each file has an "Amount" column before processing
- Dynamically detects column positions — works regardless of column order
- Sorts all rows by Amount, highest first
- Outputs `master_report.xlsx` with bold headers

---

### `fiverr_readiness_test.py` — Blind Delivery Test

Given an unseen messy Excel file with no instructions, cleaned and delivered a professional report in under 2 hours.

- Merged and deduplicated data automatically
- Cleaned text columns, handled numeric columns separately
- Generated groupby sales summary sorted by total
- Delivered professional Excel report with bold headers and highlighted top row

This script exists to demonstrate real delivery speed and quality under pressure — not just clean demo data.

---

# Web Scraping

### `scraper_app.py` — Web Scraper Pro (Live Web App)

A full web application that scrapes any website and delivers the data as a clean Excel report.

**🔗 Live demo: [mahmoud-web-scraper.streamlit.app](https://mahmoud-web-scraper.streamlit.app)**

**How to use:**
1. Enter any website URL in the sidebar
2. Choose Auto mode to detect tables automatically, or Manual mode to enter an HTML tag and CSS class
3. Optionally sort the data and generate a summary report
4. Click Download to get your scraped data as a formatted Excel file

**What it does:**
- Auto-detects HTML tables on any page
- Manual mode: scrape any element by tag and CSS class
- Cleans and formats all scraped data automatically
- Optional summary report with totals, averages, and highest values
- Applies bold headers and optional row highlighting
- Outputs a formatted Excel file ready to use

Built with Streamlit, requests, and BeautifulSoup.

---

### `multi_scraper_app.py` — Multi-Page Scraper Pro (Live Web App)

A full web application that scrapes multiple pages automatically using a URL pattern.

**🔗 Live demo: [mahmoud-multi-scraper.streamlit.app](https://mahmoud-multi-scraper.streamlit.app)**

**How to use:**
1. Enter a URL pattern using `{page}` where the page number goes (e.g. `https://example.com/page-{page}.html`)
2. Set the number of pages to scrape
3. Choose Auto or Manual scraping mode
4. Click Download to get all scraped data combined into one Excel file

**What it does:**
- Loops through multiple pages automatically
- Combines all pages into one clean dataset
- Auto-detects tables or scrapes by tag and CSS class
- Optional summary report and row highlighting
- Outputs a formatted multi-sheet Excel file

Built with Streamlit, requests, and BeautifulSoup.

---

### `price_tracker.py` — Full Site Scraper & Price Report

Scrapes product data across an entire site and outputs a price analysis report.

- Scrapes multiple pages automatically with respectful request delays
- Cleans and converts price data for analysis
- Sorts all products by price
- Outputs `price_report.xlsx` with bold headers and a Summary sheet: total items, average price, cheapest and most expensive item

---

### `scraper.py` and `multi_scraper.py` — Scraping Foundations

The command-line building blocks behind the web apps, run against the public practice site [quotes.toscrape.com](https://quotes.toscrape.com).

- `scraper.py` — fetches one page, parses quotes and authors with BeautifulSoup, saves to CSV
- `multi_scraper.py` — loops through all 10 pages with a 1-second delay between requests and saves the combined result to Excel

---

# AI & LLM Automation

Hands-on work with large language models, built from the raw API up before touching any framework: API calls → structured output → tool calling → memory → document Q&A (RAG) → agents with long-term memory. All scripts use the [Groq](https://groq.com) API with the `openai/gpt-oss-20b` model.

### Stage 1 — LLM API Foundations

| Script | What it demonstrates |
|---|---|
| `hello_llm.py` | A first end-to-end API call and reading the response |
| `loop_hello_llm.py` | Sending multiple prompts in a loop and printing each reply |
| `system_prompt_test.py` | How a `system` message changes the model's persona and behavior |
| `temperature_test.py` | The same prompt at `temperature=0` vs `temperature=1` — deterministic vs. varied output |
| `max_tokens_test.py` | What `max_tokens` does to response length |
| `chat.py` | A multi-turn CLI chatbot that keeps full conversation history |

---

### `extract_info.py` — Structured Output (Message Classifier)

Turns free-form customer messages into clean, parseable JSON — the step that makes LLM output usable inside real automations.

- Classifies each message into `{intent, urgency, summary}`
- Runs at `temperature=0` for consistent results
- Strips any stray text around the JSON before parsing, so extra prose from the model doesn't break the pipeline
- Tested against five different message types: delivery complaint, praise, store-hours question, urgent payment failure, cancellation request

---

### `tool_demo.py` — Function Calling

Shows the mechanism every AI agent is built on: the model *requests* a function call, your code *executes* it, and the result is sent back for a final answer.

- Two working tools: `get_weather` (stubbed data) and `calculate`
- The model decides when a tool is needed — general questions are answered directly
- Full request → execute → follow-up loop implemented by hand

---

### `chat_memory.py` and `chat_memory_summary.py` — Context & Memory Management

Handles what happens when conversations outgrow the context window.

- `chat_memory.py` — sliding window: keeps the system prompt plus only the most recent messages
- `chat_memory_summary.py` — rolling summary: older messages are compressed into one running summary by the model, kept separate from the trimmed history so nothing important is lost

Both keep the system prompt pinned so the persona never gets trimmed away.

---

### `assistant.py` — CLI Assistant (Everything Combined)

One working assistant that combines the stage-1 skills.

- Answers general questions as a normal chatbot with a persistent persona
- Calls tools (`get_weather`, `calculate`) only when needed
- Type `summary` to get a structured JSON summary of the conversation so far (topics and user facts)
- Rolling-summary memory keeps long chats from breaking or ballooning in cost
- Organized into clear functions instead of one long script

---

### Stage 2 — Embeddings, RAG & Agents

### `embed_similarity.py` — Embeddings & Semantic Similarity

Generates sentence embeddings with `all-MiniLM-L6-v2` and compares five sentence pairs using cosine similarity — showing that differently worded sentences with the same meaning ("She works as a doctor" / "She is a physician") score as similar, while unrelated ones don't.

---

### `chroma_intro.py` — Vector Database Basics

Loads ten text snippets into a local ChromaDB collection and runs a semantic query ("Tell me about coding") that returns the closest matches by meaning, not by keyword.

---

### `chunks.py` — RAG Pipeline over a PDF

Document Q&A grounded in the document's real content instead of the model's guesses.

**How it works:**
1. Reads `doc.pdf` and splits the text into overlapping 500-character chunks
2. Embeds each chunk and stores it in ChromaDB
3. For each question, retrieves the 3 most relevant chunks
4. Passes them to the model with an instruction to answer *only* from that context — and to say "I don't know based on the document" otherwise

Set `SHOW_MATCHES = True` to print the retrieved chunks and see exactly what the answer was based on.

`doc.pdf` is a sample employee handbook for a fictional company (Nile Brew Co.), included so the pipeline can be tried immediately.

---

### `react_agent.py` — ReAct Agent with Long-Term Memory

An agent built by hand — no framework — around the reason → act → observe → repeat loop.

- **Tools:** leave-days lookup, a restricted calculator, and `remember_fact`
- **Long-term memory:** facts are embedded and saved in a persistent ChromaDB store (`agent_memory/`), so the agent can recall something told to it in a previous session
- **Duplicate protection:** a new fact that is nearly identical to a stored one (cosine distance below a threshold) isn't saved twice
- **Relevance cutoff:** only memories close enough to the current question are recalled
- **Loop safety:** a `MAX_STEPS` limit prevents runaway loops; tool errors are returned to the model so it can retry
- **Chat commands:** `/memories` lists saved facts, `/forget` clears them, `quit` exits

---

### `week2_rag_agent.py` — Document + Memory Agent

Combines the RAG pipeline and the long-term-memory agent: a personal knowledge assistant that searches your documents *only when it needs to*.

- `search_docs` tool backed by the handbook PDF — called for company questions, skipped for general chat
- Persistent long-term memory (`remember_fact`) carried over from `react_agent.py`
- **Output guardrail:** if the calculator returned a number but the final answer doesn't contain it, the script flags the answer as untrustworthy instead of silently passing it along
- Instructed never to guess company policy numbers — unsupported questions return "I don't know based on the document"
- Debug mode prints retrieval distances so thresholds can be tuned

---

## How to Run

**Install dependencies:**
```bash
# Run these from the repository root

# Data, reporting, and scraping tools
pip install -r portfolio/requirements.txt
pip install fastapi python-dotenv

# AI & LLM scripts
pip install -r portfolio/requirements-ai.txt
```

**Set your Groq API key** (required for all AI scripts — get a free key at [console.groq.com](https://console.groq.com)):
```bash
# macOS / Linux
export GROQ_API_KEY="your_key_here"

# Windows (PowerShell)
$env:GROQ_API_KEY="your_key_here"
```
Never hard-code the key in a script or commit it to the repo.

**Run the web apps locally:**
```bash
python -m streamlit run portfolio/data_cleaner_app.py
python -m streamlit run portfolio/scraper_app.py
python -m streamlit run portfolio/multi_scraper_app.py
```

**Run the API locally:**
```bash
uvicorn fastapi_cleaner:app --reload
```
Then visit `http://127.0.0.1:8000/docs` to test the `/clean` endpoint.

**Or use the live web apps — no installation needed:**

👉 [mahmoud-data-cleaner.streamlit.app](https://mahmoud-data-cleaner.streamlit.app)

👉 [mahmoud-web-scraper.streamlit.app](https://mahmoud-web-scraper.streamlit.app)

👉 [mahmoud-multi-scraper.streamlit.app](https://mahmoud-multi-scraper.streamlit.app)

**Run any script from its folder:**
```bash
python sales_report_generator.py
python pandas_report.py
python price_tracker.py
python cleaner.py
python merge.py
python email_sender.py

# AI scripts
python extract_info.py
python assistant.py
python chunks.py
python week2_rag_agent.py
```

> The first run of any embedding-based script (`embed_similarity.py`, `chunks.py`, `react_agent.py`, `week2_rag_agent.py`) downloads the embedding model, which can take a minute or two.

---

## Requirements

- Python 3.x

**Data, reporting & scraping:** openpyxl, pandas, requests, beautifulsoup4, streamlit, plotly, fastapi, uvicorn, python-multipart, python-dotenv

**AI & LLM:** groq, chromadb, sentence-transformers, scikit-learn, pypdf, python-dotenv

---

## About

I automate Excel and data workflows using Python — cleaning messy files, merging reports, scraping the web, building APIs, and delivering results automatically by email — and I build LLM-powered tools that classify messy text, answer questions from documents, and act through tools with persistent memory. Every script is documented, non-destructive, and built to handle real-world data, not just clean demos.

**Available for work on Fiverr → [fiverr.com/pymahmoud](https://www.fiverr.com/pymahmoud)**

**Live demos:**
- [mahmoud-data-cleaner.streamlit.app](https://mahmoud-data-cleaner.streamlit.app)
- [mahmoud-web-scraper.streamlit.app](https://mahmoud-web-scraper.streamlit.app)
- [mahmoud-multi-scraper.streamlit.app](https://mahmoud-multi-scraper.streamlit.app)

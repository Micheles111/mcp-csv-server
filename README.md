# 📂 MCP CSV Explorer (Analytics Edition)

An advanced **Model Context Protocol (MCP)** server that transforms a directory of local CSV files into a structured, queryable knowledge base for LLMs.
Designed as a final project for the **Advanced Programming** course.

## 🚀 Key Features

* **Smart Analytics:** Utilizes `pandas` for **deterministic** statistical analysis (`get_stats`), reducing LLM hallucinations on math tasks.
* **Non-blocking Execution:** Handles CPU-bound CSV parsing in a separate thread pool (`asyncio.to_thread`) to prevent blocking the Event Loop, ensuring responsiveness.
* **Secure File Access:** Implements strict **Path Traversal Protection** using Object-Oriented Paths (`pathlib`) to confine access to the data directory.
* **SSE Transport:** Implements **Server-Sent Events** over HTTP (Asynchronous I/O) for robust client-server decoupling.
* **Dynamic Introspection:** Automatically discovers new CSV files via Runtime Reflection.
* **Type Safety:** Built with strict Python type hinting for reliability.

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone [REPOSITORY_URL]
cd mcp-csv-server

```

### 2. Create and Activate Virtual Environment

**On Linux/Mac/WSL:**

```bash
python3 -m venv venv
source venv/bin/activate

```

**On Windows:**

```cmd
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

## ▶️ Usage

Since the server uses the **SSE protocol**, startup requires two terminals:

### Terminal 1 (The Server)

Starts the Async Event Loop (`uvicorn` backend).

```bash
python server.py

```

The server will listen at `http://127.0.0.1:8000/sse`

### Terminal 2 (The Client/Inspector)

Uses the official MCP Inspector to test the endpoints.

```bash
npx @modelcontextprotocol/inspector

```

1. Open the link provided in the terminal (e.g., `http://localhost:5173`).
2. Select Transport: **SSE**.
3. Enter URL: `http://127.0.0.1:8000/sse`.
4. Click **Connect**.

## 🧰 Available Tools

### Data Reading

* **`list_tables`**: Lists CSV files found in the data folder.
* **`get_schema(table_name)`**: Shows columns and data types for a specific file (Reflection).
* **`query_data(table_name)`**: Returns the first few rows of data (Marshalling).

### Analytics

* **`get_stats`**: Statistical report (mean, min, max, std deviation) computed deterministically via Pandas.
* **`search_in_table`**: Filtered case-insensitive search using **vectorized operations** () for performance.

## 📝 Available Prompts (Templates)

* **`analyze_csv_full`**: Complete Data Science report workflow.
* **`audit_data_quality`**: Data integrity and anomaly check.
* **`business_report`**: Strategic analysis (e.g., Sales/Products correlation).

## 👤 Author

**Michele Sagone** - Project developed with a **Human-in-the-Loop AI methodology**.
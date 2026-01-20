# 📂 MCP CSV Explorer Server (Analytics Edition)

An advanced server compatible with the **Model Context Protocol (MCP)** that transforms a folder of CSV files into an intelligent database queryable via AI.

## 🚀 Features
- **Smart Analytics:** Not only reads data but calculates statistics and searches for patterns.
- **SSE Transport:** Uses *Server-Sent Events* over HTTP for maximum web compatibility.
- **Dynamic Resources:** Automatically exposes every new CSV file added to the folder.
- **Smart Prompts:** Includes predefined templates for data auditing, business reports, and code generation.

## 🛠️ Installation

1. **Clone the repository and enter the folder:**
   ```bash
   git clone [REPOSITORY_URL]
   cd mcp-csv-server

2. **Create and activate the virtual environment:**
   **On Linux/Mac/WSL:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate

2. **On Windows:**
   ```DOS
   python -m venv venv
   venv\Scripts\activate
   
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

## ▶️ Usage
Since the server uses the SSE protocol, startup requires two terminals:

**Terminal 1 (The Server):**
   ```bash
   python3 server.py
```
The server will start at https://www.google.com/search?q=http://0.0.0.0:8000

**Terminal 2 (The Client/Inspector):**
   ```bash
   npx @modelcontextprotocol/inspector
```

- Open the provided link (e.g., http://localhost:5173).
- Select Transport: SSE.
- Enter URL: http://127.0.0.1:8000/sse.
- Click Connect.

## 🧰 Available Tools
**Data Reading**

- **list_tables:** Lists CSV files found in the data folder.

- **get_schema(table_name):** Shows columns and data types for a specific file.

- **query_data(table_name):** Returns the first few rows of data in table format.

**Analytics**

- **get_stats:** Statistical report (mean, min, max, std deviation).

- **search_in_table:** Filtered case-insensitive search.

## 📝 Prompts
- **analyze_csv_full:** Complete report on a file.

- **audit_data_quality:** Data integrity check.

- **business_report:** Sales analysis (Products/Orders).

## 👤 Author
Michele Sagone - Project developed with an AI-Assisted approach (Human-in-the-loop).

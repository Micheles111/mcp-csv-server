# Technical Specifications: MCP CSV Explorer (Analytics Edition)

## 1. Objective
To develop an "Analytics-Ready" **Model Context Protocol (MCP)** server that exposes local CSV files not just as raw text, but as a structured, queryable knowledge base. The system emphasizes **Deterministic Analytics** to reduce LLM hallucinations and **Type Safety** for reliability.

## 2. Architecture & Tech Stack
* **Language:** Python 3.10+ (Strongly Typed).
* **Core SDK:** `mcp[cli]` (FastMCP).
* **Transport Layer:** Server-Sent Events (SSE) over HTTP (Port 8000).
    * *Rationale:* Decouples server execution from client interaction, enabling remote debugging via the **MCP Inspector**.
* **Data Engine:** `pandas` (NumPy backend).
    * *Rationale:* Provides **Vectorized** operations for high-performance filtering and **Deterministic** statistical computation.
* **Output Formatting:** `tabulate` (Markdown serialization).

## 3. Functional Requirements

### 3.1 Transport & Connectivity
* **SSE Protocol:** The server must use an Asynchronous Event Loop (`uvicorn`) to manage non-blocking I/O connections.
* **Endpoint:** Expose `http://0.0.0.0:8000/sse` for client consumption.

### 3.2 Data Marshalling & Introspection
* **Dynamic Discovery:** Automatically scan the `./data` directory at runtime using Reflection-like mechanisms to register resources.
* **Schema Extraction:** Implement `get_schema` to return strict data types (`int64`, `float64`, `object`) to the LLM.
* **Markdown Serialization:** Convert tabular data into Markdown format for optimal LLM context window usage.

### 3.3 Analytics & Logic
* **Deterministic Stats:** Implement `get_stats` to offload mathematical computations (Mean, Min, Max, StdDev) to the CPU, preventing LLM arithmetic errors.
* **Vectorized Search:** Implement `search_in_table` using Pandas vectorization ($O(n)$ or better) instead of Python loops.

### 3.4 Security
* **Path Traversal Prevention:** Ensure all file access is strictly confined to the `data/` directory using absolute path resolution (`os.path.abspath`).
* **Dependency Isolation:** Strict adherence to `requirements.txt` and `venv` for reproducibility.

## 4. API Definition (Tools)
The server exposes the following strictly-typed tools:

* `list_tables() -> List[str]`
* `get_schema(table_name: str) -> Dict[str, str]`
* `query_data(table_name: str, limit: int) -> str`
* `get_stats(table_name: str) -> str`
* `search_in_table(table_name: str, col: str, val: str) -> str`

## 5. Prompt Templates
* **`analyze_csv_full`**: Workflow for full descriptive analysis.
* **`audit_data_quality`**: Check for `NaN` values and outliers.
* **`business_report`**: Strategic cross-table analysis.

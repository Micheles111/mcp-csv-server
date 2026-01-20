# Technical Specifications: CSV MCP Server

## Objective
To develop an "Analytics-Ready" MCP server that exposes local CSV files not just as raw data, but as structured and analyzable information for LLMs, facilitating data mining and automated business intelligence.

## Functional Requirements
1. **Transport Layer (SSE):** The server must use the Server-Sent Events (SSE) protocol over HTTP (port 8000) to ensure compatibility with web clients and remote debugging interfaces, replacing standard input/output (STDIO) transport.
2. **Dynamic Resource Registry:** Automatic scanning of the `./data` folder at startup and exposure of files as MCP Resources (`csv://filename.csv`) for direct reading of raw content.
3. **Data Inspection:**
   - `list_tables`: List of available datasets.
   - `get_schema`: Structure analysis (columns and data types).
   - `query_data`: Preview of tabular data formatted in Markdown.
4. **Data Analytics:**
   - Implementation of `get_stats` to automatically calculate descriptive statistics (mean, min, max) using Pandas, reducing LLM token consumption.
   - Implementation of `search_in_table` to perform filtered "case-insensitive" searches on specific columns.
5. **Prompt Engineering:** Integration of predefined templates (`@mcp.prompt`) to guide the AI in complex tasks such as data quality auditing, business report generation, and Python script creation.

## Technology Stack
- **Language:** Python 3.x
- **Core SDK:** `mcp` (Model Context Protocol SDK - FastMCP).
- **Server:** `uvicorn` (ASGI Server to manage SSE connections).
- **Data Processing:** `pandas` library for parsing, statistical analysis, and efficient CSV filtering.
- **Output Formatting:** `tabulate` library for converting DataFrames into Markdown tables readable by the LLM.
- **Environment:** Isolated dependency management via `venv`.
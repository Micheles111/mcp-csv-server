from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

# MCP Server Initialization
mcp = FastMCP("CSV Explorer")

# Path Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_csv_path(table_name: str) -> str:
    """Helper to get the full path of a CSV file."""
    if not table_name.endswith('.csv'):
        filename = f"{table_name}.csv"
    else:
        filename = table_name
    return os.path.join(DATA_DIR, filename)

# --- BASE TOOLS (Read & Schema) ---

@mcp.tool()
def list_tables() -> list[str]:
    """Lists all available CSV files in the data directory."""
    try:
        if not os.path.exists(DATA_DIR): return []
        return [f.replace('.csv', '') for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp.tool()
def get_schema(table_name: str) -> dict:
    """Returns columns and data types for a specific table."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return {"error": "File not found"}
    try:
        df = pd.read_csv(path)
        return df.dtypes.apply(lambda x: x.name).to_dict()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def query_data(table_name: str, limit: int = 5) -> str:
    """Reads the first N rows of a table."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Error: File not found"
    try:
        df = pd.read_csv(path)
        return df.head(limit).to_markdown(index=False)
    except Exception as e:
        return f"Error: {str(e)}"

# --- ANALYTICS TOOLS ---

@mcp.tool()
def get_stats(table_name: str) -> str:
    """Returns descriptive statistics (mean, min, max) for numeric columns."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Error: File not found"
    try:
        df = pd.read_csv(path)
        return df.describe().to_markdown()
    except Exception as e:
        return f"Stats Error: {str(e)}"

@mcp.tool()
def search_in_table(table_name: str, column: str, value: str) -> str:
    """Searches for specific rows in a column (case-insensitive)."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Error: Table not found."
    try:
        df = pd.read_csv(path)
        if column not in df.columns:
            return f"Error: Column '{column}' not found."
        filtered = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        if filtered.empty: return "No results found."
        return filtered.to_markdown(index=False)
    except Exception as e:
        return f"Search Error: {str(e)}"

# --- PROMPTS (Pre-defined Templates) ---

@mcp.prompt()
def analyze_csv_full(table_name: str) -> str:
    """Complete analysis of a table (Structure + Data + Statistics)."""
    return f"""
    Act as an expert Data Scientist. Analyze the table '{table_name}' by following these steps:
    1. Use get_schema('{table_name}') to understand the structure.
    2. Use query_data('{table_name}') to see a sample of the data.
    3. Use get_stats('{table_name}') to analyze numeric values.
    
    Provide a summary report explaining what the data contains and any notable patterns.
    """

@mcp.prompt()
def audit_data_quality(table_name: str) -> str:
    """Checks data quality by looking for errors or missing values."""
    return f"""
    Perform a quality audit on the table '{table_name}'.
    1. Check the schema for unexpected data types.
    2. Use get_stats to identify outliers (suspicious min/max values).
    3. Look for any logical inconsistencies in the data.
    
    Return a list of "Warnings" if you find anything strange, otherwise certify that the data is clean.
    """

@mcp.prompt()
def business_report() -> str:
    """Generates a business report by crossing Products and Orders."""
    return """
    Analyze business performance using the tables 'products' and 'orders'.
    1. Identify the best-selling products (you can use get_stats or query_data).
    2. Use search_in_table to find any 'Cancelled' or problematic orders.
    
    Write a short memo for the CEO with key results.
    """

@mcp.prompt()
def generate_python_script(table_name: str) -> str:
    """Generates a standalone Python script to analyze this file."""
    return f"""
    Do not perform analysis now. Instead, write a complete Python script that I can copy and paste.
    The code must:
    - Load the file '{table_name}.csv' using pandas.
    - Create a bar chart using matplotlib (based on data you see in the schema).
    - Save the chart as an image.
    
    Use get_schema('{table_name}') to know which columns to use for the chart.
    """

@mcp.prompt()
def explain_relationships() -> str:
    """Explains how tables are connected (Entity Relationship)."""
    return """
    Examine all available tables with list_tables().
    For each table, request the schema.
    
    Try to deduce the relationships (Foreign Keys) between the tables based on column names (e.g., user_id, product_id).
    Draw a text-based ER diagram (mermaid or ASCII) showing the connections between files.
    """

# --- DYNAMIC RESOURCES ---

def register_resources():
    """Scans the folder and registers each CSV as a resource."""
    if not os.path.exists(DATA_DIR): return

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.csv'):
            uri = f"csv://{filename}"
            full_path = os.path.join(DATA_DIR, filename)
            
            def make_reader(p):
                return lambda: open(p, "r", encoding="utf-8").read()

            reader = make_reader(full_path)
            # Unique name mandatory for SSE
            clean_name = filename.replace(".", "_").replace("-", "_")
            reader.__name__ = f"read_{clean_name}"
            
            mcp.resource(uri)(reader)

register_resources()

if __name__ == "__main__":
    # Start in SSE mode on port 8000
    mcp.run(transport='sse')
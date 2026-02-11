from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
from typing import List, Dict, Any, Optional

# MCP Server Initialization
# We use FastMCP to abstract the low-level JSON-RPC protocol details.
mcp = FastMCP("CSV Explorer")

# Path Configuration
# Using absolute paths ensures compatibility across different environments (WSL/Windows).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_csv_path(table_name: str) -> str:
    """Helper function to resolve file paths safely."""
    if not table_name.endswith('.csv'):
        filename = f"{table_name}.csv"
    else:
        filename = table_name
    return os.path.join(DATA_DIR, filename)

# --- BASE TOOLS (Data Marshalling & Introspection) ---

@mcp.tool()
def list_tables() -> List[str]:
    """
    Lists all available datasets in the data directory.
    Acts as a catalog discovery tool for the LLM.
    """
    try:
        if not os.path.exists(DATA_DIR): return []
        # List comprehension for efficient filtering
        return [f.replace('.csv', '') for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    except Exception as e:
        return [f"System Error: {str(e)}"]

@mcp.tool()
def get_schema(table_name: str) -> Dict[str, str]:
    """
    Returns the schema (column names and types) of a dataset.
    This allows the LLM to understand the data structure before querying.
    """
    path = get_csv_path(table_name)
    if not os.path.exists(path): return {"error": "File not found"}
    try:
        # We perform Marshalling from CSV format to a Python Dictionary
        df = pd.read_csv(path)
        return df.dtypes.apply(lambda x: x.name).to_dict()
    except Exception as e:
        return {"error": f"Marshalling Error: {str(e)}"}

@mcp.tool()
def query_data(table_name: str, limit: int = 5) -> str:
    """
    Retrieves a sample of raw data.
    Returns a Markdown-formatted string for optimal LLM readability.
    """
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Error: File not found"
    try:
        df = pd.read_csv(path)
        # Using Markdown as the interchange format
        return df.head(limit).to_markdown(index=False)
    except Exception as e:
        return f"Query Error: {str(e)}"

# --- ANALYTICS TOOLS (Server-Side Computation) ---

@mcp.tool()
def get_stats(table_name: str) -> str:
    """
    Performs server-side statistical analysis.
    This offloads computational complexity from the LLM to the deterministic runtime (Pandas).
    """
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Error: File not found"
    try:
        df = pd.read_csv(path)
        return df.describe().to_markdown()
    except Exception as e:
        return f"Analytics Error: {str(e)}"

@mcp.tool()
def search_in_table(table_name: str, column: str, value: str) -> str:
    """
    Performs a case-insensitive search within a specific column.
    """
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Error: Table not found."
    try:
        df = pd.read_csv(path)
        if column not in df.columns:
            return f"Error: Column '{column}' not found in schema."
        
        # Vectorized string operation for performance
        filtered = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        
        if filtered.empty: return "No results found."
        return filtered.to_markdown(index=False)
    except Exception as e:
        return f"Search Error: {str(e)}"

# --- PROMPTS (Meta-Programming / Templates) ---

@mcp.prompt()
def analyze_csv_full(table_name: str) -> str:
    """Template for a full analysis workflow."""
    return f"""
    Act as an expert Data Scientist. Analyze the dataset '{table_name}' following this strict protocol:
    1. Inspect Structure: Call get_schema('{table_name}').
    2. Sample Data: Call query_data('{table_name}') to understand the content.
    3. Statistical Profile: Call get_stats('{table_name}') to identify distributions and outliers.
    
    Output a professional report summarizing the findings.
    """

@mcp.prompt()
def audit_data_quality(table_name: str) -> str:
    """Template for data integrity verification."""
    return f"""
    Perform a Data Quality Audit on '{table_name}'.
    1. Check for data type inconsistencies using the schema.
    2. Identify potential outliers or invalid ranges using statistics.
    3. Verify if there are missing values or anomalies.
    
    Provide a bullet-point list of warnings or certify the dataset as 'Clean'.
    """

@mcp.prompt()
def business_report() -> str:
    """Complex multi-file analysis template."""
    return """
    Generate a Business Intelligence Report by cross-referencing 'products' and 'orders'.
    1. Analyze sales volume (Quantity) from the 'orders' table.
    2. Correlate with product categories from the 'products' table.
    3. Use 'search_in_table' to investigate any 'Cancelled' orders.
    
    Produce a strategic summary for stakeholders.
    """

# --- DYNAMIC RESOURCES (Reflection & Discovery) ---

def register_resources():
    """
    Dynamically scans the filesystem and registers resources at runtime.
    This mimics a reflection-based discovery mechanism.
    """
    if not os.path.exists(DATA_DIR): return

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.csv'):
            # URI Resource Identification
            uri = f"csv://{filename}"
            full_path = os.path.join(DATA_DIR, filename)
            
            # Closure to capture the specific path
            def make_reader(p: str):
                return lambda: open(p, "r", encoding="utf-8").read()

            reader = make_reader(full_path)
            
            # Sanitizing name for internal registry
            clean_name = filename.replace(".", "_").replace("-", "_")
            reader.__name__ = f"read_{clean_name}"
            
            # Registering the resource via decorator
            mcp.resource(uri)(reader)

# Initialize dynamic resources
register_resources()

if __name__ == "__main__":
    # Starting the server using SSE transport (Asynchronous)
    print("Starting MCP Server with SSE Transport on port 8000...")
    mcp.run(transport='sse')
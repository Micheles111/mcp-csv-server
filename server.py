import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from mcp.server.fastmcp import FastMCP

# --- LOGGING CONFIGURATION ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CSV_Explorer")

# --- INITIALIZATION ---
mcp = FastMCP("CSV Explorer")

# Path Configuration using Pathlib (Robust OOP approach)
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# --- HELPER FUNCTIONS ---

def _validate_path(table_name: str) -> Path:
    """
    Resolves and validates the CSV file path.
    Uses pathlib to ensure the resolved path is strictly within DATA_DIR.
    Prevents Path Traversal attacks.
    """
    clean_name = table_name if table_name.endswith('.csv') else f"{table_name}.csv"
    
    # Resolve absolute path
    target_path = (DATA_DIR / clean_name).resolve()
    
    # Security Check: The path must start with DATA_DIR
    if not str(target_path).startswith(str(DATA_DIR)):
        raise ValueError(f"Security Alert: Attempted Path Traversal on '{table_name}'")
    
    if not target_path.exists():
        raise FileNotFoundError(f"Table '{table_name}' not found.")
        
    return target_path

async def _load_dataframe(path: Path) -> pd.DataFrame:
    """
    Loads a Pandas DataFrame in a separate thread.
    Crucial to avoid blocking the Async Event Loop (bypassing GIL limitations for I/O).
    """
    try:
        # asyncio.to_thread runs the synchronous function in a separate thread pool
        return await asyncio.to_thread(pd.read_csv, path)
    except Exception as e:
        logger.error(f"Error reading CSV {path}: {e}")
        raise

# --- TOOLS (Async) ---

@mcp.tool()
async def list_tables() -> List[str]:
    """
    Lists all available datasets in the data directory.
    """
    try:
        # Disk I/O is blocking, but directory listing is generally fast.
        # Uses pathlib glob for efficient filtering.
        files = [f.stem for f in DATA_DIR.glob("*.csv")]
        return files
    except Exception as e:
        return [f"System Error: {str(e)}"]

@mcp.tool()
async def get_schema(table_name: str) -> Dict[str, str]:
    """
    Returns the schema (column names and types) of a dataset.
    """
    try:
        path = _validate_path(table_name)
        df = await _load_dataframe(path)
        return df.dtypes.apply(lambda x: x.name).to_dict()
    except FileNotFoundError:
        return {"error": "File not found"}
    except Exception as e:
        return {"error": f"Marshalling Error: {str(e)}"}

@mcp.tool()
async def query_data(table_name: str, limit: int = 5) -> str:
    """
    Retrieves a sample of raw data (Head Sampling).
    """
    try:
        path = _validate_path(table_name)
        df = await _load_dataframe(path)
        return df.head(limit).to_markdown(index=False)
    except Exception as e:
        return f"Query Error: {str(e)}"

@mcp.tool()
async def get_stats(table_name: str) -> str:
    """
    Performs deterministic server-side statistical analysis.
    Offloads computation to a thread to keep the server responsive.
    """
    try:
        path = _validate_path(table_name)
        df = await _load_dataframe(path)
        # describe() can be computationally expensive, so we run it off-thread
        description = await asyncio.to_thread(lambda: df.describe().to_markdown())
        return description
    except Exception as e:
        return f"Analytics Error: {str(e)}"

@mcp.tool()
async def search_in_table(table_name: str, column: str, value: str) -> str:
    """
    Performs a case-insensitive search within a specific column.
    Uses Vectorized operations for performance.
    """
    try:
        path = _validate_path(table_name)
        df = await _load_dataframe(path)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found in schema."
        
        # Vectorized operation executed in the thread pool
        def perform_search():
            filtered = df[df[column].astype(str).str.contains(value, case=False, na=False)]
            return filtered.to_markdown(index=False) if not filtered.empty else "No results found."

        return await asyncio.to_thread(perform_search)

    except Exception as e:
        return f"Search Error: {str(e)}"

# --- PROMPTS ---

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

# --- DYNAMIC RESOURCES (Reflection) ---

def register_resources():
    """
    Dynamically scans the filesystem and registers resources at runtime.
    """
    if not DATA_DIR.exists(): return

    for file_path in DATA_DIR.glob("*.csv"):
        filename = file_path.name
        uri = f"csv://{filename}"
        
        # Closure to capture the specific path reliably
        # Demonstrates lexical scope understanding (avoiding late binding)
        def make_reader(p: Path):
            return lambda: p.read_text(encoding="utf-8")

        reader = make_reader(file_path)
        
        # Sanitizing name for internal registry
        clean_name = filename.replace(".", "_").replace("-", "_")
        reader.__name__ = f"read_{clean_name}"
        
        mcp.resource(uri)(reader)

# Initialize dynamic resources
register_resources()

if __name__ == "__main__":
    logger.info("Starting Async MCP Server with SSE Transport on port 8000...")
    mcp.run(transport='sse')
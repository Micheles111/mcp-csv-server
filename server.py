import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from mcp.server.fastmcp import FastMCP

# --- CONFIGURAZIONE LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CSV_Explorer")

# --- INIZIALIZZAZIONE ---
mcp = FastMCP("CSV Explorer")

# Path Configuration using Pathlib (More robust OOP approach)
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# --- HELPER FUNZIONI ---

def _validate_path(table_name: str) -> Path:
    """
    Risolve e valida il percorso del file CSV.
    Usa pathlib per garantire che il percorso risolto sia dentro DATA_DIR.
    Previene attacchi di Path Traversal.
    """
    clean_name = table_name if table_name.endswith('.csv') else f"{table_name}.csv"
    
    # Risoluzione del percorso assoluto
    target_path = (DATA_DIR / clean_name).resolve()
    
    # Security Check: Il percorso deve iniziare con DATA_DIR
    if not str(target_path).startswith(str(DATA_DIR)):
        raise ValueError(f"Security Alert: Attempted Path Traversal on '{table_name}'")
    
    if not target_path.exists():
        raise FileNotFoundError(f"Table '{table_name}' not found.")
        
    return target_path

async def _load_dataframe(path: Path) -> pd.DataFrame:
    """
    Esegue il caricamento di Pandas in un thread separato.
    Cruciale per non bloccare l'Event Loop asincrono (vedi lezione su Async/GIL).
    """
    try:
        # asyncio.to_thread esegue la funzione sincrona in un thread pool separato
        return await asyncio.to_thread(pd.read_csv, path)
    except Exception as e:
        logger.error(f"Error reading CSV {path}: {e}")
        raise

# --- TOOLS (Asincroni) ---

@mcp.tool()
async def list_tables() -> List[str]:
    """
    Lists all available datasets in the data directory.
    """
    try:
        # L'I/O su disco è bloccante, ma os.listdir è veloce. 
        # Per massima correttezza in un server ad alto carico, anche questo andrebbe in to_thread,
        # ma per semplicità qui lo lasciamo diretto o usiamo glob.
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
    Retrieves a sample of raw data.
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
    """
    try:
        path = _validate_path(table_name)
        df = await _load_dataframe(path)
        # describe() può essere computazionalmente oneroso, bene averlo off-thread
        description = await asyncio.to_thread(lambda: df.describe().to_markdown())
        return description
    except Exception as e:
        return f"Analytics Error: {str(e)}"

@mcp.tool()
async def search_in_table(table_name: str, column: str, value: str) -> str:
    """
    Performs a case-insensitive search within a specific column.
    """
    try:
        path = _validate_path(table_name)
        df = await _load_dataframe(path)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found in schema."
        
        # Operazione vettoriale eseguita nel thread pool
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
        # Questo dimostra la comprensione dello scope lessicale (Doc 05)
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
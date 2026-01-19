from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

# Inizializzazione del Server MCP
mcp = FastMCP("CSV Explorer")

# Percorso della cartella dati
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def get_csv_path(table_name: str) -> str:
    """Helper per ottenere il percorso completo di un file CSV."""
    # Aggiunge .csv se manca
    if not table_name.endswith('.csv'):
        filename = f"{table_name}.csv"
    else:
        filename = table_name
    
    return os.path.join(DATA_DIR, filename)

@mcp.tool()
def list_tables() -> list[str]:
    """Elenca tutti i file CSV disponibili nella cartella dati."""
    try:
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        # Rimuoviamo l'estensione per pulizia visiva
        tables = [f.replace('.csv', '') for f in files]
        return tables
    except Exception as e:
        return [f"Errore nella lettura della directory: {str(e)}"]

@mcp.tool()
def get_schema(table_name: str) -> dict:
    """Restituisce le colonne e i tipi di dato di una tabella (CSV)."""
    path = get_csv_path(table_name)
    
    if not os.path.exists(path):
        return {"error": f"Tabella '{table_name}' non trovata."}
    
    try:
        df = pd.read_csv(path)
        # Convertiamo i tipi in stringa per renderli leggibili via JSON
        return df.dtypes.apply(lambda x: x.name).to_dict()
    except Exception as e:
        return {"error": f"Errore nella lettura del file: {str(e)}"}

@mcp.tool()
def query_data(table_name: str, limit: int = 5) -> str:
    """
    Legge le prime righe di una tabella.
    Args:
        table_name: Il nome del file (es. 'prodotti')
        limit: Numero massimo di righe da restituire (default 5)
    """
    path = get_csv_path(table_name)
    
    if not os.path.exists(path):
        return f"Errore: Tabella '{table_name}' non trovata."
    
    try:
        df = pd.read_csv(path)
        # Restituiamo i dati in formato Markdown per facile lettura da parte dell'LLM
        return df.head(limit).to_markdown(index=False)
    except Exception as e:
        return f"Errore durante la query: {str(e)}"

if __name__ == "__main__":
    # Avvia il server

    mcp.run()

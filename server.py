from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

# Inizializzazione del Server MCP
mcp = FastMCP("CSV Explorer")

# Percorso della cartella dati
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_csv_path(table_name: str) -> str:
    """Helper per ottenere il percorso completo di un file CSV."""
    if not table_name.endswith('.csv'):
        filename = f"{table_name}.csv"
    else:
        filename = table_name
    return os.path.join(DATA_DIR, filename)

# --- TOOLS (Le funzioni operative) ---

@mcp.tool()
def list_tables() -> list[str]:
    """Elenca tutti i file CSV disponibili nella cartella dati."""
    try:
        if not os.path.exists(DATA_DIR):
            return []
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
        # Restituiamo i dati in formato Markdown (richiede 'tabulate')
        return df.head(limit).to_markdown(index=False)
    except Exception as e:
        return f"Errore durante la query: {str(e)}"

# --- RISORSE (Lettura diretta dei file) ---

def register_resources():
    """Scansiona la cartella e registra ogni CSV come risorsa."""
    if not os.path.exists(DATA_DIR):
        return

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.csv'):
            # Creiamo l'URI univoco (es. csv://prodotti.csv)
            resource_uri = f"csv://{filename}"
            full_path = os.path.join(DATA_DIR, filename)
            
            # Funzione Factory per evitare problemi di scope nei cicli
            def make_reader(p):
                def reader():
                    with open(p, "r", encoding="utf-8") as f:
                        return f.read()
                return reader

            # Creiamo la funzione di lettura specifica per questo file
            reader_func = make_reader(full_path)
            
            # ASSEGNAZIONE NOME: Fondamentale per evitare crash su FastMCP
            # Sostituiamo caratteri non validi per i nomi di funzione Python
            safe_name = filename.replace(".", "_").replace("-", "_")
            reader_func.__name__ = f"read_{safe_name}"
            
            # Registrazione effettiva
            mcp.resource(resource_uri)(reader_func)

# Eseguiamo la registrazione prima di avviare il server
register_resources()

if __name__ == "__main__":
    mcp.run()
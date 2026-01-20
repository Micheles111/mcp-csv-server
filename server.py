from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

# Inizializzazione del Server MCP
mcp = FastMCP("CSV Explorer")

# Configurazione Percorsi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_csv_path(table_name: str) -> str:
    """Helper per ottenere il percorso completo."""
    if not table_name.endswith('.csv'):
        filename = f"{table_name}.csv"
    else:
        filename = table_name
    return os.path.join(DATA_DIR, filename)

# --- TOOLS BASE (Lettura e Schema) ---

@mcp.tool()
def list_tables() -> list[str]:
    """Elenca tutti i file CSV disponibili nella cartella data."""
    try:
        if not os.path.exists(DATA_DIR): return []
        return [f.replace('.csv', '') for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    except Exception as e:
        return [f"Errore: {str(e)}"]

@mcp.tool()
def get_schema(table_name: str) -> dict:
    """Restituisce colonne e tipi di dato."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return {"error": "File non trovato"}
    try:
        df = pd.read_csv(path)
        return df.dtypes.apply(lambda x: x.name).to_dict()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def query_data(table_name: str, limit: int = 5) -> str:
    """Legge le prime righe della tabella."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Errore: File non trovato"
    try:
        df = pd.read_csv(path)
        return df.head(limit).to_markdown(index=False)
    except Exception as e:
        return f"Errore: {str(e)}"

# --- TOOLS DI ANALISI (Analytics) ---

@mcp.tool()
def get_stats(table_name: str) -> str:
    """Statistiche descrittive (media, min, max) sui campi numerici."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Errore: File non trovato"
    try:
        df = pd.read_csv(path)
        return df.describe().to_markdown()
    except Exception as e:
        return f"Errore stats: {str(e)}"

@mcp.tool()
def search_in_table(table_name: str, column: str, value: str) -> str:
    """Cerca righe specifiche in una colonna (case-insensitive)."""
    path = get_csv_path(table_name)
    if not os.path.exists(path): return "Errore: Tabella non trovata."
    try:
        df = pd.read_csv(path)
        if column not in df.columns:
            return f"Errore: Colonna '{column}' non trovata."
        filtered = df[df[column].astype(str).str.contains(value, case=False, na=False)]
        if filtered.empty: return "Nessun risultato."
        return filtered.to_markdown(index=False)
    except Exception as e:
        return f"Errore ricerca: {str(e)}"

# --- PROMPTS (Template Predefiniti) ---

@mcp.prompt()
def analyze_csv_full(table_name: str) -> str:
    """Analisi completa di una tabella (Struttura + Dati + Statistiche)."""
    return f"""
    Agisci come un Data Scientist esperto. Analizza la tabella '{table_name}' eseguendo questi passaggi:
    1. Usa get_schema('{table_name}') per capire la struttura.
    2. Usa query_data('{table_name}') per vedere un campione di dati.
    3. Usa get_stats('{table_name}') per analizzare i valori numerici.
    
    Fornisci un report riassuntivo che spieghi cosa contengono i dati e quali pattern noti.
    """

@mcp.prompt()
def audit_data_quality(table_name: str) -> str:
    """Controlla la qualità dei dati cercando errori o valori mancanti."""
    return f"""
    Esegui un audit di qualità sulla tabella '{table_name}'.
    1. Controlla lo schema per tipi di dati inaspettati.
    2. Usa get_stats per identificare outlier (valori minimi/massimi sospetti).
    3. Cerca eventuali incongruenze logiche nei dati.
    
    Restituisci una lista di "Warning" se trovi qualcosa di strano, altrimenti certifica che i dati sono puliti.
    """

@mcp.prompt()
def business_report() -> str:
    """Genera un report di business incrociando Prodotti e Ordini."""
    return """
    Analizza l'andamento del business usando le tabelle 'prodotti' e 'ordini'.
    1. Identifica quali sono i prodotti più venduti (puoi usare get_stats o query_data).
    2. Usa search_in_table per trovare eventuali ordini 'Annullati' o problematici.
    
    Scrivi un breve memo per il CEO con i risultati chiave.
    """

@mcp.prompt()
def generate_python_script(table_name: str) -> str:
    """Genera uno script Python standalone per analizzare questo file."""
    return f"""
    Non eseguire analisi ora. Invece, scrivi un codice Python completo che io possa copiare e incollare.
    Il codice deve:
    - Caricare il file '{table_name}.csv' usando pandas.
    - Creare un grafico a barre usando matplotlib (basato sui dati che vedi nello schema).
    - Salvare il grafico come immagine.
    
    Usa get_schema('{table_name}') per sapere quali colonne usare nel grafico.
    """

@mcp.prompt()
def explain_relationships() -> str:
    """Spiega come sono collegate le tabelle tra loro (Entity Relationship)."""
    return """
    Esamina tutte le tabelle disponibili con list_tables().
    Per ogni tabella, richiedi lo schema.
    
    Cerca di dedurre le relazioni (Foreign Keys) tra le tabelle basandoti sui nomi delle colonne (es. id_utente, id_prodotto).
    Disegna un diagramma ER testuale (mermaid o ASCII) che mostri le connessioni tra i file.
    """

# --- RISORSE DINAMICHE ---

def register_resources():
    """Scansiona la cartella e registra ogni CSV come risorsa."""
    if not os.path.exists(DATA_DIR): return

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.csv'):
            uri = f"csv://{filename}"
            full_path = os.path.join(DATA_DIR, filename)
            
            def make_reader(p):
                return lambda: open(p, "r", encoding="utf-8").read()

            reader = make_reader(full_path)
            # Nome univoco obbligatorio per SSE
            clean_name = filename.replace(".", "_").replace("-", "_")
            reader.__name__ = f"read_{clean_name}"
            
            mcp.resource(uri)(reader)

register_resources()

if __name__ == "__main__":
    # Avvio in modalità SSE sulla porta 8000
    mcp.run(transport='sse')
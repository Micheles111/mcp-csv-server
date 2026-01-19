# Specifiche Tecniche: CSV MCP Server

## Obiettivo
Creare un server MCP che espone file CSV locali come tabelle di database, facilitando l'interazione tra LLM e dati strutturati statici.

## Requisiti Funzionali
1. **Lettura Directory:** Il server deve scansionare automaticamente la cartella `./data` all'avvio per identificare i file disponibili.
2. **List Tools:** Deve esporre un tool (`list_tables`) per elencare tutti i file CSV trovati.
3. **Schema Inspection:** Deve permettere di analizzare la struttura (colonne e tipi di dato) di un file specifico tramite `get_schema`.
4. **Query:** Deve permettere di leggere i dati di un CSV, con la possibilità di limitare il numero di righe o filtrare i risultati tramite `query_data`.

## Stack Tecnologico
- **Linguaggio:** Python 3.x
- **Core SDK:** `mcp` (Model Context Protocol SDK)
- **Data Processing:** Libreria `pandas` per il parsing e la manipolazione efficiente dei CSV.
- **Environment:** Gestione dipendenze tramite `venv` e `pip`.

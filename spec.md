# Specifiche Tecniche: CSV MCP Server

## Obiettivo
Sviluppare un server MCP "Analytics-Ready" che esponga file CSV locali non solo come dati grezzi, ma come informazioni strutturate e analizzabili dagli LLM, facilitando il data mining e la business intelligence automatizzata.

## Requisiti Funzionali
1. **Transport Layer (SSE):** Il server deve utilizzare il protocollo Server-Sent Events (SSE) su HTTP (porta 8000) per garantire la compatibilità con client web e interfacce di debugging remote, sostituendo il trasporto standard input/output (STDIO).
2. **Dynamic Resource Registry:** Scansione automatica della cartella `./data` all'avvio ed esposizione dei file come Risorse MCP (`csv://nomefile.csv`) per la lettura diretta del contenuto grezzo.
3. **Data Inspection:**
   - `list_tables`: Elenco dei dataset disponibili.
   - `get_schema`: Analisi della struttura (colonne e tipi di dato).
   - `query_data`: Anteprima dei dati tabellari formattati in Markdown.
4. **Data Analytics:**
   - Implementazione di `get_stats` per calcolare automaticamente statistiche descrittive (media, min, max) tramite Pandas, riducendo il consumo di token per l'LLM.
   - Implementazione di `search_in_table` per eseguire ricerche filtrate "case-insensitive" su colonne specifiche.
5. **Prompt Engineering:** Integrazione di template predefiniti (`@mcp.prompt`) per guidare l'IA in task complessi come l'audit della qualità dei dati, la generazione di report di business e la creazione di script Python.

## Stack Tecnologico
- **Linguaggio:** Python 3.x
- **Core SDK:** `mcp` (Model Context Protocol SDK - FastMCP).
- **Server:** `uvicorn` (ASGI Server per gestire le connessioni SSE).
- **Data Processing:** Libreria `pandas` per il parsing, l'analisi statistica e il filtraggio efficiente dei CSV.
- **Output Formatting:** Libreria `tabulate` per la conversione dei DataFrame in tabelle Markdown leggibili dall'LLM.
- **Environment:** Gestione dipendenze isolata tramite `venv`.
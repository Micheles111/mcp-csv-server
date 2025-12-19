# Specifiche Tecniche: CSV MCP Server

## Obiettivo
[cite_start]Creare un server MCP che espone file CSV locali come tabelle di database.

## Requisiti Funzionali
1. [cite_start]**Lettura Directory:** Il server deve scansionare la cartella `./data` all'avvio.
2. [cite_start]**List Tools:** Deve esporre un tool/resource per elencare tutte le tabelle (file CSV) disponibili[cite: 201].
3. **Schema Inspection:** Deve permettere di vedere le colonne di un file specifico.
4. [cite_start]**Query:** Deve permettere di leggere i dati di un CSV, con un filtro opzionale (es. "dammi le righe dove prezzo > 100")[cite: 201].

## Stack Tecnologico
- Python
- Libreria `mcp` SDK
- Libreria `pandas` per il parsing
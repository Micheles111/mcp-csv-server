# 📂 MCP CSV Explorer Server (Analytics Edition)

Un server avanzato compatibile con il **Model Context Protocol (MCP)** che trasforma una cartella di file CSV in un database intelligente interrogabile via IA.

## 🚀 Funzionalità
- **Smart Analytics:** Non solo legge i dati, ma calcola statistiche e cerca pattern.
- **SSE Transport:** Utilizza *Server-Sent Events* su HTTP per massima compatibilità web.
- **Dynamic Resources:** Espone automaticamente ogni nuovo file CSV aggiunto.
- **Smart Prompts:** Include template predefiniti per audit dati, report business e generazione codice.

## 🛠️ Installazione

1. **Clona la repository e vai nella cartella:**
   ```bash
   git clone [URL_REPOSITORY]
   cd mcp-csv-server

2. **Crea e attiva l'ambiente virtuale: Su Linux/Mac/WSL:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate

2. **Su Windows:**
   ```DOS
   python -m venv venv
   venv\Scripts\activate
3. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt

## ▶️ Utilizzo
Poiché il server usa il protocollo SSE, l'avvio richiede due terminali:

**Terminale 1 (Il Server)**:
   ```bash
   python3 server.py
```
Il server si avvierà su https://www.google.com/search?q=http://0.0.0.0:8000

**Terminale 2 (IL Client/Inspector)**:
   ```bash
   npx @modelcontextprotocol/inspector
```

- Apri il link fornito (es. http://localhost:5173).
- Seleziona Transport: SSE.
- Inserisci URL: http://127.0.0.1:8000/sse.
- Clicca Connect.

## 🧰 Tools Disponibili
**Lettura Dati**

- **list_tables**: Elenca i file CSV trovati nella cartella data.

- **get_schema(table_name)**: Mostra le colonne e i tipi di dato di un file specifico.

- **query_data(table_name)**: Restituisce le prime righe dei dati in formato tabella.

**Analisi**

- **get_stats**: Report statistico (media, min, max, deviazione std).

- **search_in_table**: Ricerca filtrata case-insensitive.

## 📝 Prompts
- **analyze_csv_full**: Report completo su un file.

- **audit_data_quality**: Check integrità dati.

- **business_report**: Analisi vendite (Prodotti/Ordini).

## 👤 Autore
Michele Sagone - Progetto sviluppato con approccio AI-Assisted (Human-in-the-loop).

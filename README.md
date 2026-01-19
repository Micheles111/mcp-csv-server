# 📂 MCP CSV Explorer Server

Un server compatibile con il **Model Context Protocol (MCP)** che espone file CSV locali come tabelle interrogabili tramite API.
Sviluppato come progetto per il corso di Advanced Programming (Progetto B06).

## 🚀 Funzionalità
- **Scansione Automatica:** Legge tutti i file `.csv` nella cartella `./data`.
- **Schema Inspection:** Espone i tipi di dati delle colonne.
- **Querying:** Permette di visualizzare e filtrare i dati dei CSV.

## 🛠️ Installazione

1. **Clona la repository:**
   ```bash
   git clone [https://github.com/Micheles111/mcp-csv-server.git](https://github.com/Micheles111/mcp-csv-server.git)
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
   ```Bash
   pip install "mcp[cli]" pandas

▶️ Utilizzo
**Avvia il server con l'Inspector MCP per testare le funzionalità:**
   ```Bash
   mcp dev server.py

---

🧰 Tools Disponibili
list_tables Elenca i file CSV trovati nella cartella data.

get_schema(table_name) Mostra le colonne e i tipi di dato di un file specifico.

query_data(table_name) Restituisce le prime righe dei dati in formato tabella.

👤 Autore
Michele Sagone - Progetto sviluppato con approccio AI-Assisted (Human-in-the-loop).

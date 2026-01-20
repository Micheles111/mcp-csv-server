# B06 - AI-Assisted MCP Server: Project Report

**Studente:** Michele Sagone
**Progetto:** B06 - MCP Server Exposing CSV Directory
**Data:** 19/12/2025

## 1. Introduzione e Obiettivi
L'obiettivo del progetto era sviluppare un server compatibile con il Model Context Protocol (MCP) capace di esporre file CSV locali come tabelle interrogabili.
Il ruolo dell'IA è stato quello di **"Lead Developer"** per la generazione del codice Python, mentre io ho agito come **"Technical Project Manager"**, definendo le specifiche, gestendo l'ambiente (WSL) e validando i risultati.

## 2. Metodologia e Prompts (Chain of Thought)
Lo sviluppo è avvenuto attraverso una serie di iterazioni mirate. Di seguito sono riportati i 5 prompt principali che hanno definito l'architettura del server:

### Prompt 1: Setup dell'Infrastruttura Base
**Obiettivo:** Creare lo scheletro del server e la lettura file.
> "Agisci come un Senior Python Developer. Voglio creare un server MCP usando la libreria `fastmcp`. Il server deve scansionare una cartella locale `./data`, trovare tutti i file `.csv` e creare automaticamente un tool `list_tables` per elencarli. Usa `os` per la gestione dei percorsi in modo compatibile con Linux/WSL."

### Prompt 2: Data Retrieval & Formatting
**Obiettivo:** Implementare la lettura dei dati e risolvere il problema della formattazione.
> "Ho bisogno di un tool `query_data(table_name, limit)` che legga un CSV con Pandas e restituisca le righe in formato Markdown per renderle leggibili all'LLM. Se ottengo l'errore `Missing optional dependency 'tabulate'`, dimmi esattamente come risolverlo nel mio ambiente virtuale."

### Prompt 3: Implementazione Risorse Dinamiche
**Obiettivo:** Esporre i file come risorse passive (non solo tools).
> "Voglio che ogni file CSV nella cartella appaia nella tab 'Resources' dell'Inspector come `csv://nomefile.csv`. Scrivi una funzione che itera sui file e usa `@mcp.resource` per registrarli dinamicamente. Attenzione: assicurati che le funzioni di lettura non si sovrascrivano a vicenda nel ciclo for (problema di closure delle lambda)."

### Prompt 4: Cambio Architettura (Da STDIO a SSE)
**Obiettivo:** Rendere il server accessibile via rete/web.
> "Modifica il file `server.py`. Invece di usare il trasporto standard (STDIO), voglio usare SSE (Server-Sent Events) su HTTP. Configura `mcp.run()` per usare `uvicorn` sulla porta 8000 e spiegami come devo cambiare il comando di avvio nel terminale."

### Prompt 5: Analisi Avanzata dei Dati
**Obiettivo:** Aggiungere intelligenza al server (Analytics).
> "I dati grezzi sono troppi per l'LLM. Crea due nuovi tool avanzati:
> 1. `get_stats(table_name)`: che usa `pandas.describe()` per darmi media, min e max delle colonne numeriche.
> 2. `search_in_table(table_name, column, value)`: per cercare righe specifiche ignorando maiuscole/minuscole.
> Il codice deve essere robusto e gestire errori se la colonna non esiste."

## 3. Verifica e Correzioni (QA & Debugging)
Durante lo sviluppo, il codice generato dall'IA era sintatticamente corretto, ma l'integrazione con l'ambiente locale ha richiesto interventi manuali:
* **Dipendenze:** Installazione manuale di `tabulate` e `uvicorn` mancanti nei primi output dell'IA.
* **WSL vs Windows:** Risoluzione dei percorsi assoluti per permettere a Node.js (Inspector) di comunicare con Python (Server) attraverso il sottosistema Linux.

## 4. Evoluzione del Progetto: Analisi e SSE
Nella fase finale dello sviluppo, abbiamo esteso le funzionalità base per rendere il server più robusto:

### Miglioramento 1: Da STDIO a SSE
Siamo passati dal trasporto standard (STDIO) a **SSE (Server-Sent Events)** su HTTP.
* **Motivazione:** Permette di disaccoppiare il server dal client, facilitando il debugging tramite Inspector Web e preparando il sistema per integrazioni future.

### Miglioramento 2: Tool di Analisi
Abbiamo notato che l'IA faticava a calcolare statistiche leggendo righe grezze. Abbiamo quindi implementato due nuovi tool nativi in Python:
1.  **`get_stats`**: Delega a Pandas il calcolo matematico, restituendo all'IA un riassunto affidabile.
2.  **`search_in_table`**: Permette di cercare record specifici (es. ordini di un utente) senza dover leggere l'intero file.

### Miglioramento 3: Prompt Template
Sono stati aggiunti template predefiniti (es. `audit_data_quality`) direttamente nel server per standardizzare le richieste più comuni e automatizzare l'analisi dei CSV.

## 5. Conclusione
Il progetto dimostra come un server MCP ben configurato possa trasformare una semplice cartella di file statici in un "database intelligente". L'uso di tool specifici per l'analisi (`get_stats`) invece della sola lettura grezza (`query_data`) ha migliorato notevolmente le performance dell'LLM, riducendo errori di calcolo e consumo di token.
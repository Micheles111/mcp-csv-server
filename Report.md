B06 - AI-Assisted MCP Server: Project Report
Studente: [Tuo Nome] Progetto: MCP Server Exposing CSV Directory Data: 19/12/2025

1. Introduzione e Obiettivi
L'obiettivo del progetto era sviluppare un server compatibile con il Model Context Protocol (MCP) capace di esporre file CSV locali come tabelle interrogabili. Il ruolo dell'IA è stato quello di "Lead Developer" per la generazione del codice Python e il troubleshooting dell'ambiente, mentre io ho agito come "Technical Project Manager", definendo le specifiche, gestendo l'ambiente di esecuzione e validando i risultati (User Acceptance Testing).

2. Metodologia e Prompts
Il lavoro si è svolto in modalità iterativa. Di seguito i principali prompt utilizzati per guidare l'IA:

Kick-off & Architettura: "Il mio obiettivo è diventare un project manager... dimmi tu tutto quello che devo fare passo dopo passo sul mio pc per il progetto MCP Server."

Generazione Codice: "Genera il codice per server.py che soddisfi i requisiti: scansione directory ./data, tool list_tables e tool query_data con pandas."

Troubleshooting Ambiente: "Error: typer is required. Install with 'pip install mcp[cli]'" e "Impossibile trovare il percorso specificato" (per risolvere i conflitti Windows/WSL).

3. Verifica e Correzioni (QA & Debugging)
Durante lo sviluppo, il codice generato dall'IA era sintatticamente corretto, ma l'integrazione con l'ambiente locale ha richiesto diversi interventi manuali critici.

Problemi Riscontrati e Risoluzioni:
Dipendenze Mancanti: L'IA inizialmente non aveva previsto le dipendenze specifiche per la CLI (mcp[cli]).

Azione Correttiva: Eseguita installazione manuale via pip e verifica con pip list.

Conflitto Ambiente Ibrido (WSL vs Windows): L'interfaccia di test (MCP Inspector) non riusciva a trovare l'eseguibile Python a causa di discrepanze nei percorsi tra Windows e il sottosistema Linux.

Azione Correttiva: Abbiamo forzato l'uso dei percorsi assoluti Linux (/home/sagon/...) e installato Node.js nativo all'interno di WSL per garantire la compatibilità del file system.

Typo nei Percorsi: È stato identificato e corretto un errore di battitura nella configurazione del percorso (csc vs csv), dimostrando l'importanza della revisione umana sui dettagli di configurazione.

4. Validazione Finale (UAT)
Il sistema è stato validato utilizzando MCP Inspector (interfaccia web di debugging).

Test Lettura Directory: Il tool list_tables ha restituito correttamente l'array ['prodotti', 'utenti'], confermando la scansione della cartella ./data.

Test Query Dati: Il tool query_data(table_name='prodotti') ha restituito i dati strutturati in formato Markdown, verificando il corretto funzionamento della libreria pandas per il parsing del CSV.

5. Conclusione
Il progetto dimostra come un server MCP possa fungere da ponte efficace tra dati statici (CSV) e interfacce intelligenti. L'uso dell'IA ha accelerato la scrittura del codice "boilerplate", ma la supervisione umana è stata determinante per la configurazione dell'infrastruttura e la risoluzione dei conflitti di sistema (OS-level issues).
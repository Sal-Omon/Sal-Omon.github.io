 Backend Flask (BeniCulturali)
 Data: 2025-09-16   
 
 1 — Sintesi esecutiva
 Il progetto backend per il sistema BeniCulturali è stato ristrutturato in modo modulare con una factory di
 applicazione Flask, layer DAO/Service/DTO per gli artifact, e seeders modulati per popolare il database.
 Sono stati identificati e risolti numerosi problemi di mapping SQLAlchemy, di ordine di inizializzazione e di
 logging. Rimangono punti critici principalmente relativi alla corretta definizione delle relazioni
 many-to-many (Artifact ↔ Creator) e alla finalizzazione della pipeline di seeding e del mapping DTO →
 API.
 
 2 — Cosa è stato implementato
 • Factory e bootstrap: implementata create_app() che carica .env, applica la configurazione, inizializza le
 estensioni e registra blueprint/CLI.
 • Modelli e relazioni: definiti i modelli principali (Artifact, Format, Creator, Location, Material, Tag, Image,
 ConservationReport) e le tabelle di associazione per many-to-many.
 • DAO / Service / DTO: ArtifactDAO con eager loading e paginazione; ArtifactService che normalizza filtri,
 costruisce chiavi di cache e ritorna DTO.
 • Seeders modulari: seeders per formats, creators, locations, materials, tags, images, artifacts,
 conservation_reports con orchestrazione centrale in seed_all().
 • CLI: comando Click `seed-db` (flags: --drop, --dry-run) eseguito all'interno del contesto dell'app.

 3 — Problemi riscontrati e risoluzioni parziali
 • Logging: chiamate a logger con argomenti posizionali errati (es. logger.info("msg", a, b)) che causavano
 TypeError. Soluzione: usare placeholder formato.
 • Ordine di import / FK mancanti: associazioni many-to-many e ForeignKey non risolte se le tabelle di
 associazione venivano definite dopo i modelli che le referenziano. Soluzione: spostare le definizioni delle
 tabelle di associazione prima dei modelli e unificare nomi.
 • Relazioni SQLAlchemy: errori Mapper/InvalidRequest dovuti a nomi back_populates non corrispondenti
 o proprietà mancanti (es. Artifact non aveva la proprietà 'creator' prevista da Creator). Soluzione: rendere
 back_populates simmetrici e coerenti.
 • Sequenza di seeding: conservation_reports richiede artifacts esistenti; immagini possono essere create
 indipendenti ma il loro legame agli artifact è più sicuro se fatto dopo. Soluzione: centralizzare il commit in
 seed_all e eseguire i seed in ordine corretto.
 • Validazione immagini: nomi di campo errati (image_urls vs image_url) e controllo del filesystem a
 import-time. Soluzione: validazioni e path risolti all'interno del seeder.
 
 4 — Stato attuale
 L'app factory si avvia correttamente. I seeders di base (formats, creators, locations, materials, tags,
 images) creano oggetti. Le funzionalità di DAO e Service per la ricerca e la paginazione sono
 implementate. Il blocco principale rimanente è la stabilizzazione della relazione many-to-many tra Creator
 e Artifact e la verifica finale della pipeline di seeding in modalità --drop (ricreazione schema) e --dry-run.
 
 5 — Raccomandazioni (prossime azioni)
 • Stabilizzare la mappatura Creator ↔ Artifact: definire la tabella di associazione prima dei modelli e
 verificare back_populates simmetrici.
 • Centralizzare i commit in seed_all(): chiamare i seeders con commit=False e committare una sola volta
 alla fine (o rollback su error).
 • Eseguire validate_fks.py e test di import dei modelli dopo ogni modifica strutturale.
 • Risolvere tutte le chiamate logger con formato errato e aggiungere test per le principali CLI (seed-db
 dry-run).
• Integrare test unitari/di integrazione minimi per import modelli e seed_all(dry_run=True).
 
 6 — Come eseguire (comandi principali)
 • Avviare l'app in sviluppo: `python run.py` oppure `flask --app run.py run`.
 • Eseguire il seeding: `flask --app run.py seed-db` (opzioni: --drop per ricreare schema, --dry-run per non
 committare).
 Nota: assicurarsi che create_app() non esegua operazioni pesanti a import-time.
 
 7 — Conclusione
 La base modulare è pronta e le problematiche più critiche sono note e facilmente risolvibili. Dopo la
 stabilizzazione delle relazioni e l'integrazione dei test di import/seeding, il passo successivo sarà esporre
 gli endpoint API che utilizzano ArtifactDTO e ArtifactService e proseguire con i componenti React per le
 ricerche correlate

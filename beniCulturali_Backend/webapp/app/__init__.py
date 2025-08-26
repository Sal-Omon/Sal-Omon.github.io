# app/__init__.py
"""
Application factory: definisce create_app() e usa helper per separare
l'inizializzazione delle estensioni, la registrazione dei blueprint e il logging.
Mantieni qui solo la configurazione iniziale: evita azioni a livello di import.
"""

from flask import Flask
from dotenv import load_dotenv
import logging
from typing import Optional

# Importa le istanze di estensioni (single source of truth)
from .extensions import db, migrate, cache


def create_app(config_object: str = "app.config") -> Flask:
    """
    Factory function per creare l'app Flask configurata.
    - config_object: modulo di configurazione (string) o oggetto
    """

    # Carica file .env se presente, prima di leggere variabili d'ambiente
    load_dotenv()

    # Crea l'istanza Flask (instance_relative_config False va bene per config statiche)
    app = Flask(__name__, instance_relative_config=False)

    # Applica la configurazione (da app/config.py)
    app.config.from_object(config_object)

    # Inizializza le estensioni (db, migrate, cache, ecc.)
    init_extensions(app)

    # Registra blueprint e, se presenti, comandi CLI
    register_blueprints_and_commands(app)

    # Setup logging (usa app.logger)
    setup_logging(app)

    return app


def init_extensions(app: Flask) -> None:
    """
    Inizializza tutte le estensioni con init_app.
    Mantieni qui solo init_app per evitare side effects.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    # inizializza la cache di Flask-Caching (es. Redis backend) se presente
    cache.init_app(app)


def register_blueprints_and_commands(app: Flask) -> None:
    """
    Registra blueprint e comandi CLI. Eventuali moduli opzionali vengono importati
    in try/except per non bloccare l'app se mancano.
    """
    # Blueprint principale (assicurati che in app.routes.main si chiami 'main_bp')
    from app.routes.main import main_bp
    from app.cli.seed_commands import seed_db_command 
    
    app.register_blueprint(main_bp)

    # Comandi CLI opzionali, es. seed_db
    try:
        # importa il comando se il modulo esiste e registralo
        from .cli.seed_commands import seed_db_command
        app.cli.add_command(seed_db_command)
    except Exception:
        # log a livello DEBUG per non disturbare in produzione
        app.logger.debug("seed_commands non presente o errore durante l'import.")


def setup_logging(app: Flask, level: int = logging.INFO) -> None:
    """
    Configurazione base del logging. Chiama logging.basicConfig
    solo se non è già stato configurato altrove.
    """
    # Imposta basicConfig solo se non è stata configurata già (evita doppie configurazioni)
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level)

    # Aggiungi informazioni utili al logger dell'app
    app.logger.setLevel(level)
    app.logger.info("Application initialized")
    app.logger.debug("SQLALCHEMY_DATABASE_URI=%s", app.config.get("SQLALCHEMY_DATABASE_URI"))

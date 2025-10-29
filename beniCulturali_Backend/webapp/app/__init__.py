# app/__init__.py
"""
Application factory: definisce create_app() e usa helper per separare
l'inizializzazione delle estensioni, la registrazione dei blueprint e il logging.
Mantieni qui solo la configurazione iniziale: evita azioni a livello di import.
"""

from flask import Flask
from dotenv import load_dotenv
import logging

# Importa le istanze di estensioni (single source of truth)
from .extensions import db, migrate, cache


def create_app(config_object: str = "app.config") -> Flask:
    """
    create_app is wrapped in a function
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

#3 Helper functions

def init_extensions(app: Flask) -> None:
    """
    Inizializza tutte le estensioni con init_app.
    solo init_app per evitare side effects.
    """
    #init_app() method is called on the db object 
    db.init_app(app)
    
    migrate.init_app(app, db)
    # inizializza la cache di Flask-Caching (es. Redis backend) se presente
    cache.init_app(app)


def register_blueprints_and_commands(app: Flask) -> None:
    """
    Registra blueprint e comandi CLI. Eventuali moduli opzionali vengono importati
    in try/except per non bloccare l'app se mancano.
    """
    # Blueprint principale (app.routes.main si chiama 'main_bp')
    from app.routes.main import main_bp #fatto localmente per evitare import time issues
    app.register_blueprint(main_bp)

    # Comandi CLI opzionali, es. seed_db
    try:
        # importa il comando se il modulo esiste e registralo
        # evitando eventuali fallimenti dell'esecuzione dell'app 
        #nel caso in cui i comandi non siano presenti
        from app.cli.seed_commands import seed_db_command  
        app.cli.add_command(seed_db_command)
        app.logger.info("registered seed_db_command")
    except ModuleNotFoundError:
        app.logger.debug("seed_commands not found, skipping registratio.")
    except Exception:
        # log without blocking the app
        app.logger.warning("Error registering seed_commands",exc_info=True)


def setup_logging(app: Flask, level: int = logging.INFO) -> None:
    """
    Configurazione base del logging. Chiama logging.basicConfig
    solo se non è già stato configurato altrove.
    """
    #Avoid reconfiguring if an handler is already set
    root_logger = logging.getLogger()
    
    # Avoid double configuration
    if not root_logger.handlers:
        logging.basicConfig(level=level)

    # add information to the app logger
    app.logger.setLevel(level)
    app.logger.info("Application initialized")
    app.logger.debug("SQLALCHEMY_DATABASE_URI=%s", app.config.get("SQLALCHEMY_DATABASE_URI"))

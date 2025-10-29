# app/cli/seed_commands.py
import click
from flask.cli import with_appcontext # decorator to access app context, app context needs to be accessed because db is tied to app
import logging 
from flask import current_app
from sqlalchemy import text



logger = logging.getLogger(__name__)

@click.command(name="seed-db")#new command definition through the click.command decorator
@click.option(
    "--drop",#flag option
    is_flag=True,
    default=False,#disabled by default
    help="Drop all tables before seeding (DANGEROUS: destroys existing data)."
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Perform a dry run without committing changes to the database."
)

# ensures the command runs within the Flask app context
#because db is tied to the app context and without 
# the context you cannot access it

@with_appcontext 
def seed_db_command(drop: bool, dry_run: bool):
    """
    CLI command: flask --app run.py seed-db [--drop]
    If --drop is provided, the DB schema will be dropped and recreated before seeding.
    """
    
    from app.extensions import db
    from app.seeders import seed_all
    #placeholder %s str() format, d% int() format, %f floating-point , %x hexadecimal value to string
    logger.info("Checking database connection ...")
    logger.info("Database URL: %s", current_app.config['SQLALCHEMY_DATABASE_URI']) # db.engine.url is a SQLAlchemy Engine object attribute that provides the database connection URL
    
    try:
        # Test DB connection come se fosse un ping del db senza creare strutture dati
        with db.engine.connect() as connection:
            #SELECT 1 query semplice per testare la connessione
            #text() converte una stringa SQL grezza in un oggetto SQL eseguibile 
            result = connection.execute(text('SELECT 1')) 
            logger.info("Database connection successful: %s", result.scalar())
    except Exception as e:
        logger.error("Database connection failed: %s", str(e))
        
    """
    il metodo scalar() è usato per ottenere il primo valore
    della prima riga del risultato della query SELECT 1 che contiene 1.
     
    """
    
    
    
    
    
    
    logger.info("seed-db command invoked: (drop=%s dry_run=%s)", drop,dry_run) # con placeholders
    click.echo("[seed-db] starting seeding process ...")
    
    try:
        if drop:
            # Drop all tables first (destructive)
            db.drop_all()
            click.echo("[seed-db] Dropped all tables.")

        # Ensure tables exist (create_all is safe here for dev)
        db.create_all()
        click.echo("[seed-db] Created DB schema (if not present).")

        # Run the seeder (seed_all should handle transactions / commits)
        seed_all(drop=drop,dry_run=dry_run)
        
        if dry_run:
            click.echo("[seed-db] Dry-run: rolled back changes (no commit).")
        else:
            click.echo("[seed-db] Database seeded successfully.")
            logger.info("Seeding completed without errors.")
        
        
    except Exception as exc:    
        click.echo(f"[seed-db] ERROR: {exc}", err=True)
        logger.exception("Error while seeding database:")
        # raise if we want CLI to show traceback 
        raise
    
# logger is for recording events,errors and diagnostic information 
# taht might be needed later useful for debugging
# click.echo() is for user communication and feedback, 
# end user running the CLI command

# dry_run is a testing process where a command or operation is executed 
# without making any permanent changes to the system
# dry_run goes through all teh seeding steps, but 
# rolls back the transaction at the end; 
# shows what would be inserted without
# inserting it and helps verify that the seeding process 
# would work correctly before running it for real
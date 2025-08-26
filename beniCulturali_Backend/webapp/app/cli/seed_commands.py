# app/cli/seed_commands.py
import click
from flask.cli import with_appcontext
from app.extensions import db
from app.seeders import seed_all
import logging

logger = logging.getLogger(__name__)

@click.command(name="seed-db")
@click.option(
    "--drop",
    is_flag=True,
    default=False,
    help="Drop all tables before seeding (DANGEROUS: destroys existing data)."
)
@with_appcontext
def seed_db_command(drop: bool):
    """
    CLI command: flask --app run.py seed-db [--drop]
    If --drop is provided, the DB schema will be dropped and recreated before seeding.
    """
    try:
        if drop:
            # Drop all tables first (destructive)
            db.drop_all()
            click.echo("[seed-db] Dropped all tables.")

        # Ensure tables exist (create_all is safe here for dev)
        db.create_all()
        click.echo("[seed-db] Created DB schema (if not present).")

        # Run the seeder (seed_all should handle transactions / commits)
        seed_all(dry_run=False)
        click.echo("[seed-db] Database seeded successfully.")
        logger.info("Seeding completed without errors.")
    except Exception as exc:
        # If something goes wrong, rollback the session to keep DB consistent
        try:
            db.session.rollback()
        except Exception:
            logger.exception("Rollback failed after seeding error.")
        click.echo(f"[seed-db] ERROR: {exc}", err=True)
        logger.exception("Error while seeding database:")
        # re-raise if you want CLI to show traceback (optional)
        raise

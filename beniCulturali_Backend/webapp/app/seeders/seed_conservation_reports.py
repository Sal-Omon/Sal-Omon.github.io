from app.extensions import db
from app.models.conservation_report import ConservationReport
from flask import current_app
from faker import Faker
import random
import logging

fake = Faker()
logger = logging.getLogger(__name__)


def seed_conservation_reports(artifacts, commit=True):
    """If True, commits the changes to the database.
                       Otherwise, the session is left open."""
        #table's Seeding with multiple dependecies
    logger.info(f"Seeding Conservation reports for {len(artifacts) if artifacts else 0} artifacts")
    
    reports = []
    for artifact in artifacts or []:
        num_reports = random.randint(0,2)
        for _ in range(num_reports):
            report = ConservationReport(
                artifact=artifact,
                conservation_details = fake.sentence(nb_words=12),
                actual_conditions = fake.sentence(nb_words=50),
                preservation_needs = fake.sentence(nb_words=100),
                date= fake.date_between(start_date='-5y', end_date='today')
            )
            db.session.add(report)
            reports.append(report)
            
    if commit:
        try:
            db.session.commit()
            logger.info(f"Seeded conservation reports {len(reports)}")
        except Exception as e:
            logger.exception(f"Error committing conservation reports: {e}")
            raise
        
    return reports    

from app import create_app, db
from app.models.conservation_report import ConservationReport
from app.seeders.seed_creators import seed_creators
import app
from faker import Faker
import random

fake = Faker()
app = create_app()


def seed_conservation_reports(artifacts, commit=True):
        #table's Seeding with multiple dependecies
    app.logger.info(f"Seeding Conservation reports")
    
    conservation_reports_data = []
    for artifact in artifacts:
        num_reports = random.randint(0,2)
        for _ in range(num_reports):
            report = ConservationReport(
                artifact=artifact,
                conservation_details = fake.sentence(100),
                actual_conditions = fake.sentence(50),
                preservation_needs = fake.sentence(100),
                date= fake.date_between(start_date='-5y', end_date='today')
            )
            
            conservation_reports_data.append(report)
            
    db.session.add_all(conservation_reports_data)
    if commit:
        db.session.commit()
        app.logger.info(f"Seeded {len(conservation_reports_data)}")
    return conservation_reports_data    

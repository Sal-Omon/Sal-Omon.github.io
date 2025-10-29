from app.extensions import db
from app.models.creator import Creator
from faker import Faker
from flask import current_app


fake = Faker()


def seed_creators(commit=True):
    current_app.logger.info(f"Seeding Creators")
    creators_data = [Creator(creator_name=fake.name()) for _ in range(20)]
    db.session.add_all(creators_data)
    if commit:
        db.session.commit()
        current_app.logger.info(f"Seeded {len(creators_data)} Creators.")
    return creators_data

from app.extensions import db
from flask import current_app
from app.models.location import Location
from faker import Faker

fake = Faker()


def seed_locations(commit=True):
    current_app.logger.info(f"Seeding Locations")
    locations_data = [Location(location_name = fake.city()) for _ in range(10)]
    db.session.add_all(locations_data)
    if commit:
        db.session.commit()
        current_app.logger.info(f"Seeded {len(locations_data)} locations.")
    return locations_data

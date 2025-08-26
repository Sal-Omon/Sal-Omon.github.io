from app import db, create_app
import app
from app.models.location import Location
from faker import Faker

app = create_app()
fake = Faker()


def seed_locations(commit=True):
    app.logger.info(f"Seeding Locations")
    locations_data = [Location(location_name = fake.city()) for _ in range(10)]
    db.session.add_all(locations_data)
    if commit:
        db.session.commit()
        app.logger.info(f"Seeded {len(locations_data)} locations.")
    return locations_data

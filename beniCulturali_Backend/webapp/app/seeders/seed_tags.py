from app.extensions import db
from app.models.tag import Tag
from flask import current_app
from faker import Faker


fake = Faker()

        
def seed_tags(commit=True):
    current_app.logger.info("Seeding Tags")
    tags_data = [Tag(tag_name=fake.word().capitalize()) for _ in range(15)]
    db.session.add_all(tags_data)
    if commit:
        db.session.commit()
        current_app.logger.info(f"Seeded {len(tags_data)} tags.")
    return tags_data

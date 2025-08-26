from app import create_app,db
from app.models.tag import Tag
from faker import Faker


app = create_app()
fake = Faker()

        
def seed_tags(commit=True):
    app.logger.info("Seeding Tags")
    tags_data = [Tag(tag_name=fake.word().capitalize()) for _ in range(15)] 
    db.session.add_all(tags_data)
    if commit:
        db.session.commit()
        app.logger.info(f"Seeded {len(tags_data)} tags.")
    return tags_data

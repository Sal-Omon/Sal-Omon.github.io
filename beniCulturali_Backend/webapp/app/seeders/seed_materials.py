from app.extensions import db
from app.models.material import Material
from faker import Faker
from flask import current_app

fake = Faker()


def seed_materials(commit=True):
    current_app.logger.info(f"Seeding Materials")
    materials_data = [
        Material(material_name="Oil on Canva", material_description=fake.text(50)),
        Material(material_name="Bronzo", material_description=fake.text(50)),
        Material(material_name="Pergamenaceo", material_description=fake.text(50)),
        Material(material_name="Oro e Gemme", material_description=fake.text(50)),
        Material(material_name="Terracotta", material_description=fake.text(50)),
        Material(material_name="Seta", material_description=fake.text(50)),
        Material(material_name=fake.word(), material_description=fake.text(50))
    ]
    db.session.add_all(materials_data)
    if commit:
        db.session.commit()
        current_app.logger.info(f"Seeded {len(materials_data)} materials.")
    return materials_data

from app.extensions import db
from app.models.format import Format
from flask import current_app
import os



def seed_formats(commit: bool = True):
    current_app.logger.info(f"Seeding formats")
    formats_data = [
        Format(format_name = "Painting"),
        Format(format_name = "Sculpture"),
        Format(format_name = "Drawing"),
        Format(format_name = "Print"),
        Format(format_name = "Digital Art"),
        Format(format_name = "Jewellery"),
        Format(format_name = "Ceramic"),
        Format(format_name = "Textile"),
        Format(format_name = "Glass"),
        Format(format_name = "Metalwork"),
        Format(format_name = "Manuscript"),
        Format(format_name = "Photography")
    ]
    try:
        db.session.add_all(formats_data)
        if commit:
            db.session.commit()
            current_app.logger.info(f"Seeded {len(formats_data)} formats.")
    except Exception as e:
        current_app.logger.error(f"Error seeding formats: {e}")
        db.session.rollback()
        raise
    return formats_data
    
from app.extensions import db
from app.models.associations import artifact_materials,artifact_tags,artifact_creators


class Artifact(db.Model):
    __tablename__ = "artifacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)

    # Many-to-one: format, creator, location
    format_id = db.Column(db.Integer, db.ForeignKey("formats.format_id"))
    format = db.relationship("Format", back_populates="artifacts")

    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))
    location = db.relationship("Location", back_populates="artifacts")

    # Many-to-many: materials, tags
    materials = db.relationship(
        "Material",
        secondary=artifact_materials,
        back_populates="artifacts",
        lazy="selectin", #efficient loading for collections
    )

    tags = db.relationship(
        "Tag",
        secondary=artifact_tags,
        back_populates="artifacts"
    )

    creators = db.relationship(
        "Creator",
        secondary=artifact_creators,
        back_populates="artifacts",
        )

    # One-to-many: images (an artifact has many images) & conservation_reports
    images = db.relationship(
        "Image",
        back_populates="artifact",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    conservation_report = db.relationship(
        "ConservationReport", 
        back_populates="artifact",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Artifact id={self.id} name={self.name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "format": self.format.format_name if self.format else None,
            "location": self.location.location_name if self.location else None,
            "creators": [c.to_dict() for c in self.creators] if self.creators else [],
            "materials": [m.to_dict() for m in self.materials] if self.materials else [],
            "tags": [t.to_dict() for t in self.tags] if self.tags else [],
            "images": [img.to_dict() for img in self.images] if self.images else [],
        }

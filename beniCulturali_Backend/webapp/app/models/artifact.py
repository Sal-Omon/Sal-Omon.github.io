from app import db

artifact_material = db.Table(
    'artifact_material',
    db.Column('artifact_id', db.Integer, db.ForeignKey('artifacts.id'), primary_key=True),
    db.Column('material_id', db.Integer, db.ForeignKey('materials.material_id'), primary_key=True)
)

artifact_tags = db.Table(
    'artifact_tags',
    db.Column('artifact_id', db.Integer, db.ForeignKey('artifacts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
)


class Artifact(db.Model):
    __tablename__ = "artifacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)

    # Many-to-one: format, creator, location
    format_id = db.Column(db.Integer, db.ForeignKey("formats.format_id"))
    format = db.relationship("Format", back_populates="artifacts")

    creator_id = db.Column(db.Integer, db.ForeignKey("creators.creator_id"))
    creator = db.relationship("Creator", back_populates="artifacts")

    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))
    location = db.relationship("Location", back_populates="artifacts")

    # Many-to-many: materials, tags
    materials = db.relationship(
        "Material",
        secondary=artifact_material,
        back_populates="artifacts"
    )

    tags = db.relationship(
        "Tag",
        secondary=artifact_tags,
        back_populates="artifacts"
    )

    # One-to-many: images (an artifact has many images)
    images = db.relationship(
        "Image",
        back_populates="artifact",
        cascade="all, delete-orphan"
    )

    # Conservation reports (one-to-many)
    conservation_report = db.relationship("ConservationReport", back_populates="artifact")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "format": self.format.format_name if self.format else None,
            "creator": self.creator.creator_name if self.creator else None,
            "location": self.location.location_name if self.location else None,
            "materials": [m.to_dict() for m in self.materials] if self.materials else [],
            "tags": [t.to_dict() for t in self.tags] if self.tags else [],
            "images": [img.to_dict() for img in self.images] if self.images else [],
        }

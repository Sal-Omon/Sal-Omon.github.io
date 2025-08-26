from app import db

class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, nullable=False)

    # foreign key that links this image to a single artifact
    artifact_id = db.Column(db.Integer, db.ForeignKey("artifacts.id"), nullable=True)

    # relationship back to Artifact (singular)
    artifact = db.relationship("Artifact", back_populates="images")

    def to_dict(self):
        return {
            "id": self.image_id,
            "url": self.image_url
        }

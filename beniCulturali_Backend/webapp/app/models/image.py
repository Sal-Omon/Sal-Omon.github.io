from app.extensions import db
from sqlalchemy.orm import validates
import re 
import os

class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True)
    image_urls = db.Column(db.String, nullable=False)
    # foreign key that links this image to a single artifact

    # relationship back to Artifact (singular) one to many images
    artifact_id = db.Column(db.Integer, db.ForeignKey("artifacts.id"), nullable=True)
    artifact = db.relationship("Artifact", back_populates="images")


    def __repr__(self):
        return f"<Image id={self.image_id} url={self.image_urls!r}>"
    
    def to_dict(self):
        return {
            "image_id": self.image_id,
            "image_urls": self.image_urls
        }
        
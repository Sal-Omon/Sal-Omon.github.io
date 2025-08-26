from app import db

class Creator(db.Model):
    __tablename__ = "creators"
    creator_id = db.Column(db.Integer, primary_key=True)
    creator_name = db.Column(db.String, nullable=False)
    artifacts = db.relationship("Artifact", back_populates="creator")  # relationship between Creator and Artifact

    def to_dict(self):
        return {
            "id": self.creator_id,
            "name": self.creator_name
        }
    
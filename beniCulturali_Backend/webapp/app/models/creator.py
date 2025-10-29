from app.extensions import db
from .associations import artifact_creators

class Creator(db.Model):
    __tablename__ = "creators"
    creator_id = db.Column(db.Integer, primary_key=True)
    creator_name = db.Column(db.String, nullable=False)
    
    artifacts = db.relationship("Artifact", 
                                secondary=artifact_creators,
                                back_populates="creators")  
    # relationship between Creator and Artifact

    def to_dict(self):
        return {
            "creator_id": self.creator_id,
            "creator_name": self.creator_name
        }
    
from app import db

class Location(db.Model):
    __tablename__ = "locations"
    location_id = db.Column(db.Integer, primary_key=True)  # location_id is the primary key for the Location model
    location_name = db.Column(db.String, nullable=False)
    artifacts = db.relationship("Artifact", back_populates="location")  # relationship between Location and Artifact
    
    def to_dict(self):
        return {
            "id": self.location_id,
            "name": self.location_name
        }
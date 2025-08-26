from app import db


class Format(db.Model):
    __tablename__ = "formats"
    
    format_id = db.Column(db.Integer, primary_key=True) # format_id is the primary key for the Format model
    format_name = db.Column(db.String, nullable=False)

    artifacts = db.relationship("Artifact", back_populates="format") # relationship between Format and Artifact

    def to_dict(self):
        return {
            "id": self.format_id,
            "name": self.format_name
        }
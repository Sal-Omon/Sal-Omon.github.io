from app import db

class ConservationReport(db.Model):# store the restoration history, conditions reports, preservation needs
    __tablename__ = "conservation_reports"

    conservation_id = db.Column(db.Integer, primary_key=True)
    artifact_id = db.Column(db.Integer, db.ForeignKey("artifacts.id"))
    artifact = db.relationship("Artifact", back_populates="conservation_report")
    conservation_details = db.Column(db.Text, nullable=False)
    actual_conditions = db.Column(db.Text, nullable=False)  # current conditions of the artifact
    preservation_needs = db.Column(db.Text, nullable=False)  # needs for preservation
    date = db.Column(db.Date, nullable=False)  # date of the conservation report
    
    def to_dict(self):
        return{
            "id": self.conservation_id,
            "artifact_id": self.artifact_id,
            "conservation_details": self.conservation_details,
            "actual_conditions": self.actual_conditions,
            "preservation_needs": self.preservation_needs,
            "date": str(self.date)
        }

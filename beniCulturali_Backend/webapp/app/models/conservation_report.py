from app.extensions import db

# The class is defined here, but the import from this same file is removed.
# from app.models.conservation_report import ConservationReport <-- REMOVE THIS

class ConservationReport(db.Model):
    """
    Model representing a conservation report for an artifact.
    Stores restoration history, conditions, and preservation needs.
    """
    __tablename__ = "conservation_reports"

    conservation_id = db.Column(db.Integer, primary_key=True)
    artifact_id = db.Column(db.Integer, db.ForeignKey("artifacts.id"))
    conservation_details = db.Column(db.Text, nullable=False)
    actual_conditions = db.Column(db.Text, nullable=False)
    preservation_needs = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False) 
    
    # Use a string reference for the relationship
    artifact = db.relationship("Artifact", back_populates="conservation_report")

    def __repr__(self):
        return f"<ConservationReport id={self.conservation_id} artifact_id={self.artifact_id}>"

    def to_dict(self):
        return {
            "conservation_id": self.conservation_id,
            "artifact_id": self.artifact_id,
            "conservation_details": self.conservation_details,
            "actual_conditions": self.actual_conditions,
            "preservation_needs": self.preservation_needs,
            "date": str(self.date)
        }

# All data-seeding logic should be moved to a separate file,
# e.g., 'app/seeders/seed_conservation_reports.py'

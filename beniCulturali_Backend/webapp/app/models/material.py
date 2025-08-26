from app import db

 #~many to many       
class Material(db.Model):
    __tablename__ = "materials"
    material_id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String, nullable=False)
    material_description = db.Column(db.String)
    artifacts = db.relationship("Artifact",
                                secondary="artifact_material",
                                back_populates="materials")  # relationship between Material
    

    def to_dict(self):
        return {
            "id": self.material_id,
            "name": self.material_name,
            "description": self.material_description
        }
        
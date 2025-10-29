from app.extensions import db
from .associations import artifact_materials

 #~many to many       
class Material(db.Model):
    __tablename__ = "materials"
    material_id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String, nullable=False)
    material_description = db.Column(db.String)
    artifacts = db.relationship("Artifact",
                                secondary=artifact_materials,
                                back_populates="materials")  # relationship between Material
    

    def to_dict(self):
        return {
            "material_id": self.material_id,
            "material_name": self.material_name,
            "material_description": self.material_description,
            "artifact_materials": self.artifacts
        }
        
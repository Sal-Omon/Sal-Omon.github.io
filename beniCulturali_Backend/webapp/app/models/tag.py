from app.extensions import db
from .associations import artifact_tags


class Tag(db.Model):
    __tablename__ = "tags"
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False)
    
    artifacts = db.relationship("Artifact",
                               secondary=artifact_tags,
                               back_populates="tags")  # relationship between Tag and Artifact

    def to_dict(self):
        return{
            "tag_id": self.tag_id,
            "tag_name": self.tag_name
        }
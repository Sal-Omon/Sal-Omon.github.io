from app import db
from app.models.artifact import Artifact
from app.models.tag import Tag


artifact_tags = db.Table( 'artifact_tags', 
    db.Column('artifact_id', db.Integer, db.ForeignKey('artifacts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)) # many-to-many relationship between Artifact and Tag
     

class Tag(db.Model):
    __tablename__ = "tags"
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False)
    artifacts = db.relationship("Artifact",
                               secondary=artifact_tags,
                               back_populates="tags")  # relationship between Tag and Artifact

    def to_dict(self):
        return{
            "id": self.tag_id,
            "name": self.tag_name
        }
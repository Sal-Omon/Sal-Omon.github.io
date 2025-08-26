import app.models.artifact as Artifact

class ArtifactDTO:
    @staticmethod
    def to_dict(artifact: Artifact) -> dict:
        """Converte un Artifact SQLAlchemy in dizionario"""
        if artifact is None:
            return None

        return {
            "id": artifact.id,
            "name": artifact.name,
            "description": artifact.description,
            "creator": artifact.creator.name if artifact.creator else None,
            "format": artifact.format.name if artifact.format else None,
            "location": artifact.location.name if artifact.location else None,
            "materials": [m.material_name for m in getattr(artifact, 'materials', [])] if getattr(artifact, 'materials', None) else [],
            "tags": [t.tag_name for t in getattr(artifact, 'tags', [])] if getattr(artifact, 'tags', None) else [],
            "images": [img.image_url for img in getattr(artifact, 'images', [])] if getattr(artifact, 'images', None) else [],
        }

    @staticmethod
    def list_to_dict(artifacts):
        """Converte lista di Artifact in lista di dizionari"""
        return [ArtifactDTO.to_dict(artifact) for artifact in artifacts]

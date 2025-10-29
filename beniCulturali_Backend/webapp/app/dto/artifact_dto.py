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
            "format": artifact.format.format_name if artifact.format else None,
            "location": artifact.location.location_name if artifact.location else None,
            "creators": [c.creator_name for c in artifact.creators],
            "materials": [m.material_name for m in artifact.materials],
            "tags": [t.tag_name for t in getattr(artifact, 'tags', [])] if getattr(artifact, 'tags', None) else [],
            "images": [img.image_url for img in getattr(artifact, 'images', [])] if getattr(artifact, 'images', None) else [],
        }

    @staticmethod
    def list_to_dict(artifacts):
        """Converte lista di Artifact in lista di dizionari"""
        return [ArtifactDTO.to_dict(artifact) for artifact in artifacts]

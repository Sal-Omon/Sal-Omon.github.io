Data Flow & Layered Architecture
This project uses a layered approach to keep data clean, efficient, and UI‑ready. The main layers are:

Database Models

DTOs (Data Transfer Objects)

API Normalization

Frontend Formatting

1. Database Model (Complex) 🗄️
python
class Artifact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    format_id = db.Column(db.Integer, db.ForeignKey("formats.format_id"))
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))

    # Relationships
    format = db.relationship("Format", ...)
    location = db.relationship("Location", ...)
    creators = db.relationship("Creator", ...)
    materials = db.relationship("Material", ...)
    tags = db.relationship("Tag", ...)
    images = db.relationship("Image", ...)
    conservation_report = db.relationship("ConservationReport", ...)
Directly returning this model fails: SQLAlchemy objects are not JSON‑serializable.

Example:

python
artifact = Artifact.query.get(1)
return jsonify(artifact)  # ❌ Error
2. DTO (Simplified) 📦
python
class ArtifactDTO:
    @staticmethod
    def to_dict(artifact: Artifact) -> dict:
        return {
            "id": artifact.id,
            "name": artifact.name,
            "description": artifact.description,
            "format": artifact.format.format_name if artifact.format else None,
            "location": artifact.location.location_name if artifact.location else None,
            "creators": [c.creator_name for c in artifact.creators],
            "materials": [m.material_name for m in artifact.materials],
            "tags": [t.tag_name for t in artifact.tags],
            "images": [img.image_url for img in artifact.images],
        }
Example Transformation
json
// Before (model's to_dict)
{
  "creators": [{ "creator_id": 1, "creator_name": "Leonardo", "biography": "...", ... }],
  "format": { "format_id": 5, "format_name": "Painting" }
}

// After (DTO)
{
  "creators": ["Leonardo"],
  "format": "Painting"
}
✅ Smaller payloads, no circular references, JSON‑friendly.

3. API Normalization 🌐
Different endpoints may return different shapes:

python
# /api/artifacts
[ {...}, {...} ]  # Array

# /api/artifacts/search
{ "results": [ {...}, {...} ], "page": 1, "total": 100 }
Without normalization, the frontend must handle both. With a normalization layer:

js
const resp = normalizeResponse(apiData);
// Always returns { items: [...], meta: {...} }
✅ Consistent structure across endpoints.

4. Frontend Formatting 🎨
Even normalized data isn’t always UI‑ready.

API Output

json
{
  "creators": ["Leonardo da Vinci", "Workshop Assistant"],
  "images": ["https://cdn.com/monalisa-full.jpg", "https://cdn.com/monalisa-detail.jpg"]
}
UI Needs

jsx
<p>By: Leonardo da Vinci, Workshop Assistant</p>
<img src="https://cdn.com/monalisa-full.jpg?size=thumb" />
Instead of duplicating logic in every component:

js
const formatted = ArtifactFormatter.formatForDisplay(artifact);
✅ One place for display logic, reused everywhere.

🚀 Benefits
Smaller payloads → faster responses

Fewer queries → avoids N+1 problems

No circular references → safe serialization

Consistent API shape → simpler frontend code

Centralized formatting → cleaner UI components

TL;DR
Model → raw SQLAlchemy objects (not serializable)

DTO → flattens to JSON‑friendly data

Normalization → consistent API responses

Formatting → UI‑ready data

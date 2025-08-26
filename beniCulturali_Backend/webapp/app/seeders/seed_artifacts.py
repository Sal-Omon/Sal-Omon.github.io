import random
import logging
from faker import Faker
from app import db
from app.models.artifact import Artifact

logger = logging.getLogger(__name__)
fake = Faker()

def seed_artifacts(formats, creators, locations, materials, images, tags, n=30, commit=True):
    """
    Seed artifacts with relations.
    - formats, creators, locations, materials, images, tags are lists of persisted ORM instances.
    - n: number of artifacts to create
    - commit: whether to commit at the end
    Returns list of created artifacts.
    """

    # Sanity checks
    if not all([formats, creators, locations, materials, tags]):
        logger.warning("Missing required base data for seeding artifacts.")
        return []

    # Work with a local copy of images to pop from it safely
    available_images = list(images) if images else []
    random.shuffle(available_images)

    artifacts_created = []

    for i in range(n):
        artifact = Artifact(
            name=fake.catch_phrase(),
            description=fake.text(200),
            format=random.choice(formats),
            creator=random.choice(creators),
            location=random.choice(locations),
        )

        # materials (many-to-many): 1..min(3, len(materials))
        if materials:
            num_materials = random.randint(1, min(3, len(materials)))
            selected_materials = random.sample(materials, num_materials)
            artifact.materials.extend(selected_materials)

        # tags (many-to-many): 0..min(3, len(tags))
        if tags:
            num_tags = random.randint(0, min(3, len(tags)))
            if num_tags > 0:
                selected_tags = random.sample(tags, num_tags)
                artifact.tags.extend(selected_tags)

        # images (one-to-many): assign 1..3 images if available, else skip
        if available_images:
            max_for_this = min(3, len(available_images))
            num_images = random.randint(1, max_for_this)
            for _ in range(num_images):
                img = available_images.pop()  # get unique image
                # attach by appending to artifact.images (bidirectional consistency)
                artifact.images.append(img)

        # Add artifact to session
        db.session.add(artifact)
        artifacts_created.append(artifact)

    # commit or leave to caller
    if commit:
        try:
            db.session.commit()
            logger.info(f"Seeded {len(artifacts_created)} artifacts.")
        except Exception as e:
            logger.exception("Commit failed in seed_artifacts; rolling back.")
            db.session.rollback()
            raise

    return artifacts_created

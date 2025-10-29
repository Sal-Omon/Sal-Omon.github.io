import random
import logging
from typing import List
from faker import Faker
from flask import current_app

from app.extensions import db
from app.models.artifact import Artifact
from app.models.conservation_report import ConservationReport


logger = logging.getLogger(__name__)
fake = Faker()

def seed_artifacts(
    formats: List, 
    creators: List, 
    locations: List, 
    materials: List, 
    tags: List, 
    n: int=30, 
    max_creators_per_artifact: int=3,
    commit: bool = True
    ) -> List[Artifact]:
    
    """
    Seed artifacts with relations.
    - formats, creators, locations, materials, images, tags are lists of persisted ORM instances.
    - n: number of artifacts to create
    - commit: whether to commit at the end
    Returns list of created artifacts.
    """
    
    current_app.logger.debug("seed_artifacts called with n=%s", n)
    
    # Sanity checks per le entità base per procedere
    if not all([formats, creators, locations, materials, tags]):
        current_app.logger.warning("Missing required base data for seeding artifacts.")
        return []


    artifacts_created: List[Artifact] = []
    
    
    for i in range(n):  
        #create artifact without assigning many to many relationship 
        artifact = Artifact(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=100),
            format=random.choice(formats),
            location=random.choice(locations),
        )
        #creator many to many
        if creators:
            max_creators = min(max_creators_per_artifact, len(creators))
            num_creators = random.randint(1, max_creators)
            selected_creators = random.sample(creators, num_creators)
            try:
                artifact.creators.extend(selected_creators)
            except AttributeError:
                current_app.logger.warning("Artifact has no attribute creators")

            
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
        
        
        # Add artifact to session
        db.session.add(artifact)
        artifacts_created.append(artifact)

    # commit or leave to caller
    if commit:
        try:
            db.session.commit()
            current_app.logger.info(f"Seeded {len(artifacts_created)} artifacts.")
        except Exception as e:
            current_app.logger.exception("Commit failed in seed_artifacts; rolling back.")
            db.session.rollback()
            raise

    return artifacts_created

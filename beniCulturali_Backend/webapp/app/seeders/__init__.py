# app/seeders/__init__.py
"""
Seed orchestration: seed_all()

Assunzioni:
- Questo modulo viene eseguito all'interno di app.app_context()
- Le funzioni seed_* restituiranno liste di istanze ORM create (o [] se nulla).
- Le funzioni seed_* possono fare commit internamente; qui lasciamo un commit finale
  come sicurezza (idempotente) e rollback in caso di eccezione.
"""

from flask import current_app
from app.extensions import db

# singoli seeders (import corretti, senza duplicazioni)
from .seed_formats import seed_formats
from .seed_creators import seed_creators
from .seed_locations import seed_locations
from .seed_materials import seed_materials
from .seed_tags import seed_tags
from .seed_images import seed_images
from .seed_artifacts import seed_artifacts
from .seed_conservation_reports import seed_conservation_reports
 
import random


def seed_all(drop: bool = False , dry_run: bool = False):#False significa che effettuerà il commit al db
    """
    Orchestrazione del seeding completo.
    Deve essere eseguito dentro app.app_context().

    :param dry_run: se True esegue tutto ma fa db.session.rollback() anziché commit finale.
    :return: lista di artifacts creati oppure None in caso di errore.
    """
    if current_app.config.get('ENV') == 'production' and not current_app.config.get('ALLOW_PRODUCTION_SEED',False):
        raise RuntimeError('Seeding is not allowed in production without explicit permission')
    
    try:
        if drop:
            db.drop_all()
            current_app.logger.info("DB schema dropped.")
        
        
        db.create_all()
        current_app.logger.info("DB schema created (if not present).")
          
        current_app.logger.info("Seeding base entities: formats, creators, locations, materials, tags")    
        # 1) Seed delle entità di base (senza dipendenze complesse)
        formats = seed_formats(commit=False)           # -> lista di Format
        creators = seed_creators(commit=False)         # -> lista di Creator
        locations = seed_locations(commit=False)       # -> lista di Location
        materials = seed_materials(commit=False)       # -> lista di Material
        tags = seed_tags(commit=False)                 # -> lista di Tag
        
        
        current_app.logger.info("Seeding artifacts (depends on base entities)")
        # 2) Seed degli artifacts (dipende dalle entità di base)
        artifacts = seed_artifacts(
            formats=formats,
            creators=creators,
            locations=locations,
            materials=materials,
            tags=tags,
            commit=False  # lascia True se vuoi che la funzione committi i record artifacts
        )

        # 3) Seed dei rapporti di conservazione e delle immagini (gli artifacts sono stati gia creati)
        current_app.logger.info("Seeding image and conservation reports")
        
        images = seed_images(commit=False, total=50)
        
        if artifacts and images:
            for artifact in artifacts:
                n_assigned_images = random.randint(1, min(3,len(images)))
                selected_images = random.sample(images, n_assigned_images)
                
                for img in selected_images:
                    img.artifact_id = artifact.id
                    db.session.add(img)
                
                #images = [img for img in images if img not in selected_images]
        """
        controlla se images e artifacts esistono
        poi salva in n_associated_images un numero casuale tra 1 e 3,
        il metodo sample sceglie n immagini casuali dalla lista images
        loopa su selected_images
        assegna l'artifact_id di ogni immagine all'id dell'artifact corrente
        aggiunge l'immagine alla sessione
        infine rimuove le immagini già assegnate dalla lista images per evitare duplicati
        """
  
        
        conservation_reports = seed_conservation_reports(artifacts=artifacts, commit=False)





        # Commit finale o rollback se dry_run
        if dry_run:
            db.session.rollback()
            current_app.logger.info("Dry run: changes rolled back")
        else:
            # se i seed individuali hanno già committato, questo commit è noop; mantiene comunque coerenza
            db.session.commit()
            current_app.logger.info("Database seeded successfully")

        return {
            "artifacts": artifacts,
            "images": images,
            "conservation_reports": conservation_reports
        }

    except Exception as e:
        # rollback e log dell'errore: lasciamo il traceback visibile per debugging
        db.session.rollback()
        current_app.logger.error(f"Error seeding database: {e}")
        raise 
        # re-raise se si vuole che lo script termini con traceback oppure ritorna None


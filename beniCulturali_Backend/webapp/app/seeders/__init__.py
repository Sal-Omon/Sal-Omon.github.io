# app/seeders/__init__.py
"""
Seed orchestration: seed_all()

Assunzioni:
- Questo modulo viene eseguito all'interno di app.app_context()
- Le funzioni seed_* restituiranno liste di istanze ORM create (o [] se nulla).
- Le funzioni seed_* possono fare commit internamente; qui lasciamo un commit finale
  come sicurezza (idempotente) e rollback in caso di eccezione.
"""

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

# import models (opzionale, utile per tipi e verifiche)
from app.models import Artifact, Format, Creator, Location, Material, Tag, Image, ConservationReport


def seed_all(dry_run: bool = False):
    """
    Orchestrazione del seeding completo.
    Deve essere eseguito dentro app.app_context().

    :param dry_run: se True esegue tutto ma fa db.session.rollback() anziché commit finale.
    :return: lista di artifacts creati oppure None in caso di errore.
    """
    try:
        # (Opzionale) ricrea schema: drop + create. Attenzione in produzione!
        db.drop_all()
        db.create_all()

        # 1) Seed delle entità di base (senza dipendenze complesse)
        formats = seed_formats()           # -> lista di Format
        creators = seed_creators()         # -> lista di Creator
        locations = seed_locations()       # -> lista di Location
        materials = seed_materials()       # -> lista di Material
        tags = seed_tags()                 # -> lista di Tag
        images = seed_images()             # -> lista di Image

        # 2) Seed degli artifacts (dipende dalle entità di base)
        artifacts = seed_artifacts(
            formats=formats,
            creators=creators,
            locations=locations,
            materials=materials,
            images=images,
            tags=tags,
            commit=True  # lascia True se vuoi che la funzione committi i record artifacts
        )

        # 3) Seed dei rapporti di conservazione (ora che gli artifacts esistono)
        conservation_reports = seed_conservation_reports(artifacts=artifacts, commit=True)

        # Commit finale o rollback se dry_run
        if dry_run:
            db.session.rollback()
            print("Dry run: changes rolled back")
        else:
            # se i seed individuali hanno già committato, questo commit è noop; mantiene comunque coerenza
            db.session.commit()
            print("Database seeded successfully")

        return artifacts

    except Exception as e:
        # rollback e log dell'errore: lasciamo il traceback visibile per debugging
        db.session.rollback()
        print(f"Error seeding database: {e}")
        # re-raise se vuoi che lo script termini con traceback oppure ritorna None
        # raise
        return None


# Permetti l'esecuzione diretta: crea l'app, entra nel context e lancia seed_all
if __name__ == '__main__':
    # Evita di importare create_app all'import time del package: lo facciamo solo quando eseguiamo il file.
    from app import create_app
    app = create_app()
    # Esegui il seeding dentro l'app context
    with app.app_context():
        seed_all(dry_run=False)

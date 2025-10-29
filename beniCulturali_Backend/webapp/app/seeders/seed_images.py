# app/seeders/seed_images.py
import os
import random
import logging

from typing import List, Optional
from faker import Faker
from urllib.parse import urlparse
from flask import current_app
from app.extensions import db
from app.models.image import Image

fake = Faker()
logger = logging.getLogger(__name__)

def is_valid_url(url: str) -> bool:
    """
    Verifica se `url` è un URL http/https valido.
    Se inizia con '/static/images/' controlla anche l'esistenza del file locale.
    Deve essere eseguita dentro app context se controlla filesystem relativo a 
    """
    try:
        if url.startswith("/static/images/"):
            # costruisce path assoluto basato su root_path
            full_path = os.path.join(current_app.root_path, url.lstrip("/"))
            return os.path.exists(full_path)
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def is_valid_image_file(filename: str) -> bool:
    """Controlla l'estensione per capire se è plausibilmente un'immagine."""
    valid_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"}
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def _ensure_total_list(source_list: List[str], total: Optional[int]) -> List[str]:
    if total is None or total <= 0:
        return list(source_list)
    if not source_list:
        return []
    #ripeti la lisata finchè non si raggiunge la lunghezza richiesta
    out = []
    while len(out) < total:
        out.extend(source_list)
    return out[:total]
        
        
        
def seed_images(
    commit: bool = True,
    total: Optional[int]=None
    ) -> List[Image]:
    """
    Scans app/static/images (runtime, inside app context) e crea Image objects.
    - Duplica e mescola i nomi dei file se ci sono immagini locali
    - Se non ci sono file locali genera URL finti con Faker
    - Ritorna la lista di Image ORM istanziati e (se commit=True) salvati in DB
    """
    # risolve il percorso *dentro* la funzione (non a import-time)
    root = current_app.root_path
    image_folder = os.path.join(root, "static", "images")
    logger.info("Seeding Images… (folder: %s)", image_folder)

    # 1) Scansione del folder locale
    image_filenames: List[str] = []
    try:
        if os.path.isdir(image_folder):
            # uso scandir per efficienza
            with os.scandir(image_folder) as it:
                for entry in it:
                    if entry.is_file() and is_valid_image_file(entry.name):
                        image_filenames.append(f"/static/images/{entry.name}")
            logger.debug(f"Local images discovered: files {len(image_filenames)}")
        else:
            logger.info("Image folder not found: %s", image_folder)
    except Exception as e:
        logger.exception("Error scanning image folder: %s", e)




    # 2) costruzione della lista di URL per il seeding
    if image_filenames:
        # duplica per avere più URL se poche immagini fisiche, poi mescola
        image_urls = image_filenames * 2
        random.shuffle(image_urls)
        logger.info(
            "Using %d local images, total URLs prepared: %d",
            len(image_filenames),
            len(image_urls),
        )
    else:
        # fallback: genera alcuni URL finti
        faker_count = 20
        image_urls = [fake.image_url() for _ in range(max(1, faker_count))]
        logger.info("No local images: generating %d Faker URLs", len(image_urls))


    image_urls = _ensure_total_list(image_urls, total)

    # 3) Crea istanze Image 
    images_data: List[Image] = []
    for url in image_urls:
        try:
            # validazione opzionale: skip URL non validi
            if not is_valid_url(url) and not url.startswith("/static/images/"):
                # se non è un local path verificato, ma è un url web malformato, log e continua
                logger.debug("Skipping invalid URL: %s", url)
                continue

            img = Image(image_urls=url)   # <--- usare image_url, non image_urls
            images_data.append(img)
        except Exception as e:
            # non facciamo fallire tutto a causa di un singolo record problematico
            logger.exception("Failed to create Image for url=%s: %s", url, e)

    logger.debug("Prepared %d Image objects for DB insert", len(images_data))


    # 4) Persistenza nel DB (in batch)

    if images_data:
        try:
            db.session.add_all(images_data)
            if commit:
                db.session.commit()
                logger.info("Seeded %d images", len(images_data))
        except Exception as e:
            logger.exception("Database error during image seeding: %s", e)
            db.session.rollback()
            raise
    else:
        logger.warning("No image objects to persist")

    return images_data

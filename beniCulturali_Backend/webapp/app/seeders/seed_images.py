from app import create_app, db
from app.models.image import Image
from faker import Faker
import random
import os
import app
IMAGE_FOLDER_PATH = os.path.join(app.root_path,'static','images')


app = create_app()
fake = Faker()




def seed_images(commit: bool = True) -> list[Image]:
    """
    Seed the Image table by loading files from IMAGE_FOLDER_PATH,
    or generating Faker URLs if the folder is empty/not found.
    Returns the list of created Image instances.
    """
    app.logger.info("Seeding Images…")

    # 1. Raccogli i nomi dei file locali
    image_filenames = []
    if os.path.isdir(IMAGE_FOLDER_PATH):
        app.logger.debug(f"Found image folder: {IMAGE_FOLDER_PATH}")
        for fname in os.listdir(IMAGE_FOLDER_PATH):
            full_path = os.path.join(IMAGE_FOLDER_PATH, fname)
            if os.path.isfile(full_path):
                image_filenames.append(f"/static/images/{fname}")
        app.logger.debug(f"Local images discovered: {image_filenames!r}")
    else:
        app.logger.warning(f"Image folder not found: {IMAGE_FOLDER_PATH}")

    # 2. Prepara URL per il seeding
    if image_filenames:
        # Duplica e mescola per avere abbastanza URL
        image_urls = image_filenames * 2
        random.shuffle(image_urls)
        app.logger.info(f"Using {len(image_filenames)} local images, total URLs: {len(image_urls)}")
    else:
        # Fallback con Faker
        image_urls = [fake.image_url() for _ in range(20)]
        app.logger.info("No local images: generating Faker URLs")

    # 3. Crea oggetti Image
    images_data: list[Image] = []
    for url in image_urls:
        try:
            images_data.append(Image(image_url=url))
        except Exception as e:
            app.logger.error(f"Failed to instantiate Image(url={url}): {e}")

    app.logger.debug(f"Prepared {len(images_data)} Image objects for DB insert")

    # 4. Inserisci nel DB
    db.session.add_all(images_data)
    if commit:
        db.session.commit()
        app.logger.info(f"Seeded {len(images_data)} images")

    return images_data

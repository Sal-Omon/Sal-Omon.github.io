import logging
from typing import Dict, Optional
from sqlalchemy.orm import joinedload, selectinload
from app import db
from app.models.artifact import Artifact
from app.models.creator import Creator
from app.models.format import Format
from app.models.location import Location
from app.models.material import Material
from app.models.tag import Tag

# Limite pratico per evitare risposte troppo grandi
MAX_PER_PAGE = 100

logger = logging.getLogger(__name__)   

class ArtifactDAO:
    """
    Data Access Object per gli Artifact.
    - Restituisce oggetti ORM (o Pagination ORM) per lasciare al service la responsabilità di trasformarli in DTO.
    - Applica eager loading per evitare N+1 e usa distinct() quando i join possono causare duplicati.
    """

    @staticmethod
    def get_all_artifacts(page: int = 1, per_page: int = 20):
        logger.info(f"Recupero tutti gli artifact, pagina: {page}, per_page: {per_page}")
        """Ritorna un oggetto Pagination con tutti gli artifact (paginati).

        :param page: numero di pagina (1-based)
        :param per_page: elementi per pagina
        :return: sqlalchemy Pagination object
        """
        page = max(1, int(page or 1))
        per_page = max(1, min(int(per_page or 20), MAX_PER_PAGE))

        query = (
            db.session.query(Artifact)
            .options(
                # many-to-one: joinedload (single-row join)
                joinedload(Artifact.creator),
                joinedload(Artifact.format),
                joinedload(Artifact.location),
                # collections: selectinload (separate IN query, evita prodotti cartesiani)
                selectinload(Artifact.materials),
                selectinload(Artifact.tags),
                selectinload(Artifact.images),
            )
            .order_by(Artifact.id.asc())
        )

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_artifact_by_id(artifact_id: int) -> Optional[Artifact]:
        logger.info(f"Recupero artifact con ID: {artifact_id}")
        """Ritorna un singolo Artifact (o None) con relazioni principali preloadate."""
        if artifact_id is None:
            return None

        return (
            db.session.query(Artifact)
            .options(
                joinedload(Artifact.creator),
                joinedload(Artifact.format),
                joinedload(Artifact.location),
                selectinload(Artifact.materials),
                selectinload(Artifact.tags),
                selectinload(Artifact.images),
            )
            .filter(Artifact.id == int(artifact_id))
            .first()
        )

    @staticmethod
    def get_artifacts_by_name(name: str, page: int = 1, per_page: int = 20):
        logger.info(f"Ricerca artifact per nome: {name}, pagina: {page}, per_page: {per_page}")
        """Ricerca parziale (case-insensitive) sul campo name. Ritorna Pagination."""
        if not name:
            return db.session.query(Artifact).filter(False).paginate(page=1, per_page=1, error_out=False)

        page = max(1, int(page or 1))
        per_page = max(1, min(int(per_page or 20), MAX_PER_PAGE))

        base = (
            db.session.query(Artifact)
            .options(
                joinedload(Artifact.creator),
                joinedload(Artifact.format),
                joinedload(Artifact.location),
                selectinload(Artifact.materials),
                selectinload(Artifact.tags),
                selectinload(Artifact.images),
            )
            .filter(Artifact.name.ilike(f"%{name.strip()}%"))
            .order_by(Artifact.id.asc())
        )

        return base.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def search_artifacts(filters: Dict, page: int = 1, per_page: int = 20):
        logger.debug(f"Eseguendo ricerca avanzata con filtri: {filters}, pagina: {page}, per_page: {per_page}")
        """
        Ricerca avanzata che accetta più filtri (id, name, creator, format, location, material, tag).
        Ritorna un oggetto Pagination.

        - Le join su tabelle relazionate vengono effettuate solo se necessario.
        - Viene applicato distinct() se sono stati fatti join che possono generare duplicate rows.
        """
        # sanitizzazione e limiti
        page = max(1, int(page or 1))
        per_page = max(1, min(int(per_page or 20), MAX_PER_PAGE))

        query = (
            db.session.query(Artifact)
            .options(
                #prevent N+1 query problems
                joinedload(Artifact.creator),
                joinedload(Artifact.format),
                joinedload(Artifact.location),
                selectinload(Artifact.materials),
                #loading strategies for different relations
                selectinload(Artifact.tags),
                selectinload(Artifact.images),
            )
        )

        used_joins = False
        conditions = []
        #normalizzazione helper da applicare ad ogni attributo
        def norm_str(s):
            return str(s).strip().lower() if s is not None else None


        q = norm_str(filters.get("q")) if filters else None
        if q:
            or_conditions = [
                Artifact.name.ilike(f"%{q}%"), #ilike case insensitive with wildcards %
                Artifact.description.ilike(f"%{q}%"),
                #has for many-to-one or one-to-one relationships
                Artifact.creator.has(Creator.creator_name.ilike(f"%{q}%")), 
                Artifact.format.has(Format.format_name.ilike(f"%{q}%")),
                Artifact.location.has(Location.location_name.ilike(f"%{q}%")),
                #any for one-to-many or many-to-many relationships
                Artifact.materials.any(Material.material_name.ilike(f"%{q}%")),
                Artifact.tags.any(Tag.tag_name.ilike(f"%{q}%")),
                # the search is partial containing % wildcards
            ]
            query = query.filter(db.or_(*or_conditions))
        else:
            query = []


        # filtro per id (esatto)
        artifact_id = filters.get("id") if filters else None
        if artifact_id is not None and str(artifact_id).strip() != "":
            try:
                query = query.filter(Artifact.id == int(artifact_id))
            except (ValueError, TypeError):
                # id non valido -> nessun risultato
                return db.session.query(Artifact).filter(False).paginate(page=page, per_page=per_page, error_out=False)

        # filtro per name (parziale)
        name = norm_str(filters.get("name")) if filters else None
        if name:
            conditions.append(Artifact.name.ilike(f"%{name}%"))

        # filtro per creator (join necessario)
        creator = norm_str(filters.get("creator")) if filters else None
        if creator:
            used_joins = True
            conditions.append(Creator.creator_name.ilike(f"%{creator}%"))

        # filtro per format
        fmt = norm_str(filters.get("format")) if filters else None
        if fmt:
            used_joins = True
            conditions.append(Format.format_name.ilike(f"%{fmt}%"))

        # filtro per location
        location = norm_str(filters.get("location")) if filters else None
        if location:
            used_joins = True
            conditions.append(Location.location_name.ilike(f"%{location}%"))

        # filtro per material (many-to-many)
        material = norm_str(filters.get("material")) if filters else None
        if material:
            used_joins = True
            conditions.append(Material.material_name.ilike(f"%{material}%"))

        # filtro per tag (many-to-many)
        tag = norm_str(filters.get("tag")) if filters else None
        if tag:
            used_joins = True
            conditions.append(Tag.tag_name.ilike(f"%{tag}%"))

        if used_joins:
            # rimuove duplicati dovuti ai join su collezioni
            query = query.distinct()
            #join su creator, format e location many-to-one e su materials e tags(many to many)
            query = query.outerjoin(Artifact.creator).outerjoin(Artifact.format).outerjoin(Artifact.location)
            #per many-to-many collections:materials e tags
            query = query.outerjoin(Artifact.materials).outerjoin(Artifact.tags)
        # outerjoin viene utilizzato per includere anche artifact che non hanno relazioni specifiche; 



        # applica i filtri (AND)
        if conditions:
            query = query.filter(db.and_(*conditions))

        # ordine predefinito e paginazione
        query = query.order_by(Artifact.id.asc())

        return query.paginate(page=page, per_page=per_page, error_out=False)

    @classmethod
    def validate_results(results):
        if not results.items:
            logger.warning("Nessun risultato trovato.")
            return False
        logger.info(f"Trovati {len(results.items)} risultati.")
        return True
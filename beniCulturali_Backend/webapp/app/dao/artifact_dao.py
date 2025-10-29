import logging
from typing import Dict, Optional
from sqlalchemy.orm import joinedload, selectinload
from app.extensions import db,cache
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
    def _norm_str(value):
        return str(value).strip().lower() if value is not None else None
        
    @staticmethod
    def _paginate_query(query, page, per_page):
        page = max(1, int(page or 1))
        per_page = max(1, min(int(per_page or 20), MAX_PER_PAGE))
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def _base_query():
        return (
            db.session.query(Artifact)
            .options(
                joinedload(Artifact.format),
                joinedload(Artifact.location),
                selectinload(Artifact.creators),
                selectinload(Artifact.materials),
                selectinload(Artifact.tags),
                selectinload(Artifact.images),
            )
        )       
    
   
    def get_all_artifacts(self,page: int = 1, per_page: int = 20):
        logger.info(f"Recupero tutti gli artifact, pagina: {page}, per_page: {per_page}")
        """Ritorna un oggetto Pagination con tutti gli artifact (paginati).

        :param page: numero di pagina (1-based)
        :param per_page: elementi per pagina
        :return: sqlalchemy Pagination object
        """
        query =  self._base_query().order_by(Artifact.id.asc())
        return self._paginate_query(query,page=page, per_page=per_page)

   
    def get_artifact_by_id(self,artifact_id: int) -> Optional[Artifact]:
        logger.info(f"Recupero artifact con ID: {artifact_id}")
        """Ritorna un singolo Artifact (o None) con relazioni principali preloadate."""
        if artifact_id is None:
            return None
        logger.info(f"Querying Artifact per ID: {artifact_id}")
        return self._base_query().filter(Artifact.id == int(artifact_id)).first()

   
    def get_artifacts_by_name(self,name:str, page: int = 1, per_page: int = 20):
        logger.info(f"Ricerca artifact per nome: {name}, pagina: {page}, per_page: {per_page}")
        """Ricerca parziale (case-insensitive) sul campo name. Ritorna Pagination."""
        if not name:
            return self._paginate_query(
                db.session.query(Artifact).filter(False), 1, 1
            )
        logger.info(f"Ricerca artifact per nome: {name}")    
        query = ArtifactDAO._base_query().filter(Artifact.name.ilike(f"%{name.strip()}%"))
        return self._paginate_query(query.order_by(Artifact.id.asc()),page, per_page)


    def search_artifacts(self, filters: Dict, page: int = 1, per_page: int = 20):
        logger.debug(f"Eseguendo ricerca avanzata con filtri: {filters}, pagina: {page}, per_page: {per_page}")
        """
        Ricerca avanzata che accetta più filtri (id, name, creator, format, location, material, tag).
        Ritorna un oggetto Pagination.

        - Le join su tabelle relazionate vengono effettuate solo se necessario.
        - Viene applicato distinct() se sono stati fatti join che possono generare duplicate rows.
        """
        
        query = self._base_query()
        conditions = []
        distinct_needed = False #distinguer per evitare duplicati
        
        norm = self._norm_str
        #normalizzazione helper da applicare ad ogni attributo
        #convertendo in una stringa input s
        

        q = norm(filters.get("q")) if filters else None
        if q:
            or_conditions = [ 
                Artifact.name.ilike(f"%{q}%"), #ilike case insensitive with wildcards %
                Artifact.description.ilike(f"%{q}%"),
                #has for many-to-one or one-to-one relationships
                Artifact.format.has(Format.format_name.ilike(f"%{q}%")),
                Artifact.location.has(Location.location_name.ilike(f"%{q}%")),
                #any for one-to-many or many-to-many relationships
                Artifact.creators.any(Creator.creator_name.ilike(f"%{q}%")), 
                Artifact.materials.any(Material.material_name.ilike(f"%{q}%")),
                Artifact.tags.any(Tag.tag_name.ilike(f"%{q}%")),
                # the search is partial containing % wildcards
            ]
            query = query.filter(db.or_(*or_conditions))

# ------------------------SQL RELATIONSJHIP METHODS------------------------
        # filtro per id (esatto)
        artifact_id = filters.get("id") if filters else None
        if artifact_id := filters.get("id"):
            try: 
                conditions.append(Artifact.id == int(artifact_id))
            except (ValueError, TypeError):
                logger.warning(f"Invalid artifact ID filter value: %s", artifact_id)
                return self._paginate_query(db.session.query(Artifact).filter(False), page, per_page)
            
        # filtro per name (parziale) := assegna e verifica
        if name:= norm(filters.get("name")):
            conditions.append(Artifact.name.ilike(f"%{name}%"))

        # filtro per creator (many to many -> any())
        if creator:= norm(filters.get("creator")):
            distinct_needed = True
            conditions.append(Artifact.creators.any(
                Creator.creator_name.ilike(f"%{creator}%")))

        # filtro per format  (many-to-one) use  has()
        if fmt := norm(filters.get("format")):
            conditions.append(Artifact.format.has(  
                Format.format_name.ilike(f"%{fmt}%")))

        # filtro per location
        if location := norm(filters.get("location")):
            conditions.append(Artifact.location.has(    
                Location.location_name.ilike(f"%{location}%")))

        # filtro per material (many-to-many)
        if material := norm(filters.get("material")):
            distinct_needed = True
            conditions.append(Artifact.materials.any(
                Material.material_name.ilike(f"%{material}%")))

        # filtro per tag (many-to-many)
        if tag := norm(filters.get("tag")):
            distinct_needed = True
            conditions.append(Artifact.tags.any(
                Tag.tag_name.ilike(f"%{tag}%")))        
        
        # applica i filtri (AND)
        if conditions:
            query = query.filter(db.and_(*conditions))
    
        if distinct_needed:
            query = query.distinct()
            
        

        return self._paginate_query(query.order_by(Artifact.id.asc()),page, per_page)

    @staticmethod
    def validate_results(results):
        if not results.items:
            logger.warning("Nessun risultato trovato.")
            return False
        logger.info(f"Trovati {len(results.items)} risultati.")
        return True
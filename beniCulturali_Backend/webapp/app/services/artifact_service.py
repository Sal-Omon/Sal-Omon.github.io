import logging
import json
from typing import Dict, Any, Optional
from app.dao.artifact_dao import ArtifactDAO
from app.dto.artifact_dto import ArtifactDTO

from app.cache import cache


logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 100
CACHE_PREFIX = "artifact_service"
MIN_PER_PAGE = 1
MAX_PER_PAGE = 100
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10


def _make_cache_key(prefix:str, filters:Dict, page:int, per_page:int) -> str:
    """
    cache key stabile
    usa json serializzato con chiavi ordinate per evitare ordini diversi
    """
    
    #normalizza valori non serializzabili e ordina le chiavi
    normalized = {
        k : (v if isinstance(v, (str,int,float,bool)) else str(v)) for k,v in sorted(filters.items())}
    
    #crea stringa compatta
    filters_json = json.dumps(normalized, separators=(",", ":"), ensure_ascii=False)
    return f"{CACHE_PREFIX}:{prefix}:{filters_json}:p{page}:s{per_page}"
    
    
class ArtifactService:
    """
    Service layer che orchestri DAO e DTO.
    - Converte Pagination -> dict con items + metadata
    - Applica eventuali regole di business (qui minime)
    """

    def __init__(self):
        self.dao = ArtifactDAO()

    def _validate_pagination_params(self, page: int, per_page: int) -> None:
        """Validate pagination parameters"""
        if page < 1:
            raise ValueError("Page must be >= 1.")
        if not MIN_PER_PAGE <= per_page <= MAX_PER_PAGE:
            raise ValueError(f"per_page must be between {MIN_PER_PAGE} and {MAX_PER_PAGE}.")

    def _pagination_to_dict(self, pagination_obj) -> Dict[str, Any]:
        """Helper che converte l'oggetto Pagination in dict con metadata"""
        if not pagination_obj:
            logger.warning("Pagination object is None or invalid.")
            return {
                "items": [], 
                "total": 0, 
                "page": 1, 
                "per_page": 10,
                "pages": 1
            }

        result = {
            "items": ArtifactDTO.list_from_entities(pagination_obj.items),
            "total": pagination_obj.total,
            "page": pagination_obj.page,
            "per_page": pagination_obj.per_page,
            "pages": pagination_obj.pages
        }
        logger.debug(f"Pagination converted: page {result['page']} of {result['pages']}, total items {result['total']}.")
        return result
        

    def get_all_artifacts(self, page: int = DEFAULT_PAGE, per_page: int = DEFAULT_PER_PAGE) -> Dict[str, Any]:
        try:
            logger.info(f"Fetching all artifacts: page {page}, per_page {per_page}")
            self._validate_pagination_params(page, per_page)
            
            pag = self.dao.get_all_artifacts(page=page, per_page=per_page)
            result = self._pagination_to_dict(pag)
            return result
        except Exception as e:
            logger.exception(f"Error fetching all artifacts: {e}")
            raise

    def get_artifact_by_id(self, artifact_id: int) -> Optional[Dict]:
        try:
            logger.info(f"Fetching artifact by ID: {artifact_id}")
            if artifact_id is None:
                return None
            
            cache_key = f"{CACHE_PREFIX}:artifact:{artifact_id}"
            
            try:
                cached = cache.get(cache_key)
                if cached:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached
            except Exception as e:
                logger.error(f"Cache retrieval error for {cache_key}: {e}")
                
            
            artifact = self.dao.get_artifact_by_id(artifact_id)
            if not artifact:
                logger.warning(f"Artifact with ID {artifact_id} not found.")
                return None
            dto = ArtifactDTO.from_entity(artifact)
            
            try:
                cache.set(cache_key, dto, timeout = CACHE_TIMEOUT)
            except Exception as e:
                logger.warning(f"Cache set error for {cache_key}: {e}")
            
            logger.info(f"Artifact fetched successfully: {artifact_id}")
            return dto
        except Exception as e:
            logger.exception(f"Error fetching artifact by ID {artifact_id}: {e}")
            raise


    def get_artifacts_by_name(self, name: str, page: int = 1, per_page: int = 10):
        try:
            logger.info(f"Fetching artifacts by name: {name}, page: {page}, per_page: {per_page}")
            self._validate_pagination_params(page, per_page)

            if not name or not str(name).strip():
                logger.warning(f"Invalid name parameter: {name}")
                return {"items": [], "total": 0, "page": page, "per_page": per_page, "pages": 1}

            pag = self.dao.get_artifacts_by_name(name=name, page=page, per_page=per_page)
            result = self._pagination_to_dict(pag)

            logger.info(f"Artifacts fetched by name successfully: {name}")
            return result
        except Exception as e:
            logger.error(f"Error fetching artifacts by name {name}: {e}")
            raise



    def search_artifacts(self, filters: Dict, page: int = 1, per_page: int = 10):
        try: 
            filters_norm = {
                k: v.strip() 
                for k, v in (filters or {}).items()
                if v is not None and str(v).strip() != ""
            }

            #caching key include 'q' se presente
            key_parts = [f"{k}:{v}" for k, v in sorted(filters_norm.items())]
            cache_key = f"search:{'&'.join(key_parts)}:page:{page}:per_page:{per_page}"

            #controlla cache
            cached = cache.get(cache_key)
            if cached:
                return cached

            # se non presente nel cache , avvia la ricerca
            pag = self.dao.search_artifacts(filters=filters, page=page, per_page=per_page)
            result = self._pagination_to_dict(pag)

            #cache i risultati per 100 secondi
            try:
                cache.set(cache_key, result, timeout=100)
            except Exception as e:
                logger.warning(f"Cache set error for {cache_key}: {e}")

            return result
        
        except Exception as e:
            logger.error(f"Errore durante la ricerca degli artifact: {e}")
            raise

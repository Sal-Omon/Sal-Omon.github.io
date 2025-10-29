import logging
import json
from typing import Dict, Any, Optional

from app.dao.artifact_dao import ArtifactDAO
from app.dto.artifact_dto import ArtifactDTO
from app.extensions import db,cache

logger = logging.getLogger(__name__)

#Costanti di configurazione locali al service
CACHE_TIMEOUT = 100
CACHE_PREFIX = "artifact_service"
MIN_PER_PAGE = 1
MAX_PER_PAGE = 100
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10


#ripulire i campi di filters k:v e controlla se siano vuoti
def _normalize_filters(filters: Dict) -> Dict[str,str]:
    """Normalizza i filtri 
    rimuovendo chiavi con valore nullo/vuoto
    convertendo i valori in stringhe strip() 
    per avere chiavi coerenti per la cache"""

    if not filters:
        return {}
    normalized = {} #il dizionario è utilizzata solo se filters non è vuoto, evitando memory allocations inutili
    for k, v in filters.items():#{k = key: v = value} 
        if v is None:
            continue
        s = str(v).strip() #converte in stringa e rimuove spazi bianchi all'inizio e alla fine assegnando a s
        if s == "":
            continue
        normalized[k] = s #k corrisponde alla chiave corrispondente nel dizionario filters
        #Ordina le chiavi garantendo stabilità della serializzazione
    return dict(sorted(normalized.items()))           


def _make_cache_key(prefix:str, filters:Dict, page:int, per_page:int) -> str:
    """
    cache key stabile
    usa json serializzato con chiavi ordinate per evitare ordini diversi
    """
    
    #normalizza valori non serializzabili e ordina le chiavi
    norm =  _normalize_filters(filters or {})
    safe = {#dictionary comprehension che effettua il controllo v è un'istanza dei tipi elencati
        k : (v if isinstance(v, (str,int,float,bool)) else str(v)) for k,v in sorted(norm.items())
        }
    
    try:#filters_json converte il dizionario safe in una stringa json
        #crea stringa compatta
        #separators serve a specificare i caratteri di separazione tra gli elementi di un array e tra le chiave e valore
        #il primo elemento di separators rappresenta il carattere di separazione tra gli elem. di un array
        #mentre il secondo rappresenta il carattere di separazione da utilizzare tra una chiave:valore
        filters_json = json.dumps(safe, separators=(",", ":"), ensure_ascii=False,sort_keys=True)
    except Exception:
        #crea una stringa di query da un dizionario di filtri. ordinando le chiavi e unendo le coppie chiave:valore
        #con il carattere &
        # 
        filters_json = "&".join(f"{k}={safe[k]}" for k in sorted(safe.keys()))
    return f"{CACHE_PREFIX}:{prefix}:{filters_json}:p{page}:s{per_page}"
    
def _cache_get(key:str):
    try:
        val = cache.get(key)
        if val is not None:
            logger.debug("Cache hit for key=%s", key)
        else:
            logger.debug("Cache miss for key=%s", key)
        return val
    except Exception as e:
        logger.warning(f"Cache GET error for key=%s:%s", key, e)
        return None
    
def _cache_set(key:str,value,timeout:int = CACHE_TIMEOUT):
    #Helper per scrivere in cache con handling delle eccezioni.
    try:
        cache.set(key,value,timeout=timeout)
        logger.debug("Cache set for %s timeout=%s", key, timeout)
    except Exception as e:
        logger.warning(f"Cache SET error for key=%s:%s ", key,e)

    
    
class ArtifactService:
    """
    Service layer che orchestra DAO e DTO.
    - validazione dei parametri di paging
    - orchestrare chiamate al DAO(data)
    - trasformare entità iin DTO pronti per la serializzazione JSON
    - gestire la cache
    """

    def __init__(self):
        self.dao = ArtifactDAO()


    def _validate_pagination_params(self, page: int, per_page: int) -> None:
        """Validate pagination parameters"""
        if page < 1:
            raise ValueError("Validation pagination param:Page must be >= 1.")
        if not MIN_PER_PAGE <= per_page <= MAX_PER_PAGE:
            raise ValueError(f"per_page must be between {MIN_PER_PAGE} and {MAX_PER_PAGE}.")


#conversione dell oggetto SQLALchemy pagination in uno standard dictionary format
    def _pagination_to_dict(self, pagination_obj) -> Dict[str, Any]:
        """Helper che converte l'oggetto Pagination in dict con metadata"""
        if not pagination_obj:
            logger.warning("Pagination object is None or invalid.")
            return {
                "items": [], 
                "total": 0, 
                "page": DEFAULT_PAGE, 
                "per_page": DEFAULT_PER_PAGE,
                "pages": 1
            }

        result = {
            #ArtifactDTO.list_to_dict converte la lista di Artifact 
            # in una lista di dizionari perche pagination_obj.items è una lista
            "items": ArtifactDTO.list_to_dict(pagination_obj.items),
            "total": pagination_obj.total,
            "page": pagination_obj.page,
            "per_page": pagination_obj.per_page,
            "pages": pagination_obj.pages
        }
        logger.debug(f"Pagination converted: page {result['page']} of {result['pages']}, total items {result['total']}.")
        return result
        

    def get_all_artifacts(self, page: int = DEFAULT_PAGE, per_page: int = DEFAULT_PER_PAGE) -> Dict[str, Any]:
        try:
            logger.info("get_all_artifacts called page=%s per_page=%s", page, per_page)
            self._validate_pagination_params(page, per_page)
            pag = self.dao.get_all_artifacts(page=page, per_page=per_page)
            result = self._pagination_to_dict(pag)
            return result
        except Exception as e:
            logger.exception("Error fetching all artifacts: %s", e)
            raise

    def get_artifact_by_id(self, artifact_id: int) -> Optional[Dict]:
        try:
            logger.info("get_artifact_by_id called id=%s", artifact_id)
            if artifact_id is None:
                return None
            
            cache_key = _make_cache_key("artifact", {"id":str(artifact_id)}, page=1, per_page=1 )
            cached = _cache_get(cache_key)
            if cached is not None:
                return cached
            
            artifact = self.dao.get_artifact_by_id(artifact_id)
            if not artifact:
                logger.warning(f"Artifact with ID %s not found.", artifact_id)
                return None
            
            dto = ArtifactDTO.from_entity(artifact)
            
            _cache_set(cache_key, dto, timeout = CACHE_TIMEOUT)
            return dto
            
        except Exception as e:
            logger.exception("Error fetching artifact by ID %s: %s", artifact_id, e)
            raise


    def get_artifacts_by_name(self, name: str, page: int = 1, per_page: int = 10):
        try:
            logger.info("get_artifacts_by_name called name=%s page=%s per_page=%s", name, page, per_page)
            self._validate_pagination_params(page, per_page)

            if not name or not str(name).strip():
                logger.warning("Invalid name parameter provided")
                return {"items": [], "total": 0, "page": page, "per_page": per_page, "pages": 1}

            pag = self.dao.get_artifacts_by_name(name=name, page=page, per_page=per_page)
            logger.info("Artifacts fetched by name %s successfully:", name)
            return self._pagination_to_dict(pag)
            
        except Exception as e:
            logger.error(f"Error fetching artifacts by name %s " , name, e)
            raise



    def search_artifacts(self, filters: Dict, page: int = 1, per_page: int = 10):
        
        try: 
            logger.info("search_artifacts called for %s, %s, %s", filters, page, per_page)
            self._validate_pagination_params(page, per_page)
            
            _filters_norm = _normalize_filters(filters or {})
            #caching key include 'q' se presente
            cache_key = _make_cache_key("search",_filters_norm,page=page, per_page=per_page)
            #controlla cache
            cached = _cache_get(cache_key)
            if cached is not None:
                return cached

            # se non presente nel cache , avvia la ricerca
            pag = self.dao.search_artifacts(filters=filters, page=page, per_page=per_page)
            result = self._pagination_to_dict(pag)

            #cache i risultati per 100 secondi
            try:
                _cache_set(cache_key, result, CACHE_TIMEOUT)
            except Exception as e:
                logger.warning(f"Cache set error for cache key: %s, error:  %s", cache_key, e)

            return result
        
        except Exception as e:
            logger.error("Errore durante la ricerca degli artifact %s", e)
            raise

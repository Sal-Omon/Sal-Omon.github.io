from flask import Blueprint, jsonify,request
from app.extensions import db,cache
from app.services.artifact_service import ArtifactService
from typing import Dict, Any
import logging

#API gateway


# Prefisso per tutte le rotte in questo blueprint
# main blueprint name , __name__ nome del modulo corrente
main_bp = Blueprint('main', __name__, url_prefix='/api') 
service = ArtifactService()#instance of service

#astrazione dei parametri
def _get_pagination_params():#internal helper function
    """Helper function to get pagination parameters from the req"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return page, per_page

@main_bp.route('/artifacts', methods=['GET'])#declaring route for main_bp
def route_get_all_artifacts(artifacts):
    logging.info(f"Requested received for artifacts: {artifacts}")
    page, per_page = _get_pagination_params()
    result = service.get_all_artifacts(page=page, per_page=per_page)
    if not result:
        logging.warning(f"Artifact name {artifacts} not found")
        return jsonify({'error': 'All Artifacts not found'}),404
    return jsonify(result), 200


@main_bp.route('/artifacts/<int:artifact_id>', methods=['GET'])
def route_get_artifact_by_id(artifact_id):
    logging.info(f"Requested received for artifact ID: {artifact_id}")
    result = service.get_artifact_by_id(artifact_id)
    if not result:
        logging.warning(f"Artifact ID {artifact_id} not found")
        return jsonify({'error': 'Artifact ID not found'}), 404
    return jsonify(result), 200


@main_bp.route('/artifacts/name/<string:name>', methods=['GET'])
def route_get_artifacts_by_name(name:str):
    logging.info(f"Requested received for artifact: {name}")
    page, per_page = _get_pagination_params()
    result = service.get_artifacts_by_name(name=name, page=page, per_page=per_page)
    if not result:
        logging.warning(f"Artifact name {name} not found")
        return jsonify({'error': 'Artifact ID not found'}),404 
    return jsonify(result), 200
 

@main_bp.route('/artifacts/search', methods=['GET'])
def route_search_artifacts():
    """
    read the filters from query string extracting parameters from teh query string 
    of the incoming HTTP request these params are used to filter the search results
    reading the filter is necessary because the client(web browser or another API) 
    needs to specify the criteria for searching artifacts. 
    the client can control what data is returned by the API.
    """
    
    filters = {
        'id': request.args.get('id'),
        'name': request.args.get('name'),
        'creator': request.args.get('creator'),
        'format': request.args.get('format'),
        'location': request.args.get('location'),
        'material': request.args.get('material'),
        'tag': request.args.get('tag'),
        'q': request.args.get('q')
    }
    # pulizia: rimuove chiavi vuote
    filters = {k: v for k, v in filters.items() if v is not None and str(v).strip() != ''}
    logging.info(f"Processed Filters: {filters}")
    
    page, per_page = _get_pagination_params()
    
    result = service.search_artifacts(filters=filters, page=page, per_page=per_page)
    
    item_count = len(result.get('item', [])) if isinstance(result,dict) else 0
    logging.info(f"----------Search results :  {item_count} items found (Page {page}, per Page: {per_page}) ")
    
    return jsonify(result), 200


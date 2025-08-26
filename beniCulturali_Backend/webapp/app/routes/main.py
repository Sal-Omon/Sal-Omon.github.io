from flask import Blueprint, jsonify
from app.extensions import db
from app.services.artifact_service import ArtifactService
from flask import request

main_bp = Blueprint('main', __name__)
service = ArtifactService()


@main_bp.route('/artifacts', methods=['GET'])
def route_get_all_artifacts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return jsonify(service.get_all_artifacts(page=page, per_page=per_page)), 200


@main_bp.route('/artifacts/<int:artifact_id>', methods=['GET'])
def route_get_artifact_by_id(artifact_id):
    result = service.get_artifact_by_id(artifact_id)
    if not result:
        return jsonify({'error': 'Artifact not found'}), 404
    return jsonify(result), 200


@main_bp.route('/artifacts/name/<string:name>', methods=['GET'])
def route_get_artifacts_by_name(name):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return jsonify(service.get_artifacts_by_name(name=name, page=page, per_page=per_page)), 200


@main_bp.route('/artifact/search', methods=['GET'])
def route_search_artifacts():
    # legge i filtri dalla query string
    filters = {
        'id': request.args.get('id'),
        'name': request.args.get('name'),
        'creator': request.args.get('creator'),
        'format': request.args.get('format'),
        'location': request.args.get('location'),
        'material': request.args.get('material'),
        'tag': request.args.get('tag')
    }
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # pulizia: rimuove chiavi vuote
    filters = {k: v for k, v in filters.items() if v is not None and str(v).strip() != ''}

    return jsonify(service.search_artifacts(filters=filters, page=page, per_page=per_page)), 200


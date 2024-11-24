from flask import Blueprint, request, jsonify
from controllers.serviceController import create_service, get_service_by_id, get_all_services, update_service, delete_service, get_open_services
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.Service import ServiceStatus

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

service_bp = Blueprint('service', __name__)

@service_bp.route('/services', methods=['POST'])
def create_service_endpoint():
    data = request.get_json()
    service = create_service(session, data['service_name'], data['description'], data['base_price'], data['subservices'])
    return jsonify({'id': service.id, 'service_name': service.service_name, 'description': service.description, 'base_price': service.base_price, 'subservices': service.subservices, 'status': service.status.value, 'created_at': service.created_at}), 201

@service_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service_endpoint(service_id):
    service = get_service_by_id(session, service_id)
    if service:
        return jsonify({'id': service.id, 'service_name': service.service_name, 'description': service.description, 'base_price': service.base_price, 'subservices': service.subservices, 'status': service.status.value, 'created_at': service.created_at})
    return jsonify({'error': 'Service not found'}), 404

@service_bp.route('/services', methods=['GET'])
def get_all_services_endpoint():
    services = get_all_services(session)
    return jsonify([{'id': service.id, 'service_name': service.service_name, 'description': service.description, 'base_price': service.base_price, 'subservices': service.subservices, 'status': service.status.value, 'created_at': service.created_at} for service in services])

@service_bp.route('/services/<int:service_id>', methods=['PUT'])
def update_service_endpoint(service_id):
    data = request.get_json()
    service = update_service(session, service_id, data['service_name'], data['description'], data['base_price'], data['subservices'], ServiceStatus[data['status'].upper()])
    if service:
        return jsonify({'id': service.id, 'service_name': service.service_name, 'description': service.description, 'base_price': service.base_price, 'subservices': service.subservices, 'status': service.status.value, 'created_at': service.created_at})
    return jsonify({'error': 'Service not found'}), 404

@service_bp.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service_endpoint(service_id):
    service = delete_service(session, service_id)
    if service:
        return jsonify({'message': 'Service deleted successfully'})
    return jsonify({'error': 'Service not found'}), 404

@service_bp.route('/services/open', methods=['GET'])
def get_open_services_endpoint():
    services = get_open_services(session)
    return jsonify([{'id': service.id, 'service_name': service.service_name, 'description': service.description, 'base_price': service.base_price, 'subservices': service.subservices, 'status': service.status.value, 'created_at': service.created_at} for service in services])

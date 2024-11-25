from flask import Blueprint, request, jsonify
from controllers.serviceRequestController import create_service_request, get_service_request_by_id, get_all_service_requests, update_service_request, delete_service_request, get_service_requests_by_customer_id, get_service_requests_by_professional_id, get_closed_service_requests_by_professional_id
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.ServiceRequest import RequestStatus

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

service_request_bp = Blueprint('service_request', __name__)

@service_request_bp.route('/service_requests', methods=['POST'])
def create_service_request_endpoint():
    data = request.get_json()
    service_request = create_service_request(session, data['service_id'], data['user_id'], data.get('professional_id'), data.get('selected_subservices'))
    return jsonify({
        'id': service_request.id,
        'service_id': service_request.service_id,
        'user_id': service_request.user_id,
        'professional_id': service_request.professional_id,
        'selected_subservices': service_request.selected_subservices,
        'status': service_request.status.value,
        'created_at': service_request.created_at
    }), 201

@service_request_bp.route('/service_requests/<int:request_id>', methods=['GET'])
def get_service_request_endpoint(request_id):
    service_request = get_service_request_by_id(session, request_id)
    if service_request:
        return jsonify({
            'id': service_request.id,
            'service_id': service_request.service_id,
            'user_id': service_request.user_id,
            'professional_id': service_request.professional_id,
            'selected_subservices': service_request.selected_subservices,
            'status': service_request.status.value,
            'created_at': service_request.created_at
        })
    return jsonify({'error': 'Service request not found'}), 404

@service_request_bp.route('/service_requests', methods=['GET'])
def get_all_service_requests_endpoint():
    service_requests = get_all_service_requests(session)
    return jsonify([{
        'id': service_request.id,
        'service_id': service_request.service_id,
        'user_id': service_request.user_id,
        'professional_id': service_request.professional_id,
        'selected_subservices': service_request.selected_subservices,
        'status': service_request.status.value,
        'created_at': service_request.created_at
    } for service_request in service_requests])

@service_request_bp.route('/service_requests/<int:request_id>', methods=['PUT'])
def update_service_request_endpoint(request_id):
    data = request.get_json()
    service_request = update_service_request(session, request_id, RequestStatus[data['status'].upper()])
    if service_request:
        return jsonify({
            'id': service_request.id,
            'service_id': service_request.service_id,
            'user_id': service_request.user_id,
            'service_name' : service_request.service_name,
            'selected_subservices': service_request.selected_subservices,
            'status': service_request.status.value,
            'created_at': service_request.created_at
        })
    return jsonify({'error': 'Service request not found'}), 404

@service_request_bp.route('/service_requests/<int:request_id>', methods=['DELETE'])
def delete_service_request_endpoint(request_id):
    service_request = delete_service_request(session, request_id)
    if service_request:
        return jsonify({'message': 'Service request deleted successfully'})
    return jsonify({'error': 'Service request not found'}), 404

@service_request_bp.route('/service_requests/customer/<int:customer_id>', methods=['GET'])
def get_service_requests_by_customer_id_endpoint(customer_id):
    service_requests = get_service_requests_by_customer_id(session, customer_id)
    return jsonify([{
        'id': service_request.id,
        'service_id': service_request.service_id,
        'user_id': service_request.user_id,
        'professional_id': service_request.professional_id,
        'service_name' : service_request.service_name,
        'base_price' : service_request.service_base_price,
        'selected_subservices': service_request.selected_subservices,
        'status': service_request.status.value,
        'created_at': service_request.created_at
    } for service_request in service_requests])

@service_request_bp.route('/service_requests/professional/<int:professional_id>', methods=['GET'])
def get_service_requests_by_professional_id_endpoint(professional_id):
    service_requests = get_service_requests_by_professional_id(session, professional_id)
    return jsonify([{
        'id': service_request.id,
        'service_id': service_request.service_id,
        'user_id': service_request.user_id,
        'professional_id': service_request.professional_id,
        'selected_subservices': service_request.selected_subservices,
        'status': service_request.status.value,
        'created_at': service_request.created_at
    } for service_request in service_requests])

@service_request_bp.route('/service_requests/professional/<int:professional_id>/closed', methods=['GET'])
def get_service_requests_by_professional_id_closed_endpoint(professional_id):
    service_requests = get_closed_service_requests_by_professional_id(session, professional_id)
    return jsonify([{
        'id': service_request.id,
        'service_id': service_request.service_id,
        'user_id': service_request.user_id,
        'professional_id': service_request.professional_id,
        'selected_subservices': service_request.selected_subservices,
        'status': service_request.status.value,
        'created_at': service_request.created_at
    } for service_request in service_requests])
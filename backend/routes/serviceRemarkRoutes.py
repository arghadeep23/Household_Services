from flask import Blueprint, request, jsonify
from controllers.serviceRemarkController import create_service_remark, get_service_remark_by_id, get_all_service_remarks, update_service_remark, delete_service_remark, get_service_remarks_by_professional_id, get_service_remarks_by_user_id
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

service_remark_bp = Blueprint('service_remark', __name__)

@service_remark_bp.route('/service_remarks', methods=['POST'])
def create_service_remark_endpoint():
    data = request.get_json()
    service_remark = create_service_remark(session, data['service_request_id'], data['professional_id'], data['user_id'], data['service_description'], data['rating'], data['user_remark'], data['professional_contact'])
    return jsonify({
        'id': service_remark.id,
        'service_request_id': service_remark.service_request_id,
        'professional_id': service_remark.professional_id,
        'user_id': service_remark.user_id,
        'service_description': service_remark.service_description,
        'rating': service_remark.rating,
        'user_remark': service_remark.user_remark,
        'professional_contact': service_remark.professional_contact,
        'created_at': service_remark.created_at
    }), 201

@service_remark_bp.route('/service_remarks/<int:remark_id>', methods=['GET'])
def get_service_remark_endpoint(remark_id):
    service_remark = get_service_remark_by_id(session, remark_id)
    if service_remark:
        return jsonify({
            'id': service_remark.id,
            'service_request_id': service_remark.service_request_id,
            'professional_id': service_remark.professional_id,
            'user_id': service_remark.user_id,
            'service_description': service_remark.service_description,
            'rating': service_remark.rating,
            'user_remark': service_remark.user_remark,
            'professional_contact': service_remark.professional_contact,
            'created_at': service_remark.created_at
        })
    return jsonify({'error': 'Service remark not found'}), 404

@service_remark_bp.route('/service_remarks', methods=['GET'])
def get_all_service_remarks_endpoint():
    service_remarks = get_all_service_remarks(session)
    return jsonify([{
        'id': service_remark.id,
        'service_request_id': service_remark.service_request_id,
        'professional_id': service_remark.professional_id,
        'user_id': service_remark.user_id,
        'service_description': service_remark.service_description,
        'rating': service_remark.rating,
        'user_remark': service_remark.user_remark,
        'professional_contact': service_remark.professional_contact,
        'created_at': service_remark.created_at
    } for service_remark in service_remarks])

@service_remark_bp.route('/service_remarks/<int:remark_id>', methods=['PUT'])
def update_service_remark_endpoint(remark_id):
    data = request.get_json()
    service_remark = update_service_remark(session, remark_id, data['service_description'], data['rating'], data['user_remark'], data['professional_contact'])
    if service_remark:
        return jsonify({
            'id': service_remark.id,
            'service_request_id': service_remark.service_request_id,
            'professional_id': service_remark.professional_id,
            'user_id': service_remark.user_id,
            'service_description': service_remark.service_description,
            'rating': service_remark.rating,
            'user_remark': service_remark.user_remark,
            'professional_contact': service_remark.professional_contact,
            'created_at': service_remark.created_at
        })
    return jsonify({'error': 'Service remark not found'}), 404

@service_remark_bp.route('/service_remarks/<int:remark_id>', methods=['DELETE'])
def delete_service_remark_endpoint(remark_id):
    service_remark = delete_service_remark(session, remark_id)
    if service_remark:
        return jsonify({'message': 'Service remark deleted successfully'})
    return jsonify({'error': 'Service remark not found'}), 404

# Getting the service remarks of the professional based on his professional_id
@service_remark_bp.route('/service_remarks/professional/<int:professional_id>', methods=['GET'])
def get_service_remarks_by_professional_endpoint(professional_id):
    service_remarks = get_service_remarks_by_professional_id(session, professional_id)
    return jsonify([{
        'id': service_remark.id,
        'service_request_id': service_remark.service_request_id,
        'professional_id': service_remark.professional_id,
        'user_id': service_remark.user_id,
        'service_description': service_remark.service_description,
        'rating': service_remark.rating,
        'user_remark': service_remark.user_remark,
        'professional_contact': service_remark.professional_contact,
        'created_at': service_remark.created_at
    } for service_remark in service_remarks])

# Getting the service remarks of the user based on his user_id
@service_remark_bp.route('/service_remarks/user/<int:user_id>', methods=['GET'])
def get_service_remarks_by_user_endpoint(user_id):
    service_remarks = get_service_remarks_by_user_id(session, user_id)
    return jsonify([{
        'id': service_remark.id,
        'service_request_id': service_remark.service_request_id,
        'professional_id': service_remark.professional_id,
        'user_id': service_remark.user_id,
        'service_description': service_remark.service_description,
        'rating': service_remark.rating,
        'user_remark': service_remark.user_remark,
        'professional_contact': service_remark.professional_contact,
        'created_at': service_remark.created_at
    } for service_remark in service_remarks])

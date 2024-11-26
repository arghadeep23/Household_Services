from flask import Blueprint, request, jsonify
from controllers.professionalController import create_professional, get_professional_by_id, get_all_professionals, update_professional, delete_professional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.Professional import ProfessionalStatus

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

professional_bp = Blueprint('professional', __name__)

@professional_bp.route('/professionals', methods=['POST'])
def create_professional_endpoint():
    data = request.get_json()
    professional = create_professional(session, data['email'], data['password'], data['full_name'], data['experience'], data['document_url'], data['cover_photo_url'], data['address'], data['pincode'], data['service_id'])
    return jsonify({'id': professional.id, 'email': professional.email, 'full_name': professional.full_name, 'experience': professional.experience, 'document_url': professional.document_url, 'cover_photo_url': professional.cover_photo_url, 'address': professional.address, 'pincode': professional.pincode, 'status': professional.status.value, 'created_at': professional.created_at, 'service_id' : professional.service_id}), 201

@professional_bp.route('/professionals/<int:professional_id>', methods=['GET'])
def get_professional_endpoint(professional_id):
    professional = get_professional_by_id(session, professional_id)
    if professional:
        return jsonify({'id': professional.id, 'email': professional.email, 'full_name': professional.full_name, 'experience': professional.experience, 'document_url': professional.document_url, 'cover_photo_url': professional.cover_photo_url, 'address': professional.address, 'pincode': professional.pincode, 'status': professional.status.value, 'created_at': professional.created_at, 'service_id': professional.service_id})
    return jsonify({'error': 'Professional not found'}), 404

@professional_bp.route('/professionals', methods=['GET'])
def get_all_professionals_endpoint():
    professionals = get_all_professionals(session)
    return jsonify([{'id': professional.id, 'email': professional.email, 'full_name': professional.full_name, 'experience': professional.experience, 'document_url': professional.document_url, 'cover_photo_url': professional.cover_photo_url, 'address': professional.address, 'pincode': professional.pincode, 'status': professional.status.value, 'created_at': professional.created_at, 'service_id' : professional.service_id} for professional in professionals])

@professional_bp.route('/professionals/<int:professional_id>', methods=['PUT'])
def update_professional_endpoint(professional_id):
    data = request.get_json()
    professional = update_professional(session, professional_id, data['email'], data['password'], data['full_name'], data['experience'], data['document_url'], data['cover_photo_url'], data['address'], data['pincode'], ProfessionalStatus[data['status'].upper()], data['service_id'])
    if professional:
        return jsonify({'id': professional.id, 'email': professional.email, 'full_name': professional.full_name, 'experience': professional.experience, 'document_url': professional.document_url, 'cover_photo_url': professional.cover_photo_url, 'address': professional.address, 'pincode': professional.pincode, 'status': professional.status.value, 'created_at': professional.created_at, 'service_id': professional.service_id})
    return jsonify({'error': 'Professional not found'}), 404

@professional_bp.route('/professionals/<int:professional_id>', methods=['DELETE'])
def delete_professional_endpoint(professional_id):
    professional = delete_professional(session, professional_id)
    if professional:
        return jsonify({'message': 'Professional deleted successfully'})
    return jsonify({'error': 'Professional not found'}), 404

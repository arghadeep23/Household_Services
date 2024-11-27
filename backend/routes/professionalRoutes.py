from flask import Blueprint, request, jsonify, Flask
from controllers.professionalController import create_professional, get_professional_by_id, get_all_professionals, update_professional, delete_professional, update_professional_status
from controllers.serviceController import get_service_by_id
from controllers.serviceRequestController import get_service_requests_by_service_id, get_closed_service_requests_by_professional_id
from controllers.userController import get_user_by_id
from models.User import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.Professional import ProfessionalStatus
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, get_jwt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

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
        return jsonify({'id': professional.id, 'email': professional.email, 'full_name': professional.full_name, 'experience': professional.experience, 'document_url': professional.document_url, 'cover_photo_url': professional.cover_photo_url, 'address': professional.address, 'pincode': professional.pincode, 'status': professional.status.value, 'created_at': professional.created_at, 'service_id': professional.service_id, 'service_name': professional.service_name})
    return jsonify({'error': 'Professional not found'}), 404

@professional_bp.route('/professionals', methods=['GET'])
def get_all_professionals_endpoint():
    professionals = get_all_professionals(session)
    return jsonify([{'id': professional.id, 'email': professional.email, 'full_name': professional.full_name, 'experience': professional.experience, 'document_url': professional.document_url, 'cover_photo_url': professional.cover_photo_url, 'address': professional.address, 'pincode': professional.pincode, 'status': professional.status.value, 'created_at': professional.created_at, 'service_id' : professional.service_id, 'service_name' : professional.service_name} for professional in professionals])

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

# Getting the service requests which are applicable to the professional based on his service_id
@professional_bp.route('/professionals/service-requests/<int:professional_id>', methods=['GET'])
def get_professional_service_requests_endpoint(professional_id):
    professional = get_professional_by_id(session, professional_id)
    if professional:
        service_requests = get_service_requests_by_service_id(session, professional.service_id)
        # finding the user details of the service requests
        user_details = []
        for request in service_requests:
            user = get_user_by_id(session, request.user_id)
            user_details.append({'id': user.id, 'email': user.email, 'full_name':
                user.full_name, 'address': user.address, 'pincode': user.pincode})
        
        # creating a dictionary with user id as key and user details as value
        user_details = {user['id']: user for user in user_details}

        # return the service requests with user details
        return jsonify([{'id': request.id, 'user_id': request.user_id, 'service_id': request.service_id, 'status': request.status.value, 'created_at': request.created_at, 'user': user_details[request.user_id], 'selected_subservices' : request.selected_subservices} for request in service_requests])

# Getting all the closed service requests of the professional based on his professional_id
@professional_bp.route('/professionals/closed-service-requests/<int:professional_id>', methods=['GET'])
def get_professional_closed_service_requests_endpoint(professional_id):
    professional = get_professional_by_id(session, professional_id)
    if professional:
        service_requests = get_closed_service_requests_by_professional_id(session, professional_id)
        # finding the user details of the service requests
        user_details = []
        for request in service_requests:
            user = get_user_by_id(session, request.user_id)
            user_details.append({'id': user.id, 'email': user.email, 'full_name': user.full_name, 'address': user.address, 'pincode': user.pincode})
        
        # creating a dictionary with user id as key and user details as value
        user_details = {user['id']: user for user in user_details}

        # return the closed service requests with user details
        return jsonify([{'id': request.id, 'user_id': request.user_id, 'service_id': request.service_id, 'status': request.status.value, 'created_at': request.created_at, 'user': user_details[request.user_id], 'selected_subservices': request.selected_subservices, 'rating': request.user_rating, 'remark':request.user_remark} for request in service_requests])
    return jsonify({'error': 'Professional not found'}), 404

        
# For changing professional status : 
@professional_bp.route('/professionals/<int:professional_id>/status', methods=['PUT'])
def update_status(professional_id):
    data = request.get_json()
    new_status = data.get('status')
    
    try:
        professional = update_professional_status(session, professional_id, new_status)
        if not professional:
            return jsonify({'error': 'Professional not found'}), 404
        return jsonify({
            'id': professional.id,
            'status': professional.status.value
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

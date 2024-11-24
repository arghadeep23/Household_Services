from flask import Blueprint, request, jsonify
from controllers.professionalAuthController import create_professional, authenticate_professional, generate_token
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

professional_auth_bp = Blueprint('professional_auth', __name__)

@professional_auth_bp.route('/professional/signup', methods=['POST'])
def signup():
    data = request.get_json()
    professional = create_professional(session, data['email'], data['password'], data['full_name'], data['service'], data['experience'], data['document_url'], data['cover_photo_url'], data['address'], data['pincode'])
    if professional:
        token = generate_token(professional)
        return jsonify({"token": token}), 201
    return jsonify({"error": "Professional already exists"}), 409

@professional_auth_bp.route('/professional/login', methods=['POST'])
def login():
    data = request.get_json()
    professional = authenticate_professional(session, data['email'], data['password'])
    if professional:
        token = generate_token(professional)
        return jsonify({"token": token}), 200
    return jsonify({"error": "No professional found or incorrect password"}), 401

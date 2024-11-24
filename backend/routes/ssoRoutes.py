from flask import Blueprint, request, jsonify
from controllers.ssoController import authenticate_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

sso_bp = Blueprint('sso', __name__)

@sso_bp.route('/sso/login', methods=['POST'])
def sso_login():
    data = request.get_json()
    auth_response = authenticate_user(session, data['email'], data['password'], data['role'])
    token = auth_response.get('token')
    id = auth_response.get('id')
    email = auth_response.get('email')
    full_name = auth_response.get('full_name')
    role = auth_response.get('role')
    if token:
        return jsonify({"token": token, "entity" : {
            "id": id,
            "email": email,
            "full_name": full_name,
            "role": role
        }}), 200
    return jsonify({"error": "No user found or incorrect password"}), 401

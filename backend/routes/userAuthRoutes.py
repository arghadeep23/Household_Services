from flask import Blueprint, request, jsonify
from controllers.userAuthController import create_user, authenticate_user, generate_token
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/customer/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = create_user(session, data['email'], data['password'], data['full_name'], data['address'], data['pincode'])
    if user:
        token = generate_token(user)
        return jsonify({"token": token, "id":user.id, "email" : user.email, "full_name":user.full_name}), 201
    return jsonify({"error": "User already exists"}), 409

@auth_bp.route('/customer/login', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate_user(session, data['email'], data['password'])
    if user:
        token = generate_token(user)
        return jsonify({"token": token}), 200
    return jsonify({"error": "No user found or incorrect password"}), 401

from flask import Blueprint, request, jsonify
from controllers.userController import create_user, get_user_by_id, get_all_users, update_user, delete_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user_endpoint():
    data = request.get_json()
    user = create_user(session, data['email'], data['password'], data['full_name'], data['address'], data['pincode'])
    return jsonify({'id': user.id, 'email': user.email, 'full_name': user.full_name, 'address': user.address, 'pincode': user.pincode, 'created_at': user.created_at}), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_endpoint(user_id):
    user = get_user_by_id(session, user_id)
    if user:
        return jsonify({'id': user.id, 'email': user.email, 'full_name': user.full_name, 'address': user.address, 'pincode': user.pincode, 'created_at': user.created_at})
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users', methods=['GET'])
def get_all_users_endpoint():
    users = get_all_users(session)
    return jsonify([{'id': user.id, 'email': user.email, 'full_name': user.full_name, 'address': user.address, 'pincode': user.pincode, 'created_at': user.created_at} for user in users])

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
    data = request.get_json()
    user = update_user(session, user_id, data['email'], data['full_name'], data['address'], data['pincode'])
    if user:
        return jsonify({'id': user.id, 'email': user.email, 'full_name': user.full_name, 'address': user.address, 'pincode': user.pincode, 'created_at': user.created_at})
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    user = delete_user(session, user_id)
    if user:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

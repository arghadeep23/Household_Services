from flask import Blueprint, request, jsonify
from controllers.adminController import create_admin, get_admin_by_id, get_all_admins, update_admin
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///householdServices.db')
Session = sessionmaker(bind=engine)
session = Session()

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admins', methods=['POST'])
def create_admin_endpoint():
    data = request.get_json()
    admin = create_admin(session, data['email'], data['password'], data['full_name'])
    return jsonify({'id': admin.id, 'email': admin.email, 'full_name': admin.full_name, 'created_at': admin.created_at}), 201

@admin_bp.route('/admins/<int:admin_id>', methods=['GET'])
def get_admin_endpoint(admin_id):
    admin = get_admin_by_id(session, admin_id)
    if admin:
        return jsonify({'id': admin.id, 'email': admin.email, 'full_name': admin.full_name, 'created_at': admin.created_at})
    return jsonify({'error': 'Admin not found'}), 404

@admin_bp.route('/admins', methods=['GET'])
def get_all_admins_endpoint():
    admins = get_all_admins(session)
    return jsonify([{'id': admin.id, 'email': admin.email, 'full_name': admin.full_name, 'created_at': admin.created_at} for admin in admins])

@admin_bp.route('/admins/<int:admin_id>', methods=['PUT'])
def update_admin_endpoint(admin_id):
    data = request.get_json()
    admin = update_admin(session, admin_id, data['email'], data['password'], data['full_name'])
    if admin:
        return jsonify({'id': admin.id, 'email': admin.email, 'full_name': admin.full_name, 'created_at': admin.created_at})
    return jsonify({'error': 'Admin not found'}), 404

# Delete the admin account
@admin_bp.route('/admins/<int:admin_id>', methods=['DELETE'])
def delete_admin_endpoint(admin_id):
    admin = get_admin_by_id(session, admin_id)
    if admin:
        session.delete(admin)
        session.commit()
        return jsonify({'message': 'Admin deleted successfully'})
    return jsonify({'error': 'Admin not found'}), 404

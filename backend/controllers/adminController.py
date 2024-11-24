from models.Admin import Admin
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

def create_admin(session: Session, email: str, password: str, full_name: str):
    hashed_password = generate_password_hash(password)
    new_admin = Admin(email=email, password=hashed_password, full_name=full_name)
    session.add(new_admin)
    session.commit()
    return new_admin

def get_admin_by_id(session: Session, admin_id: int):
    return session.query(Admin).filter(Admin.id == admin_id).first()

def get_all_admins(session: Session):
    return session.query(Admin).all()

def update_admin(session: Session, admin_id: int, email: str, password: str, full_name: str):
    admin = get_admin_by_id(session, admin_id)
    if admin:
        admin.email = email
        admin.password = generate_password_hash(password)
        admin.full_name = full_name
        session.commit()
    return admin
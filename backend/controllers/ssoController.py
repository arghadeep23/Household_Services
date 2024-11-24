from models.User import User
from models.Professional import Professional
from models.Admin import Admin
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def authenticate_user(session: Session, email: str, password: str, role: str):
    try:
        if role == "Customer":
            user = session.query(User).filter(User.email == email).first()
            if user and check_password_hash(user.password, password):
                return generate_token(user, role)
        elif role == "Professional":
            professional = session.query(Professional).filter(Professional.email == email).first()
            if professional and check_password_hash(professional.password, password):
                return generate_token(professional, role)
        elif role == "Admin":
            admin = session.query(Admin).filter(Admin.email == email).first()
            if admin and check_password_hash(admin.password, password):
                return generate_token(admin, role)
    except Exception as e:
        print(f"Error occurred during authentication: {e}")
    return None

def generate_token(entity, role: str):
    payload = {
        "id": str(entity.id),  # Ensure id is a string
        "email": entity.email,
        "full_name": entity.full_name,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    try:
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        return {"token": token, "id": entity.id, "role": role, "full_name": entity.full_name, "email": entity.email}
    except Exception as e:
        print(f"Error occurred while generating token: {e}")
        return None

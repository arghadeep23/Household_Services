from models.Professional import Professional, ProfessionalStatus
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_professional(session: Session, email: str, password: str, full_name: str, experience: int, document_url: str, cover_photo_url: str, address: str, pincode: str, service_id: int):
    if session.query(Professional).filter(Professional.email == email).first():
        return None  # Professional already exists
    hashed_password = generate_password_hash(password)
    new_professional = Professional(email=email, password=hashed_password, full_name=full_name, experience=experience, document_url=document_url, cover_photo_url=cover_photo_url, address=address, pincode=pincode, service_id=service_id)
    session.add(new_professional)
    session.commit()
    return new_professional

def authenticate_professional(session: Session, email: str, password: str):
    professional = session.query(Professional).filter(Professional.email == email).first()
    if professional and check_password_hash(professional.password, password):
        return professional
    return None

def generate_token(professional: Professional):
    payload = {
        "id": professional.id,
        "email": professional.email,
        "full_name": professional.full_name,
        "service_id": professional.service_id,
        "status": professional.status.value,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token

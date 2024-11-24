from models.User import User
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_user(session: Session, email: str, password: str, full_name: str, address: str, pincode: str):
    if session.query(User).filter(User.email == email).first():
        return None  # User already exists
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, full_name=full_name, address=address, pincode=pincode)
    session.add(new_user)
    session.commit()
    return new_user

def authenticate_user(session: Session, email: str, password: str):
    user = session.query(User).filter(User.email == email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def generate_token(user: User):
    payload = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "exp":  datetime.now(timezone.utc) + timedelta(hours=24)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token

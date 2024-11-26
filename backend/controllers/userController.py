from models.User import User
from sqlalchemy.orm import Session

def create_user(session: Session, email: str, password: str, full_name: str, address: str, pincode: str):
    new_user = User(email=email, password=password, full_name=full_name, address=address, pincode=pincode)
    session.add(new_user)
    session.commit()
    return new_user

def get_user_by_id(session: Session, user_id: int):
    return session.query(User).filter(User.id == user_id).first()

def get_all_users(session: Session):
    return session.query(User).all()

def update_user(session: Session, user_id: int, email: str, full_name: str, address: str, pincode: str):
    user = get_user_by_id(session, user_id)
    if user:
        user.email = email
        user.full_name = full_name
        user.address = address
        user.pincode = pincode
        session.commit()
    return user

def delete_user(session: Session, user_id: int):
    user = get_user_by_id(session, user_id)
    if user:
        session.delete(user)
        session.commit()
    return user

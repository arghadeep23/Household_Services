from models.Professional import Professional, ProfessionalStatus
from sqlalchemy.orm import Session

def create_professional(session: Session, email: str, password: str, full_name: str, service: str, experience: int, document_url: str, cover_photo_url: str, address: str, pincode: str):
    new_professional = Professional(email=email, password=password, full_name=full_name, service=service, experience=experience, document_url=document_url, cover_photo_url=cover_photo_url, address=address, pincode=pincode)
    session.add(new_professional)
    session.commit()
    return new_professional

def get_professional_by_id(session: Session, professional_id: int):
    return session.query(Professional).filter(Professional.id == professional_id).first()

def get_all_professionals(session: Session):
    return session.query(Professional).all()

def update_professional(session: Session, professional_id: int, email: str, password: str, full_name: str, service: str, experience: int, document_url: str, cover_photo_url: str, address: str, pincode: str, status: ProfessionalStatus):
    professional = get_professional_by_id(session, professional_id)
    if professional:
        professional.email = email
        professional.password = password
        professional.full_name = full_name
        professional.service = service
        professional.experience = experience
        professional.document_url = document_url
        professional.cover_photo_url = cover_photo_url
        professional.address = address
        professional.pincode = pincode
        professional.status = status
        session.commit()
    return professional

def delete_professional(session: Session, professional_id: int):
    professional = get_professional_by_id(session, professional_id)
    if professional:
        session.delete(professional)
        session.commit()
    return professional

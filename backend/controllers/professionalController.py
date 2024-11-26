from models.Professional import Professional, ProfessionalStatus
from models.Service import Service
from sqlalchemy.orm import Session

def create_professional(session: Session, email: str, password: str, full_name: str, experience: int, document_url: str, cover_photo_url: str, address: str, pincode: str, service_id: int):
    new_professional = Professional(email=email, password=password, full_name=full_name, experience=experience, document_url=document_url, cover_photo_url=cover_photo_url, address=address, pincode=pincode, service_id=service_id)
    session.add(new_professional)
    session.commit()
    return new_professional

def get_professional_by_id(session: Session, professional_id: int):
    return session.query(Professional).filter(Professional.id == professional_id).first()

def get_all_professionals(session: Session):
    professionals = session.query(Professional).all()
    for professional in professionals:
        service = session.query(Service).filter(Service.id == professional.service_id).first()
        professional.service_name = service.service_name if service else None
    return professionals
    
    

def update_professional(session: Session, professional_id: int, email: str, password: str, full_name: str, experience: int, document_url: str, cover_photo_url: str, address: str, pincode: str, status: ProfessionalStatus, service_id: int):
    professional = get_professional_by_id(session, professional_id)
    if professional:
        professional.email = email
        professional.password = password
        professional.full_name = full_name
        professional.service_id = service_id
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

# Change professional status 
def update_professional_status(session: Session, professional_id: int, new_status: str):
    # Convert the new_status string to ProfessionalStatus enum
    if new_status.upper() not in ProfessionalStatus.__members__:
        raise ValueError(f"Invalid status: {new_status}")
    
    status_enum = ProfessionalStatus[new_status.upper()]

    # Fetch the professional record
    professional = session.query(Professional).filter(Professional.id == professional_id).first()
    if not professional:
        return None  # Professional not found

    # Update the status
    professional.status = status_enum
    session.commit()
    return professional
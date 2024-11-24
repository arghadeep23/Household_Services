from models.Service import Service, ServiceStatus
from sqlalchemy.orm import Session

def create_service(session: Session, service_name: str, description: str, base_price: float, subservices: dict):
    new_service = Service(
        service_name=service_name,
        description=description,
        base_price=base_price,
        subservices=subservices
    )
    session.add(new_service)
    session.commit()
    return new_service

def get_service_by_id(session: Session, service_id: int):
    return session.query(Service).filter(Service.id == service_id).first()

def get_all_services(session: Session):
    return session.query(Service).all()

def update_service(session: Session, service_id: int, service_name: str, description: str, base_price: float, subservices: dict, status: ServiceStatus):
    service = get_service_by_id(session, service_id)
    if service:
        service.service_name = service_name
        service.description = description
        service.base_price = base_price
        service.subservices = subservices
        service.status = status
        session.commit()
    return service

def delete_service(session: Session, service_id: int):
    service = get_service_by_id(session, service_id)
    if service:
        session.delete(service)
        session.commit()
    return service

# getting all services whose status is 'Open' 
def get_open_services(session: Session):
    return session.query(Service).filter(Service.status == ServiceStatus.OPEN).all()

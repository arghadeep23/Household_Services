from models.ServiceRequest import ServiceRequest, RequestStatus
from sqlalchemy.orm import Session
from models.Service import Service

def create_service_request(session: Session, service_id: int, user_id: int, professional_id: int = None, selected_subservices: dict = None):
    new_service_request = ServiceRequest(
        service_id=service_id,
        user_id=user_id,
        professional_id=professional_id,
        selected_subservices=selected_subservices
    )
    session.add(new_service_request)
    session.commit()
    return new_service_request

def get_service_request_by_id(session: Session, request_id: int):
    return session.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()

def get_all_service_requests(session: Session):
    return session.query(ServiceRequest).all()

def update_service_request(session: Session, request_id: int, status: RequestStatus):
    service_request = get_service_request_by_id(session, request_id)
    if service_request:
        service_request.status = status
        session.commit()
    return service_request

def get_service_requests_by_customer_id(session: Session, customer_id: int):
    service_requests = session.query(ServiceRequest).filter(ServiceRequest.user_id == customer_id).all()
    for request in service_requests:
        service = session.query(Service).filter(Service.id == request.service_id).first()
        request.service_name = service.service_name
        request.service_base_price = service.base_price
    return service_requests

def get_service_requests_by_professional_id(session: Session, professional_id: int): 
    return session.query(ServiceRequest).filter(ServiceRequest.professional_id == professional_id).all()

def delete_service_request(session: Session, request_id: int):
    service_request = get_service_request_by_id(session, request_id)
    if service_request:
        session.delete(service_request)
        session.commit()
    return service_request

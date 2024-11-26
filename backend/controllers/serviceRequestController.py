from models.ServiceRequest import ServiceRequest, RequestStatus
from models.Professional import Professional
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
    # for each service request, we need to check if professional_id is not None, then we need to fetch the professional details
    # and add it to the response
    service_requests = session.query(ServiceRequest).all()
    for request in service_requests:
        if request.professional_id is not None:
            professional = session.query(Professional).filter(Professional.id == request.professional_id).first()
            request.professional_name = professional.full_name
            request.professional_experience = professional.experience
            request.professional_document_url = professional.document_url
            request.professional_cover_photo_url = professional.cover_photo_url
            request.professional_address = professional.address
            request.professional_pincode = professional.pincode
        else :
            request.professional_name = 'Not Assigned'
            request.professional_experience = 'Not Assigned'
            request.professional_document_url = 'Not Assigned'
            request.professional_cover_photo_url = 'Not Assigned'
            request.professional_address = 'Not Assigned'
            request.professional_pincode = 'Not Assigned'
    return service_requests

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
        request.service_description = service.description 
        
        if(request.professional_id is not None):
            professional = session.query(Professional).filter(Professional.id == request.professional_id).first()
            request.professional_name = professional.full_name
            request.professional_email = professional.email
        else :
            request.professional_name = 'Not Assigned'
            request.professional_email = 'Not Assigned'
    return service_requests

def get_service_requests_by_professional_id(session: Session, professional_id: int): 
    return session.query(ServiceRequest).filter(ServiceRequest.professional_id == professional_id).all()

def delete_service_request(session: Session, request_id: int):
    service_request = get_service_request_by_id(session, request_id)
    if service_request:
        session.delete(service_request)
        session.commit()
    return service_request

# Get closed service requests by professional id
def get_closed_service_requests_by_professional_id(session: Session, professional_id: int):
    return session.query(ServiceRequest).filter(ServiceRequest.professional_id == professional_id, ServiceRequest.status == RequestStatus.CLOSED).all()

# Get service request by service id 
def get_service_requests_by_service_id(session: Session, service_id: int):
    return session.query(ServiceRequest).filter(ServiceRequest.service_id == service_id, ServiceRequest.status == RequestStatus.REQUESTED).all()

# Assigning a professional to a service request and updating the status of the service request to ACCEPTED
def assign_professional_to_service_request(session: Session, request_id: int, professional_id: int):
    try:
        service_request = get_service_request_by_id(session, request_id)
        if service_request:
            service_request.professional_id = professional_id
            service_request.status = RequestStatus.ACCEPTED
            session.commit()
        return service_request
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        return None
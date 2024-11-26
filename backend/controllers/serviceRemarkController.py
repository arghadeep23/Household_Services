from models.ServiceRequest import RequestStatus
from models.ServiceRemark import ServiceRemark
from controllers.serviceRequestController import get_service_request_by_id
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

def create_service_remark(
    session: Session, 
    service_request_id: int, 
    professional_id: int, 
    user_id: int, 
    service_description: str, 
    rating: float, 
    user_remark: str, 
    professional_contact: str
):
    try:
        # Fetch the service request
        service_request = get_service_request_by_id(session, service_request_id)
        if not service_request:
            raise ValueError(f"ServiceRequest with ID {service_request_id} does not exist.")

        # Update the status to CLOSED
        service_request.status = RequestStatus.CLOSED

        # Create the new ServiceRemark
        new_service_remark = ServiceRemark(
            service_request_id=service_request_id,
            professional_id=professional_id,
            user_id=user_id,
            service_description=service_description,
            rating=rating,
            user_remark=user_remark,
            professional_contact=professional_contact
        )

        # Add and commit changes
        session.add(new_service_remark)
        session.commit()

        return new_service_remark

    except (SQLAlchemyError, ValueError) as e:
        # Rollback in case of error
        session.rollback()
        raise e

def get_service_remark_by_id(session: Session, remark_id: int):
    return session.query(ServiceRemark).filter(ServiceRemark.id == remark_id).first()

def get_all_service_remarks(session: Session):
    return session.query(ServiceRemark).all()

def update_service_remark(session: Session, remark_id: int, service_description: str, rating: float, user_remark: str, professional_contact: str):
    service_remark = get_service_remark_by_id(session, remark_id)
    if service_remark:
        service_remark.service_description = service_description
        service_remark.rating = rating
        service_remark.user_remark = user_remark
        service_remark.professional_contact = professional_contact
        session.commit()
    return service_remark

def delete_service_remark(session: Session, remark_id: int):
    service_remark = get_service_remark_by_id(session, remark_id)
    if service_remark:
        session.delete(service_remark)
        session.commit()
    return service_remark

def get_service_remarks_by_professional_id(session: Session, professional_id: int):
    return session.query(ServiceRemark).filter(ServiceRemark.professional_id == professional_id).all()

def get_service_remarks_by_user_id(session: Session, user_id: int):
    return session.query(ServiceRemark).filter(ServiceRemark.user_id == user_id).all()

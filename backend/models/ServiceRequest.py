from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import JSON
from datetime import datetime, timezone
from models.base import Base
import enum


class RequestStatus(enum.Enum):
    REQUESTED = "Requested"
    ACCEPTED = "Accepted"
    CLOSED = "Closed"

class ServiceRequest(Base):
    __tablename__ = 'service_requests'
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('professionals.id', ondelete='SET NULL'), nullable=True)
    selected_subservices = Column(JSON, nullable=True)  # New field for selected subservices
    status = Column(Enum(RequestStatus), nullable=False, default=RequestStatus.REQUESTED)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    service = relationship('Service', back_populates='service_requests')
    user = relationship('User', back_populates='service_requests')
    professional = relationship('Professional', back_populates='service_requests')

    def __init__(self, service_id, user_id, professional_id=None, selected_subservices=None, status=RequestStatus.REQUESTED):
        self.service_id = service_id
        self.user_id = user_id
        self.professional_id = professional_id
        self.selected_subservices = selected_subservices
        self.status = status
        self.created_at = datetime.now(timezone.utc)

ServiceRequest.service_remarks = relationship('ServiceRemark', back_populates='service_request')

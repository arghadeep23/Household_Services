from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from models.base import Base

class ServiceRemark(Base):
    __tablename__ = 'service_remarks'
    id = Column(Integer, primary_key=True)
    service_request_id = Column(Integer, ForeignKey('service_requests.id', ondelete='CASCADE'), nullable=False)
    professional_id = Column(Integer, ForeignKey('professionals.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    service_description = Column(String, nullable=True)
    rating = Column(Float, nullable=False)
    user_remark = Column(String, nullable=True)
    professional_contact = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    service_request = relationship('ServiceRequest', back_populates='service_remarks')
    professional = relationship('Professional', back_populates='service_remarks')
    user = relationship('User', back_populates='service_remarks')

    def __init__(self, service_request_id, professional_id, user_id, service_description, rating, user_remark, professional_contact):
        self.service_request_id = service_request_id
        self.professional_id = professional_id
        self.user_id = user_id
        self.service_description = service_description
        self.rating = rating
        self.user_remark = user_remark
        self.professional_contact = professional_contact
        self.created_at = datetime.now(timezone.utc)


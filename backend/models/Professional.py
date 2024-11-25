from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base
import enum

# Base = declarative_base()

class ProfessionalStatus(enum.Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PENDING = "Pending"

class Professional(Base):
    __tablename__ = 'professionals'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    experience = Column(Integer, nullable=False)
    document_url = Column(String, nullable=True)
    cover_photo_url = Column(String, nullable=True)
    address = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    status = Column(Enum(ProfessionalStatus), nullable=False, default=ProfessionalStatus.PENDING)  # Enum field
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, email, password, full_name, service_id,experience, document_url, cover_photo_url, address, pincode, status=ProfessionalStatus.PENDING):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.service_id = service_id
        self.experience = experience
        self.document_url = document_url
        self.cover_photo_url = cover_photo_url
        self.address = address
        self.pincode = pincode
        self.status = status
        self.created_at = datetime.now(timezone.utc)

Professional.service_requests = relationship('ServiceRequest', back_populates='professional')
Professional.service_remarks = relationship('ServiceRemark', back_populates='professional')
Professional.service = relationship('Service', back_populates='professionals')

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base
import enum


class ServiceStatus(enum.Enum):
    OPEN = "Open"
    CLOSED = "Closed"

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    base_price = Column(Float, nullable=False)
    subservices = Column(JSON, nullable=True)
    status = Column(Enum(ServiceStatus), nullable=False, default=ServiceStatus.OPEN)  # Enum field
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, service_name, description, base_price, subservices, status=ServiceStatus.OPEN):
        self.service_name = service_name
        self.description = description
        self.base_price = base_price
        self.subservices = subservices
        self.status = status
        self.created_at = datetime.now(timezone.utc)

Service.service_requests = relationship('ServiceRequest', back_populates='service')
Service.professionals = relationship('Professional', back_populates='service')
# Example of subservices JSON structure:
# subservices = [
#     {"name": "Leak Repair", "price": 300},
#     {"name": "Pipe Replacement", "price": 800}
# ]

# In this model, the subservices field is a JSON column that can store an array of 
# subservice objects. Each subservice has a name and price.
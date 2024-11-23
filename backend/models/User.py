from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, email, password, full_name, address, pincode):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.address = address
        self.pincode = pincode
        self.created_at = datetime.now(timezone.utc)

User.service_requests = relationship('ServiceRequest', back_populates='user')
User.service_remarks = relationship('ServiceRemark', back_populates='user')
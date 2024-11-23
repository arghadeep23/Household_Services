from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from models.base import Base

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, email, password, full_name):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.created_at = datetime.now(timezone.utc)

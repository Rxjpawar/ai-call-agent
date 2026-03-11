from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    appointment_time = Column(DateTime, nullable=False, index=True)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
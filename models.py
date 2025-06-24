from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer)
    employee_id = Column(Integer)
    strengths = Column(String)
    improvements = Column(String)
    sentiment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)

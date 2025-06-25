from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
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
# models.py
class FeedbackRequest(Base):
    __tablename__ = "feedback_requests"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")

    employee = relationship("User", foreign_keys=[employee_id])
    manager = relationship("User", foreign_keys=[manager_id])

class PeerFeedback(Base):
    __tablename__ = "peer_feedback"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

from pydantic import BaseModel
from datetime import datetime

# Used when an employee sends peer feedback
class PeerFeedbackCreate(BaseModel):
    sender_id: int
    receiver_id: int
    message: str
    anonymous: bool = False

# Used when an employee requests feedback from their manager
class FeedbackRequestCreate(BaseModel):
    employee_id: int
    manager_id: int
    message: str

# Output schema for peer feedback, includes creation timestamp
class PeerFeedbackOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    message: str
    anonymous: bool
    created_at: datetime

    class Config:
        orm_mode = True  # Enables compatibility with ORM models (like SQLAlchemy)

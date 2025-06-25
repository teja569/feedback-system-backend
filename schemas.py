from pydantic import BaseModel
from datetime import datetime

class PeerFeedbackCreate(BaseModel):
    sender_id: int
    receiver_id: int
    message: str
    anonymous: bool = False
class FeedbackRequestCreate(BaseModel):
    employee_id: int
    manager_id: int
    message: str
class PeerFeedbackOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    message: str
    anonymous: bool
    created_at: datetime

    class Config:
        orm_mode = True

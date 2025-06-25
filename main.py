from fastapi import FastAPI, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from models import User, Feedback, FeedbackRequest, PeerFeedback
import models
from schemas import PeerFeedbackCreate, PeerFeedbackOut, FeedbackRequestCreate
from datetime import datetime, timedelta
import uuid

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://feedback-system-frontend-2nsa.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Backend is working"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        return {"error": "Invalid credentials"}
    return {"role": user.role, "id": user.id, "username": user.username}

@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        return {"error": "Username already exists"}
    user = User(username=username, password=password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully", "role": role}

@app.post("/feedback")
def submit_feedback(
    manager_id: int = Form(...),
    employee_id: int = Form(...),
    strengths: str = Form(...),
    improvements: str = Form(...),
    sentiment: str = Form(...),
    db: Session = Depends(get_db)
):
    feedback = Feedback(
        manager_id=manager_id,
        employee_id=employee_id,
        strengths=strengths,
        improvements=improvements,
        sentiment=sentiment
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"message": "Feedback submitted"}

@app.put("/feedback/update/{feedback_id}")
def update_feedback(
    feedback_id: int,
    strengths: str = Form(...),
    improvements: str = Form(...),
    sentiment: str = Form(...),
    db: Session = Depends(get_db)
):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback.strengths = strengths
    feedback.improvements = improvements
    feedback.sentiment = sentiment
    db.commit()
    return {"message": "Feedback updated"}

@app.get("/feedback/{employee_id}")
def get_feedback(employee_id: int, db: Session = Depends(get_db)):
    feedback_list = db.query(Feedback).filter(Feedback.employee_id == employee_id).all()
    return [
        {
            "id": fb.id,
            "strengths": fb.strengths,
            "improvements": fb.improvements,
            "sentiment": fb.sentiment,
            "created_at": fb.created_at,
            "acknowledged": fb.acknowledged
        }
        for fb in feedback_list
    ]

@app.put("/feedback/acknowledge/{feedback_id}")
def acknowledge_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback.acknowledged = True
    db.commit()
    return {"message": "Feedback acknowledged"}

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(User).filter(User.role == "employee").all()
    return [{"id": e.id, "username": e.username} for e in employees]

# Feedback Request
@app.post("/feedback-request")
def create_request(request: FeedbackRequestCreate, db: Session = Depends(get_db)):
    db_req = FeedbackRequest(**request.dict())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return {"message": "Request submitted!"}

@app.get("/manager-requests/{manager_id}")
def get_manager_requests(manager_id: int, db: Session = Depends(get_db)):
    return db.query(FeedbackRequest).filter_by(manager_id=manager_id, status="pending").all()

# Peer Feedback
@app.post("/peer-feedback", response_model=PeerFeedbackOut)
def create_peer_feedback(feedback: PeerFeedbackCreate, db: Session = Depends(get_db)):
    new_feedback = PeerFeedback(**feedback.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

@app.get("/peer-feedback/{receiver_id}", response_model=list[PeerFeedbackOut])
def get_feedback_for_user(receiver_id: int, db: Session = Depends(get_db)):
    return db.query(PeerFeedback).filter_by(receiver_id=receiver_id).all()

# Forgot Password
@app.post("/forgot-password")
def forgot_password(username: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = str(uuid.uuid4())
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
    db.commit()
    print(f"Reset Link: https://your-frontend-url.com/reset-password?token={token}")
    return {"message": "Password reset link generated (check console for now)."}

@app.put("/reset-password")
def reset_password_direct(username: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = new_password
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    return {"message": "Password reset successful"}


# Create tables
models.Base.metadata.create_all(bind=engine)
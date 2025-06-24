from fastapi import FastAPI, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from models import User,Feedback
import models


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Backend is working"}

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        return {"error": "Invalid credentials"}

    return {
        "role": user.role,
        "id": user.id, 
        "username": user.username
    }


@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
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

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(User).filter(User.role == "employee").all()
    return [{"id": e.id, "username": e.username} for e in employees]
@app.put("/feedback/acknowledge/{feedback_id}")
def acknowledge_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback.acknowledged = True
    db.commit()
    return {"message": "Feedback acknowledged"}

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


models.Base.metadata.create_all(bind=engine)
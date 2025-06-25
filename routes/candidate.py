from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Application, Job
from schemas import UserCreate
from auth import get_db, get_password_hash, verify_password, create_access_token, require_role
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/signup")
def signup(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already used")
    user = User(email=data.email, password=get_password_hash(data.password), role="candidate")
    db.add(user)
    db.commit()
    return {"msg": "Candidate registered"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username, User.role == "candidate").first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/applied")
def get_applied_jobs(user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    apps = db.query(Application).filter(Application.candidate_id == user.id).all()
    job_ids = [a.job_id for a in apps]
    return db.query(Job).filter(Job.id.in_(job_ids)).all()

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from models import Job, Application, User
from schemas import JobCreate
from auth import get_db, require_role
from utils.email import send_email

router = APIRouter()

@router.get("/")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.post("/post")
def post_job(data: JobCreate, user: User = Depends(require_role("recruiter")), db: Session = Depends(get_db)):
    job = Job(title=data.title, description=data.description, recruiter_id=user.id)
    db.add(job)
    db.commit()
    return job

@router.post("/{job_id}/apply")
def apply_to_job(job_id: int, background_tasks: BackgroundTasks,
                 user: User = Depends(require_role("candidate")), db: Session = Depends(get_db)):
    if db.query(Application).filter_by(candidate_id=user.id, job_id=job_id).first():
        raise HTTPException(status_code=400, detail="Already applied")
    app = Application(candidate_id=user.id, job_id=job_id)
    db.add(app)
    db.commit()
    job = db.query(Job).filter(Job.id == job_id).first()
    recruiter = db.query(User).filter(User.id == job.recruiter_id).first()
    background_tasks.add_task(send_email, "Application Sent", f"You applied for {job.title}", user.email)
    background_tasks.add_task(send_email, "New Application", f"{user.email} applied for {job.title}", recruiter.email)
    return {"msg": "Applied successfully"}

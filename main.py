from fastapi import FastAPI
from database import engine, Base
from routes import candidate, recruiter, jobs

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(candidate.router, prefix="/candidate", tags=["Candidate"])
app.include_router(recruiter.router, prefix="/recruiter", tags=["Recruiter"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

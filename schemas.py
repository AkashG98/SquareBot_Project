from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class JobCreate(BaseModel):
    title: str
    description: str

class ApplyJob(BaseModel):
    job_id: int
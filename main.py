from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
import shutil
from datetime import date
import models
from database import SessionLocal, engine
from models import CandidateDB
from schemas import Candidate

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Resume API")

UPLOAD_FOLDER = "resumes"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Mini Resume API running"}

@app.get("/health")
def health_check():
    return {"status" : "ok"}


@app.post("/candidates", response_model=Candidate)
async def create_candidate(
    full_name: str = Form(...),
    dob: date = Form(...),
    phone_number: str = Form(...),
    address: str =  Form(...),
    education: str =  Form(...),
    graduation_year: int =  Form(...),
    experience: float =  Form(...),
    skills: str =  Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    allowed_extension = (".pdf", ".doc", ".docx")
    if not resume.filename.lower().endswith(allowed_extension):
        raise HTTPException(status_code=400, detail="Invalid Resume File Type")
    
    candidate_id = str(uuid.uuid4())
    
    safe_filename = resume.filename.replace(" ", "_")
    file_path = f"{UPLOAD_FOLDER}/{candidate_id}_{safe_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
          
    if not phone_number.isdigit() or len(phone_number) != 10:
        raise HTTPException(
            status_code=400,
            detail="Phone number must be exactly 10 digits"
        )
    
    candidate = CandidateDB(
        id = candidate_id,
        full_name = full_name.strip(),
        dob = dob,
        phone_number = phone_number.strip(),
        address = address.strip(),
        education = education.strip(),
        graduation_year = graduation_year,
        experience = experience,
        skills = skills.lower().strip(),  
        resume_filename = file_path,  
        
    )    
    db.add(candidate)
    db.commit()
    db.refresh(candidate)    
    return candidate



@app.get("/candidates", response_model=List[Candidate])
def filter_candidates(
    skill : Optional[str] = None,
    experience : Optional[float] = None,
    graduation_year : Optional[int] =None,
    db : Session = Depends(get_db),
):
    
    query = db.query(CandidateDB)
    
    if skill:
        skill_list = [s.strip().lower() for s in skill.split(",")]

        for s in skill_list:
            query = query.filter(CandidateDB.skills.ilike(f"%{s}%"))
    
    if experience is not None:
        query = query.filter(CandidateDB.experience >= experience)
    
    if graduation_year is not None:
        query = query.filter(CandidateDB.graduation_year == graduation_year)
    
    return query.all()

@app.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id:str, db : Session = Depends(get_db)):
    candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate Not Found")  
    return candidate 


@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id:str, db : Session = Depends(get_db)):
    candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate Not Found")
    
    if os.path.exists(candidate.resume_filename):
        os.remove(candidate.resume_filename)
        
    db.delete(candidate)
    db.commit()
    return {"message" : "Candidate Deleted Successfully"}
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import date
import uuid


app = FastAPI(title="Mini Resume API")

candidates = []

class Candidate(BaseModel):
    id : str
    full_name : str
    dob : date 
    phone_number : str
    address : str
    education : str
    graduation_year : int
    experience : float
    skills : List[str]
    resume_filename : str
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, x: str):
        if (not x.isdigit()) or len(x) != 10:
            raise ValueError("Invalid Phone Number")
        return x
    
    @field_validator("graduation_year")
    @classmethod
    def validate_year(cls, x: int):
        if x < 1950 or x > date.today().year + 1:
            raise ValueError("Invalid Graduation Year")
        return x
    
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
    resume: UploadFile = File(...)
):
    allowed_extension = (".pdf", ".doc", ".docx")
    if not resume.filename.lower().endswith(allowed_extension):
        raise HTTPException(status_code=400, detail="Invalid Resume File Type")
    
    candidate_id = str(uuid.uuid4())
    
    candidate = Candidate(
        id = candidate_id,
        full_name = full_name.strip(),
        dob = dob,
        phone_number = phone_number.strip(),
        address = address.strip(),
        education = education.strip(),
        graduation_year = graduation_year,
        experience = experience,
        skills = [x.strip().lower() for x in skills.split(",") if x.strip()],  
        resume_filename = resume.filename,  
        
    )
    
    candidates.append(candidate)
    
    return candidate


@app.get("/candidates", response_model=List[Candidate])
def filter_candidates(
    skill : Optional[str] = None,
    experience : Optional[float] = None,
    graduation_year : Optional[int] =None,
):
    
    results = candidates
    
    if skill:
        results = [x for x in results if skill.lower() in x.skills]
    
    if experience is not None:
        results = [x for x in results if x.experience >= experience]
    
    if graduation_year is not None:
        results = [x for x in results if x.graduation_year == graduation_year]
    
    return results
    
    
@app.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id):
    for c in candidates:
        if candidate_id == c.id:
            return c
    raise HTTPException(status_code=404, detail="Candidate Not Found")

@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id):
    for i, c in enumerate(candidates):
        if c.id == candidate_id:
            candidates.pop(i)
            return {"message" : "Candidate Deleted Successfully"}
    raise HTTPException(status_code=404, detail="Candidate Not Found")
    
 
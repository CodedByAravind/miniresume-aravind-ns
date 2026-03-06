from pydantic import BaseModel, field_validator
from datetime import date
from typing import List

class Candidate(BaseModel):
    id : str
    full_name : str
    dob : date
    phone_number : str
    address : str
    education : str
    graduation_year : int
    experience : float
    skills : str
    resume_filename : str
    
    class Config:
        from_attributes = True
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Phone number must be 10 digits")
        return v
        
    
    
    
    
    
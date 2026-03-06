from sqlalchemy import Column, String, Integer, Float
from database import Base

class CandidateDB(Base):
    __tablename__ = "candidates"
    
    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    dob = Column(String)
    phone_number = Column(String)
    address = Column(String)
    education = Column(String)
    graduation_year = Column(Integer)
    experience = Column(Float)
    skills = Column(String)
    resume_filename = Column(String)
    
    
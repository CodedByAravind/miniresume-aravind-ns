# Mini Resume Management API

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic

---


---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CodedByAravind/miniresume-aravind-ns.git
cd miniresume-aravind-ns
```

### 2. Create virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment

Windows:
```bash
.\.venv\Scripts\activate
```

Linux / Mac:
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Server will run at:
```bash
http://127.0.0.1:8000
```

Swagger documentation available at:
```bash
http://127.0.0.1:8000/docs
```

## API Endpoints
### Health Check
```bash
GET /health
```
### Create Candidate
```bash
POST /candidates
```

Form fields:

full_name

dob (YYYY-MM-DD)

phone_number

address

education

graduation_year

experience

skills (comma-separated string)

resume file (PDF/DOC/DOCX)

### List / Filter Candidates
```bash
GET /candidates?skill=python&experience=1&graduation_year=2024
```
### Get Candidate by ID
```bash
GET /candidates/{candidate_id}
```
### Delete Candidate
```bash
DELETE /candidates/{candidate_id}
```
### Example Response
```json
{
  "id": "a1e2e5a3-ecc9-4bc9-8b4d-d256f08db106",
  "full_name": "Aravind",
  "dob": "2002-01-01",
  "phone_number": "9876543210",
  "address": "Kerala",
  "education": "BSc",
  "graduation_year": 2024,
  "experience": 0,
  "skills": ["python", "fastapi"],
  "resume_filename": "resume.pdf"
}
```
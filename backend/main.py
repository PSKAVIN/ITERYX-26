from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import io
from parser import parse_resume_content
from matcher import calculate_semantic_match
from scorer import generate_score_report

app = FastAPI(title="AI Resume Quality Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    jd_text: str
    resume_text: str

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
    
    content = await file.read()
    parsed_data = parse_resume_content(content, file.filename)
    text = parsed_data["text"]
    
    # Simple Heuristic to Reject Non-Resumes
    resume_keywords = ["experience", "education", "skills", "resume", "cv", "projects", "objective", "work history", "employment", "professional"]
    text_lower = text.lower()
    
    match_count = sum(1 for kw in resume_keywords if kw in text_lower)
    
    if match_count < 2 or len(text.split()) < 30:
        raise HTTPException(
            status_code=400, 
            detail="The uploaded document does not appear to be a resume. It is missing common sections like 'Experience', 'Education', or 'Skills'."
        )
        
    return {"extracted_text": text, "entities": parsed_data["entities"]}

@app.post("/analyze")
async def analyze_resume(request: AnalyzeRequest):
    if not request.resume_text or not request.jd_text:
        raise HTTPException(status_code=400, detail="Resume text and JD text are required")
        
    jd_match_result = calculate_semantic_match(request.resume_text, request.jd_text)
    jd_alignment_score = jd_match_result["score"]
    missing_keywords = jd_match_result["missing_keywords"]
    missing_skills = jd_match_result.get("missing_skills", [])
    
    report = generate_score_report(request.resume_text, jd_alignment_score, missing_keywords, missing_skills)
    return report

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

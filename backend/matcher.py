import re

# We are leaving the Sentence-BERT code commented out because downloading 
# the 90MB 'all-MiniLM-L6-v2' model is taking too long on the current network.
# For the hackathon MVP demo, we'll use a fast mathematical fallback.
# 
# from sentence_transformers import SentenceTransformer, util
# model = SentenceTransformer('all-MiniLM-L6-v2') 

def calculate_semantic_match(resume_text: str, jd_text: str) -> float:
    if not resume_text or not jd_text:
        return {"score": 50.0, "missing_keywords": []}
    
    # ---------------------------------------------------------
    # SUPER FAST HEURISTIC MATCHER (Fallback for Demo)
    # ---------------------------------------------------------
    resume_words = set(re.findall(r'\b[a-z]{3,}\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b[a-z]{3,}\b', jd_text.lower()))
    
    # Very basic stop words to ignore
    stop_words = {"the", "and", "for", "with", "that", "this", "you", "are", "not", "have", "has", "will", "can", "our", "your", "from", "their", "they"}
    jd_keywords = jd_words - stop_words
    
    if len(jd_keywords) == 0:
        return {"score": 50.0, "missing_keywords": []}
        
    common_words = resume_words.intersection(jd_keywords)
    missing_words = jd_keywords - resume_words
    
    # ---------------------------------------------------------
    # HARD SKILLS MATCHER
    # ---------------------------------------------------------
    # A lightweight knowledge base of common industry skills
    known_skills = {
        "python", "java", "javascript", "react", "node", "sql", "aws", "azure",
        "excel", "agile", "scrum", "marketing", "sales", "seo", "design", "figma",
        "kubernetes", "docker", "machine learning", "ai", "pandas", "pytorch",
        "communication", "leadership", "management", "c++", "c#", "html", "css",
        "git", "linux", "jenkins", "jira", "tableau", "powerbi", "salesforce"
    }
    
    jd_skills_required = known_skills.intersection(jd_words)
    missing_skills = jd_skills_required - resume_words
    
    coverage = len(common_words) / float(len(jd_keywords))
    
    score = (coverage * 100) * 1.8 
    normalized = max(0.0, min(100.0, score + 20)) # +20 base score
    
    # Return top 5 missing words that might be important (excluding known skills to prevent duplicates)
    other_missing = missing_words - known_skills
    top_missing = sorted(list(other_missing), key=len, reverse=True)[:5]
    
    return {
        "score": round(normalized, 2),
        "missing_keywords": top_missing,
        "missing_skills": list(missing_skills)
    }


def generate_score_report(resume_text: str, jd_alignment_score: float, missing_keywords: list = None, missing_skills: list = None) -> dict:
    
    content_score = 0
    format_score = 0
    feedback = []
    
    resume_lower = resume_text.lower()
    
    if missing_keywords is None:
        missing_keywords = []
    if missing_skills is None:
        missing_skills = []

    # 1. Content Heuristics
    action_verbs = ['achieved', 'managed', 'developed', 'led', 'designed', 'created', 'implemented', 'improved', 'increased', 'optimized']
    verbs_found = [v for v in action_verbs if v in resume_lower]
    
    if len(verbs_found) >= 5:
        content_score += 100
        feedback.append({"type": "positive", "text": "Strong use of action verbs to describe accomplishments."})
    elif len(verbs_found) >= 2:
        content_score += 60
        feedback.append({"type": "warning", "text": "Consider adding more action verbs like 'achieved' or 'optimized' for impact."})
    else:
        content_score += 30
        feedback.append({"type": "negative", "text": "Missing strong action verbs. Rewrite bullet points to lead with impactful terms."})

    # 2. Format Heuristics
    sections = {
        "Education": ["education", "university", "college", "bachelor", "master", "ph.d", "bs", "ms"],
        "Experience": ["experience", "work history", "employment", "professional"],
        "Skills": ["skills", "technologies", "core competencies", "tools"]
    }
    
    missing_sections = []
    format_points = 100
    for section, keywords in sections.items():
        if not any(kw in resume_lower for kw in keywords):
            missing_sections.append(section)
            format_points -= 30
            
    if missing_sections:
        feedback.append({"type": "negative", "text": f"Could not detect critical sections: {', '.join(missing_sections)}."})
    else:
        feedback.append({"type": "positive", "text": "Standard resume sections (Education, Experience, Skills) are present and clear."})
            
    format_score = max(0, format_points)
    
    # 3. Length Check
    word_count = len(resume_text.split())
    if word_count < 200:
        feedback.append({"type": "negative", "text": "Resume content is thin. Add more details and quantifiable metrics to your roles."})
        content_score = max(0, content_score - 20)
    elif word_count > 1000:
        feedback.append({"type": "warning", "text": "Resume is slightly long. Ensure clarity and remove non-relevant legacy roles."})
        format_score = max(0, format_score - 20)
    else:
        feedback.append({"type": "positive", "text": "Resume length is optimal and easy to parse."})
        
    # Quantitative Check
    if '%' not in resume_text and '$' not in resume_text:
        feedback.append({"type": "warning", "text": "Lack of quantifiable metrics (e.g. %, $ values). Numbers help demonstrate measurable impact."})
        content_score = max(0, content_score - 15)
        
    # Skills Feedback (NEW)
    if missing_skills:
        feedback.append({
            "type": "negative", 
            "text": f"Lacking Key Skill Abilities: The Job Description requires the following core skills which are not clearly found in your resume: [{', '.join(missing_skills).title()}]"
        })
        jd_alignment_score = max(0, jd_alignment_score - (len(missing_skills) * 5))
        
    # Alignment Feedback
    if jd_alignment_score > 80:
        feedback.append({"type": "positive", "text": "Excellent semantic alignment with the given job description!"})
    elif jd_alignment_score < 40:
        feedback.append({"type": "negative", "text": f"Poor semantic match with JD. Tailor your focus more towards the job's core requirements. Missing keywords: {', '.join(missing_keywords)}"})
    else:
        feedback.append({"type": "warning", "text": f"Moderate JD match. Make sure core skills directly match the requirements. Missing keywords: {', '.join(missing_keywords)}"})

    # Ensure max 100 bounds on content
    content_score = min(100, max(0, content_score))
    format_score = min(100, max(0, format_score))

    # Overall Formula (Weights)
    overall_score = (content_score * 0.4) + (jd_alignment_score * 0.4) + (format_score * 0.2)
    
    # Sort feedback: negatives first, then warnings, then positive
    order = {"negative": 0, "warning": 1, "positive": 2}
    feedback = sorted(feedback, key=lambda x: order.get(x["type"], 3))
    
    return {
        "overall_score": round(overall_score),
        "sub_scores": {
            "content": round(content_score),
            "format": format_score,
            "alignment": round(jd_alignment_score)
        },
        "feedback": feedback
    }

import fitz  # PyMuPDF
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spacy model 'en_core_web_sm' not found. Entities extraction will be skipped.")
    nlp = None

def parse_resume_content(file_bytes: bytes, filename: str):
    text = ""
    if filename.endswith('.pdf'):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
    elif filename.endswith('.docx'):
        try:
            import docx
            from io import BytesIO
            doc = docx.Document(BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
        except ImportError:
            print("Warning: python-docx not installed. Run pip install python-docx")
            text = "DOCX extraction failed internally."
            
    entities = {}
    if nlp and text:
        # process text in chunks if it's too long, but for a resume it's fine
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            if ent.text.strip() not in entities[ent.label_]:
                entities[ent.label_].append(ent.text.strip())
                
    return {
        "text": text.strip(),
        "entities": entities
    }

# AI-Powered Resume Quality Analyzer

This document outlines the implementation plan for the 24-hour MVP of the AI-Powered Resume Quality Analyzer. We will build a full-stack application using Next.js for the frontend and FastAPI for the backend, focusing on core functionality like PDF parsing, semantic matching, and AI-driven quality scoring.

## User Review Required

> [!IMPORTANT]
> The backend relies on machine learning models (`spacy` with `en_core_web_sm` and `sentence-transformers`). Downloading these models might take some time on the first run. Please confirm if you are okay with running Python locally for the backend. I will provide a virtual environment setup script.

> [!NOTE]
> Since this is a 24-hour hackathon scope, we will store processing results in memory/local file system instead of setting up PostgreSQL and AWS S3, as requested. Let me know if you would like me to set up placeholders for the DB integration.

## Proposed Changes

### Backend (FastAPI + Python ML)

The backend will expose a REST API to process PDF/DOCX resumes and evaluate them against Job Descriptions.

*   **`backend/requirements.txt`**: Dependencies including `fastapi`, `uvicorn`, `python-multipart`, `PyMuPDF` (for PDF text extraction), `spacy`, and `sentence-transformers` (Sentence-BERT).
*   **`backend/main.py`**: The FastAPI application entry point with `/upload` and `/analyze` routes.
*   **`backend/services/parser.py`**: Logic to extract text from PDFs using PyMuPDF and extract entities (skills, experience, education) using spaCy NER.
*   **`backend/services/matcher.py`**: Semantic matching engine using Sentence-BERT cosine similarity to compare resume text against JD text.
*   **`backend/services/scorer.py`**: Heuristics engine to compute the overall score (Content 40%, JD Alignment 40%, Format 20%) and generate line-level feedback.

### Frontend (Next.js + Tailwind CSS)

The frontend will provide a modern, dark/light theme supporting responsive interface for users to upload resumes and view analytics.

*   **`frontend/package.json`**: Dependencies like `React`, `Next.js`, `TailwindCSS`, `axios`, `react-dropzone` (for file upload), and `recharts` / `react-circular-progressbar` (for the dashboard).
*   **`frontend/app/globals.css` & `tailwind.config.ts`**: Modern aesthetic styling tokens.
*   **`frontend/app/page.tsx`**: Main landing page layout.
*   **`frontend/components/Dropzone.tsx`**: Drag and drop file upload component.
*   **`frontend/components/JdInput.tsx`**: Text area for the Job Description.
*   **`frontend/components/Dashboard.tsx`**: Results view containing circular charts for the overall score and bar charts for sub-scores, along with feedback details.

## Open Questions

> [!QUESTION]
> 1. Which version of Tailwind CSS would you prefer to use? I recommend Tailwind v3 with Next.js App Router for stability, but we can use v4 if preferred.
> 2. For the UI design, do you prefer a specific primary color (e.g., deep blue/indigo, electric purple, emerald green) for the "Premium UI" feel?

## Verification Plan

### Automated Tests
*   Start the FastAPI server and verify the `/health` endpoint.
*   Test the `/analyze` endpoint using built-in mock text to ensure Sentence-BERT and spaCy are loading correctly without crashing.

### Manual Verification
*   Start the Next.js dev server.
*   Upload a sample PDF resume and a sample Software Engineer JD.
*   Verify that the analytics dashboard renders the charts, and the correct overall score, sub-scores, and line-level qualitative feedback are displayed.

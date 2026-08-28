import os
import shutil
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.genai.errors import ClientError

from app.services.analysis_service import analyze_documents
from app.rag.retriever import DocumentRetriever
from app.services.document_service import process_pdf
from app.services.qa_service import answer_question


class QuestionRequest(BaseModel):
    question: str


app = FastAPI(
    title="JobMatch RAG API",
    description="RAG-powered Resume and Job Description Matching API",
    version="1.0.0",
)


# ---------------------------------------------------------
# RAG RETRIEVER
# ---------------------------------------------------------

document_retriever = None


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://jobmatch-rag.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "JobMatch RAG API is running."
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# RAG QUESTION ANSWERING
# ---------------------------------------------------------

@app.post("/api/ask")
async def ask_question(
    request: QuestionRequest,
):

    global document_retriever

    if not request.question.strip():
        return {
            "success": False,
            "message": "Question cannot be empty.",
        }

    if document_retriever is None:
        return {
            "success": False,
            "message": (
                "Please analyze a resume before "
                "asking questions."
            ),
        }

    try:

        result = answer_question(
            question=request.question,
            retriever=document_retriever,
            top_k=3,
        )

        return {
            "success": True,
            "data": result,
        }

    except ClientError as error:

        print(
            f"Gemini question answering error: {error}"
        )

        if error.code == 429:
            return {
                "success": False,
                "message": (
                    "Gemini API quota is temporarily "
                    "exhausted. Please try again later."
                ),
            }

        return {
            "success": False,
            "message": (
                "Gemini was unable to answer "
                "the question."
            ),
        }

    except Exception as error:

        print(
            f"Question answering failed: {error}"
        )

        return {
            "success": False,
            "message": (
                "Unable to answer the question."
            ),
        }


# ---------------------------------------------------------
# File Validation
# ---------------------------------------------------------

def validate_pdf(
    file: UploadFile,
) -> None:

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is missing.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail=(
                f"{file.filename} must be a PDF file."
            ),
        )


# ---------------------------------------------------------
# Temporary File Helper
# ---------------------------------------------------------

def save_upload_temporarily(
    file: UploadFile,
) -> str:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    ) as temp_file:

        shutil.copyfileobj(
            file.file,
            temp_file,
        )

        return temp_file.name


# ---------------------------------------------------------
# JobMatch Analysis
# ---------------------------------------------------------

@app.post("/api/analyze")
async def analyze_job_match(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
):

    global document_retriever

    validate_pdf(resume)
    validate_pdf(job_description)

    resume_path = None
    jd_path = None

    try:

        # -------------------------------------------------
        # Save uploaded files
        # -------------------------------------------------

        resume_path = save_upload_temporarily(
            resume
        )

        jd_path = save_upload_temporarily(
            job_description
        )

        # -------------------------------------------------
        # Process PDFs
        # -------------------------------------------------

        resume_chunks = process_pdf(
            resume_path,
            document_type="resume",
        )

        jd_chunks = process_pdf(
            jd_path,
            document_type="job_description",
        )

        # -------------------------------------------------
        # JobMatch analysis
        # -------------------------------------------------

        result = analyze_documents(
            resume_chunks,
            jd_chunks,
        )

        # -------------------------------------------------
        # Index current resume for RAG
        # -------------------------------------------------

        document_retriever = DocumentRetriever()

        document_retriever.index_documents(
            resume_chunks
        )

        print(
            f"Indexed {len(resume_chunks)} "
            "resume chunks for RAG."
        )

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------

        return {
            "success": True,
            "data": result,
        }

    except ClientError as error:

        print(
            f"Gemini JobMatch error: {error}"
        )

        if error.code == 429:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Gemini API quota is temporarily "
                    "exhausted. Please try again later."
                ),
            )

        raise HTTPException(
            status_code=502,
            detail=(
                "The Gemini API could not process "
                "the job match request."
            ),
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print(
            f"JobMatch analysis error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while analyzing the documents."
            ),
        )

    finally:

        # -------------------------------------------------
        # Cleanup temporary files
        # -------------------------------------------------

        if (
            resume_path
            and os.path.exists(resume_path)
        ):
            os.remove(resume_path)

        if (
            jd_path
            and os.path.exists(jd_path)
        ):
            os.remove(jd_path)
from app.rag.document_loader import load_pdf
from app.rag.text_splitter import split_text
from app.rag.document_context import build_document_context

from app.services.job_matcher import analyze_job_match
from app.services.match_score import calculate_match_score


# ---------------------------------------------------------
# PDF PROCESSING
# ---------------------------------------------------------

def process_pdf(
    file_path: str,
    document_type: str,
) -> list[dict]:

    documents = load_pdf(
        file_path,
        document_type=document_type,
    )

    if not documents:
        raise ValueError(
            f"No readable text found in {file_path}"
        )

    chunks = split_text(documents)

    if not chunks:
        raise ValueError(
            f"No usable chunks created for {file_path}"
        )

    return chunks


# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------

RESUME_PATH = "data/sample_resume.pdf"
JOB_DESCRIPTION_PATH = "data/sample_job_description.pdf"


# ---------------------------------------------------------
# MAIN TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("JOBMATCH RAG — JOB MATCH TEST")
    print("=" * 60)

    # -----------------------------------------------------
    # Process Resume
    # -----------------------------------------------------

    print("\nProcessing resume...")

    resume_chunks = process_pdf(
        RESUME_PATH,
        document_type="resume",
    )

    print(
        f"Resume chunks: {len(resume_chunks)}"
    )

    # -----------------------------------------------------
    # Process Job Description
    # -----------------------------------------------------

    print("\nProcessing job description...")

    jd_chunks = process_pdf(
        JOB_DESCRIPTION_PATH,
        document_type="job_description",
    )

    print(
        f"Job description chunks: {len(jd_chunks)}"
    )

    # -----------------------------------------------------
    # Build RAG Context
    # -----------------------------------------------------

    resume_context = build_document_context(
        resume_chunks
    )

    jd_context = build_document_context(
        jd_chunks
    )

    # -----------------------------------------------------
    # Gemini Job Analysis
    # -----------------------------------------------------

    print("\nRunning Gemini job analysis...")

    analysis = analyze_job_match(
        resume_context,
        jd_context,
    )

    # -----------------------------------------------------
    # Calculate Score
    # -----------------------------------------------------

    match_score = calculate_match_score(
        analysis.get(
            "required_skills",
            [],
        ),
        analysis.get(
            "matching_skills",
            [],
        ),
    )

    # -----------------------------------------------------
    # Display Results
    # -----------------------------------------------------

    print("\n")
    print("=" * 60)
    print("JOB MATCH ANALYSIS")
    print("=" * 60)

    print("\nMatch Score:")
    print(f"{match_score}%")

    print("\nRequired Skills:")
    print(
        analysis.get(
            "required_skills",
            [],
        )
    )

    print("\nCandidate Skills:")
    print(
        analysis.get(
            "candidate_skills",
            [],
        )
    )

    print("\nMatching Skills:")
    print(
        analysis.get(
            "matching_skills",
            [],
        )
    )

    print("\nMissing Skills:")
    print(
        analysis.get(
            "missing_skills",
            [],
        )
    )

    print("\nRelevant Experience:")

    for experience in analysis.get(
        "relevant_experience",
        [],
    ):
        print(f"- {experience}")

    print("\nStrengths:")

    for strength in analysis.get(
        "strengths",
        [],
    ):
        print(f"- {strength}")

    print("\nGaps:")

    for gap in analysis.get(
        "gaps",
        [],
    ):
        print(f"- {gap}")

    print("\n")
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)


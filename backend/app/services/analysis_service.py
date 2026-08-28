from app.rag.document_context import build_document_context
from app.services.job_matcher import analyze_job_match
from app.services.match_score import calculate_match_score


def analyze_documents(
    resume_chunks: list[dict],
    jd_chunks: list[dict],
) -> dict:

    resume_context = build_document_context(
        resume_chunks
    )

    jd_context = build_document_context(
        jd_chunks
    )

    analysis = analyze_job_match(
        resume_context,
        jd_context,
    )

    required_skills = analysis.get(
        "required_skills",
        [],
    )

    matching_skills = analysis.get(
        "matching_skills",
        [],
    )

    score = calculate_match_score(
        required_skills,
        matching_skills,
    )

    return {
        "match_score": score,
        **analysis,
    }
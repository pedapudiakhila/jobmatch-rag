import json
import re

from app.rag.generator import generate_analysis


def extract_json(text: str) -> dict:
    """
    Extract JSON from Gemini's response.
    Handles cases where the model wraps JSON in markdown fences.
    """

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return json.loads(text)


def analyze_job_match(
    resume_context: str,
    job_description_context: str,
) -> dict:

    prompt = f"""
You are an expert resume and job-description
analysis assistant.

Analyze the candidate resume against the job description.

Use ONLY the information provided below.

Do not invent skills, experience, projects,
qualifications, technologies, achievements,
or candidate preferences.

RESUME CONTEXT:
{resume_context}

JOB DESCRIPTION CONTEXT:
{job_description_context}

Return ONLY valid JSON using exactly this structure:

{{
    "required_skills": [],
    "candidate_skills": [],
    "matching_skills": [],
    "missing_skills": [],
    "other_requirements": [],
    "relevant_experience": [],
    "strengths": [],
    "gaps": []
}}

IMPORTANT SKILL CLASSIFICATION RULES:

1. required_skills must contain ONLY actual skills,
   technologies, tools, programming languages,
   technical competencies, or clearly defined
   professional competencies required by the job.

2. Do NOT put travel, relocation, work location,
   extended stays, working hours, availability,
   willingness, or employment conditions inside
   required_skills.

3. Put such non-skill requirements inside
   other_requirements.

4. candidate_skills must contain skills explicitly
   supported by the resume.

5. matching_skills must contain skills supported
   by BOTH the resume and the job description.

6. missing_skills must contain required skills for
   which there is no explicit evidence in the resume.

7. Use concise and consistent skill names.

8. Do not create multiple variations of the same skill.

9. Normalize equivalent names where appropriate:
   - "React.js" and "React" → "React"
   - "RESTful APIs" and "REST APIs" → "REST APIs"
   - "Microsoft Excel" and "Excel proficiency" → "Excel"
   - "Microsoft PowerPoint" and "PowerPoint proficiency"
     → "PowerPoint"
   - "Problem-solving skills" and "Problem solving"
     → "Problem Solving"
   - "Communication skills" and "Communication"
     → "Communication"

10. A skill must not appear in both
    matching_skills and missing_skills.

11. Do not infer a skill merely because another
    related skill exists.

12. Do not invent AWS, Docker, Kubernetes, cloud
    platforms, programming languages, frameworks,
    or other technologies unless supported by
    the provided documents.

13. Do not treat travel, relocation, or other
    employment conditions as skills.

OTHER REQUIREMENTS:

- Include meaningful non-skill requirements from the
  job description such as:
  travel requirements,
  relocation requirements,
  work-location requirements,
  extended stays,
  availability requirements,
  or similar employment conditions.

- Do not invent candidate willingness or preferences.

CONTENT RULES:

- relevant_experience must contain resume experience
  or projects relevant to the job.

- strengths must describe evidence-based advantages
  supported by the resume and job description.

- gaps must describe meaningful gaps between the
  resume and job description.

- If an other requirement is not supported by the
  resume, mention it as a gap where appropriate.

- Do not claim that the candidate is willing to travel,
  relocate, work overtime, or accept other conditions
  unless the resume explicitly provides evidence.

- Use ONLY information from the provided documents.

- Keep all arrays concise.

Return ONLY the JSON object.
"""

    response_text = generate_analysis(
        prompt
    )

    return extract_json(
        response_text
    )
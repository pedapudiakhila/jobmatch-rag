import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )

client = genai.Client(
    api_key=api_key
)

GENERATION_MODEL = "gemini-3.6-flash"


SYSTEM_INSTRUCTION = """
You are JobMatch RAG, a resume and job-description
analysis assistant.

Answer using only the information provided in the context.

Do not invent or assume:
- skills
- work experience
- projects
- qualifications
- technologies
- achievements

If the requested information is not supported by the
provided context, clearly state that the information
is not available.

Keep answers concise, accurate, and evidence-based.
"""


def generate_answer(
    question: str,
    context: str,
) -> str:

    prompt = f"""
{SYSTEM_INSTRUCTION}

CONTEXT:
{context}

QUESTION:
{question}

Answer the question using only the context.
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    return response.text


def generate_analysis(prompt: str) -> str:

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
        ),
    )

    return response.text
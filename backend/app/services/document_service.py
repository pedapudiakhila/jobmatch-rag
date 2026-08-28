from app.rag.document_loader import load_pdf
from app.rag.text_splitter import split_text


def process_pdf(
    file_path: str,
    document_type: str,
    source_name: str | None = None,
) -> list[dict]:

    documents = load_pdf(
        file_path,
        document_type=document_type,
        source_name=source_name,
    )

    if not documents:
        raise ValueError(
            "The PDF does not contain readable text."
        )

    chunks = split_text(documents)

    if not chunks:
        raise ValueError(
            "No usable text chunks were created."
        )

    return chunks
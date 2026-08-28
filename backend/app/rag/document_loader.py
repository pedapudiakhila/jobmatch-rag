from pathlib import Path

from pypdf import PdfReader


def load_pdf(
    file_path: str,
    document_type: str = "unknown",
    source_name: str | None = None,
) -> list[dict]:

    reader = PdfReader(file_path)

    documents = []

    source = (
        source_name
        if source_name
        else Path(file_path).name
    )

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):

        text = page.extract_text() or ""

        text = text.strip()

        if not text:
            continue

        documents.append(
            {
                "text": text,
                "metadata": {
                    "source": source,
                    "page": page_number,
                    "document_type": document_type,
                },
            }
        )

    return documents
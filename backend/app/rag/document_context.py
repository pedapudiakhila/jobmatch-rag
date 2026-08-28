def build_document_context(
    documents: list[dict],
) -> str:

    parts = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        metadata = document.get("metadata", {})

        source = metadata.get(
            "source",
            "Unknown source",
        )

        page = metadata.get(
            "page",
            "Unknown page",
        )

        parts.append(
            f"""
[Document {index}]
Source: {source}
Page: {page}

{document["text"]}
"""
        )

    return "\n".join(parts)
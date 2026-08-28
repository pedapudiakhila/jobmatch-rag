from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(
    documents: list[dict],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict]:
    """
    Split page-level documents into smaller chunks while
    preserving source and page metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = []

    for document in documents:
        text = document["text"]
        metadata = document["metadata"]

        split_texts = splitter.split_text(text)

        for chunk_text in split_texts:
            chunks.append(
                {
                    "text": chunk_text,
                    "metadata": metadata.copy(),
                }
            )

    # Assign a unique ID to every chunk.
    for chunk_id, chunk in enumerate(chunks):
        chunk["metadata"]["chunk_id"] = chunk_id

    return chunks
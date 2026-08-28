from app.rag.retriever import DocumentRetriever
from app.rag.generator import generate_answer


def answer_question(
    question: str,
    retriever: DocumentRetriever,
    top_k: int = 3,
):
    """
    Retrieve relevant resume chunks and generate
    a grounded answer using the RAG pipeline.
    """

    retrieved_chunks = retriever.retrieve(
        question,
        top_k=top_k,
    )

    if not retrieved_chunks:

        return {
            "answer": (
                "I could not find relevant information "
                "in the provided resume."
            ),
            "sources": [],
        }

    context_parts = []
    sources = []

    seen_sources = set()

    for chunk in retrieved_chunks:

        text = chunk.get(
            "text",
            "",
        )

        metadata = chunk.get(
            "metadata",
            {},
        )

        source = metadata.get(
            "source",
            "Unknown source",
        )

        page = metadata.get(
            "page",
            "Unknown",
        )

        # ---------------------------------------------
        # Build context for Gemini
        # ---------------------------------------------

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{text}"
        )

        # ---------------------------------------------
        # Deduplicate displayed sources
        # ---------------------------------------------

        source_key = (
            source,
            page,
        )

        if source_key not in seen_sources:

            sources.append(
                {
                    "source": source,
                    "page": page,
                }
            )

            seen_sources.add(
                source_key
            )

    # ---------------------------------------------
    # Combine retrieved context
    # ---------------------------------------------

    context = "\n\n---\n\n".join(
        context_parts
    )

    # ---------------------------------------------
    # Generate grounded answer
    # ---------------------------------------------

    answer = generate_answer(
        question,
        context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }
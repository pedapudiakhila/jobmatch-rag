def build_context(results: list[dict]) -> str:
    """
    Convert retrieved chunks into a structured context
    for the Gemini generation model.
    """

    context_parts = []

    for index, result in enumerate(results, start=1):

        metadata = result["metadata"]

        source = metadata.get("source", "Unknown source")
        page = metadata.get("page", "Unknown page")

        context_parts.append(
            f"""
[Source {index}]
Source: {source}
Page: {page}

{result["text"]}
"""
        )

    return "\n".join(context_parts)
from app.rag.context_builder import build_context
from app.rag.generator import generate_answer
from app.rag.retriever import DocumentRetriever


class RAGPipeline:

    def __init__(self):
        self.retriever = DocumentRetriever()

    def index_documents(self, documents: list[dict]):
        self.retriever.index_documents(documents)

    def ask(
        self,
        question: str,
        top_k: int = 3,
    ) -> dict:

        results = self.retriever.retrieve(
            question,
            top_k=top_k,
        )

        if not results:
            return {
                "answer": "I could not find relevant information in the provided documents.",
                "sources": [],
            }

        context = build_context(results)

        answer = generate_answer(
            question,
            context,
        )

        sources = [
            {
                "source": result["metadata"].get(
                    "source",
                    "Unknown",
                ),
                "page": result["metadata"].get(
                    "page",
                    "Unknown",
                ),
            }
            for result in results
        ]

        return {
            "answer": answer,
            "sources": sources,
        }
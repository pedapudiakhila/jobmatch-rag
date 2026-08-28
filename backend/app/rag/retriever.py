from app.rag.embeddings import create_embedding
from app.rag.vector_store import FAISSVectorStore


class DocumentRetriever:

    def __init__(self):
        self.vector_store = FAISSVectorStore()

    def index_documents(self, documents: list[dict]):
        """
        Create embeddings for documents and store them in FAISS.
        """

        texts = [
            document["text"]
            for document in documents
        ]

        from app.rag.embeddings import create_embeddings

        embeddings = create_embeddings(texts)

        self.vector_store.add_documents(
            documents,
            embeddings,
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:

        query_embedding = create_embedding(query)

        return self.vector_store.search(
            query_embedding,
            top_k,
        )
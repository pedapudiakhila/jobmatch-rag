import faiss
import numpy as np


class FAISSVectorStore:

    def __init__(self):
        self.index = None
        self.documents = []

    def add_documents(self, documents: list[dict], embeddings: list[list[float]]):
        """
        Add document embeddings and their corresponding
        document data to the FAISS index.
        """

        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        dimension = vectors.shape[1]

        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(vectors)

        self.documents.extend(documents)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> list[dict]:

        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_vector,
            top_k,
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0],
        ):
            if index == -1:
                continue

            document = self.documents[index].copy()

            document["distance"] = float(distance)

            results.append(document)

        return results
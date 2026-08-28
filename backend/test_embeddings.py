from app.rag.embeddings import create_embedding


text = "The candidate has experience developing REST APIs."

embedding = create_embedding(text)

print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])
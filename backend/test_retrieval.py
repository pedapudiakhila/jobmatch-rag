from app.rag.document_loader import load_pdf
from app.rag.text_splitter import split_text
from app.rag.retriever import DocumentRetriever


PDF_PATH = "sample_resume.pdf"


documents = load_pdf(PDF_PATH)

chunks = split_text(documents)

retriever = DocumentRetriever()

retriever.index_documents(chunks)


queries = [
    "What programming skills does the candidate have?",
    "Does the candidate have backend development experience?",
    "What AI experience does the candidate have?",
]


for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)
    print("=" * 60)

    results = retriever.retrieve(
        query,
        top_k=3,
    )

    for rank, result in enumerate(results, start=1):

        print(f"\nResult {rank}")
        print("Distance:", result["distance"])
        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Text:")
        print(result["text"][:500])
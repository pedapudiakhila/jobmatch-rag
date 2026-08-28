from app.rag.document_loader import load_pdf
from app.rag.text_splitter import split_text
from app.rag.rag_pipeline import RAGPipeline


PDF_PATH = "sample_resume.pdf"


documents = load_pdf(PDF_PATH)

chunks = split_text(documents)

rag = RAGPipeline()

rag.index_documents(chunks)


questions = [
    "What technical skills does the candidate have?",
    "Does the candidate have AI experience?",
    "Does the candidate have backend development experience?",
    "Does the candidate have AWS experience?",
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    result = rag.ask(
        question,
        top_k=3,
    )

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['source']} | Page {source['page']}"
        )
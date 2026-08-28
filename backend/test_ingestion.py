from app.rag.document_loader import load_pdf
from app.rag.text_splitter import split_text


PDF_PATH = "sample_resume.pdf"


def main():

    # -----------------------------
    # Step 1: Load PDF
    # -----------------------------

    documents = load_pdf(PDF_PATH)

    print("\nPages extracted:", len(documents))

    for document in documents:
        print("\n--- PAGE ---")

        print("Source:", document["metadata"]["source"])
        print("Page:", document["metadata"]["page"])

        print(document["text"][:300])


    # -----------------------------
    # Step 2: Split into chunks
    # -----------------------------

    chunks = split_text(documents)

    print("\nTotal chunks:", len(chunks))


    # -----------------------------
    # Step 3: Inspect chunks
    # -----------------------------

    for i, chunk in enumerate(chunks, start=1):

        print(f"\n--- CHUNK {i} ---")

        print("Length:", len(chunk["text"]))

        print("Source:", chunk["metadata"]["source"])

        print("Page:", chunk["metadata"]["page"])

        print("Chunk ID:", chunk["metadata"]["chunk_id"])

        print("\nContent:")

        print(chunk["text"])


if __name__ == "__main__":
    main()
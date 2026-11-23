
from pypdf import PdfReader
import ollama
import chromadb


# Configuration
PDF_PATH = "knowledge/lecturenotes.pdf"
CHUNK_SIZE = 1000
OVERLAP = 200
EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "ml_notes_cosine"


# STEP 1: Extract text from PDF
def load_pdf():

    reader = PdfReader(PDF_PATH)

    full_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            full_text += page_text + "\n"

    if not full_text.strip():
        raise ValueError("No readable text found in PDF.")

    return full_text


# STEP 2: Split text into overlapping chunks
def create_chunks(full_text):

    chunks = []

    start = 0

    while start < len(full_text):

        end = start + CHUNK_SIZE

        chunk = full_text[start:end]

        chunks.append(chunk)

        if end >= len(full_text):
            break

        start = end - OVERLAP

    return chunks


# STEP 3: Generate embedding for one chunk
def create_embedding(text):

    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text
    )

    return response["embedding"]


# STEP 4: Store chunks and embeddings in ChromaDB
def store_embeddings(chunks):

    client = chromadb.PersistentClient(
        path="knowledge/chroma_db"
    )

    collection=client.get_or_create_collection(
        name="ml_notes_cosine",
        metadata={"hnsw:space": "cosine"}
    )

    # Remove old records before re-ingesting this PDF
    existing_data = collection.get()

    if existing_data["ids"]:
        collection.delete(
            ids=existing_data["ids"]
        )

    for i in range(len(chunks)):

        embedding = create_embedding(chunks[i])

        collection.add(
            ids=[str(i)],

            documents=[chunks[i]],

            embeddings=[embedding],

            metadatas=[{
                "source": PDF_PATH,
                "chunk_index": i
            }]
        )

        print(f"Stored chunk {i + 1}/{len(chunks)}")

    return collection


# STEP 5: Main execution
def main():

    print("Loading PDF...")

    full_text = load_pdf()

    print("Creating chunks...")

    chunks = create_chunks(full_text)

    if not chunks:
        raise ValueError("No chunks were created.")

    print("Total chunks:", len(chunks))

    print("Generating embeddings and storing in ChromaDB...")

    collection = store_embeddings(chunks)

    print("\n========== INGESTION COMPLETE ==========")

    print("Collection:", COLLECTION_NAME)
    print("Stored chunks:", collection.count())


if __name__ == "__main__":
    main()

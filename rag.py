
import ollama
import chromadb

MODEL = "nomic-embed-text"
COLLECTION_NAME = "ml_notes_cosine"
RELEVANCE_THRESHOLD=0.40

# Connect to our existing ChromaDB
def get_collection():

    client = chromadb.PersistentClient(
        path="knowledge/chroma_db"
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


# Convert user's question into an embedding
def create_query_embedding(query):

    response = ollama.embeddings(
        model=MODEL,
        prompt=query
    )

    return response["embedding"]


# Retrieve relevant document chunks
def retrieve(query, top_k=3):

    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = create_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "distances", "metadatas"]
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):

        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return retrieved_chunks


# Prepare relevant retrieved chunks as readable context
def get_context(query, top_k=3):

    results = retrieve(query, top_k)

    if not results:
        return None

    # Keep only chunks within our relevance threshold
    relevant_results = [
        result for result in results
        if result["distance"] <= RELEVANCE_THRESHOLD
    ]

    if not relevant_results:
        return None

    context = ""

    for i, result in enumerate(relevant_results, start=1):

        context += f"\nDocument Chunk {i}:\n"
        context += result["text"]
        context += "\n"

    return context
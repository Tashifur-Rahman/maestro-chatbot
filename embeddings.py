from pypdf import PdfReader
import ollama
import chromadb
reader=PdfReader("knowledge/lecturenotes.pdf")
full_text=""
for page in reader.pages:
    full_text+=page.extract_text()+"\n"

chunk_size=1000
overlap=200
chunks=[]
start=0
while start<len(full_text):
    end=start+chunk_size
    chunk=full_text[start:end]
    chunks.append(chunk)
    start=end-overlap

#create embeddings for all chunk
embedding_vectors=[]
for chunk in chunks:
    response=ollama.embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )
    embedding_vectors.append(response["embedding"])
# print("chunks",chunks[:3])
print("chunk length:",len(chunks))
print("Embedding length:",len(embedding_vectors[0]))
#create a local chroma db to store the embeddings
client=chromadb.PersistentClient(path="knowledge/chroma_db")
#create a collection
collection=client.create_collection(name="ml_notes")
#store every chunk and its embedding in the collection
for i in range(len(chunks)):
    collection.add(
        ids=[str(i)],#store id as string
        documents=[chunks[i]],#store the chunk as document
        embeddings=[embedding_vectors[i]]#store the embedding vector
    )
print("Collection count:",collection.count())

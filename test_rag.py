
from rag import retrieve, get_collection

collection = get_collection()

print("Collection:", collection.name)
print("Metric:", collection.metadata)
print("Chunks:", collection.count())

queries = [
    "Explain multivariate regression",
    "What is the bias variance tradeoff?",
    "How does Q-learning work?",
    "Explain quantum computing",
    "How do I cook biryani?"
]

for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)

    results = retrieve(query, top_k=3)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("Distance:", round(result["distance"], 4))
        print("Text preview:", result["text"][:250].replace("\n", " "))


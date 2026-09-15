import chromadb

client = chromadb.Client()
collection = client.create_collection(name="my_notes")
collection.add(
    documents=[
        "The cat sat on the mat.",
        "Python is a popular programming language.",
        "The stock market crashed today.",
        "She works as a doctor at the hospital.",
        "It's raining heavily outside right now.",
        "Machine learning is a subset of artificial intelligence.",
        "The weather is sunny and clear today.",
        "I need to buy groceries after work.",
        "The physician diagnosed the patient with the flu.",
        "Programming in Python is fun and productive."
    ],
    ids=["doc1", "doc2", "doc3", "doc4", "doc5", "doc6", "doc7", "doc8", "doc9", "doc10"]
)
results = collection.query(
    query_texts=["Tell me about coding"],
    n_results=3
)

print(results)
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer("all-MiniLM-L6-v2")
pairs =[
    ("The cat sat on the mat.", "A feline rested on the rug."),
    ("I love programming in Python.", "Python is my favorite language to code in."),
    ("The stock market crashed today.", "My dog needs a walk."),
    ("She works as a doctor.", "She is a physician."),
    ("It's raining outside.", "The weather is sunny and clear.")
]
for sentence1, sentence2 in pairs:
    embedding1 = model.encode(sentence1)
    embedding2 = model.encode(sentence2)

    # cosine_similarity expects 2D arrays, so wrap each in a list
    score = cosine_similarity([embedding1], [embedding2])[0][0]

    print(f"'{sentence1}'  vs  '{sentence2}'")
    print(f"Similarity: {score:.4f}")
    print("---")
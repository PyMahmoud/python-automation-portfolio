import os
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq

# ---------- 1. Load + chunk the PDF ----------
reader = PdfReader("doc.pdf")
text = ""
for page in reader.pages:
    text += (page.extract_text() or "") + "\n"

def chunk_text(text, size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

chunks = chunk_text(text)
print(len(chunks), "chunks created")

# ---------- 2. Embed + store (done once) ----------
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("pdf_rag")

collection.add(
    documents=chunks,
    embeddings=model.encode(chunks).tolist(),
    ids=[f"chunk_{i}" for i in range(len(chunks))],
)

groq = Groq(api_key=os.environ["GROQ_API_KEY"])

# ---------- 3. Ask questions in a loop ----------
SHOW_MATCHES = True  # set to False to hide the retrieved chunks

while True:
    question = input("\nAsk a question (or type 'quit'): ").strip()
    if question.lower() == "quit":
        break
    if not question:
        continue

    q_emb = model.encode([question]).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=3)
    retrieved = results["documents"][0]

    if SHOW_MATCHES:
        for i, doc in enumerate(retrieved):
            print(f"\n=== Match {i+1} ===")
            print(doc)

    context = "\n---\n".join(retrieved)

    response = groq.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "Answer ONLY using the context below. If the answer is not in the context, say 'I don't know based on the document.'"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        max_tokens=1000,
    )

    print("\n=== ANSWER ===")
    print(response.choices[0].message.content)
import os
import re
import json
import uuid
import chromadb
from groq import Groq
from pypdf import PdfReader

print("Loading embedding model (first start can take 1-2 minutes, please wait)...")
from sentence_transformers import SentenceTransformer

# ---------- Settings ----------
MODEL = "openai/gpt-oss-20b"
PDF_PATH = "doc.pdf"
MAX_STEPS = 6
DOC_K = 3                    # chunks returned by search_docs
RECALL_K = 3
RECALL_MAX_DISTANCE = 0.85   # memory cutoff (cosine distance)
DUPLICATE_DISTANCE = 0.12
DEBUG = True                 # print retrieval distances

client = Groq(api_key=os.environ["GROQ_API_KEY"])
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# =====================================================
# KNOWLEDGE BASE (RAG): the PDF, rebuilt at every start
# =====================================================
def load_pdf_chunks(path, size=500, overlap=100):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

doc_chunks = load_pdf_chunks(PDF_PATH)
docs_db = chromadb.Client()   # in-memory: rebuilt each run, so no duplicates
docs = docs_db.create_collection("pdf_docs", metadata={"hnsw:space": "cosine"})
docs.add(
    documents=doc_chunks,
    embeddings=embedder.encode(doc_chunks).tolist(),
    ids=[f"chunk_{i}" for i in range(len(doc_chunks))],
)
print(f"Knowledge base ready: {len(doc_chunks)} chunks from {PDF_PATH}")

def search_docs(query):
    res = docs.query(
        query_embeddings=embedder.encode([query]).tolist(),
        n_results=min(DOC_K, docs.count()),
    )
    if DEBUG:
        for d, dist in zip(res["documents"][0], res["distances"][0]):
            print(f"  [doc search] distance={dist:.2f}  {d[:60].strip()!r}")
    return "\n---\n".join(res["documents"][0])

# =====================================================
# LONG-TERM MEMORY: facts saved on disk (folder "agent_memory")
# =====================================================
db = chromadb.PersistentClient(path="agent_memory")
memory = db.get_or_create_collection("facts", metadata={"hnsw:space": "cosine"})

def remember_fact(fact):
    fact = fact.strip()
    if not fact:
        return "Error: empty fact"
    emb = embedder.encode([fact]).tolist()
    if memory.count() > 0:
        nearest = memory.query(query_embeddings=emb, n_results=1)
        if nearest["distances"][0][0] < DUPLICATE_DISTANCE:
            return f"Already in memory: {nearest['documents'][0][0]}"
    memory.add(documents=[fact], embeddings=emb, ids=[str(uuid.uuid4())])
    return f"Saved to long-term memory: {fact}"

def recall(query, k=RECALL_K):
    count = memory.count()
    if count == 0:
        return []
    res = memory.query(
        query_embeddings=embedder.encode([query]).tolist(),
        n_results=min(k, count),
    )
    facts = []
    for doc, dist in zip(res["documents"][0], res["distances"][0]):
        if DEBUG:
            print(f"  [memory check] distance={dist:.2f}  {doc[:60]}")
        if dist <= RECALL_MAX_DISTANCE:
            facts.append(doc)
    return facts

# =====================================================
# TOOLS
# =====================================================
def calculator(expression):
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed or "**" in expression or len(expression) > 100:
        return "Error: only numbers and + - * / ( ) are allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

TOOL_FUNCTIONS = {
    "search_docs": search_docs,
    "calculator": calculator,
    "remember_fact": remember_fact,
}

tools = [
    {"type": "function", "function": {
        "name": "search_docs",
        "description": "Search the Nile Brew Co. employee handbook (leave, salary, benefits, coffee standards, training, complaints, company facts). Use it for ANY question about the company.",
        "parameters": {"type": "object",
                       "properties": {"query": {"type": "string", "description": "What to look up, in plain words"}},
                       "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate a math expression such as '30 * 450'.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string", "description": "The math expression"}},
                       "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "remember_fact",
        "description": "Save a lasting fact about the user or their business to long-term memory. Use it when the user shares such a fact or says 'remember'.",
        "parameters": {"type": "object",
                       "properties": {"fact": {"type": "string", "description": "One clear, self-contained sentence"}},
                       "required": ["fact"]}}},
]

def run_tool(name, raw_args):
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"Error: unknown tool '{name}'"
    try:
        return str(func(**json.loads(raw_args or "{}")))
    except Exception as e:
        return f"Error running {name}: {e}"

# =====================================================
# GUARDRAIL: detect answers that don't contain the calculator's result
# =====================================================
def answer_contains(answer, value):
    try:
        target = float(value)
    except ValueError:
        return True   # not a number, nothing to check
    for n in re.findall(r"\d[\d,]*\.?\d*", answer):
        try:
            if abs(float(n.replace(",", "").rstrip(".")) - target) < 0.01:
                return True
        except ValueError:
            pass
    return False

# =====================================================
# SHORT-TERM MEMORY + AGENT LOOP
# =====================================================
messages = [
    {"role": "system", "content": (
        "You are an assistant for Nile Brew Co. "
        "For any question about the company, call search_docs and answer ONLY from what it returns; "
        "if the passages do not contain the answer, say 'I don't know based on the document.' "
        "Never assume or guess any company policy number (leave days, salary rules, limits). "
        "Always call search_docs FIRST, and only then use the calculator. "
        "Always use the calculator tool for any arithmetic, and copy its result exactly. "
        "When the user shares a lasting fact, save it with remember_fact. "
        "If a system message lists facts saved from earlier sessions, trust and use them. "
        "General questions that have nothing to do with the company can be answered directly."
    )}
]

def run_agent(task):
    calc_results = []

    recalled = recall(task)
    extra = []
    if recalled:
        print("[MEMORY RECALLED]", recalled)
        extra = [{"role": "system",
                  "content": "Facts saved from earlier sessions:\n- " + "\n- ".join(recalled)}]

    messages.append({"role": "user", "content": task})

    for step in range(1, MAX_STEPS + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[messages[0]] + extra + messages[1:],
                tools=tools,
                max_tokens=2000,
                temperature=0,
            )
        except Exception as e:
            print(f"\nAPI error: {e}")
            if step == 1:
                messages.pop()
            return None

        msg = response.choices[0].message

        if not msg.tool_calls:
            if not msg.content:
                print("\nWarning: empty answer (model may have run out of tokens). Try again.")
            messages.append({"role": "assistant", "content": msg.content or ""})
            print(f"\n[Step {step}] FINAL ANSWER: {msg.content}")
            if calc_results and not answer_contains(msg.content or "", calc_results[-1]):
                print(f"\n⚠ CHECK FAILED: the calculator returned {calc_results[-1]} "
                      f"but the answer does not contain it. Do not trust this answer.")
            return msg.content

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        })

        for tc in msg.tool_calls:
            result = run_tool(tc.function.name, tc.function.arguments)
            if tc.function.name == "calculator":
                calc_results.append(result)
            shown = result if len(result) < 150 else result[:150] + "..."
            print(f"[Step {step}] ACT: {tc.function.name}({tc.function.arguments}) -> OBSERVE: {shown!r}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    print("\nStopped: reached MAX_STEPS without a final answer.")

# =====================================================
# CHAT LOOP
# =====================================================
print(f"\nMemories in database: {memory.count()}")
print("Commands: /memories, /forget, quit")

while True:
    try:
        user = input("\nuser: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nBye.")
        break

    if user.lower() == "quit":
        break
    elif user == "/memories":
        saved = memory.get()["documents"]
        print("\n".join(f"- {d}" for d in saved) if saved else "(memory is empty)")
    elif user == "/forget":
        ids = memory.get()["ids"]
        if ids:
            memory.delete(ids=ids)
        print("All long-term memories deleted.")
    elif user:
        run_agent(user)
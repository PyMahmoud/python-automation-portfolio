import os
import json
import uuid
import chromadb
from groq import Groq

print("Loading embedding model (first start can take 1-2 minutes, please wait)...")
from sentence_transformers import SentenceTransformer

# ---------- Settings ----------
MODEL = "openai/gpt-oss-20b"
MAX_STEPS = 5
RECALL_K = 3
RECALL_MAX_DISTANCE = 0.85   # recall only facts at least this close (cosine distance)
DUPLICATE_DISTANCE = 0.12    # closer than this = treat as the same fact
DEBUG = True                 # print recall distances so you can tune the numbers

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ---------- LONG-TERM MEMORY (saved on disk in the folder "agent_memory") ----------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
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
    results = memory.query(
        query_embeddings=embedder.encode([query]).tolist(),
        n_results=min(k, count),
    )
    facts = []
    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        if DEBUG:
            print(f"  [recall check] distance={dist:.2f}  {doc[:70]}")
        if dist <= RECALL_MAX_DISTANCE:
            facts.append(doc)
    return facts

# ---------- Other tools ----------
def get_leave_days(years_of_service):
    return 30 if years_of_service >= 5 else 21

def calculator(expression):
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed or "**" in expression or len(expression) > 100:
        return "Error: only numbers and + - * / ( ) are allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

TOOL_FUNCTIONS = {
    "get_leave_days": get_leave_days,
    "calculator": calculator,
    "remember_fact": remember_fact,
}

tools = [
    {"type": "function", "function": {
        "name": "get_leave_days",
        "description": "Get the annual paid leave days for an employee, based on years of service.",
        "parameters": {"type": "object",
                       "properties": {"years_of_service": {"type": "number", "description": "Years the employee has worked"}},
                       "required": ["years_of_service"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate a math expression such as '30 / 7'.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string", "description": "The math expression"}},
                       "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "remember_fact",
        "description": "Save an important, lasting fact about the user or their business to long-term memory so it can be recalled in future sessions. Use it when the user shares such a fact or says 'remember'.",
        "parameters": {"type": "object",
                       "properties": {"fact": {"type": "string", "description": "One clear, self-contained sentence stating the fact"}},
                       "required": ["fact"]}}},
]

def run_tool(name, raw_args):
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"Error: unknown tool '{name}'"
    try:
        args = json.loads(raw_args or "{}")
        return str(func(**args))
    except Exception as e:
        return f"Error running {name}: {e}"   # the model sees this and can retry

# ---------- SHORT-TERM MEMORY (clean: no injected memory text in here) ----------
messages = [
    {"role": "system", "content": (
        "You are a helpful assistant. Use the tools when you need facts. "
        "Always use the calculator tool for any arithmetic. "
        "When the user shares a lasting fact, save it with remember_fact. "
        "If a system message lists facts saved from earlier sessions, trust them and use them."
    )}
]

# ---------- Agent loop ----------
def run_agent(task):
    # Recall is attached to THIS call only and is never stored in the history
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
            )
        except Exception as e:
            print(f"\nAPI error: {e}")
            if step == 1:
                messages.pop()   # drop the unanswered user message
            return None

        msg = response.choices[0].message

        if not msg.tool_calls:
            if not msg.content:
                print("\nWarning: empty answer (the model may have run out of tokens). Try again.")
            messages.append({"role": "assistant", "content": msg.content or ""})
            print(f"\n[Step {step}] FINAL ANSWER: {msg.content}")
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
            print(f"[Step {step}] ACT: {tc.function.name}({tc.function.arguments}) -> OBSERVE: {result}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    print("\nStopped: reached MAX_STEPS without a final answer.")

# ---------- Chat loop ----------
print(f"\nMemories in database: {memory.count()}")
print("Commands: /memories (list saved facts), /forget (delete all), quit")

while True:
    try:
        user = input("\nuser: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nBye.")
        break

    if user.lower() == "quit":
        break
    elif user == "/memories":
        docs = memory.get()["documents"]
        print("\n".join(f"- {d}" for d in docs) if docs else "(memory is empty)")
    elif user == "/forget":
        ids = memory.get()["ids"]
        if ids:
            memory.delete(ids=ids)
        print("All long-term memories deleted.")
    elif user:
        run_agent(user)
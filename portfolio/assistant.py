from groq import Groq
import json

client = Groq()

# ---------- Day 4: Tools ----------
def calculate(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def get_weather(city):
    fake_weather_data = {
        "Cairo": "28°C and sunny",
        "London": "14°C and rainy",
        "Tokyo": "20°C and cloudy"
    }
    return fake_weather_data.get(city, "Weather data not available for that city")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "The name of the city"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a basic math calculation",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string", "description": "A math expression, e.g. '5 + 3'"}},
                "required": ["expression"]
            }
        }
    }
]

TOOL_FUNCTIONS = {"get_weather": get_weather, "calculate": calculate}

# ---------- Day 5: Memory ----------
conversation = [
    {"role": "system", "content": "You are a sarcastic robot butler who is secretly very kind."}
]
running_summary = ""
MAX_RECENT_MESSAGES = 6


def trim_and_summarize():
    global running_summary, conversation
    if len(conversation) > MAX_RECENT_MESSAGES + 1:
        messages_to_drop = conversation[1:][:-MAX_RECENT_MESSAGES]
        if messages_to_drop:
            summary_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{
                    "role": "system",
                    "content": f"Combine this existing summary: '{running_summary}' with these older messages into ONE short updated summary: {messages_to_drop}"
                }]
            )
            running_summary = summary_response.choices[0].message.content
        conversation = [conversation[0]] + conversation[1:][-MAX_RECENT_MESSAGES:]


def build_messages_to_send():
    if running_summary:
        return [conversation[0], {"role": "system", "content": f"Summary of earlier conversation: {running_summary}"}] + conversation[1:]
    return conversation


# ---------- Day 3: JSON summary on request ----------
def print_json_summary():
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{
            "role": "system",
            "content": "Return ONLY valid JSON (no prose) summarizing this conversation as {\"topics\": [...], \"user_facts\": [...]}."
        }] + conversation[1:]
    )
    raw = response.choices[0].message.content
    try:
        data = json.loads(raw)
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError:
        print("Model didn't return clean JSON:", raw)


# ---------- Main loop ----------
while True:
    user_input = input("YOU: ")
    if user_input.lower() == "quit":
        break

    if user_input.lower() in ("summary", "json"):
        print_json_summary()
        continue

    conversation.append({"role": "user", "content": user_input})
    trim_and_summarize()

    messages_to_send = build_messages_to_send()
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages_to_send,
        tools=tools
    )
    tool_calls = response.choices[0].message.tool_calls

    if not tool_calls:
        reply = response.choices[0].message.content
        print("AI:", reply)
        conversation.append({"role": "assistant", "content": reply})
        continue

    # A tool was requested
    call = tool_calls[0]
    args = json.loads(call.function.arguments)
    value = next(iter(args.values()))
    result = TOOL_FUNCTIONS[call.function.name](value)

    conversation.append(response.choices[0].message)
    conversation.append({"role": "tool", "tool_call_id": call.id, "content": result})

    followup = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=build_messages_to_send()
    )
    reply = followup.choices[0].message.content
    print("AI:", reply)
    conversation.append({"role": "assistant", "content": reply})
from groq import Groq
import json
client = Groq()
def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
def get_weather(city):
    fake_weather_data={
        "Cairo": "28°C and sunny",
        "London": "14°C and rainy",
        "Tokyo": "20°C and cloudy"
    }
    return fake_weather_data.get(city,"Weather data not available for that city")
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a basic math calculation, e.g. addition, subtraction, multiplication, or division",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression to evaluate, e.g. '5 + 3'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

while True:
    user_input = input("Ask me something (or 'quit'): ")
    if user_input.lower() == "quit":
        break

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": user_input}],
        tools=tools
    )

    tool_calls = response.choices[0].message.tool_calls

    if not tool_calls:
        # No tool was needed — the model just answered directly
        print(response.choices[0].message.content)
        continue   # skip the rest, go back to asking for input

    text = tool_calls[0]
    arg = text.function.arguments
    data = json.loads(arg)
    value = next(iter(data.values()))

    if text.function.name == "get_weather":
        result = get_weather(value)
    elif text.function.name == "calculate":
        result = calculate(value)

    messages_followup = [
        {"role": "user", "content": user_input},
        response.choices[0].message,
        {
            "role": "tool",
            "tool_call_id": text.id,
            "content": result
        }
    ]
    response2 = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages_followup
    )
    print(response2.choices[0].message.content)
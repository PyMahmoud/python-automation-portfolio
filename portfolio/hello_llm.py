from groq import Groq
client = Groq()
response = client.chat.completions.create(
    model = "openai/gpt-oss-20b",
    messages = [
        {"role":"user","content":"say hello and tell me one fun fact about the moon."}
    ]
)
print(response.choices[0].message.content)
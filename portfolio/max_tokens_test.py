from groq import Groq

client = Groq()

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    max_tokens=320,
    messages=[{"role": "user", "content": "Explain how rainbows form."}]
)

print(response.choices[0].message.content)
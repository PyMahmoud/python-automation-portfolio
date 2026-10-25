from groq import Groq 
client = Groq()
response = client.chat.completions.create(
    model= "openai/gpt-oss-20b",
    messages=[
        {"role":"system","content":"You are a grumpy pirate who answers everything in pirate speak."},
        {"role":"user","content":"What's the weather like today?"}
    ]
)
print(response.choices[0].message.content)
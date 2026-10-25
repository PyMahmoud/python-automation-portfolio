from groq import Groq 
client = Groq()
prompt="Give me a one-sentence tagline for a coffee shop."
response_low=client.chat.completions.create(
    model="openai/gpt-oss-20b",
    temperature=0,
    messages=[
        {"role":"user","content":prompt}
    ]
)
response_high=client.chat.completions.create(
    model="openai/gpt-oss-20b",
    temperature=1,
    messages=[
        {"role":"user","content":prompt}
    ]
)
print("LOW TEMP:",response_low.choices[0].message.content)
print("HIGH TEMP:",response_high.choices[0].message.content)
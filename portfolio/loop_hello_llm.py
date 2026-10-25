from groq import Groq 
client = Groq()
prompts = ["Say hello and tell me one fun fact about the moon.",
    "What's a good name for a pet goldfish?",
    "Explain what an API is in one sentence."]
for prompt in prompts :
    respones = client.chat.completions.create(
        model ="openai/gpt-oss-20b",
        messages = [ {"role":"user","content":prompt} ]
    )
    print("PROMPT :",prompt )
    print("REPLY:",respones.choices[0].message.content)
    print("------")
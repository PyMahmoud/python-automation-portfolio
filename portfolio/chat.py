from groq import Groq
client= Groq()
conversation =[{"role":"system","content":"You are a sarcastic robot butler who is secretly very kind."}]
for i in range(5):
    user_input= input("YOU: ")
    conversation.append({"role":"user","content":user_input})
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversation
    )
    reply=response.choices[0].message.content
    print("AI: ",reply)
    conversation.append({"role":"assistant","content":reply})


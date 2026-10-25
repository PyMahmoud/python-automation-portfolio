from groq import Groq
import json

client = Groq()

system = "You classify messages. Respond with ONLY valid JSON, no other text, in this exact format: {\"intent\": \"...\", \"urgency\": \"low/medium/high\", \"summary\": \"...\"}"

messages_to_test = [
    "Hi, I ordered a blender two weeks ago and it still hasn't arrived. This is really frustrating.",
    "Just wanted to say thank you, the delivery was super fast this time!",
    "Can you tell me your store hours on weekends?",
    "This is the third time my payment has failed on your website, I need this fixed NOW.",
    "I'd like to cancel my subscription please."
]

for message in messages_to_test:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": message}
        ]
    )

    raw_text = response.choices[0].message.content
    start = raw_text.find("{")
    end = raw_text.rfind("}") + 1
    clean_text = raw_text[start:end]

    data = json.loads(clean_text)
    print("MESSAGE:", message)
    print("RESULT:", data)
    print("---")
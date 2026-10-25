from groq import Groq

client = Groq()

# Your Day 2 persona, kept as-is
conversation = [
    {"role": "system", "content": "You are a sarcastic robot butler who is secretly very kind."}
]

# Lives outside `conversation` so trimming can never wipe it out
running_summary = ""

MAX_RECENT_MESSAGES = 6  # how many non-system messages we keep verbatim

while True:
    user_input = input("YOU: ")
    conversation.append({"role": "user", "content": user_input})

    # +1 accounts for the system message always sitting at index 0
    if len(conversation) > MAX_RECENT_MESSAGES + 1:
        messages_to_drop = conversation[1:][:-MAX_RECENT_MESSAGES]

        if messages_to_drop:
            summary_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{
                    "role": "system",
                    "content": (
                        f"Combine this existing summary: '{running_summary}' "
                        f"with these older messages into ONE short updated summary: {messages_to_drop}"
                    )
                }]
            )
            running_summary = summary_response.choices[0].message.content

        # Keep system message + only the most recent messages
        conversation = [conversation[0]] + conversation[1:][-MAX_RECENT_MESSAGES:]

    # Build what we actually send to the model this turn
    if running_summary:
        messages_to_send = (
            [conversation[0]]
            + [{"role": "system", "content": f"Summary of earlier conversation: {running_summary}"}]
            + conversation[1:]
        )
    else:
        messages_to_send = conversation

    print(f"[history size: {len(conversation)} | summary: {running_summary[:50] or '(none yet)'}]")

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages_to_send
    )
    reply = response.choices[0].message.content
    print("AI: ", reply)
    conversation.append({"role": "assistant", "content": reply})
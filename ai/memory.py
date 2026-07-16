from ai.prompts import SYSTEM_PROMPT

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def add_user_message(text):
    messages.append({
        "role": "user",
        "content": text
    })


def add_ai_message(text):
    messages.append({
        "role": "assistant",
        "content": text
    })


def get_messages():
    return messages


def clear_memory():
    global messages

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
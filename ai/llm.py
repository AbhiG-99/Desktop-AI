import os
from dotenv import load_dotenv
from openai import OpenAI
from ai.prompts import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "openai/gpt-oss-20b:free"

def ask_ai(messages, image_b64=None):
    if image_b64:
        # Attach the image to the most recent user message
        last = messages[-1]
        messages = messages[:-1] + [{
            "role": last["role"],
            "content": [
                {"type": "text", "text": last["content"]},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
            ]
        }]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content
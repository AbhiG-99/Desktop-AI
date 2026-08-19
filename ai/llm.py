import os
from dotenv import load_dotenv
from openai import OpenAI
from ai.prompts import SYSTEM_PROMPT
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"
def ask_ai(messages, image_b64=None):
    if image_b64:
        last = messages[-1]
        messages = messages[:-1] + [{
            "role": last["role"],
            "content": [
                {"type": "text", "text": last["content"]},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
            ]
        }]
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        if not response.choices:
            return "Hmm, I didn't get a proper response that time — mind trying again?"
        return response.choices[0].message.content
    except Exception:
        return "Sorry, I'm having trouble reaching the AI right now. Please try again in a moment."
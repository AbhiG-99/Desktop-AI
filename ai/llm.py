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


def ask_ai(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    return response.choices[0].message.content
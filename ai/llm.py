import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODELS = [
    "openai/gpt-oss-20b:free",
]


def ask_ai(prompt: str):
    last_error = None

    for model in MODELS:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            print(f"Using model: {model}")
            return completion.choices[0].message.content

        except Exception as e:
            print(f"{model} failed")
            last_error = e

    raise last_error
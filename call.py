import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # take environment variables from .env.

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "write a short poem about strawberries"}],
    stream=True,
)
for part in stream:
    print(part.choices[0].delta.content or "", end="")


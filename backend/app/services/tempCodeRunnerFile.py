import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

print(repr(os.getenv("GEMINI_API_KEY")))
print([ord(c) for c in os.getenv("GEMINI_API_KEY")[:5]])

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY").strip()
)
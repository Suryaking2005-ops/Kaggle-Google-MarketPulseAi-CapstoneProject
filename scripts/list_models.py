"""List the Gemini models your API key can use for generateContent.

Run from the project root:  python -m scripts.list_models
"""
import google.generativeai as genai

from marketpulse.config import get_api_key

genai.configure(api_key=get_api_key())

print("Available models:")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

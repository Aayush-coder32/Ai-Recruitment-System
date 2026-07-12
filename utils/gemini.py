import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Make sure it is set in your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(
         model="gemini-2.0-flash",   
         contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {str(e)}")
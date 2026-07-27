import os
from google import genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

try:
    client = genai.Client(api_key=api_key)
    print("Available models:")
    for m in client.models.list():
        if "generateContent" in m.supported_actions:
            print(m.name)
except Exception as e:
    print("ERROR: ", str(e))


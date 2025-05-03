import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

apikey = os.environ['GEMINI_API_KEY']

client = genai.Client(api_key=apikey)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["How does AI work?"]
)
print(response.text)
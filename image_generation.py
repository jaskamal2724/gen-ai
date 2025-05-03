from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Load API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# ✅ Pass API key to genai.Client
client = genai.Client(api_key=api_key)

contents = """Soch tu kisi se keh raha hai:
“Amitabh Bachchan ban ke dialogue bol.”
Ab banda normal tareeke se toh bolega nahi, woh turant apni awaaz gahri karega, style badlega, aur bolega:
“Rishtey mein toh hum tumhare baap lagte hain…”
Kya swag aaya na? Kyunki usko ek role mil gaya — persona mil gaya.

Bas waise hi, persona-based prompting mein AI ko bolte ho:
“Tum ek strict history teacher ho.”
Ya
“Ek friendly South Indian uncle ki tarah explain karo.”
Ya
“Act like Virat Kohli giving motivational advice.”

Toh AI bhi usi hisaab se tone, style aur reasoning ko adjust karta hai — jaise ek actor apna character nibhata hai.

Ye ekdum waise hai jaise:

Kabhi mummy ban jao toh daantne ka style

Kabhi dosti mode on ho toh mast chill replies

Kabhi teacher mode mein toh proper gyaan!

Toh tum AI ko bolte ho:
“Bhai, aaj tu expert ban ja, baki hum dekh lenge!”

Desi line:
Persona-based prompting = "AI ko bolna: 'Aaj tu Ranveer Singh ban ja, pura energy chahiye!' 💥"

Yeh style use karo toh model ekdum customized jawab deta hai — jaise tailor-made sherwani ho shaadi ke liye! 😉

now based on the above information generate an image of two boys having the above conversation, or simply display two boys with some hand reaction and above their heads make a clouds and write the conversation in them . make sure to add full conversation  don't cut any part of the conversation 

generate a good image with proper character , clear words , without any blur effect , user exact words of conversation 
"""

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save('gemini-native-image.png')
        image.show()

import json
from openai import OpenAI
from dotenv import load_dotenv
import os 
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# client = OpenAI(
#     api_key=api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

client = genai.Client(api_key=api_key)


def get_weather(city:str):
    return "32 degree celcius"

available_tools={
    "get_weather":{
        "fn":get_weather,
        "description":"takes the city name as input and return the current weather of the city"
    }
}

system_prompt="""
    You are an helpful AI assistant who is specialized in resolving user query
    You work on start , plan , action and observe mode
    For the given user query and avaliable toos, plan the step by step execution , based on the planing,
    select the revelant tool from the available tool and baed on the tool selection you perform an action to call the tool
    wait for the observation and based on the observation from the tool called resolve the user query       

    Rules :
        -Follow the output JSON format 
        -Always perform one step at a time and wait for next input
        -Carefully analyze the user query
    
    Output JSON Format:
    {{
        "step":"string",
        "content":"string",
        "function":"The name function if the step is action",
        "input":"The input parameter for the fucntion",
    }}

    Available Tools
        -get_weather:takes the city name as input and return the current weather of the city

    Example : 
        User Quey : what is the weather of New York
        Output : {{"step":"plan", "content":"the user is interested in weather data of new york"}}
        Output : {{"step":"plan", "content":"from the available tool i should call a get_weather"}}
        Output : {{"step":"action", "function":"get_weather", "input":"new york"}}
        Output : {{"step":"observe", "output":"12 degree celcius"}}
        Output : {{"step":"output", "content":"The weather of new york seems to be  12 degree celcius"}}
"""

messages=[
    system_prompt,
]

user_input = input(">>")

messages.append(f"{user_input}")

while True:
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=messages
    )

    # print(response.text.replace("`","").replace("json",""))
    parsed_output=json.loads(response.text.replace("`","").replace("json",""))
    messages.append(json.dumps(parsed_output))

    if parsed_output.get("step") == "plan":
        print(f"🧠 : {parsed_output.get("content")}")
    
    if parsed_output.get("step") == "action":
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")

        if available_tools.get(tool_name, False) != False:
            output = available_tools[tool_name].get("fn")(tool_input)
            messages.append(json.dumps({"step": "observe", "output": output }))

    if parsed_output.get("step") == "output":
        print(f"🤖 : {parsed_output.get("content")}")
        break

# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents=[
#         system_prompt,
#         "what is the weather of gurugram",
#         json.dumps({"step":"plan", "content":"the user is interested in weather data of Gurugram"}),
#         json.dumps({"step":"plan", "content":"from the available tool i should call a get_weather"}),
#         json.dumps({"step": "action", "function": "get_weather", "input": "gurugram"}),
#         json.dumps({"step": "observe", "output": "32 degree celcius"}),
#     ]
    
# )

# ans=response.text.replace("`","").replace("json","")
# print(ans)

# what is the weather of gurugram




#First test of the IFM API

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # Load environment variables from .env file


client = OpenAI(
    api_key=os.getenv("IFM_API_KEY"), 
    base_url=os.getenv("IFM_BASE_URL")
)

response = client.chat.completions.create(
    model=os.getenv("IFM_MODEL"),
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
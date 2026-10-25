#First test of the IFM API
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() # Load environment variables from .env file
def parse_decision(text):
    """Turn the AI's reply into (action, amount). Falls back to hold if anything is wrong."""
    try:
        data = json.loads(text.strip())
    except json.JSONDecodeError:
        print("WARNING: reply was not valid JSON:", repr(text))
        return "hold", 0

    action = data.get("action")
    amount = data.get("amount")

    if action not in ["buy", "sell", "hold"]:
        print("WARNING: invalid action:", repr(action))
        return "hold", 0

    if not isinstance(amount, int) or amount < 1 or amount > 5:
        print("WARNING: invalid amount:", repr(amount))
        return "hold", 0

    return action, amount

client = OpenAI(
    api_key=os.getenv("IFM_API_KEY"), 
    base_url=os.getenv("IFM_BASE_URL")
)

response = client.chat.completions.create(
    model=os.getenv("IFM_MODEL"),
    messages=[
         {"role": "user", "content": (
            "You are Alice, a stock trader. You have 1000 cash and 0 shares. "
            "The share price is 100. Decide what to do today. "
            'Reply ONLY with JSON in this format: {"action": "<buy|sell|hold>", "amount": <whole number 1-5>} '
            'where action is "buy", "sell" or "hold" and amount is a whole number from 1 to 5. '
            "No other text."
        )}
    ]
)

reply = response.choices[0].message.content
print("Raw reply:", repr(reply))
print("Decision:", parse_decision(reply))


print("\n--- Safety tests ---")
print(parse_decision("I would buy 3 shares"))
print(parse_decision('{"action": "Buy", "amount": 3}'))
print(parse_decision('{"action": "sell", "amount": 10}'))
print(parse_decision('{"action": "hold", "amount": "three"}'))
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
def ai_decide(trader, price):
    """Ask the AI what this trader should do. Returns (action, amount)."""
    prompt = (
        f"You are {trader['name']}, a stock trader. "
        f"You have {trader['cash']} cash and {trader['shares']} shares. "
        f"The share price is {price}. Decide what to do today. "
        'Reply ONLY with JSON in this format: {"action": "<buy|sell|hold>", "amount": <whole number 1-5>} '
        "No other text."
    )

    response = client.chat.completions.create(
        model=os.getenv("IFM_MODEL"),
        messages=[{"role": "user", "content": prompt}],
    )

    reply = response.choices[0].message.content
    print(f"  [AI raw reply for {trader['name']}: {reply.strip()}]")
    return parse_decision(reply)

if __name__ == "__main__":
    test_trader = {"name": "Alice", "cash": 500, "shares": 4}
    print(ai_decide(test_trader, 120))
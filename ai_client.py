# RumorMill - AI connection: asks the model for trading decisions,
# with retry, rate-limit handling and record/replay

import json
import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load IFM_API_KEY, IFM_BASE_URL and IFM_MODEL from .env

MAX_ATTEMPTS = 3                  # first try + 2 retries for invalid replies
RECORDING_FILE = "recording.json"


def parse_decision(text):
    """Check the AI's reply. Returns ((action, amount), None) if valid, or (None, reason) if not."""
    try:
        data = json.loads(text.strip())
    except json.JSONDecodeError:
        return None, "Your reply was not valid JSON."

    if not isinstance(data, dict):
        return None, 'Your reply must be a JSON object like {"action": ..., "amount": ...}.'

    action = data.get("action")
    amount = data.get("amount")

    if action not in ["buy", "sell", "hold"]:
        return None, f'action must be exactly "buy", "sell" or "hold", not {action!r}.'

    if isinstance(amount, bool) or not isinstance(amount, int) or not 1 <= amount <= 5:
        return None, f"amount must be a whole number from 1 to 5, not {amount!r}."

    return (action, amount), None


def build_prompt(trader, price):
    """The first message the AI sees for this trader today."""
    return (
        f"You are {trader['name']}, a stock trader. "
        f"You have {trader['cash']} cash and {trader['shares']} shares. "
        f"The share price is {price}. Decide what to do today. "
        'Reply ONLY with JSON in this format: {"action": "<buy|sell|hold>", "amount": <whole number 1-5>} '
        "No other text."
    )


def feedback_message(error):
    """What we tell the AI after an invalid reply."""
    return f"That reply was invalid: {error} Reply again with ONLY the JSON."


client = OpenAI(
    api_key=os.getenv("IFM_API_KEY"),
    base_url=os.getenv("IFM_BASE_URL"),
    max_retries=5,   # retry rate limits and network errors, waiting longer each time
    timeout=120,     # give up on a single request after 2 minutes
)

recorded_calls = []  # every AI call made during this run

replay_mode = False
replay_queue = []  # recorded calls waiting to be replayed, in order


def save_recording():
    """Write every AI call so far to disk, so a crash never loses work."""
    with open(RECORDING_FILE, "w") as f:
        json.dump(recorded_calls, f, indent=2)


def start_replay(filename):
    """Switch to replay mode using a saved recording."""
    global replay_mode
    with open(filename) as f:
        replay_queue.extend(json.load(f))
    replay_mode = True
    print(f"Replaying {len(replay_queue)} AI calls from {filename}")


def get_reply(trader, messages):
    """One AI reply for this conversation: from the recording in replay mode, otherwise from the API."""
    if replay_mode:
        if not replay_queue:
            raise RuntimeError("Replay ran out of recorded AI calls")
        record = replay_queue.pop(0)
        if record["messages"] != messages:
            raise RuntimeError(f"Replay mismatch for {trader['name']}: conversation differs from the recording")
        return record["reply"]

    try:
        response = client.chat.completions.create(
            model=os.getenv("IFM_MODEL"),
            messages=messages,
        )
    except openai.RateLimitError:
        raise SystemExit(
            "STOPPED: IFM rate limit still exceeded after retries "
            "(possibly the daily token cap, which resets at 00:00 UTC). "
            f"{len(recorded_calls)} AI calls are saved in {RECORDING_FILE}."
        )
    except openai.APIError as e:
        raise SystemExit(
            f"STOPPED: AI call failed ({type(e).__name__}). "
            f"{len(recorded_calls)} AI calls are saved in {RECORDING_FILE}."
        )

    reply = response.choices[0].message.content.strip()
    recorded_calls.append({
        "trader": trader["name"],
        "messages": list(messages),  # a COPY - the conversation keeps growing after this
        "reply": reply,
    })
    save_recording()
    return reply


def ai_decide(trader, price):
    """Ask the AI what this trader should do, retrying with feedback. Returns (action, amount)."""
    messages = [{"role": "user", "content": build_prompt(trader, price)}]

    for attempt in range(1, MAX_ATTEMPTS + 1):
        reply = get_reply(trader, messages)
        print(f"  [AI reply for {trader['name']}, attempt {attempt}: {reply}]")

        decision, error = parse_decision(reply)
        if error is None:
            return decision

        print(f"  WARNING: {error}")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": feedback_message(error)})

    print(f"  GAVE UP after {MAX_ATTEMPTS} attempts: {trader['name']} holds.")
    return "hold", 0
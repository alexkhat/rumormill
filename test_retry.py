# Forces the retry path using a fake recording - no API calls

import ai_client as ac

trader = {"name": "Tess", "cash": 1000, "shares": 0}
price = 100

# The conversation exactly as ai_decide will build it
first_messages = [{"role": "user", "content": ac.build_prompt(trader, price)}]
bad_reply = '{"action": "Buy", "amount": 3}'
_, error = ac.parse_decision(bad_reply)
second_messages = first_messages + [
    {"role": "assistant", "content": bad_reply},
    {"role": "user", "content": ac.feedback_message(error)},
]
good_reply = '{"action": "buy", "amount": 3}'

# Pretend these were recorded from a real AI
ac.replay_mode = True
ac.replay_queue.extend([
    {"trader": "Tess", "messages": first_messages, "reply": bad_reply},
    {"trader": "Tess", "messages": second_messages, "reply": good_reply},
])

result = ac.ai_decide(trader, price)
print("Result:", result)

assert result == ("buy", 3), "retry did not produce the corrected decision"
assert len(ac.replay_queue) == 0, "not every recorded reply was used"
print("TEST PASSED: invalid reply was retried and corrected")
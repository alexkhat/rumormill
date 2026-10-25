# RumorMill - runs the simulation

import random
from market import buy_shares, sell_shares, show_trader, net_worth, decide
from ai_client import ai_decide
random.seed(42)  # for reproducibility

stock_price = 100

alice = {"name": "Alice", "cash": 1000, "shares": 0, "brain": "ai"}  # Alice will use the AI to make decisions
bob = {"name": "Bob", "cash": 1000, "shares": 0, "brain": "random"}  # Bob will make random decisions
carol = {"name": "Carol", "cash": 1000, "shares": 0, "brain": "random"}
trader_list = [alice, bob, carol]

print("RumorMill market is starting...")

print("\n--- Rule tests ---")
buy_shares(alice, stock_price, 20)   # too expensive -> should be rejected
buy_shares(alice, stock_price, -5)   # negative -> should be rejected
buy_shares(alice, stock_price, 0)    # zero -> should be rejected
sell_shares(bob, stock_price, 10)    # Bob owns nothing -> should be rejected

print("\n--- Trading simulation (3 days) ---")

for day in range(1, 4):
    print(f"\n--- Day {day}---")

    # Fresh counters every morning
    shares_bought = 0
    shares_sold = 0

    for trader in trader_list:
        if trader['brain'] == 'ai':
            action, amount = ai_decide(trader, stock_price)
        else:
            action, amount = decide(trader, stock_price)
        print(f"{trader['name']} wants to {action} {amount} shares")

        if action == "buy":
            if buy_shares(trader, stock_price, amount):
                shares_bought += amount
        elif action == "sell":
            if sell_shares(trader, stock_price, amount):
                shares_sold += amount
        else:
            print(f"{trader['name']} holds and does nothing.")

    # Move the price
    net_demand = shares_bought - shares_sold
    stock_price = stock_price + net_demand

    if stock_price < 1:
        stock_price = 1  # price floor

    print(f"\nEnd of day {day}: net demand {net_demand}, new price {stock_price}")
    for trader in trader_list:
        show_trader(trader)

print(f"\nFinal price: {stock_price}")
for trader in trader_list:
    print(f"{trader['name']}'s net worth: {net_worth(trader, stock_price)}")
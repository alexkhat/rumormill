# RumorMill - market rules

import random


def buy_shares(investor, price, shares):
    """Try to buy shares. Returns True if the trade happened, False if it was refused."""
    if shares <= 0:
        print(f"REJECTED: {investor['name']} tried to buy {shares} shares. Amount must be positive.")
        return False

    total_cost = price * shares

    if investor["cash"] < total_cost:
        print(f"REJECTED: {investor['name']} needs {total_cost} but only has {investor['cash']}.")
        return False

    investor["cash"] -= total_cost
    investor["shares"] += shares
    print(f"{investor['name']} bought {shares} shares at {price} each (total {total_cost}).")
    return True


def sell_shares(investor, price, shares):
    """Try to sell shares. Returns True if the trade happened, False if it was refused."""
    if shares <= 0:
        print(f"REJECTED: {investor['name']} tried to sell {shares} shares. Amount must be positive.")
        return False

    if investor["shares"] < shares:
        print(f"REJECTED: {investor['name']} tried to sell {shares} shares but only has {investor['shares']}.")
        return False

    total_revenue = price * shares
    investor["cash"] += total_revenue
    investor["shares"] -= shares
    print(f"{investor['name']} sold {shares} shares at {price} each (total {total_revenue}).")
    return True


def show_trader(investor):
    print(f"  {investor['name']}: cash {investor['cash']}, shares {investor['shares']}")


def net_worth(investor, price):
    """Calculate the net worth of an investor."""
    return investor["cash"] + investor["shares"] * price


def decide(trader, price):
    """Decide what a trader wants to do. Returns (action, amount)."""
    action = random.choice(["buy", "sell", "hold"])
    amount = random.randint(1, 5)
    return action, amount
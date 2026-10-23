import random
random.seed(42)  # for reproducibility
# RumorMill - Milestone 1: the market board

stock_price = 100  # whole numbers for now (see note below)

alice = {"name": "Alice", "cash": 1000, "shares": 0}
bob = {"name": "Bob", "cash": 1000, "shares": 0}
carol = {"name": "Carol", "cash": 1000, "shares": 0}
trader_list = [alice, bob, carol]


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


def show_trader(investor):
    print(f"  {investor['name']}: cash {investor['cash']}, shares {investor['shares']}")


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
  


def net_worth(investor, price):
    """Calculate the net worth of an investor."""
    return investor["cash"] + investor["shares"] * price


print("RumorMill market is starting...")

print("\n--- Rule tests ---")
buy_shares(alice, stock_price, 20)   # too expensive -> should be rejected
buy_shares(alice, stock_price, -5)   # negative -> should be rejected
buy_shares(alice, stock_price, 0)    # zero -> should be rejected
sell_shares(bob, stock_price, 10)    # Bob tries to sell shares he doesn't own -> should be rejected

print("\n--- Trading simulation (3 days) ---")

for day in range(1, 4):
    print(f"\n--- Day {day}---")

    # Fresh Counters every morning
    shares_bought = 0
    shares_sold = 0

    for trader in trader_list:
            action = random.choice (["buy", "sell", "hold"])
            amount = random.randint(1, 5)
            print(f"{trader['name']} wants to {action} {amount} shares")

    # Traders - only count the ones that actually trade
    if day == 1:
        if buy_shares(alice, stock_price, 3):
            shares_bought += 3
    elif day == 2:
        if buy_shares(bob, stock_price, 2):
            shares_bought += 2
    else:
        if sell_shares(alice, stock_price, 1):
            shares_sold += 1

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
    
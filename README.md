# RumorMill

A multi-agent stock market simulation for studying how AI agents react to fake news.

## What is this?

RumorMill is a pretend stock market that runs on your computer. Traders buy and sell
shares, and the share price moves up or down depending on how much buying and selling
happens each day.

The long-term plan is to replace the traders with AI agents, then add one dishonest
agent that spreads fake news, and measure who gets fooled.

## Why?

AI agents are starting to read information and act on it in the real world. If a single
fake post can trick an AI agent into a bad decision, that is a real security problem.
This project is built to measure that risk, and to test ways of defending against it.

## Current status: Milestone 1 (market engine)

What works right now:

- Traders with cash and shares
- Buying and selling shares
- Rules that reject bad trades (not enough cash, not enough shares, zero or negative amounts)
- A share price that rises with buying and falls with selling, with a minimum price of 1
- Net worth calculation (cash + shares × price) to see who is winning

## Roadmap

1. **Market engine** - done
2. **Random traders**: more traders who decide for themselves each day
3. **AI traders**: traders powered by a large language model (IFM K2 Horizon)
4. **The rumour experiment**: a fake-news agent, a fact-checker, and results comparing both
5. **Cloud**: running the simulation on AWS

## How to run

Requires Python 3.

    py market.py


# RumorMill

A multi-agent stock market where AI traders read the news, talk on a shared forum,
and trade. One of them is lying.

## The idea

AI agents are starting to read information and act on it. RumorMill tests how easily
they can be manipulated.

The market is full of AI investors. Each day they read the news and the forum, then
decide to buy, sell or hold. One agent is a manipulator: it posts fake news and
rumours to push the price in its favour.

Every experiment runs twice, once with the manipulator and once without, using the
same seed so the only difference is the liar. Then the results are compared:

- How far does the price move away from where it should be?
- Which traders get fooled, and which ones don't?
- Do traders start copying each other and panic together?
- Does adding a fact-checking agent reduce the damage?

## How it works

    News + Forum  ->  AI traders decide  ->  Market applies the rules  ->  Results saved
         ^                                                                      |
         +------------------------------ next day <-----------------------------+

**The market** is plain Python with no AI. It holds prices, cash and shares, and
enforces the rules: no spending money you don't have, no selling shares you don't own.

**The traders** are AI agents in three tiers, each running a different model size:

| Tier | Model | Role |
|---|---|---|
| Retail | K2 Horizon 0.9B | Simple investors, easy to influence |
| Informed | K2 Horizon 7B | More careful investors |
| Institutional | K2 Horizon 375B | Few, well-informed investors |

**The manipulator** posts fake headlines and rumours to the forum.

**The fact-checker** reviews forum posts and flags ones that look false.

## Engineering

- **Reproducible runs:** fixed random seeds, and every AI call is recorded so any run can be replayed exactly
- **Structured AI output:** every decision is validated against a schema before it touches the market
- **Crash recovery:** progress is saved after each day, so a long run can resume where it stopped
- **Rate-limit handling:** waits and retries on API limits instead of crashing
- **Tracing:** every agent's input, reasoning and decision can be inspected
- **Tested rules:** automated tests check that cash and shares always add up

## Tech stack

| Area | Technology |
|---|---|
| Language | Python |
| AI models | IFM K2 Horizon (OpenAI-compatible API) |
| Agent orchestration | LangGraph |
| Tracing and evaluation | LangSmith |
| Output validation | Pydantic |
| Testing | pytest |
| Analysis and charts | pandas, matplotlib |
| Cloud | AWS Lambda, Step Functions, DynamoDB, S3, Secrets Manager |
| Infrastructure | AWS SAM |
| CI | GitHub Actions |
| Querying results | MCP server |

## Status

- [x] Market engine: trading rules, price movement, net worth, reproducible runs
- [x] Traders that decide for themselves each day
- [ ] AI traders
- [ ] Manipulator and fact-checker
- [ ] Experiment runs and results
- [ ] AWS deployment

## Run it

Requires Python 3.

    py market.py
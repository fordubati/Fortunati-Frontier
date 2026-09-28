# Fortunati Frontier: Editorial Guide

The routine that writes each edition follows this guide exactly. The reader is Rohan Fortunati, a Finance student (Economics and Accounting minors) at Montana State University in Bozeman who is recruiting for finance internships, plus the subscribers he shares it with. They are smart, busy, and reading on a phone at 7 AM.

## Voice: write like a sharp human editor, not an AI

**The rule of every item:** bold one-line takeaway → 1–2 short sentences of *why it matters* → source link. Then stop.

- **Lead with the fact or number.** "10-yr yield: 4.62%, up 9 bp." Not "Yields continued their upward trajectory this week as…"
- **Short.** Sentences under 25 words. Paragraphs of 3 sentences max. If a word can go, cut it.
- **Plain words.** "Rose," "fell," "because." Explain jargon once, in 5 words or fewer, in parentheses.
- **Concrete over abstract.** Name the company, the number, the date, the place.
- **No filler or AI tells.** Never use: "Here's what…", "Let's dive in", "It's worth noting", "In today's…", "landscape", "navigate", "delve", "amid", "a testament to", "underscores", "pivotal", "robust", "notably", "Additionally," "Moreover," "In conclusion", "ripped", rhetorical questions in the body, or em-dash chains. No exclamation points. No emoji in body text.
- **Neutral and factual.** Report what happened and what each side argues. No partisan adjectives; describe political actors by their actions and stated positions.
- **Market angle** on every political or geopolitical item: one italic line starting with *Markets:*.
- **Not advice.** Educational commentary only. No buy/sell calls.

## Links: every item is clickable

Every item ends with a link to the best source article, formatted exactly `[Read more →](url)`. Use the article itself, not a homepage. Prefer original reporting (Reuters, AP, WSJ, Bloomberg, CNBC, FT, the Fed, company releases, Bozeman Daily Chronicle, Montana Free Press, Daily Montanan). One link per item; extra sources can go inline.

## Numbers and charts: data first

1. **Before writing,** run the chart builder:
   - Daily: `pip install -q matplotlib && python3 scripts/charts.py --date YYYY-MM-DD`
   - Weekly: add `--weekly`
2. It writes `assets/charts/YYYY-MM-DD/` with `markets.png`, `watchlist.png` (if the watchlist has tickers), `yield_curve.png` (weekly), and **`data.json`**.
3. **Quote market levels and % or bp changes from `data.json`.** It holds real FRED and exchange data. Use web sources only for things it doesn't cover (earnings, news, politics, local). If `data.json` lists errors for a series, find the number from a reliable source or leave it out.
4. **Embed each chart that exists** at the section it belongs to, using the site's relative path:
   `![Markets, last 3 months]({{ site.baseurl }}/assets/charts/YYYY-MM-DD/markets.png)`
5. Commit the whole `assets/charts/YYYY-MM-DD/` folder with the post.

## Watchlist

`watchlist.md` holds the reader's tickers, one per line (`- NVDA`, with an optional note). Read it every run and never edit it. Use `data.json` → `watchlist` for price moves. Skip malformed lines; flag unknown symbols as "unrecognized ticker: XYZ".

## Daily Brief (Mon–Sat): 350–550 words, a 3-minute read

Front matter:
```yaml
---
layout: post
title: "Daily Brief: Monday, September 28"
categories: [daily]
date: 2026-09-28 06:17:42 -0600   # the ACTUAL current time: TZ=America/Denver date "+%Y-%m-%d %H:%M:%S %z"
summary: "One sentence, under 20 words: the day's headline."
---
```

Body, in this order:
1. `## In 60 seconds`: exactly 3 bullets, one line each, the three things that matter most today.
2. `## Markets`: the markets chart, then 3–5 items (bonds, stocks, housing, tariffs, commodities; only what moved).
3. `## Watchlist`: the watchlist chart, then one bullet per ticker with material news or a move of about ±3% or more: `**TICKER** +x.x%: what happened. [Read more →](url)`. End with a single line listing the quiet tickers.
4. `## World`: 1–3 items (Japan, UK, China, others).
5. `## Politics & Geopolitics`: 1–3 items, each with a *Markets:* line.
6. `## Montana & Bozeman`: 1–3 items.
7. `## One question`: one thought-provoking question, one line.

Skip any section (except 1 and 7) when nothing notable happened.

## Weekly Edition (Sun): 1,200–1,800 words, an 8–10-minute read

Front matter as above, with `categories: [weekly]` and title `Weekly Edition: Week of <Monday's date>`.

Body, in this order:
1. `## The week in 60 seconds`: 5 one-line bullets.
2. `## Markets`: the markets chart and the yield curve chart, then a compact **scoreboard table** from `data.json` (instrument | level | 1-wk change). Then `### Bonds`, `### Stocks`, `### Housing`, `### Tariffs & Trade`, `### Commodities`, each 2–4 items in the item format (≤ 120 words per subsection).
3. `### Watchlist`: the watchlist chart; table (ticker | close | 1-wk %) from `data.json`; then 1–2 sentences per ticker on the week's news, with a link.
4. `## Key Economies`: `### Japan`, `### United Kingdom`, `### China`, each ≤ 80 words with a *Markets:* line and a link.
5. `## Politics & Geopolitics`: `### Conflicts`, `### U.S. National Politics`, `### Global Affairs`, each 2–3 items.
6. `## Montana & Bozeman`: `### Housing`, `### Business`, `### Local Politics`, each 1–3 items.
7. `## Connecting the dots`: 3 bullets linking stories across sections (e.g., Red Sea shipping → oil → inflation → yields).
8. `## Questions to think about`: 3 questions with no single right answer.
9. `## Interview angle`: 3 questions an interviewer might ask about this week, each with a 1–2 sentence model answer.
10. `## The week ahead`: bullets of the dated data releases, Fed events, earnings, and political events.

## Files and publishing

- Weekly: `_posts/YYYY-MM-DD-weekly-edition.md`. Daily: `_posts/YYYY-MM-DD-daily-brief.md`, using today's Mountain Time date.
- The front-matter `date` must be the real current time (never a future time), or Jekyll hides the post.
- If today's file already exists, update it instead of creating a duplicate.
- Commit the post and its `assets/charts/YYYY-MM-DD/` folder to `main` with the message `Daily Brief YYYY-MM-DD` or `Weekly Edition YYYY-MM-DD`, then push to `main`.
- Touch nothing else in this repository.

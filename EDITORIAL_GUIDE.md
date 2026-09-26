# Fortunati Frontier: Editorial Guide

The routine that writes each edition follows this guide exactly. The reader is Rohan Fortunati, a Finance student (Economics and Accounting minors) at Montana State University in Bozeman, recruiting for summer 2027 finance internships, plus the subscribers he shares it with. Write for a sharp reader who is still learning: explain jargon once, briefly, the first time it appears in an edition.

## Voice and rules

1. **Neutral and factual.** Report what happened, what each side argues, and why it matters for markets, businesses, and households. Never editorialize or take partisan sides. Describe political actors by their actions and stated positions, not adjectives.
2. **Market angle on everything.** For each political or geopolitical item, add one line: *Why it matters for markets:* ...
3. **Cross-reference.** When stories connect (e.g., a Red Sea attack → shipping rates → oil → inflation expectations → Treasury yields), say so explicitly and link to the related section or a prior edition in `_posts/`.
4. **Context.** Give one or two sentences of background so a reader who missed last week can follow along.
5. **Sources.** Every key number or claim gets an inline source link, e.g. `([Reuters](url))`. Use only facts found in this run's research, and never invent numbers. If a figure can't be confirmed, leave it out.
6. **Recency.** Daily briefs cover roughly the last 24 hours (Monday's covers since Saturday's). The weekly covers the last 7 days. Check `_posts/` for the previous edition so you don't repeat stale items; if a story has no update, skip it.
7. **Not advice.** Educational commentary only. No buy/sell recommendations and no personalized financial advice.
8. **Dates.** All dates and times are America/Denver (Mountain Time).

## Sections (always in this order; use these exact `##` headings)

### Weekly Edition (Sundays, target 2,000–2,800 words, about a 12–15 minute read)

Front matter:
```yaml
---
layout: post
title: "Weekly Edition: Week of September 21, 2026"
categories: [weekly]
date: 2026-09-27 06:17:42 -0600   # the ACTUAL current time: TZ=America/Denver date "+%Y-%m-%d %H:%M:%S %z"
summary: "One sentence: the week's single most important theme."
---
```

Body:
- A 3–4 sentence opening: the week's through-line.
- `## Markets`
  - `### Bonds`: Treasury yields (2y, 10y, 30y), yield-curve shape, Fed expectations, credit spreads. 1–2 paragraphs.
  - `### Stocks`: S&P 500, Nasdaq, Dow, Russell 2000 weekly moves; sector leaders and laggards; notable earnings. 1–2 paragraphs.
  - `### Housing`: mortgage rates, national price data, housing starts and sales. 1–2 paragraphs.
  - `### Tariffs & Trade`: tariff actions, trade negotiations, court rulings, effects on prices and supply chains. 1–2 paragraphs.
  - `### Commodities`: oil (WTI/Brent), natural gas, gold, copper, agriculture (wheat and cattle matter to Montana). 1–2 paragraphs.
  - A compact **scoreboard table**: instrument | level | weekly change.
  - `### Watchlist`: only if `watchlist.md` lists tickers. First a table (ticker | company | close | weekly % change), then 2–3 sentences per ticker: the week's news and catalysts (earnings, guidance, analyst actions, deals, lawsuits, sector moves), why it moved, and what's coming next (e.g., an earnings date). Factual only; never buy/sell opinions.
- `## Key Economies`
  - `### Japan`, `### United Kingdom`, `### China`: central bank, currency, growth, and politics, each with a market angle. One paragraph each.
- `## Politics & Geopolitics`
  - `### Conflicts`: e.g., Iran, the Houthis and Red Sea shipping, and other active conflicts and negotiations.
  - `### U.S. National Politics`: e.g., the midterms, White House actions, Congress, the courts.
  - `### Global Affairs`: e.g., AI policy and competition, alliances, diplomacy and negotiations.
- `## Montana & Bozeman`
  - `### Housing`: Bozeman / Gallatin County and Montana housing.
  - `### Business`: local and Montana business news, Montana banks (Stockman, First Interstate, Glacier), D.A. Davidson, big employers.
  - `### Local Politics`: city, county, and state government.
- `## Connecting the Dots`: 3–5 bullets linking stories across sections.
- `## Questions to Think About`: 3–5 thought-provoking questions with no single right answer (e.g., "If tariffs raise input costs but the dollar weakens, who absorbs the margin hit?").
- `## Interview Angle`: 3 questions an interviewer might ask about this week, each with a 1–2 sentence model answer.
- `## The Week Ahead`: the key data releases, Fed speakers, earnings, and political events coming up.

### Daily Brief (Mon–Sat, target 450–700 words, about a 4–5 minute read)

Front matter:
```yaml
---
layout: post
title: "Daily Brief: Monday, September 28"
categories: [daily]
date: 2026-09-28 06:17:42 -0600   # the ACTUAL current time: TZ=America/Denver date "+%Y-%m-%d %H:%M:%S %z"
summary: "One sentence: the day's headline."
---
```

Body: skim format, 1–3 bullets per section and only what actually moved. Skip a section entirely if nothing notable happened.
- `## Markets` (bonds, stocks, housing, tariffs, commodities, merged into one list)
- `## Watchlist`: only if `watchlist.md` lists tickers. One bullet per ticker with **material** news or a notable move (roughly ±3% or more) since the last brief: `**TICKER** +x.x%: what happened ([source](url))`. Then one line listing the quiet tickers ("No major news: AAPL, KO"). Factual only; never buy/sell opinions.
- `## World` (Japan / UK / China and other economies)
- `## Politics & Geopolitics`
- `## Montana & Bozeman`
- `## One Question`: one thought-provoking question.

## Watchlist

`watchlist.md` holds the reader's tickers, one per line (`- NVDA`, with an optional note in parentheses). Read it on every run. Ignore blank, placeholder, or malformed lines; if a symbol isn't a real ticker, skip it and mention "unrecognized ticker: XYZ" at the end of the Watchlist section. Research each ticker's news and price move for the edition's time window. Never edit `watchlist.md`.

## Files and publishing

- Weekly: `_posts/YYYY-MM-DD-weekly-edition.md`. Daily: `_posts/YYYY-MM-DD-daily-brief.md`, using today's Mountain Time date.
- The front-matter `date` must be the real current time (never a future time), or Jekyll will hide the post.
- If today's file already exists, update it instead of creating a duplicate.
- Commit to `main` with the message `Daily Brief YYYY-MM-DD` or `Weekly Edition YYYY-MM-DD`, then push to `main`. GitHub Pages publishes automatically.
- Touch nothing outside `_posts/` unless the run's instructions say to.

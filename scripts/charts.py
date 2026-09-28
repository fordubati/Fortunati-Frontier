#!/usr/bin/env python3
"""Fortunati Frontier chart + data builder.

Usage:  python3 scripts/charts.py [--date YYYY-MM-DD] [--weekly]

Writes to assets/charts/<date>/:
  markets.png      4 small multiples: S&P 500, 10-yr Treasury, WTI oil, 30-yr mortgage
  watchlist.png    one small multiple per ticker in watchlist.md (if any)
  yield_curve.png  (weekly only) curve today vs 1 month ago vs 1 year ago
  data.json        latest levels and 1-day / 1-week / 1-month changes, the source of
                   truth for numbers quoted in the edition

Every fetch is independent: a failed series is skipped and recorded in
data.json["errors"], never fatal.
"""
import argparse, csv, io, json, os, re, sys, time, urllib.request
from datetime import date, datetime, timedelta

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker
except ImportError:
    sys.exit("matplotlib missing: pip install matplotlib")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (FortunatiFrontier chart bot)"}

# Palette (validated reference palette, light mode)
SURFACE = "#fcfcfb"; INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"
GRID = "#e1e0d9"; AXIS = "#c3c2b7"; UP = "#006300"; DOWN = "#d03b3b"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": AXIS,
    "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.facecolor": SURFACE, "figure.facecolor": SURFACE,
})

errors = []


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1 + i)
    raise last


def fred(series_id, start):
    txt = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}")
    out = []
    for row in csv.DictReader(io.StringIO(txt)):
        v = row.get(series_id) or list(row.values())[-1]
        d = row.get("observation_date") or row.get("DATE") or list(row.values())[0]
        try:
            out.append((datetime.strptime(d, "%Y-%m-%d").date(), float(v)))
        except (ValueError, TypeError):
            continue
    if not out:
        raise ValueError(f"no data for {series_id}")
    return out


def stock(ticker):
    """Daily closes for ~6 months. Yahoo chart API first, Stooq as fallback."""
    try:
        j = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=6mo&interval=1d"))
        res = j["chart"]["result"][0]
        closes = res["indicators"]["quote"][0]["close"]
        pts = [(datetime.utcfromtimestamp(t).date(), c) for t, c in zip(res["timestamp"], closes) if c is not None]
        name = res.get("meta", {}).get("longName") or res.get("meta", {}).get("shortName") or ticker
        if pts:
            return pts, name
    except Exception as e:  # noqa: BLE001
        errors.append(f"yahoo {ticker}: {e}")
    txt = get(f"https://stooq.com/q/d/l/?s={ticker.lower()}.us&i=d")
    pts = []
    for row in csv.DictReader(io.StringIO(txt)):
        try:
            pts.append((datetime.strptime(row["Date"], "%Y-%m-%d").date(), float(row["Close"])))
        except (KeyError, ValueError):
            continue
    pts = [p for p in pts if p[0] >= date.today() - timedelta(days=190)]
    if not pts:
        raise ValueError(f"no price data for {ticker}")
    return pts, ticker


def value_on_or_before(pts, d):
    cands = [v for (x, v) in pts if x <= d]
    return cands[-1] if cands else None


def changes(pts, is_rate):
    last_d, last = pts[-1]
    prev = pts[-2][1] if len(pts) > 1 else None
    wk = value_on_or_before(pts, last_d - timedelta(days=7))
    mo = value_on_or_before(pts, last_d - timedelta(days=30))

    def ch(base):
        if base is None:
            return None
        return round((last - base) * 100, 1) if is_rate else round((last / base - 1) * 100, 2)
    return {"as_of": last_d.isoformat(), "level": round(last, 3), "unit": "bp" if is_rate else "%",
            "chg_1d": ch(prev), "chg_1w": ch(wk), "chg_1m": ch(mo)}


def arrow(v, unit):
    if v is None:
        return "", INK2
    sign = "▲" if v > 0 else ("▼" if v < 0 else "■")
    if unit == "bp":  # rates: up is not "good" or "bad", so keep neutral ink
        return f"{sign} {abs(v):.0f} bp", INK2
    return f"{sign} {abs(v):.1f}%", (UP if v > 0 else DOWN if v < 0 else INK2)


def fmt_level(v, kind):
    if kind == "rate":
        return f"{v:.2f}%"
    if kind == "usd":
        return f"${v:,.2f}"
    return f"{v:,.0f}"


def panel(ax, pts, title, kind, ch, window_days=92):
    cutoff = pts[-1][0] - timedelta(days=window_days)
    xs = [d for d, _ in pts if d >= cutoff]
    ys = [v for d, v in pts if d >= cutoff]
    ax.plot(xs, ys, color=SERIES[0], linewidth=2, solid_capstyle="round")
    ax.plot([xs[-1]], [ys[-1]], "o", color=SERIES[0], markersize=6, markeredgecolor=SURFACE, markeredgewidth=2)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0, labelsize=9)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.text(0, 1.19, title, transform=ax.transAxes, fontsize=10.5, color=INK2, va="bottom")
    ax.text(0, 1.03, fmt_level(ys[-1], kind), transform=ax.transAxes, fontsize=16, fontweight="bold", color=INK, va="bottom")
    day_txt, day_col = arrow(ch.get("chg_1d"), ch["unit"])
    wk_txt, wk_col = arrow(ch.get("chg_1w"), ch["unit"])
    ax.text(1, 1.03, f"{day_txt} day", transform=ax.transAxes, ha="right", fontsize=10, color=day_col, va="bottom")
    ax.text(1, 1.12, f"{wk_txt} wk", transform=ax.transAxes, ha="right", fontsize=10, color=wk_col, va="bottom")


def save(fig, path):
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--weekly", action="store_true")
    a = ap.parse_args()
    outdir = os.path.join(ROOT, "assets", "charts", a.date)
    os.makedirs(outdir, exist_ok=True)
    start = (date.today() - timedelta(days=400)).isoformat()
    data = {"generated": datetime.utcnow().isoformat() + "Z", "markets": {}, "watchlist": {}, "curve": {}, "charts": [], "errors": errors}

    # ---- Markets ----
    specs = [("SP500", "S&P 500", "index", False), ("DGS10", "10-yr Treasury yield", "rate", True),
             ("DCOILWTICO", "WTI crude ($/bbl)", "usd", False), ("MORTGAGE30US", "30-yr mortgage rate", "rate", True)]
    extra = [("NASDAQCOM", "Nasdaq Composite", False), ("DJIA", "Dow Jones", False), ("DGS2", "2-yr Treasury", True),
             ("DGS30", "30-yr Treasury", True)]
    series = {}
    for sid, name, kind, is_rate in specs:
        try:
            pts = fred(sid, start); series[sid] = (pts, name, kind, is_rate)
            data["markets"][name] = changes(pts, is_rate)
        except Exception as e:  # noqa: BLE001
            errors.append(f"FRED {sid}: {e}")
    for sid, name, is_rate in extra:
        try:
            data["markets"][name] = changes(fred(sid, start), is_rate)
        except Exception as e:  # noqa: BLE001
            errors.append(f"FRED {sid}: {e}")
    if series:
        fig, axes = plt.subplots(2, 2, figsize=(10, 6.4))
        for ax, sid in zip(axes.flat, [s for s, *_ in specs]):
            if sid in series:
                pts, name, kind, is_rate = series[sid]
                panel(ax, pts, name, kind, changes(pts, is_rate), window_days=365 if sid == "MORTGAGE30US" else 92)
            else:
                ax.axis("off")
        fig.suptitle("Markets, last 3 months", x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK, y=1.03)
        fig.text(0.01, -0.02, "Source: FRED, Federal Reserve Bank of St. Louis. Mortgage rate is weekly (1-yr view).", fontsize=8, color=MUTED)
        fig.tight_layout(h_pad=4.5, w_pad=3)
        save(fig, os.path.join(outdir, "markets.png")); data["charts"].append("markets.png")

    # ---- Watchlist ----
    tickers = []
    wl = os.path.join(ROOT, "watchlist.md")
    if os.path.exists(wl):
        for line in open(wl, encoding="utf-8"):
            m = re.match(r"^-\s+\"?([A-Za-z.\-]{1,6})\b", line)  # top-level list items only (skips indented examples)
            if m:
                tickers.append(m.group(1).upper())
    got = []
    for t in tickers[:9]:
        try:
            pts, name = stock(t)
            data["watchlist"][t] = dict(changes(pts, False), name=name)
            got.append((t, pts))
        except Exception as e:  # noqa: BLE001
            errors.append(f"price {t}: {e}")
    if got:
        cols = min(3, len(got)); rows = (len(got) + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(3.6 * cols, 2.9 * rows), squeeze=False)
        for ax in axes.flat:
            ax.axis("off")
        for ax, (t, pts) in zip(axes.flat, got):
            ax.axis("on")
            panel(ax, pts, t, "usd", data["watchlist"][t])
        fig.suptitle("Watchlist, last 3 months", x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK, y=1.04)
        fig.tight_layout(h_pad=4.5, w_pad=2.5)
        save(fig, os.path.join(outdir, "watchlist.png")); data["charts"].append("watchlist.png")

    # ---- Yield curve (weekly) ----
    if a.weekly:
        tenors = [("DGS3MO", "3M", 0.25), ("DGS6MO", "6M", 0.5), ("DGS1", "1Y", 1), ("DGS2", "2Y", 2),
                  ("DGS5", "5Y", 5), ("DGS10", "10Y", 10), ("DGS30", "30Y", 30)]
        curves = {"Today": [], "1 month ago": [], "1 year ago": []}
        for sid, lab, yrs in tenors:
            try:
                pts = fred(sid, start); last_d = pts[-1][0]
                for key, back in (("Today", 0), ("1 month ago", 30), ("1 year ago", 365)):
                    v = value_on_or_before(pts, last_d - timedelta(days=back))
                    if v is not None:
                        curves[key].append((lab, v))
            except Exception as e:  # noqa: BLE001
                errors.append(f"FRED {sid}: {e}")
        if curves["Today"]:
            data["curve"] = {k: dict(v) for k, v in curves.items()}
            fig, ax = plt.subplots(figsize=(10, 4.6))
            for (key, pts), col in zip(curves.items(), SERIES):
                if not pts:
                    continue
                xs = list(range(len(pts))); ys = [v for _, v in pts]
                ax.plot(xs, ys, color=col, linewidth=2.5 if key == "Today" else 2, marker="o", markersize=5,
                        markeredgecolor=SURFACE, markeredgewidth=1.5, label=key)
                ax.text(xs[-1] + 0.12, ys[-1], key, color=INK2, fontsize=10, va="center")
            ax.set_xticks(range(len(curves["Today"])))
            ax.set_xticklabels([lab for lab, _ in curves["Today"]])
            ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.2f}%"))
            ax.grid(axis="y", color=GRID, linewidth=0.8)
            for s in ("top", "right", "left"):
                ax.spines[s].set_visible(False)
            ax.tick_params(length=0)
            ax.set_xlim(-0.3, len(curves["Today"]) - 1 + 1.2)
            ax.legend(frameon=False, loc="upper left", fontsize=10)
            ax.set_title("U.S. Treasury yield curve", loc="left", fontsize=13, fontweight="bold", color=INK, pad=12)
            fig.text(0.01, -0.03, "Source: FRED, Federal Reserve Bank of St. Louis.", fontsize=8, color=MUTED)
            save(fig, os.path.join(outdir, "yield_curve.png")); data["charts"].append("yield_curve.png")

    with open(os.path.join(outdir, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(json.dumps({"outdir": outdir, "charts": data["charts"], "errors": errors}, indent=2))


if __name__ == "__main__":
    main()

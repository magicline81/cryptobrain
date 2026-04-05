"""
Crypto Signal System — Auto-Update Script
Holt täglich Marktdaten und aktualisiert index.html
Quellen: CoinGecko (kostenlos) + Alternative.me (kostenlos)
Kein API Key nötig!
"""

import requests, re, sys, json, os
from datetime import datetime, timezone, timedelta

# Windows console needs UTF-8 for emoji output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML_FILE          = "index.html"
SCORE_HISTORY_FILE = "score-history.json"
PAPER_TRADES_FILE  = "paper-trades.json"
TIMEOUT            = 15
WIEN               = timezone(timedelta(hours=2))  # UTC+2 Österreich

# ── Coin-Liste ─────────────────────────────────────────────────────
COINS = {
    "solana":       "SOL",
    "ripple":       "XRP",
    "ethereum":     "ETH",
    "cardano":      "ADA",
    "chainlink":    "LINK",
    "sui":          "SUI",
    "bittensor":    "TAO",
    "ondo-finance": "ONDO",
    "iota":         "IOTA",
}

# Reverse lookup: ticker → coingecko id
TICKER_TO_ID = {v: k for k, v in COINS.items()}

# Signals that trigger paper trade opening
BUY_SIGNALS = {"KAUFEN", "AKKUMULIEREN"}

# ── Hilfsfunktionen ────────────────────────────────────────────────
def fmt_price(usd):
    if usd >= 1000:  return f"${usd:,.0f}"
    elif usd >= 1:   return f"${usd:.2f}"
    elif usd >= 0.01: return f"${usd:.3f}"
    else:            return f"${usd:.4f}"

def fmt_change(pct):
    return f"+{pct:.1f}%" if pct >= 0 else f"{pct:.1f}%"

def fear_text(v):
    if v <= 20:   return "Extreme Fear 😱"
    elif v <= 40: return "Fear 😟"
    elif v <= 60: return "Neutral 😐"
    elif v <= 80: return "Greed 😏"
    else:         return "Extreme Greed 🤑"

def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))

# ── Daten holen ────────────────────────────────────────────────────
def get_fear():
    print("📊 Fear & Greed Index...")
    r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=TIMEOUT)
    v = int(r.json()["data"][0]["value"])
    print(f"   → {v}/100 — {fear_text(v)}")
    return v

def get_global():
    print("₿  BTC Dominanz...")
    r = requests.get("https://api.coingecko.com/api/v3/global", timeout=TIMEOUT)
    d = r.json()["data"]
    btc_dom = round(d["market_cap_percentage"]["btc"], 1)
    print(f"   → {btc_dom}%")
    return btc_dom

def get_prices():
    print("💰 Coin-Preise...")
    ids = ",".join(COINS.keys())
    r = requests.get(
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd&include_24hr_change=true",
        timeout=TIMEOUT
    )
    data = r.json()
    for cid, ticker in COINS.items():
        if cid in data:
            p = data[cid]["usd"]
            c = data[cid].get("usd_24h_change", 0)
            print(f"   → {ticker:5s}: {fmt_price(p):10s}  {fmt_change(c)}")
    return data

# ── HTML aktualisieren ─────────────────────────────────────────────
def update_html(fear, btc_dom, prices):
    print(f"\n📝 Aktualisiere {HTML_FILE}...")

    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"❌ {HTML_FILE} nicht gefunden! Datei muss 'index.html' heissen.")
        sys.exit(1)

    now = datetime.now(WIEN)
    changes = 0

    # 1. Datum oben in der App aktualisieren
    months_de = {1:"Januar",2:"Februar",3:"März",4:"April",5:"Mai",6:"Juni",
                 7:"Juli",8:"August",9:"September",10:"Oktober",11:"November",12:"Dezember"}
    new_date = f"{now.day}. {months_de[now.month]} {now.year} · {now.strftime('%H:%M')} Uhr"
    new_html = re.sub(r'date: "[^"]*"', f'date: "{new_date}"', html)
    if new_html != html: changes += 1
    html = new_html
    print(f"   ✅ Datum: {new_date}")

    # 2. Coin-Preise ersetzen
    if prices:
        for coin_id, ticker in COINS.items():
            if coin_id not in prices: continue
            p   = prices[coin_id]["usd"]
            chg = prices[coin_id].get("usd_24h_change", 0)
            new_price  = fmt_price(p)
            new_change = fmt_change(chg)

            def replace_in_coin_block(h, search_ticker, new_p, new_c):
                pattern = (
                    r'(ticker:"' + re.escape(search_ticker) + r'"[^}]*?)'
                    r'(price:")([^"]*?)(")'
                    r'([^}]*?)'
                    r'(change:")([^"]*?)(")'
                )
                def replacer(m):
                    return m.group(1) + m.group(2) + new_p + m.group(4) + \
                           m.group(5) + m.group(6) + new_c + m.group(8)
                return re.sub(pattern, replacer, h, flags=re.DOTALL)

            updated = replace_in_coin_block(html, ticker, new_price, new_change)
            if updated != html: changes += 1
            html = updated

    # 3. "Letzte Aktualisierung" Zeile — falls vorhanden
    ts = now.strftime("%d.%m.%Y %H:%M")
    new_html = re.sub(
        r'Letzte Aktualisierung: [\d\.: ]+',
        f'Letzte Aktualisierung: {ts} Uhr',
        html
    )
    if new_html != html: changes += 1
    html = new_html

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"   ✅ {changes} Änderungen in {HTML_FILE} gespeichert")
    return html, changes

# ── Score-Extraktion aus HTML ──────────────────────────────────────
def extract_market_score(html):
    """Berechnet gewichteten Markt-Score aus MARKET_SIGNAL_COMPONENTS."""
    m = re.search(r'const MARKET_SIGNAL_COMPONENTS = \[(.*?)\];', html, re.DOTALL)
    if not m:
        print("   ⚠️  MARKET_SIGNAL_COMPONENTS nicht gefunden")
        return None
    block = m.group(1)
    items = re.findall(r'score:(\d+), weight:(\d+)', block)
    if not items:
        return None
    total_w = sum(int(w) for _, w in items)
    weighted = sum(int(s) * int(w) for s, w in items) / total_w
    return round(clamp(weighted))

def extract_coin_data(html):
    """Liest ticker → {score, signal} aus COIN_MODELS."""
    m = re.search(r'const COIN_MODELS = \[(.*?)\];\s*\n', html, re.DOTALL)
    if not m:
        print("   ⚠️  COIN_MODELS nicht gefunden")
        return {}
    block = m.group(1)
    result = {}
    # Jeder Coin beginnt mit einem neuen Objekt, erkennbar an name:"XXX", ticker:"YYY"
    ticker_ms = list(re.finditer(r'ticker:"([A-Z]+)"', block))
    for idx, tm in enumerate(ticker_ms):
        start = tm.start()
        end   = ticker_ms[idx + 1].start() if idx + 1 < len(ticker_ms) else len(block)
        cb    = block[start:end]
        sm    = re.search(r'\bscore:(\d+),\s*signal:"([^"]+)"', cb)
        if sm:
            result[tm.group(1)] = {
                "score":  int(sm.group(1)),
                "signal": sm.group(2),
            }
    return result

def extract_chart_setups(html):
    """Liest ticker → {entry_chart, stop, tp1} aus CHART_ANALYSIS_MODELS."""
    m = re.search(r'const CHART_ANALYSIS_MODELS = \[(.*?)\];\s*\n', html, re.DOTALL)
    if not m:
        print("   ⚠️  CHART_ANALYSIS_MODELS nicht gefunden")
        return {}
    block   = m.group(1)
    setups  = {}
    tickers = list(re.finditer(r'ticker:"([A-Z]+)"', block))
    for idx, tm in enumerate(tickers):
        start    = tm.start()
        end      = tickers[idx + 1].start() if idx + 1 < len(tickers) else len(block)
        cb       = block[start:end]
        stop_m   = re.search(r'\bstop:"([^"]+)"', cb)
        tp_m     = re.search(r'takeProfit:\["([^"]+)"', cb)
        bz_m     = re.search(r'buyZone:"([^"]+)"', cb)
        if stop_m:
            def parse_num(s):
                try:    return float(s.replace(",", "").strip())
                except: return None
            stop = parse_num(stop_m.group(1))
            tp1  = parse_num(tp_m.group(1)) if tp_m else None
            # buyZone "76.0 - 78.5" → lower bound als Entry
            entry_chart = None
            if bz_m:
                parts = bz_m.group(1).split("-")
                if parts:
                    entry_chart = parse_num(parts[0])
            setups[tm.group(1)] = {
                "entry_chart": entry_chart,
                "stop":        stop,
                "tp1":         tp1,
            }
    return setups

# ── Score-History aktualisieren ────────────────────────────────────
def update_score_history(market_score, coin_data, date_str):
    """Hängt den heutigen Score-Snapshot an score-history.json an."""
    print(f"\n📈 Aktualisiere {SCORE_HISTORY_FILE}...")
    history = []
    if os.path.exists(SCORE_HISTORY_FILE):
        with open(SCORE_HISTORY_FILE, "r", encoding="utf-8") as f:
            try:   history = json.load(f)
            except Exception: history = []

    # Heutigen Eintrag überschreiben (idempotent bei mehrfachem Lauf)
    history = [h for h in history if h.get("date") != date_str]
    history.append({
        "date":   date_str,
        "market": market_score,
        "coins":  {ticker: d["score"] for ticker, d in coin_data.items()},
    })
    # Nur die letzten 90 Tage behalten
    history = sorted(history, key=lambda h: h["date"])[-90:]

    with open(SCORE_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print(f"   ✅ Score-History: {len(history)} Einträge ({date_str}: Markt={market_score})")

# ── Paper-Trading aktualisieren ────────────────────────────────────
def update_paper_trades(coin_data, chart_setups, prices, date_str):
    """Prüft offene Trades auf TP/SL und öffnet neue bei Kaufsignalen."""
    print(f"\n📊 Aktualisiere {PAPER_TRADES_FILE}...")

    # Datei laden
    trades = {"open": [], "closed": []}
    if os.path.exists(PAPER_TRADES_FILE):
        with open(PAPER_TRADES_FILE, "r", encoding="utf-8") as f:
            try:   trades = json.load(f)
            except Exception: pass

    wins = 0
    losses = 0
    still_open = []

    # 1. Offene Trades auf TP/SL prüfen
    for trade in trades.get("open", []):
        ticker  = trade["coin"]
        coin_id = TICKER_TO_ID.get(ticker)
        if not coin_id or coin_id not in prices:
            still_open.append(trade)
            continue

        current = prices[coin_id]["usd"]
        tp      = trade.get("take_profit")
        sl      = trade.get("stop_loss")

        if tp and current >= tp:
            pnl = round((tp - trade["entry"]) / trade["entry"] * 100, 2)
            trades["closed"].append({**trade, "outcome":"WIN",  "exit":tp,  "exit_price_actual":round(current,6), "closed":date_str, "pnl_pct":pnl})
            print(f"   ✅ WIN  {ticker}: +{pnl:.1f}%  (Kurs {fmt_price(current)} ≥ TP {fmt_price(tp)})")
            wins += 1
        elif sl and current <= sl:
            pnl = round((sl - trade["entry"]) / trade["entry"] * 100, 2)
            trades["closed"].append({**trade, "outcome":"LOSS", "exit":sl,  "exit_price_actual":round(current,6), "closed":date_str, "pnl_pct":pnl})
            print(f"   ❌ LOSS {ticker}: {pnl:.1f}%  (Kurs {fmt_price(current)} ≤ SL {fmt_price(sl)})")
            losses += 1
        else:
            still_open.append(trade)

    trades["open"] = still_open

    # 2. Neue Trades für Kaufsignale öffnen
    open_tickers = {t["coin"] for t in trades["open"]}
    new_trades   = 0

    for ticker, data in coin_data.items():
        if data["signal"] not in BUY_SIGNALS:
            continue
        if ticker in open_tickers:
            continue  # bereits offen
        coin_id = TICKER_TO_ID.get(ticker)
        if not coin_id or coin_id not in prices:
            continue

        current = prices[coin_id]["usd"]
        setup   = chart_setups.get(ticker, {})
        entry   = setup.get("entry_chart") or current
        stop    = setup.get("stop")
        tp1     = setup.get("tp1")

        # Fallback: -8% / +20%
        if not stop: stop = round(entry * 0.92, 6)
        if not tp1:  tp1  = round(entry * 1.20, 6)

        trade = {
            "id":            f"{ticker}-{date_str}",
            "coin":          ticker,
            "signal":        data["signal"],
            "entry":         entry,
            "entry_type":    "chart" if setup.get("entry_chart") else "market",
            "stop_loss":     stop,
            "take_profit":   tp1,
            "opened":        date_str,
            "price_at_open": round(current, 6),
        }
        trades["open"].append(trade)
        print(f"   📈 NEU  {ticker}: Entry={fmt_price(entry)}  SL={fmt_price(stop)}  TP={fmt_price(tp1)}")
        new_trades += 1

    with open(PAPER_TRADES_FILE, "w", encoding="utf-8") as f:
        json.dump(trades, f, ensure_ascii=False, indent=2)

    print(f"   ✅ Paper Trades: {len(trades['open'])} offen · {len(trades['closed'])} geschlossen  "
          f"(+{new_trades} neu, {wins} WIN, {losses} LOSS heute)")
    return trades

# ── Main ───────────────────────────────────────────────────────────
def main():
    now      = datetime.now(WIEN)
    date_str = now.strftime("%Y-%m-%d")
    print("=" * 56)
    print(f"  🎯 Crypto Signal — Auto-Update")
    print(f"  {now.strftime('%d.%m.%Y %H:%M')} Uhr (Wien)")
    print("=" * 56)

    try:
        fear    = get_fear()
        btc_dom = get_global()
        prices  = get_prices()

        # HTML aktualisieren (Preise + Datum)
        html, changes = update_html(fear, btc_dom, prices)

        # Scores aus (aktualisiertem) HTML extrahieren
        market_score = extract_market_score(html)
        coin_data    = extract_coin_data(html)
        chart_setups = extract_chart_setups(html)

        if market_score is not None:
            print(f"\n   📊 Markt-Score: {market_score}/100")

        # Score-History anhängen
        if market_score is not None and coin_data:
            update_score_history(market_score, coin_data, date_str)

        # Paper Trades prüfen / öffnen
        if coin_data and prices:
            update_paper_trades(coin_data, chart_setups, prices, date_str)

        print()
        print("=" * 56)
        print(f"  ✅ Fertig — {changes} HTML-Werte aktualisiert")
        print(f"  Fear & Greed : {fear}/100 — {fear_text(fear)}")
        print(f"  BTC Dominanz : {btc_dom}%")
        if prices and "solana" in prices:
            print(f"  SOL Preis    : {fmt_price(prices['solana']['usd'])}")
        print("=" * 56)

    except requests.exceptions.Timeout:
        print("❌ API Timeout — Server antwortet nicht. Nächstes Mal wieder.")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print("❌ Keine Internetverbindung. Nächstes Mal wieder.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        raise

if __name__ == "__main__":
    main()

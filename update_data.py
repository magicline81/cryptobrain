"""
Crypto Signal System — Auto-Update Script
Holt täglich Marktdaten und aktualisiert index.html
Quellen: CoinGecko (kostenlos) + Alternative.me (kostenlos)
Kein API Key nötig!
"""

import requests, re, sys
from datetime import datetime, timezone, timedelta

HTML_FILE  = "index.html"
TIMEOUT    = 15
WIEN       = timezone(timedelta(hours=2))  # UTC+2 Österreich

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
    # Strategie: suche ticker-spezifisch im Block jedes Coins
    if prices:
        for coin_id, ticker in COINS.items():
            if coin_id not in prices: continue
            p   = prices[coin_id]["usd"]
            chg = prices[coin_id].get("usd_24h_change", 0)
            new_price  = fmt_price(p)
            new_change = fmt_change(chg)

            # Ersetze price:"..." — alle Varianten (mit $, mit Komma, etc.)
            # Sucht nach: price:"$IRGENDWAS" gefolgt von change:"IRGENDWAS"
            # innerhalb des Coin-Blocks (zwischen dem Ticker und dem nächsten Ticker)
            def replace_in_coin_block(h, search_ticker, new_p, new_c):
                # Findet den Block dieses Coins (von ticker:"XXX" bis zur nächsten Zeile)
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
    return changes

# ── Main ───────────────────────────────────────────────────────────
def main():
    now = datetime.now(WIEN)
    print("=" * 50)
    print(f"  🎯 Crypto Signal — Auto-Update")
    print(f"  {now.strftime('%d.%m.%Y %H:%M')} Uhr (Wien)")
    print("=" * 50)

    try:
        fear    = get_fear()
        btc_dom = get_global()
        prices  = get_prices()
        changes = update_html(fear, btc_dom, prices)

        print()
        print("=" * 50)
        print(f"  ✅ Fertig — {changes} Werte aktualisiert")
        print(f"  Fear & Greed : {fear}/100 — {fear_text(fear)}")
        print(f"  BTC Dominanz : {btc_dom}%")
        if prices and "solana" in prices:
            print(f"  SOL Preis    : {fmt_price(prices['solana']['usd'])}")
        print("=" * 50)

    except requests.exceptions.Timeout:
        print("❌ API Timeout — Server antwortet nicht. Nächstes Mal wieder.")
        sys.exit(0)  # kein Fehler — einfach nächstes Mal
    except requests.exceptions.ConnectionError:
        print("❌ Keine Internetverbindung. Nächstes Mal wieder.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

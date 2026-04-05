# Crypto Signal System
### Systemdokumentation · Stand 5. April 2026

> Projektart: Statisches Analyse-Dashboard fuer Krypto-Markt- und Coin-Bewertung
> Laufzeit: React 18 UMD + ReactDOM UMD + Babel Standalone direkt im Browser
> Aktiver Einstieg: `index.html`
> Hosting-Ziel: GitHub Pages
> Hinweis: Keine Finanzberatung

---

## 1. Zweck des Systems

Das Projekt ist ein statisches Research- und Analyse-Dashboard. Es trennt vier Ebenen sauber:

- Marktregime
- Coin-spezifische Bewertung
- technische Chartanalyse und Setup-Qualitaet
- Signal-Performance-Tracking via Paper-Trading-Simulator

Das System soll keine Preisziele vorhersagen, sondern ein nachvollziehbares Scoring liefern. Die Darstellung ist absichtlich erklaerbar aufgebaut: Marktkomponenten, Coin-Subscores, Quellenkontext und Herleitungen koennen direkt im UI aufgeklappt werden. Der Paper-Trading-Simulator erlaubt es, die Signal-Qualitaet ueber Zeit zu messen und das Modell zu verbessern.

---

## 2. Projektbestand

### Kern-Dateien

| Datei | Rolle |
|------|------|
| `index.html` | Aktive Hauptdatei fuer GitHub Pages und aktuelle Laufzeit |
| `crypto-signal-system-docs.md` | Diese Systemdokumentation |
| `score-berechnungen.md` | Technische Formelbeschreibung des Scoring-Modells |
| `score-berechnungen-einfach.md` | Laienverstaendliche Beschreibung der Kennzahlen |
| `score-handbuch.md` | Sammeldokument fuer beide Score-Dokumente |

### Datendateien (neu ab 5. April 2026)

| Datei | Rolle |
|------|------|
| `score-history.json` | Taeglich wachsender Score-Snapshot (Market + alle Coins), max. 90 Eintraege |
| `paper-trades.json` | Paper-Trading-Simulator: offene und geschlossene simulierte Trades |

### Automatisierung und Hilfsdateien

| Datei | Rolle |
|------|------|
| `update_data.py` | Holt Fear & Greed, BTC-Dominanz, Coin-Preise, Score-History und Paper-Trades |
| `.github/workflows/update.yml` | Taeglicher GitHub-Action-Run um 07:00 UTC (= 09:00 Wien) |
| `auto-push.bat` | Einfaches lokales `git push`-Hilfsskript |
| `check-babel.js` | Prueft JSX-Transpilierung lokal |
| `babel-standalone.js` | Lokale Babel-Kopie fuer Syntaxchecks |
| `SKILL.md` | Lokale Arbeitsanweisungen fuer Frontend-Design |

---

## 3. Aktueller Systemstand (5. April 2026)

### Metadaten

- Datenstand `META.date`: `4. April 2026 · 14:39 Uhr`
- Markt-Score: `46/100`
- Markt-Verdict: `ABWARTEN`

### Aktuelle Coin-Scores

| Coin | Score | Signal | Preis (05.04.) |
|------|------:|--------|------:|
| SOL | 75 | KAUFEN | $80.19 |
| XRP | 72 | KAUFEN | $1.31 |
| LINK | 72 | KAUFEN | $8.65 |
| ETH | 67 | HALTEN | $2,051 |
| ADA | 62 | HALTEN | $0.245 |
| TAO | 59 | BEOBACHTEN | $307.98 |
| ONDO | 58 | BEOBACHTEN | $0.258 |
| IOTA | 53 | BEOBACHTEN | $0.063 |
| SUI | 50 | BEOBACHTEN | $0.871 |

### Aktuelle Breakdown-Gruppen

| Gruppe | Score |
|------|------:|
| Sentiment F&G | 82 |
| BTC Dominanz | 25 |
| On-Chain | 39 |
| Katalysatoren | 88 |
| Fed & Zinsen | 15 |
| Geopolitik | 14 |
| Inst. Flows | 45 |

---

## 4. Architektur und Laufzeitmodell

### Frontend-Aufbau

Die Anwendung wird vollstaendig clientseitig ausgefuehrt:

1. Browser laedt HTML, CSS und CDN-Skripte
2. Babel transpiliert das JSX direkt im Browser
3. React rendert in `#root`
4. Ein Loading-Overlay wird vor dem finalen Render angezeigt
5. `score-history.json` und `paper-trades.json` werden via `fetch()` beim Start geladen

### Technische Merkmale

- kein Build-Tool, kein Bundler, kein separates API-Backend
- Datenstand wird statisch in `index.html` gehalten
- Score-History und Paper-Trades in separaten JSON-Dateien im Repo
- Binance-API wird clientseitig fuer Live-Chartdaten und Formation-Analyse genutzt
- CoinGecko und Alternative.me werden serverseitig (GitHub Actions) genutzt

### Wichtige Konstanten und Funktionen

**Datenmodell:**
- `META`, `MARKET_SIGNAL_COMPONENTS`, `MARKET_BREAKDOWN_GROUPS`
- `COIN_MODELS`, `CHART_ANALYSIS_MODELS`
- `SOURCE_INFO`, `CHANCE_RISK_DERIVATION`

**Scoring-Logik:**
- `clampScore()`, `getWeightedScore()`, `getMarketVerdict()`
- `buildMarketBreakdownBars()`, `getMarketComponentScores()`
- `getChanceRiskProfile()`
- `getCoinSubScoreComponents()`, `getWeightedMarketScore()`
- `getDynamicSubScore()`, `getCoinSignal()`, `buildAnalystExplanation()`
- `getCoinConfidence()` — neu: Konfidenz-Score (HOCH/MITTEL/NIEDRIG) aus Stddev der 6 Subscores

**Chart-Logik:**
- `MiniGauge()`, `Gauge()`
- `TradingViewAdvancedChart()`, `ProMarketChart()`
- `mapChartIntervalToKlineInterval()`, `calculateEMA()`
- `getChartPrecision()`, `formatChartNumber()`, `formatChartLevel()`, `formatChartRange()`
- `getSetupMetrics()`, `buildChartScenario()`, `buildPremiumChartReadout()`
- `toPatternCandle()`, `detectCandlestickPatterns()`, `useCandlestickPatternAnalysis()`
- `detectStructurePatterns()`, `buildFallbackStructurePattern()`, `useStructurePatternAnalysis()`
- `ChartAnalysisReport()`

**Formation-Analyse (neu):**
- `detectCandlePatterns()` — erkennt Candle-Muster der letzten 3 Kerzen mit Staerke-Score 0-10
- `countTouches()` — Hilfsfunktion fuer Support/Resistance-Touchzaehlung
- `detectSRLevels()` — findet Pivot-Hochs/-Tiefs als S/R-Level mit Staerke-Score 0-10
- `detectTrendLines()` — prueft hoehere Tiefs / niedrigere Hochs und bewertet Trend mit 0-10
- `useLiveFormationAnalysis()` — React-Hook, ruft Binance-Daten ab und gibt Formation-Ergebnis zurueck

**UI-Hilfsfunktionen (neu):**
- `ScoreSparkline()` — SVG-Sparkline fuer Score-Verlaeufe
- `StrengthBar()` — Fortschrittsbalken mit Farbkodierung fuer Staerke-Scores 0-10

**App-Komponente:**
- `App()`

---

## 5. Marktmodell

Das Marktmodell besteht aus 12 gewichteten Komponenten auf einer 0-100-Skala.

### Komponenten und Gewichte

| Komponente | Gewicht | Stand 05.04.2026 |
|------|------:|------:|
| Fear & Greed Index | 15% | 82 |
| BTC Dominanz | 15% | 25 |
| Fed & Zinspolitik | 12% | 15 |
| Upgrade-Katalysatoren | 10% | 88 |
| Geopolitik / Kriege | 8% | 8 |
| Exchange Flows | 8% | 20 |
| Regulierung / ETFs | 7% | 88 |
| Institutionelle ETF Flows | 8% | 45 |
| Funding Rates | 5% | 45 |
| Globale Liquiditaet M2 | 4% | 25 |
| On-Chain Adressen | 4% | 60 |
| TVL Trend (DeFi) | 4% | 50 |

### Formel

```
marketScore = clampScore(weightedAverage(MARKET_SIGNAL_COMPONENTS))
```

### Verdict-Logik

| Bereich | Verdict |
|------|------|
| 70-100 | AKKUMULIEREN |
| 55-69 | VORSICHTIG KAUFEN |
| 40-54 | ABWARTEN |
| 25-39 | DEFENSIV |
| 0-24 | MEIDEN |

---

## 6. Coin-Modell

Jeder Coin startet mit 6 Basisdimensionen:

1. Upgrade-Katalysator
2. Institutionelle Flows
3. Technologie
4. Fundamentals
5. Makro-Exposition
6. Discount zum ATH

### Rechenlogik

```
weightedMarketScore = Overlay je Dimension aus Marktgruppen
marketTilt = (weightedMarketScore - 50) / 50

adjustedBase =
  bei Discount zum ATH: baseScore * 0.35 + discountPct * 0.65
  sonst: baseScore

headroom =
  bei positivem Tilt: 100 - adjustedBase
  bei negativem Tilt: adjustedBase

regimeAdjustment = headroom * marketTilt * sensitivity
finalSubScore = clampScore(adjustedBase + regimeAdjustment)
coinScore = clampScore(Durchschnitt aller 6 finalen Subscores)
```

### Sensitivitaeten

| Dimension | Sensitivity |
|------|------:|
| Upgrade-Katalysator | 0.30 |
| Institutionelle Flows | 0.35 |
| Technologie | 0.20 |
| Fundamentals | 0.20 |
| Makro-Exposition | 0.45 |
| Discount zum ATH | 0.30 |

### Coin-Signal-Logik

| Score | Signal |
|------|------|
| 80+ | AKKUMULIEREN |
| 70-79 | KAUFEN |
| 60-69 | HALTEN |
| unter 60 | BEOBACHTEN |

### Konfidenz-Badge (neu)

Auf jeder Coin-Karte wird zusaetzlich ein Konfidenz-Badge angezeigt:

```
stddev = Standardabweichung der 6 Subscore-Endwerte
HOCH   = stddev < 10  (alle Dimensionen zeigen in dieselbe Richtung)
MITTEL = stddev < 20
NIEDRIG = stddev >= 20 (widersprüchliche Signale)
```

---

## 7. Chance/Risiko-Modell

Das Chance/Risiko-Modell ist von Markt- und Coin-Score getrennt.

### Upside

```
upsideComposite =
  Fear & Greed             25%
  Upgrade-Katalysatoren    25%
  Institutionelle ETF Flows 25%
  On-Chain Adressen        15%
  Regulierung / ETFs       10%
```

### Risiko

```
downsidePressure =
  100 - BTC Dominanz       30%
  100 - Fed & Zinspolitik  25%
  100 - Geopolitik         25%
  100 - Exchange Flows     20%
```

### Umrechnung

```
contrarianBoost = max(0, 55 - marketScore) / 100
upside = min/max-begrenztes Multiple aus upsideComposite + contrarianBoost
risk   = min/max-begrenztes Multiple aus downsidePressure
ratio  = upside / risk
```

---

## 8. UI-Struktur

### Reiter-Navigation (4 Tabs)

```
Markt Signal  |  Coin Analyse  |  Chart Analyse  |  Performance
```

### Tab: Markt Signal

- Score-Legende mit Handlungsanweisungen je Bereich
- erklaerbare Einzelgewichte der Marktindikatoren
- Quellen- und Methodikblock
- Key Alerts
- Score-Verlaufs-Sparkline (letzte 30 Tage aus `score-history.json`)
- grosser Markt-Gauge
- Chance/Risiko-Box mit Herleitung
- Analysten-Einschaetzung
- Breakdown-Balken

### Tab: Coin Analyse

- Markt-Signal-Header mit Kurzkommentar
- responsive Coin-Grid (automatische Spaltenanzahl)
- zeilenweises Auf- und Zuklappen via `toggleCoinRow()`
- pro Coin-Karte:
  - Konfidenz-Badge (HOCH / MITTEL / NIEDRIG)
  - Signal-Badge
  - 14-Tage-Sparkline des Coin-Scores (aus `score-history.json`)
  - 6 Subscore-Module mit Erklaerung, Herleitung und Quellenzusammenfassung
  - Analystenbegruendung

### Tab: Chart Analyse

- Coin-Auswahl-Chips
- Intervall-Umschalter 1H / 4H / 1D
- Pro-Chart mit echten Binance-Kerzen, EMA20/50/200, Candle-Muster, Strukturformationen, Preislinien
- KPI-Zeile: Entry, Stop, TP1, CRV
- dokumentartiger Analyse-Report (Big Picture, Struktur, Level, Indikatoren, Szenarien)
- TradingView-Referenzansicht
- **Live Formation & Level Analyse** (unten, dynamisch je Coin und Intervall):
  - Kerzenformationen mit Staerke-Score 0-10
  - Support & Widerstand-Level mit Anzahl Tests und Staerke-Score 0-10
  - Trendlinien mit Staerke-Score 0-10

### Tab: Performance (neu)

- 6 KPI-Kacheln: offene Positionen, abgeschlossene Trades, Trefferquote, Ø P&L, Wins/Losses, bester Coin
- Offene Positionen: Coin, Entry, Eintrittszeit, Distanz zu TP und SL
- kumulierte P&L-Sparkline
- Trade-Historie: alle geschlossenen Trades mit WIN/LOSS-Badge und P&L in %

### Interaktionszustand in `App()`

- `openCoins`, `openCoinSubScores`
- `openLegend`, `openWeight`, `openBreakdown`, `openChanceRiskDetails`
- `tab` — neu: auch `"performance"`
- `coinGridColumns`, `chartCoinIndex`, `chartInterval`
- `paperTrades` — neu: geladen aus `paper-trades.json`
- `scoreHistory` — neu: geladen aus `score-history.json`

---

## 9. Paper-Trading-Simulator

### Konzept

Kein echtes Geld — rein simulierte Trades zur Validierung der Signal-Qualitaet.

### Ablauf

```
Taeglich 09:00 Wien (07:00 UTC) laeuft der GitHub-Actions-Workflow:

1. TP/SL-Pruefung offener Trades
   → Vergleich: Binance-Kurs heute 09:00 Wien vs. TP und SL
   → Kurs >= TP → WIN, Trade wird geschlossen
   → Kurs <= SL → LOSS, Trade wird geschlossen

2. Neue Trades oeffnen
   → Alle Coins mit Signal KAUFEN oder AKKUMULIEREN, die keinen offenen Trade haben
   → Entry = Binance-Kurs von gestern 09:00 Wien (rueckwirkend)
   → SL und TP aus CHART_ANALYSIS_MODELS.setup.stop / takeProfit[0]
   → Fallback: -8% SL, +20% TP
```

### Preisquelle

```
Binance REST API:
https://api.binance.com/api/v3/klines?symbol=SOLUSDT&interval=1h&startTime=<ts>&limit=1

Einstiegspreis = open-Wert der 1H-Kerze um 07:00 UTC (= 09:00 Wien)
Datum der 1H-Kerze:
  fuer Entry: gestern 07:00 UTC
  fuer TP/SL-Pruefung: heute 07:00 UTC
```

### Datenstruktur `paper-trades.json`

```json
{
  "open": [
    {
      "id": "SOL-2026-04-04",
      "coin": "SOL",
      "signal": "KAUFEN",
      "entry": 80.47,
      "chart_buy_zone": 76.0,
      "stop_loss": 72.0,
      "take_profit": 86.0,
      "opened": "2026-04-04",
      "entry_time": "09:00 Wien"
    }
  ],
  "closed": [
    {
      "id": "...",
      "outcome": "WIN",
      "exit": 86.0,
      "exit_price_9am": 86.50,
      "closed": "2026-04-10",
      "pnl_pct": 6.87
    }
  ]
}
```

### Initialer Stand (05.04.2026)

| Coin | Entry | SL | TP | Eroeffnet |
|------|------:|------:|------:|------:|
| SOL | $80.47 | $72.00 | $86.00 | 04.04. |
| XRP | $1.32 | $1.15 | $1.34 | 04.04. |
| LINK | $8.68 | $7.95 | $9.35 | 04.04. |

---

## 10. Score-History

### Konzept

Taeglich wird ein Snapshot aller Scores in `score-history.json` angehaengt. Das erlaubt:

- 30-Tage-Sparkline des Market Scores im Markt-Signal-Tab
- 14-Tage-Sparkline pro Coin in den Coin-Karten

### Datenstruktur `score-history.json`

```json
[
  {
    "date": "2026-04-05",
    "market": 46,
    "coins": {
      "SOL": 75,
      "XRP": 72,
      "LINK": 72,
      "ADA": 62,
      "ETH": 67,
      "SUI": 50,
      "TAO": 59,
      "ONDO": 58,
      "IOTA": 53
    }
  }
]
```

Maximale Eintraege: 90 (aeltere werden automatisch entfernt).

---

## 11. Live Formation & Level Analyse

Unten im Chart-Analyse-Tab, dynamisch je gewaehltem Coin und Zeitrahmen.

### Datenquelle

```
Binance REST API: letzte 100 1H/4H/1D-Kerzen
Verarbeitung: clientseitig im Browser via useLiveFormationAnalysis()
```

### Kerzenformationen (Staerke 0-10)

Erkannte Muster aus den letzten 1-3 Kerzen:

| Muster | Typ | Erkennungslogik |
|------|------|------|
| Doji | neutral | Koerper < 10% der Gesamtrange |
| Hammer | bullish | unterer Docht > 2x Koerper, kaum oberer Docht |
| Shooting Star | bearish | oberer Docht > 2x Koerper, kaum unterer Docht |
| Bullish Engulfing | bullish | aktuelle bullische Kerze umschliesst vorherige bearische |
| Bearish Engulfing | bearish | aktuelle bearische Kerze umschliesst vorherige bullische |
| Bullish/Bearish Marubozu | bullish/bearish | Koerper > 85% der Gesamtrange |
| Morning Star | bullish | 3-Kerzen-Umkehrmuster nach unten |
| Evening Star | bearish | 3-Kerzen-Umkehrmuster nach oben |

Staerke-Score: basiert auf Verhaeltnis Docht/Koerper oder Engulfing-Ratio.

### Support & Widerstand (Staerke 0-10)

```
Pivot-Hoch = Kerzen-Hoch liegt ueber den 2 benachbarten Kerzen → Resistance
Pivot-Tief = Kerzen-Tief liegt unter den 2 benachbarten Kerzen → Support

Staerke = touches * 1.8 + (1 - recency) * 3.5
  touches  = Anzahl Kerzen innerhalb 0.7% des Levels
  recency  = 0 (jungstes Level) bis 1 (aeltestes Level)

Deduplizierung: Level innerhalb 1% Abstand werden zusammengefasst
Anzeige: Top 6 nach Staerke, mit Anzahl Tests und S/R-Badge
```

### Trendlinien (Staerke 0-10)

```
Aufwaertstrend  = aufeinanderfolgende hoehere Tiefs in den letzten 30 Kerzen
Abwaertstrend   = aufeinanderfolgende niedrigere Hochs in den letzten 30 Kerzen
Staerke = Anzahl konsekutiver Punkte * 1.4 (max 10)
```

---

## 12. Automatisierung

### `update_data.py` — vollstaendiger Ablauf

```
1. Fear & Greed Index (Alternative.me)
2. BTC-Dominanz (CoinGecko Global)
3. Coin-Preise und 24h-Aenderungen (CoinGecko)
4. index.html aktualisieren (Datum, Preise)
5. Market Score und Coin-Scores aus index.html extrahieren
6. score-history.json aktualisieren (append)
7. Binance 09:00 Wien Kurse heute (fuer TP/SL-Pruefung)
8. Binance 09:00 Wien Kurse gestern (fuer neue Trade-Entries)
9. paper-trades.json aktualisieren (TP/SL pruefen + neue Trades oeffnen)
```

### Neue Funktionen in `update_data.py`

| Funktion | Zweck |
|------|------|
| `extract_market_score(html)` | Berechnet gewichteten Markt-Score aus `MARKET_SIGNAL_COMPONENTS` |
| `extract_coin_data(html)` | Liest ticker → score, signal aus `COIN_MODELS` |
| `extract_chart_setups(html)` | Liest ticker → stop, tp1, buy_zone aus `CHART_ANALYSIS_MODELS` |
| `update_score_history(score, coins, date)` | Haengt Tages-Snapshot an `score-history.json` an |
| `get_binance_9am_prices(day_offset)` | Holt Binance 1H-Kerze um 07:00 UTC fuer gestern/heute |
| `update_paper_trades(coin_data, setups, today, yesterday, date)` | Prueft TP/SL, oeffnet neue Trades |

### GitHub Actions

`.github/workflows/update.yml` fuehrt taeglich um `07:00 UTC` (= 09:00 Wien) aus.

```yaml
git add index.html score-history.json paper-trades.json
```

Alle drei Dateien werden bei Aenderung automatisch committed und gepusht.

---

## 13. Bekannte Einschraenkungen

### 1. Markt-Score bleibt manuell gepflegt

`update_data.py` schreibt Fear & Greed und BTC-Dominanz-Abruf nicht automatisch in die `MARKET_SIGNAL_COMPONENTS`-Werte zurueck. Der Market Score aendert sich also nur wenn die Werte manuell in `index.html` angepasst werden.

### 2. Texte koennen von berechneten Werten abweichen

Die Erklaertexte in `META.breakdownBars` sind statisch. Berechnete Scores koennen abweichen. Beispiel: Gruppe `On-Chain` berechnet `39`, Text nennt moeglicherweise einen anderen Wert.

### 3. Paper-Trades pruefen nur den 09:00-Wien-Snapshot

Der TP/SL-Check basiert ausschliesslich auf dem Binance-Kurs um 09:00 Wien. Intraday-Peaks (z.B. TP wurde kurz beruehrt, aber nicht um 09:00 gehalten) werden nicht erfasst.

### 4. Encoding-Artefakte in aelteren Dateien

Einige Dokumentationsdateien enthalten kaputte Umlaute. Die Logik in `index.html` ist davon nicht betroffen.

---

## 14. Empfohlene Einordnung

| Bereich | Stand |
|------|------|
| UI-Qualitaet | Ausgereift — Frosted-Glass, responsive, animiert |
| Scoring-Logik | Solide — Markt, Coin, Chance/Risiko konsistent implementiert |
| Chart-Analyse | Stark — echte Binance-Daten, EMAs, Muster, Formation-Scoring |
| Score-History | Laufend aufgebaut ab 05.04.2026 |
| Paper-Trading | Aktiv seit 04.04.2026, taegliche Auswertung via Binance 09:00 Wien |
| Datenpflege | Teilautomatisch — Preise und Datum automatisch, Scores und Texte manuell |

---

## 15. Changelog

### 5. April 2026

**Performance-Tab (neu)**
- Vierter Reiter in der Navigation
- KPI-Kacheln: offene Positionen, abgeschlossene Trades, Trefferquote, Ø P&L, Wins/Losses, bester Coin
- Offene-Positionen-Karte mit Distanz zu TP und SL
- Trade-Historie mit WIN/LOSS-Badge und P&L in %
- kumulierte P&L-Sparkline

**Score-History (neu)**
- `score-history.json` wird taeglich durch `update_data.py` befuellt
- 30-Tage-Sparkline des Market Scores im Markt-Signal-Tab
- 14-Tage-Sparkline pro Coin in den Coin-Karten
- `ScoreSparkline()`-Komponente als SVG-Inline-Chart

**Paper-Trading-Simulator (neu)**
- `paper-trades.json` speichert offene und geschlossene Trades
- Entry: Binance 1H-Kerzen-Open von gestern 09:00 Wien
- TP/SL-Pruefung: Binance 1H-Kerzen-Open von heute 09:00 Wien
- Initialer Stand: SOL $80.47 / XRP $1.32 / LINK $8.68 (alle 04.04.2026)
- `get_binance_9am_prices()`, `update_paper_trades()` in `update_data.py`

**Konfidenz-Badge (neu)**
- HOCH / MITTEL / NIEDRIG je Coin-Karte
- Berechnung via Standardabweichung der 6 Subscore-Endwerte
- `getCoinConfidence()` in `index.html`

**Live Formation & Level Analyse (neu)**
- im Chart-Analyse-Tab, unterhalb des Report-Blocks
- dynamisch je Coin und Zeitrahmen (1H / 4H / 1D)
- Kerzenformationen, Support/Resistance, Trendlinien mit Staerke-Score 0-10
- `StrengthBar()`-Komponente fuer visuelle Staerke-Anzeige
- `detectCandlePatterns()`, `detectSRLevels()`, `detectTrendLines()`, `useLiveFormationAnalysis()`

**GitHub Actions erweitert**
- `paper-trades.json` und `score-history.json` werden jetzt mit committed

---

*Zuletzt aktualisiert: 5. April 2026*

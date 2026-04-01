# Crypto Signal System
### Systemdokumentation · Reanalyse Stand 1. April 2026

> Projektart: Statisches Analyse-Dashboard fuer Krypto-Markt- und Coin-Bewertung
> Laufzeit: React 18 UMD + ReactDOM UMD + Babel Standalone direkt im Browser
> Aktiver Einstieg: `index.html`
> Hosting-Ziel: GitHub Pages
> Hinweis: Keine Finanzberatung

---

## 1. Zweck des Systems

Das Projekt ist ein statisches Research- und Analyse-Dashboard. Es trennt drei Ebenen sauber:

- Marktregime
- Coin-spezifische Bewertung
- technische Chartanalyse und Setup-Qualitaet
- Chance/Risiko-Verhaeltnis

Das System soll keine Preisziele vorhersagen, sondern ein nachvollziehbares Scoring liefern. Die Darstellung ist absichtlich erklaerbar aufgebaut: Marktkomponenten, Coin-Subscores, Quellenkontext und Herleitungen koennen direkt im UI aufgeklappt werden.

---

## 2. Tatsachlicher Projektbestand

### Kern-Dateien

| Datei | Rolle |
|------|------|
| `index.html` | Aktive Hauptdatei fuer GitHub Pages und aktuelle Laufzeit |
| `CryptoSignalSystem.html` | Aeltere, aehnlich aufgebaute HTML-Version mit abweichenden Datenstaenden |
| `crypto-signal-system-docs.md` | Diese ueberschreibende Systemdokumentation |
| `score-berechnungen.md` | Technische Formelbeschreibung des Scoring-Modells |
| `score-berechnungen-einfach.md` | Laienverstaendliche Beschreibung der Kennzahlen |
| `score-handbuch.md` | Sammeldokument fuer beide Score-Dokumente |

### Automatisierung und Hilfsdateien

| Datei | Rolle |
|------|------|
| `update_data.py` | Holt Fear & Greed, BTC-Dominanz und Coin-Preise und schreibt Werte in `index.html` |
| `.github/workflows/update.yml` | Geplanter taeglicher GitHub-Action-Run fuer `update_data.py` und Push nach `main` |
| `auto-push.bat` | Einfaches lokales `git push`-Hilfsskript |
| `check-babel.js` | Prueft JSX-Transpilierung lokal gegen den aktuellen `text/babel`-Block in `index.html` |
| `script-to-check.jsx` | JSX-Pruefdatei fuer `check-babel.js` |
| `babel-standalone.js` | Lokale Babel-Kopie fuer Syntaxchecks |
| `SKILL.md` | Lokale Arbeitsanweisungen fuer Frontend-Design |

### Sonstiges

- `.git/` ist vorhanden
- `.github/workflows/update.yml` ist der einzige Workflow im Repo

---

## 3. Aktiver Systemstand in `index.html`

`index.html` ist die relevante Datei fuer den aktuellen Produktstand. Die Datei enthaelt:

- komplettes HTML, CSS und React/JSX in einer einzigen Datei
- CDN-Einbindung von `react`, `react-dom` und `@babel/standalone`
- zusaetzlich CDN-Einbindung von `lightweight-charts` fuer den Pro-Chart
- Frosted-Glass-UI mit responsive Layout, Animationen und SVG-Gauges
- Datenmodell, Berechnungslogik und Rendering direkt im Browser
- neue Chartanalyse mit dokumentartigem Report-Aufbau, Pro-Chart und TradingView-Referenz

### Aktuelle Metadaten aus dem Code

- Datenstand in `META.date`: `31. Maerz 2026 · 19:17 Uhr`
- Markt-Score: `52/100`
- Markt-Verdict: `ABWARTEN`
- Chance: `2.2x`
- Risiko: `1.8x`
- Chance/Risiko-Verhaeltnis: `1.26:1`

### Aktuelle abgeleitete Coin-Scores

| Coin | Score | Signal | Preis |
|------|------:|--------|------:|
| SOL | 80 | AKKUMULIEREN | $80.50 |
| LINK | 79 | KAUFEN | $9.10 |
| XRP | 75 | KAUFEN | $1.34 |
| ADA | 73 | KAUFEN | $0.241 |
| ETH | 73 | KAUFEN | $2,050 |
| IOTA | 73 | KAUFEN | $0.055 |
| ONDO | 71 | KAUFEN | $0.270 |
| SUI | 67 | HALTEN | $0.96 |
| TAO | 67 | HALTEN | $350 |

### Aktuelle Breakdown-Gruppen

| Gruppe | Score |
|------|------:|
| Sentiment F&G | 88 |
| BTC Dominanz | 18 |
| On-Chain | 54 |
| Katalysatoren | 88 |
| Fed & Zinsen | 22 |
| Geopolitik | 18 |
| Inst. Flows | 68 |

### Aktueller Stand der Chartanalyse

- eigener Tab `Chart Analyse` fuer technische Setups pro Coin
- Reihenfolge der Hauptreiter: `Markt Signal` -> `Coin Analyse` -> `Chart Analyse`
- chart-spezifisches Datenmodell ueber `CHART_ANALYSES`
- Referenzchart via `TradingViewAdvancedChart`
- eigener Pro-Chart via `ProMarketChart`
- echte OHLC-Kerzen aus Binance-Klines je Intervall `1H`, `4H`, `1D`
- EMA20, EMA50 und EMA200 werden aus derselben Candle-Basis berechnet
- Stop, Support, Resistance und Take-Profit werden als horizontale Preislinien gerendert
- Candlestick-Muster werden aus echten Binance-Kerzen erkannt und bewertet
- beruecksichtigte Candle-Muster: `Doji`, `Hammer`, `Shooting Star / Inverted Hammer`, `Bullish/Bearish Engulfing`, `Morning Star`, `Evening Star`, `Piercing Pattern`, `Dark Cloud Cover`, `Bullish/Bearish Harami`
- Strukturformationen werden aus den letzten Kerzen erkannt und bewertet
- beruecksichtigte Formationen: `Bullisches Dreieck`, `Bearisches Dreieck`, `Falling Wedge`, `Rising Wedge`, `Aufwaertskanal`, `Abwaertskanal`, `Double Bottom`, `Double Top`
- Formationen und Candle-Muster werden direkt im Pro-Chart eingezeichnet
- wenn keine dominante Live-Formation erkannt wird, wird eine sichtbare Fallback-Formation aus dem Coin-Overlay gezeichnet
- coin-spezifische Preisformatierung, z. B. `IOTA` mit 4 Nachkommastellen
- Chartscore ist bewusst getrennt vom Coin-Gesamtscore

--- 

## 4. Architektur und Laufzeitmodell

### Frontend-Aufbau

Die Anwendung wird vollstaendig clientseitig ausgefuehrt:

1. Browser laedt HTML, CSS und CDN-Skripte
2. Babel transpiliert das JSX direkt im Browser
3. React rendert in `#root`
4. Ein Loading-Overlay wird vor dem finalen Render angezeigt

### Wichtige technische Merkmale

- kein Build-Tool
- kein bundler
- kein separates API-Backend
- keine persistente Datenbank
- Datenstand wird statisch in der HTML-Datei gehalten

### Wichtige Konstanten und Funktionen

- `META`
- `MARKET_SIGNAL_COMPONENTS`
- `MARKET_BREAKDOWN_GROUPS`
- `COIN_MODELS`
- `SOURCE_INFO`
- `clampScore()`
- `parsePriceValue()`
- `getWeightedScore()`
- `getMarketVerdict()`
- `buildMarketBreakdownBars()`
- `getMarketComponentScores()`
- `getChanceRiskProfile()`
- `getCoinSubScoreComponents()`
- `getWeightedMarketScore()`
- `getDynamicSubScore()`
- `getCoinSignal()`
- `buildAnalystExplanation()`
- `MiniGauge()`
- `Gauge()`
- `TradingViewAdvancedChart()`
- `ProMarketChart()`
- `mapChartIntervalToKlineInterval()`
- `calculateEMA()`
- `getChartPrecision()`
- `formatChartNumber()`
- `formatChartLevel()`
- `formatChartRange()`
- `getSetupMetrics()`
- `buildChartScenario()`
- `toPatternCandle()`
- `detectCandlestickPatterns()`
- `useCandlestickPatternAnalysis()`
- `detectStructurePatterns()`
- `buildFallbackStructurePattern()`
- `useStructurePatternAnalysis()`
- `ChartAnalysisReport()`
- `App()`

---

## 5. Marktmodell

Das Marktmodell besteht aus 12 gewichteten Komponenten auf einer 0-100-Skala.

### Komponenten und Gewichte

| Komponente | Gewicht | Stand in `index.html` |
|------|------:|------:|
| Fear & Greed Index | 15% | 88 |
| BTC Dominanz | 15% | 18 |
| Fed & Zinspolitik | 12% | 22 |
| Upgrade-Katalysatoren | 10% | 90 |
| Geopolitik / Kriege | 8% | 10 |
| Exchange Flows | 8% | 35 |
| Regulierung / ETFs | 7% | 85 |
| Institutionelle ETF Flows | 8% | 68 |
| Funding Rates | 5% | 60 |
| Globale Liquiditaet M2 | 4% | 35 |
| On-Chain Adressen | 4% | 68 |
| TVL Trend (DeFi) | 4% | 70 |

### Formel

```text
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

Der aktuelle Wert `52` fuehrt korrekt zu `ABWARTEN`.

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

Das Coin-Modell nimmt nicht einfach statische Subscores, sondern berechnet aus den Basiswerten dynamische Endscores:

```text
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

---

## 7. Chance/Risiko-Modell

Das Chance/Risiko-Modell ist von Markt- und Coin-Score getrennt.

### Upside

```text
upsideComposite =
  Fear & Greed 25
  Upgrade-Katalysatoren 25
  Institutionelle ETF Flows 25
  On-Chain Adressen 15
  Regulierung / ETFs 10
```

### Risiko

```text
downsidePressure =
  100 - BTC Dominanz       30
  100 - Fed & Zinspolitik  25
  100 - Geopolitik         25
  100 - Exchange Flows     20
```

### Umrechnung

```text
contrarianBoost = max(0, 55 - marketScore) / 100
upside = min/max-begrenztes Multiple aus upsideComposite + contrarianBoost
risk   = min/max-begrenztes Multiple aus downsidePressure
ratio  = upside / risk
```

### Aktueller Stand

- `upsideComposite = 80`
- `downsidePressure = 80`
- `upside = 2.2x`
- `risk = 1.8x`
- `ratio = 1.26:1`

---

## 8. UI-Struktur

### Globale Struktur

- Ladeoverlay
- Hero-Panel
- Tab-Navigation
- Tab `Markt Signal`
- Tab `Coin Analyse`
- Tab `Chart Analyse`

### Coin Analyse

- Markt-Signal-Header mit Kurzkommentar aus `META.aiReasoning`
- responsive Coin-Grid
- Zeilenweises Auf- und Zuklappen von Coin-Karten
- pro Coin 6 Subscore-Module
- pro Subscore:
  - einfache Erklaerung
  - Zusammensetzung
  - Rechenhinweis
  - Quellenzusammenfassung
- Analystenbegruendung pro Coin

### Chart Analyse

- dokumentartiger Report-Aufbau statt klassischem Dashboard
- kompakter Kopfbereich mit Coin-Auswahl und Intervall-Umschalter
- Marktbericht-Header mit Paar, Preis, 24h-Aenderung und Metadaten
- ein dominanter Hauptchart ueber `ProMarketChart`
- KPI-Zeile fuer Entry, Stop, TP1 und CRV
- echte Pattern-Ebene fuer Candlestick-Muster aus den letzten Binance-Kerzen
- echte Struktur-Ebene fuer Dreiecke, Wedges, Kanaele und Double Bottom / Top
- direkte Zeichnung von Candlestick-Mustern und Strukturformationen im Chart
- sichtbare Fallback-Formationslinien aus dem Coin-Setup, falls der Live-Scan keine dominante Formation findet
- textliche Sektionen fuer:
  - Charttechnische Bewertung
  - Setup-Empfehlung
  - Multi-Timeframe
  - Schluessellevel
  - Wahrscheinlichkeiten
  - Indikatoren & Szenarien
- zusaetzliche TradingView-Referenzansicht zum direkten Gegencheck des Pro-Charts
- technischer Score getrennt vom fundamentalen Coin-Score

### Markt Signal

- Score-Legende mit Handlungsanweisungen
- erklaerbare Einzelgewichte der Marktindikatoren
- Quellen- und Methodikblock
- Key Alerts
- grosser Markt-Gauge
- Chance/Risiko-Box mit Herleitung
- Analysten-Einschaetzung
- Breakdown-Balken

### Interaktionszustand in `App()`

- `openCoins`
- `openCoinSubScores`
- `openLegend`
- `openWeight`
- `openBreakdown`
- `openChanceRiskDetails`
- `tab`
- `coinGridColumns`
- `chartCoinIndex`
- `chartInterval`

Besonderheit: Coin-Karten oeffnen zeilenweise, nicht nur einzeln. Das wird ueber `toggleCoinRow()` und die berechnete Grid-Spaltenzahl gesteuert.

---

## 9. Datenquellen und Dokumentationslogik

`SOURCE_INFO` ordnet Marktbausteinen Quelle, Detail und Verwendungszweck zu. Im UI werden diese Informationen:

- global im Block "Quellen & Methodik" gezeigt
- lokal je Coin-Subscore erneut aggregiert ausgegeben

Quellkategorien im Code:

- Alternative.me
- CoinGecko
- CoinShares / ETF- und Fondsdaten
- Projektseiten / Release-Kommunikation
- Fed / Makro-Research
- Makro-News / Marktkommentar

Wichtig: Die Daten sind nicht live zur Laufzeit angebunden. Die Anwendung zeigt statisch eingetragene Werte und Erklaertexte an, die separat gepflegt oder per Skript aktualisiert werden.

---

## 10. Automatisierung

### `update_data.py`

Das Python-Skript aktualisiert nur einen Teil des Systems:

- `META.date`
- Coin-Preise und 24h-Aenderungen
- optional "Letzte Aktualisierung"-Text, falls vorhanden

Es nutzt:

- `https://api.alternative.me/fng/?limit=1`
- `https://api.coingecko.com/api/v3/global`
- `https://api.coingecko.com/api/v3/simple/price`

Wichtig: Das Skript berechnet keine neuen Marktkomponenten, keine neuen Coin-Basisscores und keine neuen Texte. Es ersetzt nur klar erkennbare String-Werte in `index.html`.

### GitHub Actions

`.github/workflows/update.yml` fuehrt taeglich um `07:00 UTC` aus. Der Kommentar im Workflow bezeichnet dies als `09:00 Uhr Wien`.

Der Job:

1. checkt das Repository aus
2. installiert Python 3.11
3. installiert `requests`
4. fuehrt `python update_data.py` aus
5. commitet `index.html` nur bei Aenderungen
6. pusht zurueck

---

## 11. Wichtige Abweichungen und Risiken

### 1. `index.html` und `CryptoSignalSystem.html` sind nicht synchron

Die Dateien haben gleiche Struktur, aber klar unterschiedliche Datenstaende, Datumswerte, Coin-Daten und Kommentare. `index.html` ist der aktuelle Referenzstand. `CryptoSignalSystem.html` sollte als Altversion betrachtet werden, solange keine bewusste Synchronisation erfolgt.

### 2. Die Dokumentation war veraltet

Die bisherige Doku beschrieb mehrere Werte nicht mehr korrekt. Beispiel:

- alte Coin-Rangfolge stimmte nicht mehr mit den berechneten Endwerten in `index.html` ueberein
- die Automatisierung wurde zu pauschal beschrieben
- der Dateiname war teils falsch geschrieben

### 3. Harte Textwerte und berechnete Scores koennen auseinanderlaufen

Die Breakdown-Balken werden teilweise neu aus `MARKET_SIGNAL_COMPONENTS` berechnet, waehrend die zugehoerigen Erklaertexte in `META.breakdownBars` statische Aussagen enthalten. Dadurch gibt es bereits Abweichungen, zum Beispiel:

- Gruppe `On-Chain` berechnet `54`, Text nennt `58`
- Gruppe `Geopolitik` berechnet `18`, Text spricht an einer Stelle von `Score 10`

Das ist ein inhaltliches Wartungsrisiko.

### 4. `update_data.py` aktualisiert weniger als der Workflow-Kommentar erwarten laesst

Das Skript holt zwar Fear & Greed und BTC-Dominanz, schreibt diese beiden Werte aber derzeit nicht in die Marktkomponenten zurueck. Der eigentliche Markt-Score bleibt damit weiterhin manuell gepflegt.

### 5. Chartanalyse ist funktional stark erweitert, aber weiter ein Feinschliff-Bereich

Die Chartanalyse wurde stark erweitert und arbeitet inzwischen nicht nur mit statischen Setup-Texten, sondern mit echten Binance-Kerzen, Candle-Muster-Erkennung, Strukturformationen und sichtbaren Chart-Markierungen. Der Bereich ist damit fachlich deutlich naeher an einer echten technischen Analyse, bleibt aber ein Feinschliff-Bereich fuer weitere visuelle Priorisierung, Signalgewichtung und Referenzgenauigkeit.

### 6. Encoding-Artefakte

Mehrere Dateien enthalten kaputte Umlaute oder Symbolartefakte aus Zeichensatz-Konflikten. Die Logik funktioniert davon unabhaengig, die Lesbarkeit leidet aber sichtbar.

---

## 12. Empfohlene Einordnung des Systems

Der aktuelle Projektzustand ist funktional, aber hybrid:

- die UI ist fuer ein statisches Single-File-Dashboard bereits weit ausgebaut
- die neue Chartanalyse hebt das System ueber ein reines Score-Dashboard hinaus
- die mathematische Logik fuer Markt, Coins und Chance/Risiko ist im Code konsistent implementiert
- die technische Chartlogik arbeitet jetzt zusaetzlich mit echten Binance-Candles, lokal berechneten EMAs, Candlestick-Mustern und Strukturformationen
- die Datenpflege ist nur teilweise automatisiert
- Texte, Zahlen und Parallelversionen koennen auseinanderlaufen

Praktisch bedeutet das:

- `index.html` ist die operative Wahrheit
- `CryptoSignalSystem.html` ist momentan eine Neben- bzw. Altversion
- `update_data.py` ist ein Teilautomationsskript, keine vollstaendige Datenpipeline
- die Doku muss sich an den berechneten Werten aus `index.html` orientieren, nicht an historischen Texten

---

## 13. Fazit

Das Crypto Signal System ist aktuell ein erklaerbares, statisches Analyse-Dashboard mit relativ ausgereifter Frontend-Praesentation und solider Scoring-Logik. Die groessten offenen Punkte liegen nicht im UI, sondern in der Datenpflege:

- fehlende Vollsynchronisation der HTML-Varianten
- nur partielle Auto-Aktualisierung
- statische Erklaertexte mit Drift-Risiko
- sichtbare Encoding-Altlasten

Neu hinzugekommen ist eine eigene Chartanalyse-Schicht mit getrenntem technischem Score, echtem Pro-Candlestick-Chart auf Binance-Basis und TradingView-Referenz zum Abgleich. Die Chartanalyse bewertet inzwischen nicht nur Markt und Coin-Qualitaet, sondern auch das konkrete technische Setup je Asset inklusive Candlestick-Mustern, Strukturformationen und direkt eingezeichneter Leitlinien im Chart.

Als Systemdokumentation gilt ab jetzt:

- `index.html` hat Vorrang vor `CryptoSignalSystem.html`
- berechnete Endwerte haben Vorrang vor hart eingetragenen Beschreibungstexten
- Automatisierung ist vorhanden, aber nur teilweise vollstaendig

---

*Zuletzt vollstaendig neu analysiert und dokumentiert: 1. April 2026*

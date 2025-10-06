# Bot de tranzacționare MetaTrader 5

## Descriere

Acest proiect conține un sistem complet de tranzacționare automată pentru MetaTrader 5, scris în Python. Sistemul include botul principal pentru tranzacționare automată, instrumente de diagnostic și verificări rapide pre-trading.

**ATENȚIE:** Acest bot este destinat exclusiv pentru învățare și testare. Folosiți întotdeauna conturi DEMO pentru testare și înțelegeți riscurile tranzacționării automate.

---

## Instalare

### Cerințe preliminare

- MetaTrader 5 — descărcat de pe site-ul oficial al brokerului sau al MetaQuotes.
- Python 3.7+ — descărcat de pe python.org.
- Cont DEMO — înregistrare la un broker care oferă cont demo MT5.

### Configurare MetaTrader 5

1. Deschideți MetaTrader 5 și conectați-vă la contul DEMO.
2. Activați Automated Trading:
   - Click dreapta în orice grafic → Expert Advisors → Allow Automated Trading
   - Butonul Auto Trading trebuie să fie verde
3. Adăugați simbolul în Market Watch:
   - Apăsați Ctrl+M pentru fereastra Market Watch
   - Click dreapta → Symbols → căutați EURUSD → bifați → Show

### Instalare pachete Python

Instalați pachetele necesare:

pip install MetaTrader5 pandas numpy

---

## Utilizare

### Verificări rapide

Rulați verificările rapide înainte de rulare:

python checks.py

### Diagnostic complet

Pentru diagnostic complet:

python diagnostic.py

### Testare strategii pe date istorice

Rulați backtest-urile cu:

python run_backtest.py

### Pornire bot tranzacționare

Pornire bot:

python bot_mt5.py

---

## Fișiere proiect

- `bot_mt5.py` — Botul principal pentru tranzacționare live
- `backtesting_engine.py` — Sistem de testare strategii pe date istorice
- `run_backtest.py` — Script pentru rularea testelor
- `diagnostic.py` — Instrument de diagnosticare probleme
- `checks.py` — Verificări rapide pre-trading
- `strategies/` — Director cu strategii de tranzacționare
- `results/` — Rezultate testare (generate automat)

---

## Configurare strategii

### Strategii incluse

- **EMAStrategy** — Strategie bazată pe crossover între medii mobile exponentiale
- **RSIStrategy** — Strategie bazată pe indicatorul RSI

### Adăugare strategie nouă

1. Creați un fișier nou în folderul `strategies/`.
2. Definiți o clasă cu metoda `generate_signals`.
3. Modificați configurația din `bot_mt5.py` pentru a selecta noua strategie.

### Exemplu configurație

În `bot_mt5.py` modificați valorile:

STRATEGY_MODULE = "nume_fisier_strategie"
STRATEGY_CLASS = "NumeClasaStrategie"
STRATEGY_PARAMS = parametrii_strategiei

---

## Management risc

Setările de management al riscului se găsesc în `bot_mt5.py`:

- STOP_LOSS_TICKS — Număr de ticks pentru Stop Loss
- TAKE_PROFIT_TICKS — Număr de ticks pentru Take Profit
- LOT_SIZE — Dimensiunea lotului de tranzacționare
- TRADING_START_HOUR — Ora de începere tranzacționare
- TRADING_END_HOUR — Ora de încheiere tranzacționare

---

## Depanare

### Probleme frecvente

- **Eroare "Failed to initialize MT5"** — Verificați că MT5 este deschis și contul este conectat.
- **Eroare "No module named"** — Verificați că fișierul strategiei există în folderul `strategies/`.
- **Eroare 10027 "Trade context busy"** — Așteptați câteva secunde; botul reîncearcă automat.

### Flux recomandat

1. Rulați `python checks.py` pentru verificări inițiale.
2. Testați strategiile cu `python run_backtest.py`.
3. Alegeți strategia cu cele mai bune rezultate.
4. Configurați strategia în `bot_mt5.py`.
5. Rulați `python bot_mt5.py` pe cont DEMO.

---

## Securitate

- Folosiți doar cont DEMO pentru testare.
- Testați cu volume mici (ex.: 0.01 lot).
- Monitorizați primele rulări ale botului.
- Înțelegeți riscurile tranzacționării automate.
- Faceți backup la cod înainte de modificări.

---

## Dezvoltare

Proiectul acceptă contribuții pentru:

- Noi strategii de tranzacționare
- Îmbunătățiri la sistemul de backtesting
- Instrumente de monitoring și raportare
- Documentație îmbunătățită

---

## Suport

Pentru probleme sau întrebări:

- Consultați această documentație.
- Rulați `python diagnostic.py` pentru informații detaliate.
- Asigurați-vă că toate cerințele sunt îndeplinite.

---

**Notă:** Succesul în tranzacționare necesită învățare continuă și management al riscului.


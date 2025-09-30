# bot_mt5

## Bot de tranzacționare MetaTrader 5

### Descriere

Acest proiect conține un sistem complet de tranzacționare automată pentru MetaTrader 5, scris în Python. Sistemul include:
- botul principal pentru tranzacționare automată
- instrumente de diagnostic
- verificări rapide (pre-trading)

ATENȚIE: Acest bot este destinat exclusiv pentru învățare și testare. Folosiți întotdeauna conturi DEMO pentru testare și înțelegeți riscurile tranzacționării automate.

---

## Instalare

### Cerințe preliminare

- MetaTrader 5 — descărcat de pe site-ul oficial al brokerului sau al MetaQuotes
- Python 3.7+ — descărcat de pe python.org
- Cont DEMO — înregistrare la un broker care oferă cont demo MT5

### Configurare MetaTrader 5

1. Deschideți MetaTrader 5 și conectați-vă la contul DEMO.
2. Activați Automated Trading:
   - Click dreapta în orice grafic → Expert Advisors → Allow Automated Trading
   - Butonul Auto Trading trebuie să fie verde
3. Adăugați simbolul în Market Watch:
   - Apăsați Ctrl+M pentru fereastra Market Watch
   - Click dreapta → Symbols → căutați USDJPY → bifați → Show

### Instalare pachete Python

Instalați pachetele necesare cu managerul de pachete preferat (ex.: pip install MetaTrader5 pandas)

### Descarcare proiect

- git clone [URL-ul repository-ului]
- cd MT5-Trading-Bot

---

## Fișiere principale

- bot_mt5.py — botul principal de tranzacționare (strategia EMA)
- diagnostic.py — script de diagnostic detaliat pentru depanare
- checks.py — script pentru verificări rapide pre-trading

---

## Utilizare

### Verificări inițiale

Rulați verificările rapide înainte de orice rulare:

python checks.py

După rulare, ar trebui să vedeți toate verificările marcate cu ✅.

### Diagnostic (opțional)

Pentru un diagnostic complet:

python diagnostic.py

### Pornire bot principal

Pornire:

python bot_mt5.py

---

## Botul principal (bot_mt5.py)

### Strategie

Botul folosește o strategie EMA (Exponential Moving Average):

- EMA cu perioada 14 pe timeframe M1 (1 minut)
- Se cumpără când prețul Bid este peste EMA
- Se vinde când prețul Bid este sub EMA
- Stop Loss: 10 ticks
- Take Profit: 20 ticks
- Limită: maximum 1 tranzacție pe minut

### Setări configurabile

În fișierul bot_mt5.py puteți modifica:

- SYMBOL = "USDJPY" — perechea valutară
- LOT_SIZE = 0.01 — dimensiunea lotului
- STOP_LOSS_TICKS = 10 — Stop Loss în ticks
- TAKE_PROFIT_TICKS = 20 — Take Profit în ticks
- TRADING_START_HOUR = 0 — ora de start
- TRADING_END_HOUR = 23 — ora de sfârșit
- TIMEOUT_MINUTES = 30 — durata rulare (minute)
- EMA_PERIOD = 14 — perioada EMA
- TIMEFRAME = mt5.TIMEFRAME_M1 — timeframe-ul

---

## diagnostic.py — instrument de depanare

### Când să folosiți

- La prima configurare
- Când apar erori neașteptate
- După update-uri MT5
- Când conexiunea nu funcționează

### Utilizare

python diagnostic.py

---

## checks.py — verificări rapide

### Când să folosiți

- Înainte de fiecare rulare a botului
- La pornirea zilnică a sistemului
- Pentru verificări rapide

### Verificări efectuate

- MT5 deschis și cont logat
- Buton Auto Trading activat
- Simbol adăugat în Market Watch
- Conexiune internet stabilă
- Cont demo (nu real)
- Fonduri suficiente
- Fără alte Expert Advisors activi

---

## Depanare

### Probleme comune & soluții

- "Failed to initialize MT5"
  - Cauze: MT5 nu este deschis sau contul nu este logat
  - Soluție: Deschideți MT5 și rulați python checks.py

- Eroare 10027 — "Trade context busy"
  - Soluție: Botul reîncearcă automat; așteptați 5–10 secunde

- Eroare 10030 — "Unsupported filling mode"
  - Soluție: Folosiți scripturile actualizate

- "No tick data available"
  - Soluție: Verificați dacă simbolul este în Market Watch

### Flux de depanare recomandat

1. Rulați python checks.py
2. Dacă există probleme, rulați python diagnostic.py
3. Rezolvați problemele identificate
4. Rulați din nou python checks.py
5. Porniți botul principal cu python bot_mt5.py

---

## Avertismente de securitate

- FOLOSIȚI DOAR CONT DEMO pentru testare
- TESTAȚI CU VOLUME MICI (ex.: 0.01 lot)
- MONITORIZAȚI primele rulări ale botului
- ÎNȚELEGEȚI RISCURILE tranzacționării automate
- FACEȚI BACKUP la cod înainte de modificări
- NU FOLOSIȚI BANII NECESARI PENTRU TRAIUL ZILNIC

---

## Mentenanță

### Verificări periodice

- Actualizați MetaTrader 5 la versiunea cea mai recentă
- Rulați python checks.py înainte de rulări importante
- Verificați fișierele de log pentru erori neașteptate
- Actualizați pachetele Python

---

## Performanță și monitorizare

- Verificați fișierele de log generate de bot
- Monitorizați contul în MT5 pentru tranzacții (ferestrele "Trade" și "History")
- Verificați tab-ul "Experts" din jurnalul MT5 pentru erori

---

## Suport

Dacă întâmpinați probleme:

- Consultați mai întâi această documentație
- Folosiți diagnostic.py pentru identificarea problemelor
- Asigurați-vă că toți pașii de instalare și configurare au fost respectați

---

## Pași recomandați

- Testați pe cont DEMO timp de cel puțin 1 săptămână
- Analizați performanța și ajustați parametrii
- Personalizați strategia după preferințe
- Automatizați rularea cu un task scheduler (de ex. cron sau Task Scheduler) și monitorizați periodic


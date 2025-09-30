# bot_mt5

🤖 Bot de Tranzacționare MetaTrader 5
<div align="center">
https://img.shields.io/badge/Python-3.7+-blue.svg
https://img.shields.io/badge/Platform-MetaTrader%25205-orange.svg
https://img.shields.io/badge/Automated-Trading-brightgreen.svg

Sistem complet de tranzacționare automată pentru MetaTrader 5

Descriere • Instalare • Utilizare • Fișiere • Configurare • Depanare

</div>
📖 Descriere

Acest proiect conține un sistem complet de tranzacționare automată pentru MetaTrader 5, scris în Python. Sistemul include:

🤖 Bot principal cu strategie EMA pentru tranzacționare automată

🔍 Instrumente de diagnostic pentru depanare aprofundată

✅ Verificări rapide pentru validarea rapidă a sistemului

⚙️ Configurare flexibilă pentru diferite strategii și perechi valutare

⚠️ IMPORTANT: Acest bot este destinat pentru învățare și testare. Folosiți întotdeauna conturi DEMO pentru testare și înțelegeți riscurile tranzacționării automate.

🚀 Instalare Rapidă
Cerințe Preliminare
MetaTrader 5 - Descarcă de aici

Python 3.7+ - Descarcă de aici

Cont DEMO - Înregistrează-te la un broker care oferă cont demo MT5

Configurare MetaTrader 5
Deschide MetaTrader 5 și loghează-te pe contul DEMO

Activează Trading Automat:

Click dreapta în orice grafic → Expert Advisors → ✅ Allow Automated Trading

Butonul "Auto Trading" trebuie să fie VERDE

Adaugă simbolul în Market Watch:

Apasă Ctrl+M pentru fereastra Market Watch

Click dreapta → Symbols → Caută USDJPY → Bifează → Show

Instalare Python Packages
bash
# Instalează pachetele necesare
pip install MetaTrader5 pandas
Descarcă Proiectul
bash
# Clonează repository-ul sau descarcă fișierele manual
git clone [URL_REPOSITORY]

cd MT5-Trading-Bot

📁 Structura Proiectului

MT5-Trading-Bot/

├── 🤖 bot_mt5.py          # Botul principal de tranzacționare

├── 🔍 diagnostic.py       # Diagnostic detaliat al sistemului

├── ✅ checks.py           # Verificări rapide pre-trading

└── 📚 README.md           # Această documentație
🎯 Utilizare
Pasul 1: Verificări Inițiale
bash
# Verificare rapidă a sistemului (10 secunde)
python checks.py
Așteaptă să vezi:

text
📋 LISTĂ DE VERIFICĂRI:
   ✅ MT5 deschis și cont logat
   ✅ Buton Auto Trading activat
   ✅ Simbol în Market Watch
   ✅ Conexiune internet stabilă
   ✅ Cont demo (nu real) pentru teste
   ✅ Fonduri suficiente
   ✅ Alt EA nu rulează
Pasul 2: Diagnostic Complet (Opțional)
bash
# Diagnostic detaliat pentru probleme complexe
python diagnostic.py
Pasul 3: Pornește Botul
bash
# Rulează botul principal
python bot_mt5.py
🤖 Botul Principal (bot_mt5.py)
Strategia Implementată
Botul folosește o strategie EMA (Exponential Moving Average):

EMA 14 pe timeframe M1 (1 minut)

Cumpără când prețul Bid este PESTE EMA

Vinde când prețul Bid este SUB EMA

Stop Loss: 10 ticks | Take Profit: 20 ticks

Limită: 1 tranzacție pe minut pentru a evita overtrading

Setări Configurabile
python
# În bot_mt5.py poți modifica:
SYMBOL = "USDJPY"                  # Perechea valutară
LOT_SIZE = 0.01                    # Dimensiunea lotului (0.01 = 1,000 unități)
STOP_LOSS_TICKS = 10               # Stop Loss în ticks
TAKE_PROFIT_TICKS = 20             # Take Profit în ticks
TRADING_START_HOUR = 0             # Ora de start (0 = miezul nopții)
TRADING_END_HOUR = 23              # Ora de sfârșit (23 = 11 PM)
TIMEOUT_MINUTES = 30               # Durată maximă de rulare
EMA_PERIOD = 14                    # Perioada EMA
TIMEFRAME = mt5.TIMEFRAME_M1       # Timeframe-ul de analiză
Exemplu de Output
text
🤖 BOT MT5 PORNIT - STRATEGIE EMA
==================================================
✅ MT5 inițializat cu succes!
📊 [14:23:20] Bid: 147.868, EMA: 147.855
🎯 Condiție CUMPĂRARE: Bid 147.868 > EMA 147.855
✅ ✅ ORDIN REUȘIT! Ticket: 53460019976
📈 Ordin de cumpărare #1 plasat cu succes!
⏳ Aștept 55s până la următorul trade...
🔍 Diagnostic.py - Instrument de Depanare
Când să folosești Diagnostic.py
🔧 La prima configurare

🐛 Când apar erori neașteptate

🔄 După update-uri MT5

📡 Când conexiunea nu funcționează

Ce verifică
bash
python diagnostic.py
Output așteptat:

text
🔍 DIAGNOSTIC COMPLET MT5
============================================================
1. 🔄 Inițializare MT5... ✅
2. 💻 Informații terminal... ✅  
3. 👤 Informații cont... ✅
4. 📈 Verific simbolul USDJPY... ✅
5. ⏰ Verific date tick... ✅
6. 🔐 Verific permisiuni trading... ✅
7. 🧪 Test ordin simplu... ✅ ✅ ✅ ORDIN TEST REUȘIT!
✅ Checks.py - Verificări Rapide
Când să folosești Checks.py
🚀 Înainte de fiecare rulare a botului

📅 La pornirea zilnică a sistemului

⚡ Pentru verificări rapide de sănătate

Verificări efectuate
✅ MT5 deschis și cont logat

✅ Buton Auto Trading activat

✅ Simbol în Market Watch

✅ Conexiune internet stabilă

✅ Cont demo (nu real)

✅ Fonduri suficiente

✅ Fără alte Expert Advisors activi

⚙️ Personalizare Avansată
Schimbă Perechea Valutară
python
# În bot_mt5.py
SYMBOL = "EURUSD"  # Schimbă în orice alt simbol disponibil
Modifică Strategia
python
# În funcția principală din bot_mt5.py, poți modifica condiția:

# Exemplu: Cumpără doar dacă prețul este cu 0.1% peste EMA
if tick.bid > ema * 1.001:
    place_order(mt5.ORDER_TYPE_BUY, STOP_LOSS_TICKS, TAKE_PROFIT_TICKS)

# Exemplu: Vinde doar dacă prețul este cu 0.1% sub EMA  
elif tick.bid < ema * 0.999:
    place_order(mt5.ORDER_TYPE_SELL, STOP_LOSS_TICKS, TAKE_PROFIT_TICKS)
Timeframe-uri Disponibile
python
TIMEFRAME = mt5.TIMEFRAME_M1    # 1 minut
TIMEFRAME = mt5.TIMEFRAME_M5    # 5 minute
TIMEFRAME = mt5.TIMEFRAME_M15   # 15 minute
TIMEFRAME = mt5.TIMEFRAME_H1    # 1 oră
TIMEFRAME = mt5.TIMEFRAME_H4    # 4 ore
🛠 Depanare
Probleme Comune și Soluții
❌ "Failed to initialize MT5"
Cauze:

MT5 nu este deschis

Contul nu este logat

Probleme de permisiuni

Soluții:

Deschide MetaTrader 5 și loghează-te

Rulează python checks.py pentru verificare

Dacă persistă, rulează python diagnostic.py pentru detalii

❌ Eroare 10027 - "Trade context busy"
Soluție: Botul se reîncearcă automat. Așteaptă 5-10 secunde.

❌ Eroare 10030 - "Unsupported filling mode"
Soluție: Folosește scripturile actualizate care elimină type_filling.

❌ "No tick data available"
Soluție:

Verifică dacă simbolul este în Market Watch

Așteaptă conexiunea la piață

Rulează python checks.py

❌ Butonul "Auto Trading" nu devine verde
Soluție:

Click dreapta în grafic → Expert Advisors → Allow Automated Trading

Restartează MT5

Verifică dacă antivirusul blochează MT5

Flux de Depanare Recomandat
Verifică rapid cu python checks.py

Dacă există probleme, rulează python diagnostic.py

Rezolvă problemele identificate

Rulează din nou python checks.py pentru confirmare

Pornește botul principal cu python bot_mt5.py

⚠️ Avertismente de Securitate
⚠️ FOLOSEȘTE DOAR CONT DEMO pentru testare

⚠️ TESTEAZĂ CU VOLUME MICI (0.01 lot)

⚠️ MONITORIZEAZĂ primele rulări ale botului

⚠️ ÎNȚELEGE RISCURILE tranzacționării automate

⚠️ FAȚI BACKUP la cod înainte de modificări

⚠️ NU FOLOSI BANII NECESARI pentru traiul zilnic

🔄 Mentenanță și Actualizări
Verificări Periodice
✅ Actualizează MetaTrader 5 la versiunea latest

✅ Rulează python checks.py înainte de rulări importante

✅ Verifică logs pentru erori neașteptate

✅ Actualizează pachetele Python (pip install --upgrade MetaTrader5 pandas)

Upgrade la Versiuni Viitoare
Când actualizezi scripturile:

Salvează configurațiile personalizate

Compară fișierele vechi cu cele noi

Testează pe cont DEMO înainte de a folosi versiunea nouă

Actualizează documentația dacă este necesar

📞 Suport și Contribuții
Dacă întâmpinați probleme sau aveți sugestii:

Verificați această documentație mai întâi

Folosiți diagnostic.py pentru a identifica problemele

Asigurați-vă că toți pașii de instalare sunt respectați

📊 Performanță și Monitorizare
Pentru a monitoriza performanța botului:

Verificați fișierele de log generate de bot

Monitorizați contul în MT5 pentru tranzacții

Folosiți ferestrele "Trade" și "History" din MT5

Verificați tab-ul "Experts" din jurnalul MT5 pentru erori

🎉 Felicitări!
Acum ai un sistem complet de tranzacționare automată pentru MetaTrader 5.

Următorii pași recomandați:

🧪 Testează pe cont DEMO timp de cel puțin 1 săptămână

📊 Analizează performanța și ajustează parametrii

🔧 Personalizează strategia după preferințe

⚡ Automatizează rularea cu task scheduler

<div align="center">
💡 Remember: Successful trading requires continuous learning and risk management!

</div>

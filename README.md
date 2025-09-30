# bot_mt5

Bot de Tranzacționare MetaTrader 5
Descriere
Acest proiect contine un sistem complet de tranzactionare automata pentru MetaTrader 5, scris în Python. Sistemul include bot principal pentru tranzactionare automata, instrumente de diagnostic si verificari rapide.

ATENTIE: Acest bot este destinat pentru învatare si testare. Folositi întotdeauna conturi DEMO pentru testare si înțelegeți riscurile tranzactionarii automate.

Instalare
Cerinte Preliminare
MetaTrader 5 - Descarcat de pe site-ul oficial

Python 3.7+ - Descarcat de pe python.org

Cont DEMO - Înregistrare la un broker care oferă cont demo MT5

Configurare MetaTrader 5
Deschideți MetaTrader 5 si logati-va pe contul DEMO

Activati Trading Automat:

Click dreapta în orice grafic -> Expert Advisors -> Allow Automated Trading

Butonul "Auto Trading" trebuie sa fie verde

Adaugati simbolul în Market Watch:

Apasati Ctrl+M pentru fereastra Market Watch

Click dreapta -> Symbols -> Cautati USDJPY -> Bifati -> Show

Instalare Pachete Python: pip install MetaTrader5 pandas

Descarcare Proiect: git clone [URL-ul repository-ului]
                    cd MT5-Trading-Bot

Fisiere Proiect
bot_mt5.py - Botul principal de tranzactionare cu strategie EMA

diagnostic.py - Script de diagnostic detaliat pentru depanare

checks.py - Script pentru verificari rapide pre-trading

Utilizare
Verificari Initiale: python checks.py

Dupa rulare, trebuie sa vedeti toate verificările cu bifa verde (✅).

Diagnostic Complet (Optional): python diagnostic.py

Pornire Bot Principal: python bot_mt5.py

Botul Principal (bot_mt5.py)
Strategie
Botul foloseste o strategie EMA (Exponential Moving Average):

EMA 14 pe timeframe M1 (1 minut)

Cumpara cand pretul Bid este PESTE EMA

Vinde cand pretul Bid este SUB EMA

Stop Loss: 10 ticks | Take Profit: 20 ticks

Limita: 1 tranzactie pe minut

Setari Configurabile
In fisierul bot_mt5.py puteti modifica:
   SYMBOL = "USDJPY"                  # Perechea valutară
   LOT_SIZE = 0.01                    # Dimensiunea lotului
   STOP_LOSS_TICKS = 10               # Stop Loss în ticks
   TAKE_PROFIT_TICKS = 20             # Take Profit în ticks
   TRADING_START_HOUR = 0             # Ora de start
   TRADING_END_HOUR = 23              # Ora de sfârșit
   TIMEOUT_MINUTES = 30               # Durata rulare
   EMA_PERIOD = 14                    # Perioada EMA
   TIMEFRAME = mt5.TIMEFRAME_M1       # Timeframe-ul

Diagnostic.py - Instrument Depanare
Cand sa folositi
La prima configurare

Cand apar erori neasteptate

Dupa update-uri MT5

Cand conexiunea nu functioneaza

Utilizare: python diagnostic.py

Diagnostic.py - Instrument Depanare
Cand sa folositi
La prima configurare

Cand apar erori neasteptate

Dupa update-uri MT5

Cand conexiunea nu functioneaza

Checks.py - Verificari Rapide
Cand sa folositi
Înainte de fiecare rulare a botului

La pornirea zilnica a sistemului

Pentru verificari rapide

Verificari efectuate
MT5 deschis si cont logat

Buton Auto Trading activat

Simbol în Market Watch

Conexiune internet stabila

Cont demo (nu real)

Fonduri suficiente

Fara alte Expert Advisors activi
Depanare
Probleme Comune
"Failed to initialize MT5"

Cauze: MT5 nu este deschis, contul nu este logat

Solutii: Deschideti MT5, rulati python checks.py

Eroare 10027 - "Trade context busy"

Solutie: Botul se reîncearca automat. Asteptati 5-10 secunde.

Eroare 10030 - "Unsupported filling mode"

Solutie: Folositi scripturile actualizate

"No tick data available"

Solutie: Verificati daca simbolul este în Market Watch

Flux Depanare Recomandat
Rulati python checks.py

Daca exista probleme, rulati python diagnostic.py

Rezolvati problemele identificate

Rulati din nou python checks.py

Porniti botul principal cu python bot_mt5.py

Avertizari Securitate
FOLOSITI DOAR CONT DEMO pentru testare

TESTATI CU VOLUME MICI (0.01 lot)

MONITORIZATI primele rulari ale botului

ÎNȚELECETI RISCURILE tranzactionarii automate

FACETI BACKUP la cod înainte de modificari

NU FOLOSITI BANII necesari pentru traiul zilnic

Mentenanta
Verificari Periodice
Actualizati MetaTrader 5 la versiunea latest

Rulati python checks.py înainte de rulari importante

Verificati logs pentru erori neasteptate

Actualizati pachetele Python

Suport
Daca întâmpinati probleme:

Verificati aceasta documentatie mai întâi

Folositi diagnostic.py pentru a identifica problemele

Asigurati-va ca toti pasii de instalare sunt respectati

Performanta si Monitorizare
Pentru a monitoriza performanta botului:

Verificati fisierele de log generate de bot

Monitorizati contul în MT5 pentru tranzactii

Folositi ferestrele "Trade" si "History" din MT5

Verificati tab-ul "Experts" din jurnalul MT5 pentru erori

Urmatorii Pasi Recomandati
Testati pe cont DEMO timp de cel putin 1 saptamâna

Analizati performanta si ajustati parametrii

Personalizati strategia dupa preferinte

Automatizati rularea cu task scheduler

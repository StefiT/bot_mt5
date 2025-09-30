# bot_mt5
Automated trading bot for MetaTrader 5

Explicații Bot de Tranzacționare MetaTrader 5
📌 Descriere Generală
Acest bot execută tranzacții automate pe perechea valutară USDJPY folosind MetaTrader 5. El rulează continuu pentru o perioadă prestabilită (30 de minute implicit), verificând condiții simple de tranzacționare în intervalul orar specificat.

⚙️ Setări de Configurare
Variabile Globale:
SYMBOL: Instrumentul financiar (USDJPY)

LOT_SIZE: Volumul tranzacției (0.1 = 10.000 unități)

STOP_LOSS_TICKS: Pierdere maximă în ticks (10 ticks)

TAKE_PROFIT_TICKS: Profit țintă în ticks (20 ticks)

TRADING_START_HOUR & TRADING_END_HOUR: Intervalul orar de tranzacționare (0-23)

TIMEOUT_MINUTES: Durata de funcționare a botului (0.5 = 30 minute)

🔧 Funcționalități Principale
1. Funcția place_order
Plasează ordine de cumpărare/vânzare cu stop-loss și take-profit automate.

Parametrii:

action_type: Tipul ordinului (BUY/SELL)

stop_loss_ticks: Distanța SL în ticks

take_profit_ticks: Distanța TP în ticks

Procesul:

Verifică disponibilitatea simbolului

Preia prețul curent (Bid/Ask)

Calculează SL și TP bazat pe ticks

Trimite ordinul către serverul MT5

2. Funcția main
Controlează fluxul principal al botului:

Conexiune:

Inițializează conexiunea cu MT5

Setează timer-ul de timeout (30 minute)

Loop-ul de Tranzacționare:

Verifică dacă este în intervalul orar setat

Preia datele tick curente

Verifică condiția de tranzacționare (test simplu: Bid < Ask)

Plasează ordin de Cumpărare dacă condiția este îndeplinită

Așteaptă 5 secunde între verificări

🚨 Condiții de Tranzacționare
⚠️ ATENȚIE: Botul folosește în prezent o condiție PUR TESTARE care este aproape întotdeauna adevărată:

python
if tick.bid < tick.ask:  # Mereu adevărat în condiții normale
Aceasta înseamnă că botul va plasa ordine de CUMĂRARE continuu! Pentru utilizare reală, trebuie înlocuită cu o logică reală de tranzacționare.

🛠 Instrucțiuni de Utilizare
1. Cerințe Prealabile
python
pip install MetaTrader5
2. Pregătire Cont MT5
Asigurați-vă că contul este deschis și conectat

Verificați disponibilitatea simbolului USDJPY

Aveți suficienți bani în cont pentru tranzacții

3. Personalizare
Modificați următoarele în cod:

Simbol și mărime lot

Logică de tranzacționare reală în loc de condiția de test

Orele de tranzacționare și distanțele SL/TP

4. Lansare
bash
python nume_script.py
⚠️ Avertismente Importante
Nu folosiți în producție cu condiția actuală - va tranzacționa continuu!

Testați întotdeauna pe un cont demo mai întâi

Verificați conexiunea MT5 înainte de rulare

Monitorizați botul în timp real

Setări de risc - ajustați LOT_SIZE conform strategiei dvs.

🔄 Modificări Recomandate
Pentru Utilizare Reală:
Înlocuiți condiția cu logică tehnică (ex: RSI, Medii Mobile)

Adăugați gestionarea erorilor mai robustă

Implementați risk management (ex: max pierderi/zi)

Adăugați logging extins pentru debugging

Exemplu condiție reală:

python
# Înlocuiți secțiunea condiției curente
if tick.bid > moving_average:  # Exemplu simplu
    place_order(mt5.ORDER_TYPE_BUY, STOP_LOSS_TICKS, TAKE_PROFIT_TICKS)
📝 Notă: Acest bot este un schelet de bază. Pentru utilizare reală, este necesară implementarea unei strategii de tranzacționare valide și testarea extensivă.



import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time

# ========== SETĂRI CONFIGURABILE ==========
SYMBOL = "USDJPY"
LOT_SIZE = 0.01
STOP_LOSS_TICKS = 10
TAKE_PROFIT_TICKS = 20
TRADING_START_HOUR = 0
TRADING_END_HOUR = 23
TIMEOUT_MINUTES = 10  # Rulează 10 minute pentru test
TRADE_INTERVAL_SECONDS = 60  # Plasează ordin la fiecare 60 de secunde

# ========== FUNCȚIA PLASARE ORDINE CORECTATĂ ==========
def place_order(action_type, stop_loss_ticks, take_profit_ticks):
    """Plasează ordin de cumpărare/vânzare cu SL/TP"""
    try:
        print(f"🎯 Încerc plasare ordin...")
        
        # Obținem informațiile despre simbol
        symbol_info = mt5.symbol_info(SYMBOL)
        if not symbol_info:
            print(f"❌ Simbol {SYMBOL} negăsit")
            return False

        # Selectăm simbolul
        if not mt5.symbol_select(SYMBOL, True):
            print(f"❌ Nu s-a putut selecta simbolul {SYMBOL}")
            return False

        # Obținem tick-ul curent
        tick = mt5.symbol_info_tick(SYMBOL)
        if tick is None:
            print(f"❌ Nu sunt date tick pentru {SYMBOL}")
            return False

        print(f"📊 Preț curent - Bid: {tick.bid}, Ask: {tick.ask}")

        # Calculăm prețurile
        order_type_str = "CUMPĂRARE" if action_type == mt5.ORDER_TYPE_BUY else "VÂNZARE"
        price = tick.ask if action_type == mt5.ORDER_TYPE_BUY else tick.bid
        
        # Calculează SL și TP
        if action_type == mt5.ORDER_TYPE_BUY:
            sl = price - stop_loss_ticks * symbol_info.point
            tp = price + take_profit_ticks * symbol_info.point
        else:
            sl = price + stop_loss_ticks * symbol_info.point
            tp = price - take_profit_ticks * symbol_info.point

        print(f"💸 Ordin {order_type_str} la: {price:.5f}")
        print(f"🛑 Stop Loss: {sl:.5f}")
        print(f"🎯 Take Profit: {tp:.5f}")

        # Cerere corectată fără type_filling
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": LOT_SIZE,
            "type": action_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "Bot Test Continuu",
            "type_time": mt5.ORDER_TIME_GTC,
            # FĂRĂ type_filling - lasă brokerul să decidă
        }

        # Trimitem ordinul
        result = mt5.order_send(request)
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"✅ ✅ ORDIN REUȘIT! Ticket: {result.order}")
            print(f"   Preț executat: {result.price}")
            print(f"   Volum: {result.volume}")
            return True
        else:
            print(f"❌ Ordin eșuat, cod: {result.retcode}")
            print(f"   Mesaj: {result.comment}")
            return False

    except Exception as e:
        print(f"❌ Eroare la plasare ordin: {e}")
        return False

# ========== VERIFICARE SETĂRI SIMBOL ==========
def check_symbol_settings():
    """Verifică setările simbolului înainte de a începe"""
    print("🔍 VERIFICARE SETĂRI SIMBOL")
    print("=" * 40)
    
    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info:
        print(f"📊 Simbol: {SYMBOL}")
        print(f"📍 Point: {symbol_info.point}")
        print(f"🔢 Digits: {symbol_info.digits}")
        print(f"💰 Volume Min: {symbol_info.volume_min}")
        print(f"🎯 Trade Stops Level: {symbol_info.trade_stops_level}")
        print("✅ Setări verificate cu succes!")
    else:
        print(f"❌ Simbolul {SYMBOL} nu a putut fi găsit")
    
    print("=" * 40)

# ========== FUNCȚIA PRINCIPALĂ CU CONDITIE MEREU ADEVĂRATĂ ==========
def main():
    """Funcția principală cu condiție mereu adevărată pentru testare"""
    
    print("🤖 BOT TEST - CONDITIE MEREU ADEVĂRATĂ")
    print("=" * 50)
    
    # Inițializăm conexiunea la MT5
    if not mt5.initialize():
        print("❌ Eroare la inițializarea MT5")
        return

    print("✅ MT5 inițializat cu succes!")
    
    # Verifică setările simbolului
    check_symbol_settings()
    
    # Setăm timpul de timeout
    timeout_time = datetime.now() + timedelta(minutes=TIMEOUT_MINUTES)
    order_count = 0
    last_trade_time = None
    
    print(f"⏰ Botul va rula pentru {TIMEOUT_MINUTES} minute")
    print(f"💸 Lot size: {LOT_SIZE}")
    print(f"🔄 Interval tranzacții: {TRADE_INTERVAL_SECONDS} secunde")
    print("🎯 STRATEGIE: Condiție mereu adevărată (timp)")
    print("🔄 Pornit la:", datetime.now().strftime("%H:%M:%S"))
    
    try:
        while datetime.now() < timeout_time:
            current_time = datetime.now()
            
            # Verificăm dacă suntem în orele de tranzacționare
            if TRADING_START_HOUR <= current_time.hour <= TRADING_END_HOUR:
                
                # Obținem tick-ul curent
                tick = mt5.symbol_info_tick(SYMBOL)
                if tick is None:
                    print(f"❌ Nu sunt date tick pentru {SYMBOL}")
                    time.sleep(5)
                    continue

                # 🔥 CONDITIE MEREU ADEVĂRATĂ: Timpul trecut de la ultimul trade
                time_since_last_trade = None
                if last_trade_time:
                    time_since_last_trade = (current_time - last_trade_time).total_seconds()
                
                # Condiția este adevărată dacă nu am făcut niciun trade sau au trecut suficiente secunde
                condition_met = (last_trade_time is None) or (time_since_last_trade >= TRADE_INTERVAL_SECONDS)
                
                if condition_met:
                    print(f"✅ [{current_time.strftime('%H:%M:%S')}] CONDITIE ACTIVATĂ - Plasare ordin...")
                    
                    # Alternă între cumpărare și vânzare
                    if order_count % 2 == 0:
                        # Cumpără la ordinele pare
                        print("📈 Plasare ordin de CUMPĂRARE...")
                        if place_order(mt5.ORDER_TYPE_BUY, STOP_LOSS_TICKS, TAKE_PROFIT_TICKS):
                            order_count += 1
                            last_trade_time = current_time
                            print(f"✅ Ordin de cumpărare #{order_count} plasat cu succes!")
                        else:
                            print("❌ Eșuat la plasarea ordinului de cumpărare")
                    else:
                        # Vinde la ordinele impare
                        print("📉 Plasare ordin de VÂNZARE...")
                        if place_order(mt5.ORDER_TYPE_SELL, STOP_LOSS_TICKS, TAKE_PROFIT_TICKS):
                            order_count += 1
                            last_trade_time = current_time
                            print(f"✅ Ordin de vânzare #{order_count} plasat cu succes!")
                        else:
                            print("❌ Eșuat la plasarea ordinului de vânzare")
                else:
                    # Afișează countdown până la următorul trade
                    seconds_remaining = TRADE_INTERVAL_SECONDS - time_since_last_trade
                    print(f"⏳ [{current_time.strftime('%H:%M:%S')}] Aștept {seconds_remaining:.0f}s până la următorul trade...")
                
                time.sleep(5)  # Verifică la fiecare 5 secunde
                
            else:
                # În afara orelor de tranzacționare
                print(f"⏰ [{current_time.strftime('%H:%M:%S')}] În afara orelor de tranzacționare")
                time.sleep(30)  # Așteaptă mai mult în afara orelor

    except KeyboardInterrupt:
        print("\n⏹ Bot oprit manual de utilizator")
    except Exception as e:
        print(f"\n❌ Eroare neașteptată: {e}")
    finally:
        # Închide conexiunea MT5
        mt5.shutdown()
        print("🔌 Conexiune MT5 închisă")
        print(f"📊 REZUMAT: {order_count} ordine plasate în {TIMEOUT_MINUTES} minute")
        print("👋 Bot oprit la:", datetime.now().strftime("%H:%M:%S"))

# ========== RULARE BOT ==========
if __name__ == "__main__":
    print("🚀 BOT DE TEST - CONDITIE MEREU ADEVĂRATĂ")
    print("🎯 Configurat pentru:", SYMBOL)
    print("⏰ Pornește în 3 secunde...")
    time.sleep(3)
    
    main()
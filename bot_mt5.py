import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
import importlib
import sys
import os

# Adaugă directorul strategies la path
sys.path.append(os.path.join(os.path.dirname(__file__), 'strategies'))

# ========== SETĂRI CONFIGURABILE ==========
SYMBOL = "EURUSD"
LOT_SIZE = 0.01
STOP_LOSS_TICKS = 10
TAKE_PROFIT_TICKS = 20
TRADING_START_HOUR = 0
TRADING_END_HOUR = 23
TIMEOUT_MINUTES = 30

# ========== CONFIGURARE STRATEGIE ==========
STRATEGY_MODULE = "rsi_strategy"  # Schimbă de la "ema_cross"
STRATEGY_CLASS = "RSIStrategy"    # Schimbă de la "EMAStrategy"
STRATEGY_PARAMS = {
    'rsi_period': 14,
    'oversold': 30,
    'overbought': 70,
    'lot_size': LOT_SIZE
}

# ========== ISTORIC PENTRU STRATEGII ==========
HISTORICAL_DATA_POINTS = 100
TIME_FRAME = mt5.TIMEFRAME_H1

class LiveTradingBot:
    def __init__(self):
        self.strategy = None
        self.historical_data = []
        self.load_strategy()
        
    def load_strategy(self):
        """Încarcă strategia din folderul strategies"""
        try:
            # Importă modulul strategiei
            strategy_module = importlib.import_module(STRATEGY_MODULE)
            
            # Creează instanța strategiei
            strategy_class = getattr(strategy_module, STRATEGY_CLASS)
            self.strategy = strategy_class(**STRATEGY_PARAMS)
            
            print(f"✅ Strategie încărcată: {STRATEGY_MODULE}.{STRATEGY_CLASS}")
            print(f"⚙️ Parametri: {STRATEGY_PARAMS}")
            
        except Exception as e:
            print(f"❌ Eroare la încărcarea strategiei {STRATEGY_MODULE}.{STRATEGY_CLASS}: {e}")
            print("📁 Verifică că:")
            print(f"   - Fișierul strategies/{STRATEGY_MODULE}.py există")
            print(f"   - Clasa {STRATEGY_CLASS} există în fișier")
            print(f"   - Folderul strategies conține __init__.py")
            self.strategy = None
    
    def get_historical_data(self):
        """Obține datele istorice pentru strategie"""
        try:
            rates = mt5.copy_rates_from_pos(SYMBOL, TIME_FRAME, 0, HISTORICAL_DATA_POINTS)
            if rates is None:
                print("❌ Nu s-au putut obține datele istorice")
                return None
                
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            return df
            
        except Exception as e:
            print(f"❌ Eroare la obținerea datelor istorice: {e}")
            return None
    
    def get_current_signal(self):
        """Obține semnalul curent de la strategie"""
        if self.strategy is None:
            print("❌ Nicio strategie încărcată")
            return 0
            
        try:
            # Obține datele istorice
            data = self.get_historical_data()
            if data is None or data.empty:
                print("❌ Date istorice lipsă sau goale")
                return 0
            
            # Verifică dacă strategia are metoda generate_signals
            if not hasattr(self.strategy, 'generate_signals'):
                print("❌ Strategia nu are metoda 'generate_signals'")
                return 0
            
            # Generează semnalele
            signals_df = self.strategy.generate_signals(data)
            
            if signals_df is None or 'signal' not in signals_df.columns:
                print("❌ Nu s-au putut genera semnale")
                return 0
                
            # Returnează ultimul semnal
            last_signal = signals_df['signal'].iloc[-1]
            return last_signal
            
        except Exception as e:
            print(f"❌ Eroare la generarea semnalului: {e}")
            return 0

# ========== FUNCȚIA PLASARE ORDINE ==========
def place_order(action_type, stop_loss_ticks, take_profit_ticks):
    """Plasează ordin de cumpărare/vânzare cu SL/TP"""
    try:
        print(f"🎯 Încerc plasare ordin...")
        
        symbol_info = mt5.symbol_info(SYMBOL)
        if not symbol_info:
            print(f"❌ Simbol {SYMBOL} negăsit")
            return False

        if not mt5.symbol_select(SYMBOL, True):
            print(f"❌ Nu s-a putut selecta simbolul {SYMBOL}")
            return False

        tick = mt5.symbol_info_tick(SYMBOL)
        if tick is None:
            print(f"❌ Nu sunt date tick pentru {SYMBOL}")
            return False

        print(f"📊 Preț curent - Bid: {tick.bid}, Ask: {tick.ask}")

        order_type_str = "CUMPĂRARE" if action_type == mt5.ORDER_TYPE_BUY else "VÂNZARE"
        price = tick.ask if action_type == mt5.ORDER_TYPE_BUY else tick.bid
        
        if action_type == mt5.ORDER_TYPE_BUY:
            sl = price - stop_loss_ticks * symbol_info.point
            tp = price + take_profit_ticks * symbol_info.point
        else:
            sl = price + stop_loss_ticks * symbol_info.point
            tp = price - take_profit_ticks * symbol_info.point

        print(f"💸 Ordin {order_type_str} la: {price:.5f}")
        print(f"🛑 Stop Loss: {sl:.5f}")
        print(f"🎯 Take Profit: {tp:.5f}")

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
            "comment": f"Bot {STRATEGY_MODULE}.{STRATEGY_CLASS}",
            "type_time": mt5.ORDER_TIME_GTC,
        }

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

# ========== FUNCȚIA PRINCIPALĂ ==========
def main():
    """Funcția principală care rulează botul cu strategii"""
    
    print("🤖 BOT MT5 PORNIT - STRATEGIE LIVE")
    print("=" * 50)
    
    if not mt5.initialize():
        print("❌ Eroare la inițializarea MT5")
        return

    print("✅ MT5 inițializat cu succes!")
    
    check_symbol_settings()
    
    bot = LiveTradingBot()
    
    if bot.strategy is None:
        print("❌ Botul nu poate porni fără strategie")
        mt5.shutdown()
        return
    
    timeout_time = datetime.now() + timedelta(minutes=TIMEOUT_MINUTES)
    order_count = 0
    last_trade_time = None
    
    print(f"⏰ Botul va rula pentru {TIMEOUT_MINUTES} minute")
    print(f"📈 Strategie: {STRATEGY_MODULE}.{STRATEGY_CLASS}")
    print(f"💸 Lot size: {LOT_SIZE}")
    print(f"📊 Timeframe strategie: {TIME_FRAME}")
    print("🔄 Pornit la:", datetime.now().strftime("%H:%M:%S"))
    
    try:
        while datetime.now() < timeout_time:
            current_time = datetime.now()
            
            if TRADING_START_HOUR <= current_time.hour <= TRADING_END_HOUR:
                
                signal = bot.get_current_signal()
                
                tick = mt5.symbol_info_tick(SYMBOL)
                if tick is None:
                    print(f"❌ Nu sunt date tick pentru {SYMBOL}")
                    time.sleep(5)
                    continue

                print(f"📊 [{current_time.strftime('%H:%M:%S')}] Bid: {tick.bid:.5f}, Semnal: {signal}")
                
                can_trade = (last_trade_time is None or 
                           (current_time - last_trade_time).total_seconds() > 60)
                
                if signal == 1 and can_trade:
                    print(f"🎯 SEMNAL CUMPĂRARE de la {STRATEGY_MODULE}.{STRATEGY_CLASS}")
                    if place_order(mt5.ORDER_TYPE_BUY, STOP_LOSS_TICKS, TAKE_PROFIT_TICKS):
                        order_count += 1
                        last_trade_time = current_time
                        print(f"📈 Ordin de cumpărare #{order_count} plasat cu succes!")
                    else:
                        print("❌ Eșuat la plasarea ordinului de cumpărare")
                        
                elif signal == -1 and can_trade:
                    print(f"🎯 SEMNAL VÂNZARE de la {STRATEGY_MODULE}.{STRATEGY_CLASS}")
                    if place_order(mt5.ORDER_TYPE_SELL, STOP_LOSS_TICKS, TAKE_PROFIT_TICKS):
                        order_count += 1
                        last_trade_time = current_time
                        print(f"📉 Ordin de vânzare #{order_count} plasat cu succes!")
                    else:
                        print("❌ Eșuat la plasarea ordinului de vânzare")
                else:
                    if last_trade_time:
                        seconds_since_last = (current_time - last_trade_time).total_seconds()
                        if seconds_since_last < 60:
                            print(f"⏳ Aștept {(60 - seconds_since_last):.0f}s înainte de următorul trade")
                    else:
                        print("⏳ Aștept semnal de tranzacționare...")
                
                time.sleep(5)
                
            else:
                print(f"⏰ [{current_time.strftime('%H:%M:%S')}] În afara orelor de tranzacționare")
                time.sleep(30)

    except KeyboardInterrupt:
        print("\n⏹ Bot oprit manual de utilizator")
    except Exception as e:
        print(f"\n❌ Eroare neașteptată: {e}")
    finally:
        mt5.shutdown()
        print("🔌 Conexiune MT5 închisă")
        print(f"📊 Rezumat: {order_count} ordine plasate în {TIMEOUT_MINUTES} minute")
        print("👋 Bot oprit la:", datetime.now().strftime("%H:%M:%S"))

if __name__ == "__main__":
    print("🚀 BOT DE TRANZACȚIONARE CU STRATEGII")
    print("🎯 Configurat pentru:", SYMBOL)
    print("📈 Strategie activă:", f"{STRATEGY_MODULE}.{STRATEGY_CLASS}")
    print("⏰ Pornește în 3 secunde...")
    time.sleep(3)
    
    main()
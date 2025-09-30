import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time

def comprehensive_diagnostic():
    """Script care verifică toate aspectele conexiunii și permisiunilor - VERSIUNE CORECTATĂ"""
    
    print("🔍 DIAGNOSTIC COMPLET MT5")
    print("=" * 60)
    
    # 1. Verifică inițializarea
    print("1. 🔄 Inițializare MT5...")
    if not mt5.initialize():
        print("   ❌ EROARE CRITICĂ: Nu se poate inițializa MT5")
        print("   📝 Cauze posibile:")
        print("      - MT5 nu este deschis")
        print("      - Contul nu este logat")
        print("      - Probleme de permisiuni")
        return False
    
    print("   ✅ MT5 inițializat cu succes")
    
    # 2. Verifică informații terminal
    print("2. 💻 Informații terminal...")
    terminal_info = mt5.terminal_info()
    if terminal_info is None:
        print("   ❌ Nu se pot obține informații terminal")
        mt5.shutdown()
        return False
    
    print(f"   ✅ Terminal: {terminal_info.name}")
    print(f"   🔗 Conectat: {terminal_info.connected}")
    print(f"   📈 Trading permis: {terminal_info.trade_allowed}")
    print(f"   📍 Cale: {terminal_info.path}")
    print(f"   👥 Comunity account: {terminal_info.community_account}")
    print(f"   📞 Comunity connection: {terminal_info.community_connection}")
    
    if not terminal_info.connected:
        print("   ❌ TERMINAL NU ESTE CONECTAT LA INTERNET/SERVER")
        mt5.shutdown()
        return False
        
    if not terminal_info.trade_allowed:
        print("   ❌ TRADING NU ESTE PERMIS - Verifică butonul 'Auto Trading'")
    
    # 3. Verifică informații cont
    print("3. 👤 Informații cont...")
    account_info = mt5.account_info()
    if account_info is None:
        print("   ❌ Nu se pot obține informații cont")
        mt5.shutdown()
        return False
        
    print(f"   ✅ Cont: {account_info.login}")
    print(f"   🏢 Broker: {account_info.server}")
    print(f"   💰 Sold: {account_info.balance}")
    print(f"   💵 Equity: {account_info.equity}")
    print(f"   🆓 Margin liber: {account_info.margin_free}")
    print(f"   📊 Leverage: 1:{account_info.leverage}")
    print(f"   🔐 Nume: {account_info.name}")
    
    # 4. Verifică simbolul
    symbol = "USDJPY"
    print(f"4. 📈 Verific simbolul {symbol}...")
    
    # Verifică dacă simbolul există
    all_symbols = mt5.symbols_get()
    symbol_exists = any(s.name == symbol for s in all_symbols)
    print(f"   ✅ Simbol există în baza de date: {symbol_exists}")
    
    # Încearcă să selecteze simbolul
    if mt5.symbol_select(symbol, True):
        print(f"   ✅ Simbol {symbol} selectat în Market Watch")
    else:
        print(f"   ❌ Nu s-a putut selecta {symbol} în Market Watch")
    
    # Obține informații detaliate simbol
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"   ❌ Nu se pot obține informații pentru {symbol}")
        mt5.shutdown()
        return False
        
    print(f"   📊 Bid: {symbol_info.bid}, Ask: {symbol_info.ask}")
    print(f"   📏 Point: {symbol_info.point}")
    print(f"   📐 Digits: {symbol_info.digits}")
    print(f"   📈 Trade MODE: {symbol_info.trade_mode}")
    print(f"   💰 Trade STOPS_LEVEL: {symbol_info.trade_stops_level}")
    print(f"   📦 Trade VOLUME_MIN: {symbol_info.volume_min}")
    
    # 5. Verifică tick-ul în timp real
    print("5. ⏰ Verific date tick în timp real...")
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print("   ❌ Nu se pot obține date tick")
        mt5.shutdown()
        return False
        
    print(f"   ✅ Tick primit - Bid: {tick.bid}, Ask: {tick.ask}")
    print(f"   🕒 Timp tick: {datetime.fromtimestamp(tick.time)}")
    print(f"   📈 Volume: {tick.volume}")
    
    # 6. Verifică permisiuni de trading
    print("6. 🔐 Verific permisiuni trading...")
    
    # Verifică dacă simbolul este activ pentru trading
    trade_modes = {
        0: "SYMBOL_TRADE_MODE_DISABLED",
        1: "SYMBOL_TRADE_MODE_LONGONLY", 
        2: "SYMBOL_TRADE_MODE_SHORTONLY",
        3: "SYMBOL_TRADE_MODE_CLOSEONLY",
        4: "SYMBOL_TRADE_MODE_FULL"
    }
    
    current_trade_mode = trade_modes.get(symbol_info.trade_mode, 'NECUNOSCUT')
    print(f"   📋 Modul de trading: {current_trade_mode}")
    
    if symbol_info.trade_mode != 4:  # SYMBOL_TRADE_MODE_FULL
        print("   ⚠️ ATENȚIE: Simbolul are restricții de trading!")
        print("   📝 Poate fi doar pentru citire sau cu restricții")
    else:
        print("   ✅ Simbolul are trading full permis")
    
    # 7. Testează ordin simplu FĂRĂ SL/TP
    print("7. 🧪 Test ordin simplu (fără SL/TP)...")
    
    # Folosește un volum mic pentru test
    test_volume = max(0.01, symbol_info.volume_min)
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": test_volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "deviation": 20,
        "magic": 999999,
        "comment": "TEST DIAGNOSTIC",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    print(f"   📦 Volume test: {test_volume}")
    print(f"   💰 Preț ask: {tick.ask}")
    
    result = mt5.order_send(request)
    
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("   ✅ ✅ ✅ ORDIN TEST REUȘIT! ✅ ✅ ✅")
        print(f"      Ticket: {result.order}")
        print(f"      Preț executat: {result.price}")
        print(f"      Volume executat: {result.volume}")
        
        # Închide poziția imediat
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": test_volume,
            "type": mt5.ORDER_TYPE_SELL,
            "position": result.order,
            "price": tick.bid,
            "deviation": 20,
            "magic": 999999,
            "comment": "CLOSE TEST",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        
        close_result = mt5.order_send(close_request)
        if close_result.retcode == mt5.TRADE_RETCODE_DONE:
            print("   ✅ Poziție închisă cu succes")
        else:
            print(f"   ⚠️ Poziție nu s-a putut închide: {close_result.retcode}")
            
    else:
        print(f"   ❌ ORDIN TEST EȘUAT: {result.retcode}")
        print(f"      Mesaj: {result.comment}")
        
        # Analiză eroare detaliată
        error_messages = {
            10004: "Cerere invalida",
            10006: "Nu sunt conexiuni",
            10013: "Parametri invalizi",
            10014: "Volum invalid",
            10015: "Pret invalid",
            10016: "Simbol invalid",
            10017: "Ordine invalide",
            10018: "Piata inchisa",
            10019: "Fonduri insuficiente",
            10020: "Tranzactie interzisa",
            10021: "Limita depasita",
            10022: "Ordine blocata",
            10023: "Ordine permisiuni",
            10024: "Client/O server ocupat",
            10025: "Ordine timeout",
            10026: "Ordine invalidă",
            10027: "Context tranzacționare ocupat",
            10028: "Preț invalid pentru piata",
            10029: "Broker nu permite tranzacții",
            10030: "Versiune terminal incompatibila"
        }
        
        if result.retcode in error_messages:
            print(f"   📋 Explicație: {error_messages[result.retcode]}")
        else:
            print(f"   🔍 Cod eroare necunoscut: {result.retcode}")
    
    print("=" * 60)
    mt5.shutdown()
    return result.retcode == mt5.TRADE_RETCODE_DONE

if __name__ == "__main__":
    comprehensive_diagnostic()
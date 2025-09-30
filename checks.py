import MetaTrader5 as mt5

def mandatory_checklist():
    """Listă de verificări obligatorii înainte de trading"""
    
    checks = {
        "MT5 deschis și cont logat": False,
        "Buton Auto Trading activat": False,
        "Simbol în Market Watch": False,
        "Conexiune internet stabilă": False,
        "Cont demo (nu real) pentru teste": False,
        "Fonduri suficiente": False,
        "Alt EA nu rulează": False
    }
    
    if mt5.initialize():
        terminal = mt5.terminal_info()
        checks["MT5 deschis și cont logat"] = terminal.connected
        checks["Buton Auto Trading activat"] = terminal.trade_allowed
        
        symbol_info = mt5.symbol_info("USDJPY")
        checks["Simbol în Market Watch"] = symbol_info is not None
        
        account = mt5.account_info()
        checks["Fonduri suficiente"] = account.balance > 10  # Minimum $10
        
        mt5.shutdown()
    
    print("📋 LISTĂ DE VERIFICĂRI:")
    for check, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {check}")
    
    return all(checks.values())

mandatory_checklist()
from backtesting_engine import BacktestingEngine
from strategies.ema_cross import EMAStrategy  # Folosește versiunea pentru backtesting
from strategies.rsi_strategy import RSIStrategy  # Folosește versiunea pentru backtesting
from datetime import datetime, timedelta
import MetaTrader5 as mt5  # Adaugă importul pentru MT5

def main():
    # Inițializează motorul de backtesting
    engine = BacktestingEngine(initial_balance=10000)
    
    # Definește perioada de test
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 luni
    
    # Configurare strategii de testat
    strategies_config = [
        {
            'strategy': EMAStrategy,  # Folosește clasa pentru backtesting
            'symbol': 'EURUSD',
            'timeframe': mt5.TIMEFRAME_H1,
            'start_date': start_date,
            'end_date': end_date,
            'fast_period': 10,
            'slow_period': 20,
            'lot_size': 0.01
        },
        {
            'strategy': RSIStrategy,  # Folosește clasa pentru backtesting
            'symbol': 'EURUSD', 
            'timeframe': mt5.TIMEFRAME_H1,
            'start_date': start_date,
            'end_date': end_date,
            'rsi_period': 14,
            'oversold': 30,
            'overbought': 70,
            'lot_size': 0.01
        },
    ]
    
    print("🚀 Pornesc backtesting pentru multiple strategii...")
    print(f"📅 Perioadă: {start_date.date()} - {end_date.date()}")
    print("=" * 60)
    
    # Rulează comparația strategiilor
    results_df = engine.compare_strategies(strategies_config)
    
    # Afișează rezultatele
    print("\n📊 REZULTATE COMPARATIVE:")
    print("=" * 60)
    
    if not results_df.empty:
        print(results_df.to_string(index=False))
        
        # Salvează rezultatele
        engine.save_results()
        
        # Găsește strategia cu cel mai bun profit factor
        best_strategy = results_df.loc[results_df['Profit Factor'].idxmax()]
        print(f"\n🏆 CEA MAI BUNĂ STRATEGIE: {best_strategy['Strategy']}")
        print(f"   Profit Factor: {best_strategy['Profit Factor']:.2f}")
        print(f"   Win Rate: {best_strategy['Win Rate %']:.1f}%")
        print(f"   Total PnL: ${best_strategy['Total PnL']:.2f}")
    else:
        print("❌ Nu s-au putut genera rezultate. Verifică erorile de mai sus.")

if __name__ == "__main__":
    main()
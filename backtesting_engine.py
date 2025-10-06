import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Any

class BacktestingEngine:
    def __init__(self, initial_balance=10000, spread=0.0002, commission=0.0001):
        self.initial_balance = initial_balance
        self.spread = spread
        self.commission = commission
        self.results = {}
        
    def load_data(self, symbol: str, timeframe: int, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Încarcă datele istorice din MT5"""
        if not mt5.initialize():
            raise ConnectionError("Nu se poate conecta la MT5")
            
        rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
        mt5.shutdown()
        
        if rates is None:
            raise ValueError(f"Nu există date pentru {symbol} în perioada specificată")
            
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        return df
    
    def run_backtest(self, strategy, symbol: str, timeframe: int, 
                    start_date: datetime, end_date: datetime, 
                    **strategy_params) -> Dict[str, Any]:
        """Rulează backtest pentru o strategie"""
        
        # Încarcă datele
        data = self.load_data(symbol, timeframe, start_date, end_date)
        
        # Inițializează strategia
        strategy_instance = strategy(**strategy_params)
        
        # Rulează strategia
        trades, equity_curve = strategy_instance.execute(data)
        
        # Analizează performanța
        performance = self.analyze_performance(trades, equity_curve)
        
        # Salvează rezultatele
        result_id = f"{strategy.__name__}_{symbol}_{timeframe}"
        self.results[result_id] = {
            'strategy': strategy.__name__,
            'symbol': symbol,
            'timeframe': timeframe,
            'period': f"{start_date.date()} to {end_date.date()}",
            'trades': trades,
            'equity_curve': equity_curve,
            'performance': performance
        }
        
        return self.results[result_id]
    
    def analyze_performance(self, trades: List[Dict], equity_curve: List[float]) -> Dict[str, float]:
        """Analizează performanța tranzacțiilor"""
        if not trades:
            return {}
            
        df_trades = pd.DataFrame(trades)
        
        # Calculează metrici de performanță
        total_trades = len(df_trades)
        winning_trades = len(df_trades[df_trades['pnl'] > 0])
        losing_trades = len(df_trades[df_trades['pnl'] < 0])
        
        if total_trades == 0:
            return {}
            
        win_rate = (winning_trades / total_trades) * 100
        total_pnl = df_trades['pnl'].sum()
        avg_trade = df_trades['pnl'].mean()
        
        # Calcul drawdown
        equity_series = pd.Series(equity_curve)
        rolling_max = equity_series.expanding().max()
        drawdown = (equity_series - rolling_max) / rolling_max * 100
        max_drawdown = drawdown.min()
        
        # Profit factor
        gross_profit = df_trades[df_trades['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(df_trades[df_trades['pnl'] < 0]['pnl'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'average_pnl': avg_trade,
            'max_drawdown': max_drawdown,
            'profit_factor': profit_factor,
            'largest_win': df_trades['pnl'].max(),
            'largest_loss': df_trades['pnl'].min()
        }
    
    def compare_strategies(self, strategies_config: List[Dict]) -> pd.DataFrame:
        """Compară multiple strategii"""
        comparison_results = []
        
        for config in strategies_config:
            try:
                result = self.run_backtest(**config)
                perf = result['performance']
                
                comparison_results.append({
                    'Strategy': config['strategy'].__name__,
                    'Symbol': config['symbol'],
                    'Timeframe': config['timeframe'],
                    'Total Trades': perf.get('total_trades', 0),
                    'Win Rate %': perf.get('win_rate', 0),
                    'Total PnL': perf.get('total_pnl', 0),
                    'Avg Trade': perf.get('average_pnl', 0),
                    'Max Drawdown %': perf.get('max_drawdown', 0),
                    'Profit Factor': perf.get('profit_factor', 0)
                })
            except Exception as e:
                print(f"Eroare la testarea strategiei {config['strategy'].__name__}: {e}")
        
        return pd.DataFrame(comparison_results)
    
    def save_results(self, filename: str = None):
        """Salvează rezultatele în fișier"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backtest_results_{timestamp}.json"
            
        os.makedirs('results', exist_ok=True)
        filepath = os.path.join('results', filename)
        
        # Convertim pentru serializare JSON
        serializable_results = {}
        for key, result in self.results.items():
            serializable_results[key] = {
                k: v for k, v in result.items() 
                if k not in ['trades', 'equity_curve']
            }
            # Adăugăm doar rezumatul tranzacțiilor
            if 'trades' in result:
                serializable_results[key]['trades_count'] = len(result['trades'])
                serializable_results[key]['trades_summary'] = pd.DataFrame(result['trades']).describe().to_dict()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Rezultate salvate în {filepath}")
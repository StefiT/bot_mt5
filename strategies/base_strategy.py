from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any, Optional

class BaseStrategy(ABC):
    def __init__(self, name: str, lot_size: float = 0.01):
        self.name = name
        self.lot_size = lot_size
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Metodă abstractă - trebuie implementată în clasele derivate"""
        pass
    
    def execute(self, data: pd.DataFrame) -> tuple:
        """Execută strategia pentru backtesting"""
        data_with_signals = self.generate_signals(data)
        trades = self.simulate_trading(data_with_signals)
        equity_curve = self.calculate_equity_curve(trades)
        return trades, equity_curve
    
    def get_current_signal(self, data: pd.DataFrame) -> int:
        """Obține semnalul curent pentru trading live"""
        signals_df = self.generate_signals(data)
        if 'signal' not in signals_df.columns:
            return 0
        return signals_df['signal'].iloc[-1]
    
    def simulate_trading(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Simulează tranzacționarea pentru backtesting"""
        trades = []
        position = None
        entry_price = 0
        entry_index = 0
        
        for i, row in data.iterrows():
            current_price = row['close']
            
            # Logică pentru deschidere/închidere poziții
            if position is None and row['signal'] == 1:  # Semnal de cumpărare
                position = 'long'
                entry_price = current_price
                entry_index = i
                
            elif position == 'long' and row['signal'] == -1:  # Semnal de vânzare
                pnl = (current_price - entry_price) * self.lot_size * 100000
                trade_duration = (i - entry_index).total_seconds() / 3600  # ore
                
                trades.append({
                    'entry_time': entry_index,
                    'exit_time': i,
                    'position': 'long',
                    'entry_price': entry_price,
                    'exit_price': current_price,
                    'pnl': pnl,
                    'duration_hours': trade_duration
                })
                position = None
        
        # Închide orice poziție deschisă la final
        if position == 'long':
            current_price = data.iloc[-1]['close']
            pnl = (current_price - entry_price) * self.lot_size * 100000
            trade_duration = (data.index[-1] - entry_index).total_seconds() / 3600
            
            trades.append({
                'entry_time': entry_index,
                'exit_time': data.index[-1],
                'position': 'long',
                'entry_price': entry_price,
                'exit_price': current_price,
                'pnl': pnl,
                'duration_hours': trade_duration
            })
        
        return trades
    
    def calculate_equity_curve(self, trades: List[Dict]) -> List[float]:
        """Calculează curba de equity pentru backtesting"""
        if not trades:
            return [self.lot_size * 100000]  # equity initial
        
        equity = [self.lot_size * 100000]  # Starting equity
        for trade in trades:
            equity.append(equity[-1] + trade['pnl'])
        
        return equity
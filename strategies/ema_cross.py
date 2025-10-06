import pandas as pd
import numpy as np

class EMAStrategy:
    def __init__(self, fast_period=10, slow_period=20, lot_size=0.01):
        self.name = "EMA Crossover"
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.lot_size = lot_size
        
    def generate_signals(self, data):
        """Generează semnale pentru datele istorice"""
        df = data.copy()
        
        # Calculează EMA-urile
        df['ema_fast'] = df['close'].ewm(span=self.fast_period, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=self.slow_period, adjust=False).mean()
        
        # Generează semnale: 1 = cumpărare, -1 = vânzare, 0 = stai
        df['signal'] = 0
        
        # Cumpără când EMA fast trece peste EMA slow
        buy_signal = (df['ema_fast'] > df['ema_slow']) & (df['ema_fast'].shift(1) <= df['ema_slow'].shift(1))
        df.loc[buy_signal, 'signal'] = 1
        
        # Vinde când EMA fast trece sub EMA slow  
        sell_signal = (df['ema_fast'] < df['ema_slow']) & (df['ema_fast'].shift(1) >= df['ema_slow'].shift(1))
        df.loc[sell_signal, 'signal'] = -1
        
        return df
import pandas as pd
import numpy as np

class RSIStrategy:
    def __init__(self, rsi_period=14, oversold=30, overbought=70, lot_size=0.01):
        self.name = "RSI Strategy"
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        self.lot_size = lot_size
        
    def calculate_rsi(self, prices, period=14):
        """Calculează RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
        
    def generate_signals(self, data):
        """Generează semnale pentru datele istorice"""
        df = data.copy()
        
        # Calculează RSI
        df['rsi'] = self.calculate_rsi(df['close'], self.rsi_period)
        
        # Generează semnale
        df['signal'] = 0
        
        # Cumpără când RSI iese din zona de oversold
        buy_signal = (df['rsi'] > self.oversold) & (df['rsi'].shift(1) <= self.oversold)
        df.loc[buy_signal, 'signal'] = 1
        
        # Vinde când RSI iese din zona de overbought
        sell_signal = (df['rsi'] < self.overbought) & (df['rsi'].shift(1) >= self.overbought)
        df.loc[sell_signal, 'signal'] = -1
        
        return df
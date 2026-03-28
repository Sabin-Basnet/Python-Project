"""
indicators.py
Calculates technical indicators for stocks.
"""
import pandas as pd
import pandas_ta as ta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame with 'Close' column and calculates:
    - MA20, MA50, MA100, MA200
    - RSI14
    """
    if df.empty or 'Close' not in df.columns:
        return pd.DataFrame()

    df = df.copy()

    # Calculate Moving Averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA100'] = df['Close'].rolling(window=100).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    # Calculate RSI
    df['RSI14'] = ta.rsi(df['Close'], length=14)

    return df[['MA20', 'MA50', 'MA100', 'MA200', 'RSI14']]

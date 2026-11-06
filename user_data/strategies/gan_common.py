# FREQ-GAN shared helpers for futures strategies (long + short, isolated, fixed modest leverage)
import numpy as np
import pandas as pd


def supertrend(df: pd.DataFrame, period: int = 10, mult: float = 3.0) -> pd.Series:
    """Returns +1 (uptrend) / -1 (downtrend)."""
    hl2 = (df['high'] + df['low']) / 2
    tr = pd.concat([df['high'] - df['low'], (df['high'] - df['close'].shift()).abs(),
                    (df['low'] - df['close'].shift()).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / period, adjust=False).mean()
    upper = (hl2 + mult * atr).to_numpy()
    lower = (hl2 - mult * atr).to_numpy()
    close = df['close'].to_numpy()
    fu, fl = upper.copy(), lower.copy()
    direction = np.ones(len(df))
    for i in range(1, len(df)):
        fu[i] = upper[i] if (upper[i] < fu[i - 1] or close[i - 1] > fu[i - 1]) else fu[i - 1]
        fl[i] = lower[i] if (lower[i] > fl[i - 1] or close[i - 1] < fl[i - 1]) else fl[i - 1]
        if direction[i - 1] == -1 and close[i] > fu[i - 1]:
            direction[i] = 1
        elif direction[i - 1] == 1 and close[i] < fl[i - 1]:
            direction[i] = -1
        else:
            direction[i] = direction[i - 1]
    return pd.Series(direction, index=df.index)

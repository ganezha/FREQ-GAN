# Momentum reversal: MACD signal cross on the "wrong" side of zero + RSI turning from extreme zone. Long + short.
import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib
from GanBase import GanBase


class GanMacdRsi(GanBase):
    timeframe = '15m'
    minimal_roi = {"0": 0.04, "180": 0.02, "480": 0.008}
    stoploss = -0.07

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        m = ta.MACD(df, fastperiod=12, slowperiod=26, signalperiod=9)
        df['macd'], df['macds'] = m['macd'], m['macdsignal']
        df['rsi'] = ta.RSI(df, timeperiod=14)
        df['rsi_min5'] = df['rsi'].rolling(5).min()
        df['rsi_max5'] = df['rsi'].rolling(5).max()
        df['ema200'] = ta.EMA(df, timeperiod=200)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        v = df['volume'] > 0
        df.loc[v & qtpylib.crossed_above(df['macd'], df['macds']) & (df['macd'] < 0) & (df['rsi_min5'] < 35)
               & (df['rsi'] > df['rsi'].shift(1)), ['enter_long', 'enter_tag']] = (1, 'macd_up_rsi_low')
        df.loc[v & qtpylib.crossed_below(df['macd'], df['macds']) & (df['macd'] > 0) & (df['rsi_max5'] > 65)
               & (df['rsi'] < df['rsi'].shift(1)), ['enter_short', 'enter_tag']] = (1, 'macd_dn_rsi_high')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[(df['rsi'] > 65) | qtpylib.crossed_below(df['macd'], df['macds']), ['exit_long', 'exit_tag']] = (1, 'macd_rsi_exit')
        df.loc[(df['rsi'] < 35) | qtpylib.crossed_above(df['macd'], df['macds']), ['exit_short', 'exit_tag']] = (1, 'macd_rsi_exit')
        return df

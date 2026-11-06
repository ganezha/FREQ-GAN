# 4h trend following: EMA21/EMA55 cross with EMA200 regime + ADX, ATR-style trailing via freqtrade trailing stop.
import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib
from GanBase import GanBase


class GanTrendEma4h(GanBase):
    timeframe = '4h'
    startup_candle_count = 220
    minimal_roi = {"0": 0.40}
    stoploss = -0.12
    trailing_stop = True
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.10
    trailing_only_offset_is_reached = True

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['ema21'] = ta.EMA(df, timeperiod=21)
        df['ema55'] = ta.EMA(df, timeperiod=55)
        df['ema200'] = ta.EMA(df, timeperiod=200)
        df['adx'] = ta.ADX(df, timeperiod=14)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        v = (df['volume'] > 0) & (df['adx'] > 20)
        df.loc[v & qtpylib.crossed_above(df['ema21'], df['ema55']) & (df['close'] > df['ema200']),
               ['enter_long', 'enter_tag']] = (1, 'ema_cross_up')
        df.loc[v & qtpylib.crossed_below(df['ema21'], df['ema55']) & (df['close'] < df['ema200']),
               ['enter_short', 'enter_tag']] = (1, 'ema_cross_dn')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df['ema21'] < df['ema55'], ['exit_long', 'exit_tag']] = (1, 'ema_recross')
        df.loc[df['ema21'] > df['ema55'], ['exit_short', 'exit_tag']] = (1, 'ema_recross')
        return df

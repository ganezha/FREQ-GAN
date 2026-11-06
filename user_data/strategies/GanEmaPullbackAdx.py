# Trend pullback: EMA50/EMA200 trend + ADX strength, enter on pullback to EMA20 with RSI reset. Long + short.
import talib.abstract as ta
from pandas import DataFrame
from freqtrade.strategy import IntParameter
from GanBase import GanBase


class GanEmaPullbackAdx(GanBase):
    timeframe = '1h'
    minimal_roi = {"0": 0.08, "720": 0.04, "1440": 0.02}
    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True
    adx_min = IntParameter(18, 35, default=25, space='buy')

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['ema20'] = ta.EMA(df, timeperiod=20)
        df['ema50'] = ta.EMA(df, timeperiod=50)
        df['ema200'] = ta.EMA(df, timeperiod=200)
        df['adx'] = ta.ADX(df, timeperiod=14)
        df['rsi'] = ta.RSI(df, timeperiod=14)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        strong = (df['adx'] > self.adx_min.value) & (df['volume'] > 0)
        up = (df['ema50'] > df['ema200']) & (df['close'] > df['ema200'])
        dn = (df['ema50'] < df['ema200']) & (df['close'] < df['ema200'])
        df.loc[strong & up & (df['low'] <= df['ema20']) & (df['close'] > df['ema20']) & (df['rsi'].between(40, 55)),
               ['enter_long', 'enter_tag']] = (1, 'pullback_up')
        df.loc[strong & dn & (df['high'] >= df['ema20']) & (df['close'] < df['ema20']) & (df['rsi'].between(45, 60)),
               ['enter_short', 'enter_tag']] = (1, 'pullback_dn')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df['close'] < df['ema50'], ['exit_long', 'exit_tag']] = (1, 'lost_ema50')
        df.loc[df['close'] > df['ema50'], ['exit_short', 'exit_tag']] = (1, 'lost_ema50')
        return df

# Connors-style short-term mean reversion WITH the trend: RSI(2) extreme against an EMA200 trend, exit on SMA5 recross.
# Long only above EMA200, short only below. Long + short.
import talib.abstract as ta
from pandas import DataFrame
from freqtrade.strategy import IntParameter, DecimalParameter
from GanBase import GanBase


class GanConnorsRsi2(GanBase):
    timeframe = '1h'
    minimal_roi = {"0": 0.10}
    stoploss = -0.10
    rsi_entry_long = IntParameter(3, 20, default=10, space='buy')
    rsi_entry_short = IntParameter(80, 97, default=90, space='sell')
    adx_min = IntParameter(0, 30, default=0, space='buy', optimize=False)

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['rsi2'] = ta.RSI(df, timeperiod=2)
        df['sma5'] = ta.SMA(df, timeperiod=5)
        df['ema200'] = ta.EMA(df, timeperiod=200)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        v = df['volume'] > 0
        df.loc[v & (df['close'] > df['ema200']) & (df['rsi2'] < self.rsi_entry_long.value),
               ['enter_long', 'enter_tag']] = (1, 'rsi2_dip_uptrend')
        df.loc[v & (df['close'] < df['ema200']) & (df['rsi2'] > self.rsi_entry_short.value),
               ['enter_short', 'enter_tag']] = (1, 'rsi2_pop_downtrend')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df['close'] > df['sma5'], ['exit_long', 'exit_tag']] = (1, 'above_sma5')
        df.loc[df['close'] < df['sma5'], ['exit_short', 'exit_tag']] = (1, 'below_sma5')
        return df


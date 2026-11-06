# Breakout: 20-bar Donchian break with volume surge + ADX; exit on 10-bar opposite channel. Long + short.
import talib.abstract as ta
from pandas import DataFrame
from GanBase import GanBase


class GanDonchianBreakout(GanBase):
    timeframe = '1h'
    minimal_roi = {"0": 0.12, "1440": 0.05}
    stoploss = -0.08
    trailing_stop = True
    trailing_stop_positive = 0.025
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['dc_hi'] = df['high'].rolling(20).max().shift(1)
        df['dc_lo'] = df['low'].rolling(20).min().shift(1)
        df['ex_hi'] = df['high'].rolling(10).max().shift(1)
        df['ex_lo'] = df['low'].rolling(10).min().shift(1)
        df['vol_ma'] = df['volume'].rolling(20).mean()
        df['adx'] = ta.ADX(df, timeperiod=14)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        base = (df['volume'] > 1.5 * df['vol_ma']) & (df['adx'] > 20)
        df.loc[base & (df['close'] > df['dc_hi']), ['enter_long', 'enter_tag']] = (1, 'dc_break_up')
        df.loc[base & (df['close'] < df['dc_lo']), ['enter_short', 'enter_tag']] = (1, 'dc_break_dn')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df['close'] < df['ex_lo'], ['exit_long', 'exit_tag']] = (1, 'dc_exit')
        df.loc[df['close'] > df['ex_hi'], ['exit_short', 'exit_tag']] = (1, 'dc_exit')
        return df

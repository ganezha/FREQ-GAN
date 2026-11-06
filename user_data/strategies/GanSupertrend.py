# Supertrend flip with EMA200 regime filter; exit on opposite flip. Long + short.
import talib.abstract as ta
from pandas import DataFrame
from GanBase import GanBase
from gan_common import supertrend


class GanSupertrend(GanBase):
    timeframe = '1h'
    minimal_roi = {"0": 0.15}
    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.06
    trailing_only_offset_is_reached = True

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['st'] = supertrend(df, 10, 3.0)
        df['ema200'] = ta.EMA(df, timeperiod=200)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        flip_up = (df['st'] == 1) & (df['st'].shift(1) == -1)
        flip_dn = (df['st'] == -1) & (df['st'].shift(1) == 1)
        df.loc[flip_up & (df['close'] > df['ema200']) & (df['volume'] > 0), ['enter_long', 'enter_tag']] = (1, 'st_flip_up')
        df.loc[flip_dn & (df['close'] < df['ema200']) & (df['volume'] > 0), ['enter_short', 'enter_tag']] = (1, 'st_flip_dn')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df['st'] == -1, ['exit_long', 'exit_tag']] = (1, 'st_flip')
        df.loc[df['st'] == 1, ['exit_short', 'exit_tag']] = (1, 'st_flip')
        return df

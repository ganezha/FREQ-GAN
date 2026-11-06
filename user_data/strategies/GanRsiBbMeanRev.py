# Mean reversion: Bollinger band extremes + RSI, only in low-trend regimes (ADX filter). Long + short.
import talib.abstract as ta
from pandas import DataFrame
from freqtrade.strategy import IntParameter
from technical import qtpylib
from GanBase import GanBase


class GanRsiBbMeanRev(GanBase):
    timeframe = '15m'
    minimal_roi = {"0": 0.03, "120": 0.015, "360": 0.005}
    stoploss = -0.08          # = ~4% price move at 2x
    rsi_low = IntParameter(20, 35, default=30, space='buy')
    rsi_high = IntParameter(65, 80, default=70, space='sell')
    adx_max = IntParameter(20, 40, default=30, space='buy')

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        bb = qtpylib.bollinger_bands(qtpylib.typical_price(df), window=20, stds=2)
        df['bb_l'], df['bb_m'], df['bb_u'] = bb['lower'], bb['mid'], bb['upper']
        df['rsi'] = ta.RSI(df, timeperiod=14)
        df['adx'] = ta.ADX(df, timeperiod=14)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        rng = (df['adx'] < self.adx_max.value) & (df['volume'] > 0)
        df.loc[rng & (df['close'] < df['bb_l']) & (df['rsi'] < self.rsi_low.value), ['enter_long', 'enter_tag']] = (1, 'bb_rsi_low')
        df.loc[rng & (df['close'] > df['bb_u']) & (df['rsi'] > self.rsi_high.value), ['enter_short', 'enter_tag']] = (1, 'bb_rsi_high')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df['close'] > df['bb_m'], ['exit_long', 'exit_tag']] = (1, 'bb_mid')
        df.loc[df['close'] < df['bb_m'], ['exit_short', 'exit_tag']] = (1, 'bb_mid')
        return df

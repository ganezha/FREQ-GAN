# Multi-timeframe: 1h trend (EMA50 vs EMA200 + slope) decides side, 15m RSI pullback times the entry. Long + short.
import talib.abstract as ta
from pandas import DataFrame
from freqtrade.strategy import IntParameter, informative
from GanBase import GanBase


class GanMtfTrendRsi(GanBase):
    timeframe = '15m'
    minimal_roi = {"0": 0.035, "240": 0.02, "720": 0.01}
    stoploss = -0.08
    rsi_buy = IntParameter(25, 45, default=35, space='buy')
    rsi_sell = IntParameter(55, 75, default=65, space='sell')

    @informative('1h')
    def populate_indicators_1h(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['ema50'] = ta.EMA(df, timeperiod=50)
        df['ema200'] = ta.EMA(df, timeperiod=200)
        df['ema50_slope'] = df['ema50'] - df['ema50'].shift(5)
        return df

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['rsi'] = ta.RSI(df, timeperiod=14)
        df['ema20'] = ta.EMA(df, timeperiod=20)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        up = (df['ema50_1h'] > df['ema200_1h']) & (df['ema50_slope_1h'] > 0)
        dn = (df['ema50_1h'] < df['ema200_1h']) & (df['ema50_slope_1h'] < 0)
        v = df['volume'] > 0
        df.loc[v & up & (df['rsi'] < self.rsi_buy.value) & (df['rsi'] > df['rsi'].shift(1)), ['enter_long', 'enter_tag']] = (1, 'mtf_up_rsi_dip')
        df.loc[v & dn & (df['rsi'] > self.rsi_sell.value) & (df['rsi'] < df['rsi'].shift(1)), ['enter_short', 'enter_tag']] = (1, 'mtf_dn_rsi_pop')
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[(df['rsi'] > 70) | (df['ema50_1h'] < df['ema200_1h']), ['exit_long', 'exit_tag']] = (1, 'mtf_exit')
        df.loc[(df['rsi'] < 30) | (df['ema50_1h'] > df['ema200_1h']), ['exit_short', 'exit_tag']] = (1, 'mtf_exit')
        return df

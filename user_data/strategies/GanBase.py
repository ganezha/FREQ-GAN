# FREQ-GAN base: futures, long+short, fixed modest leverage. Not a strategy by itself.
from freqtrade.strategy import IStrategy


class GanBase(IStrategy):
    INTERFACE_VERSION = 3
    can_short = True
    use_exit_signal = True
    exit_profit_only = False
    process_only_new_candles = True
    startup_candle_count = 240
    order_types = {'entry': 'limit', 'exit': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
    LEVERAGE = 2.0

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return min(self.LEVERAGE, max_leverage)

# 4h variant of GanConnorsRsi2 (own file so hyperopt parameters export cleanly).
from GanConnorsRsi2 import GanConnorsRsi2


class GanConnorsRsi2_4h(GanConnorsRsi2):
    timeframe = '4h'
    startup_candle_count = 220

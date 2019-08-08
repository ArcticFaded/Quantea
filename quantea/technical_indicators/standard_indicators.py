from ta.momentum import (
    rsi, tsi
)
from ta.trend import (
    macd, macd_signal, macd_diff, 
    ema_indicator, trix, dpo, 
    kst, kst_sig, aroon_up, aroon_down
)
from ta.volatility import (
    bollinger_mavg, bollinger_hband, bollinger_lband, 
    bollinger_hband_indicator, bollinger_lband_indicator, donchian_channel_hband, 
    donchian_channel_lband, donchian_channel_hband_indicator, donchian_channel_lband_indicator
)

class BaseTechnicalIndicator():
    """
    Example Usage
    """
    def __init__(self, indicator):
        self.indicator = indicator

    def to_column(self, close):
        return self.indicator(close)

class BollingerBand(BaseTechnicalIndicator):
    """
    Bollinger Band is a lagging indicator which tracks an N day movement
    """

    def __init__(self, N_day):
        super().__init__(
            indicator=lambda x: bollinger_mavg(x, N_day)
        )
        self.lookback_window = N_day

class MACD(BaseTechnicalIndicator):
    """
    Moving Average Convergence Divergence (MACD)

    Compares two N1 and N2 day averages to detect stock trend movement
    """

    def __init__(self, N1, N2):
        super().__init__(
            indicator=lambda x: macd(x, N1, N2)
        )
        self.lookback_window = max(N1, N2)

class EMA(BaseTechnicalIndicator):
    """
    Exponential Moving Average (EMA)

    considers a relatively short N-day period and gets the exponentatial average
    """
    def __init__(self, N_day):
        super().__init__(
            indicator=lambda x: ema_indicator(x, N_day)
        )

        self.lookback_window = N_day

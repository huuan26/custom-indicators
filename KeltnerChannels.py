import backtrader as bt


class AncKeltnerChannels(bt.Indicator):
    """
    Keltner Channels Indicator.
    Formula:
      - Mid: EMA(20)
      - Upper: Mid + (2.0 * ATR)
      - Lower: Mid - (2.0 * ATR)
    Lines:
      - mid, upper, lower
      - trend_state: Signal for strategy logic
    """
    lines = ('mid', 'upper', 'lower', 'trend_state',)

    params = (
        ('ema_period', 20),
        ('atr_period', 10),
        ('multiplier', 2.0),
    )

    plotinfo = dict(plot=True, subplot=False, plotname='Keltner Channels', overlay=True)
    plotlines = dict(
        mid=dict(color='blue', linestyle='--'),
        upper=dict(color='green'),
        lower=dict(color='red'),
        trend_state=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.mid = bt.indicators.EMA(
            self.data.close,
            period=self.params.ema_period
        )
        self.atr = bt.indicators.ATR(
            self.data,
            period=self.params.atr_period
        )
        self.lines.upper = self.lines.mid + (self.atr * self.params.multiplier)
        self.lines.lower = self.lines.mid - (self.atr * self.params.multiplier)

    def next(self):
        close = self.data.close[0]
        if close > self.lines.upper[0]:
            self.lines.trend_state[0] = 1.0  # Super Uptrend
        elif close < self.lines.lower[0]:
            self.lines.trend_state[0] = -1.0  # Super Downtrend
        elif close > self.lines.mid[0]:
            self.lines.trend_state[0] = 0.5  # Uptrend Zone
        elif close < self.lines.mid[0]:
            self.lines.trend_state[0] = -0.5  # Downtrend Zone
        else:
            self.lines.trend_state[0] = 0.0
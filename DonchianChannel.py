import backtrader as bt


class AncDonchianChannels(bt.Indicator):
    """
    Donchian Channels Indicator.
    Lines:
      - upper: Highest High of N periods
      - lower: Lowest Low of N periods
      - mid: Average of Upper and Lower
      - signal:
          1: New High Breakout (Long)
         -1: New Low Breakdown (Short)
    """
    lines = ('upper', 'lower', 'mid', 'signal',)

    params = (
        ('period', 20),
    )

    plotinfo = dict(plot=True, subplot=False, plotname='Donchian Channels', overlay=True)
    plotlines = dict(
        upper=dict(color='green', ls='--'),
        lower=dict(color='red', ls='--'),
        mid=dict(color='blue'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.upper = bt.indicators.Highest(self.data.high, period=self.params.period)
        self.lines.lower = bt.indicators.Lowest(self.data.low, period=self.params.period)
        self.lines.mid = (self.lines.upper + self.lines.lower) / 2

    def next(self):
        self.lines.signal[0] = 0
        # Close > Previous High -> Breakout
        prev_high_period = max(self.data.high.get(ago=-1, size=self.params.period))
        prev_low_period = min(self.data.low.get(ago=-1, size=self.params.period))
        close = self.data.close[0]
        if close > prev_high_period:
            self.lines.signal[0] = 1  # Breakout Long
        elif close < prev_low_period:
            self.lines.signal[0] = -1  # Breakdown Short

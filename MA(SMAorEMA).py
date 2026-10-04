import backtrader as bt


class AncMA(bt.Indicator):
    """
    Moving Average Indicator (SMA/EMA)
    - Mode: 0 for SMA, 1 for EMA
    - Output:
        + ma: Moving average value
        + signal: 1 (Uptrend), -1 (Downtrend)
    """
    lines = ('ma', 'signal',)

    params = (
        ('period', 20),
        ('method', 0),  # 0: SMA, 1: EMA
    )

    plotinfo = dict(plot=True, plotname='Trend MA', overlay=True)

    def __init__(self):
        if self.params.method == 0: # SMA
            self.lines.ma = bt.indicators.SimpleMovingAverage(
                self.data.close, period=self.params.period
            )
            self.plotinfo['plotname'] = f'SMA ({self.params.period})'
        else: # EMA
            self.lines.ma = bt.indicators.ExponentialMovingAverage(
                self.data.close, period=self.params.period
            )
            self.plotinfo['plotname'] = f'EMA ({self.params.period})'

    def next(self):
        # Quant Logic
        # Close > MA -> Signal = 1 (Uptrend)
        # Close < MA -> Signal = -1 (Downtrend)

        if self.data.close[0] > self.lines.ma[0]:
            self.lines.signal[0] = 1
        elif self.data.close[0] < self.lines.ma[0]:
            self.lines.signal[0] = -1
        else:
            self.lines.signal[0] = 0

        spread_pct = (self.data.close[0] - self.lines.ma[0]) / self.lines.ma[0] * 100  # Percentage deviation
        # Use spread_pct to distinguish explosive breakouts from steady trends
import backtrader as bt


class AncFibonacci(bt.Indicator):
    """
    Dynamic Fibonacci Retracement Levels.
    Automatically identifies High/Low over a 'lookback' period.
    Lines:
      - fib_236, fib_382, fib_500, fib_618
      - signal:
          1: Bounce from Support (Buy Zone)
         -1: Breakdown Support (Sell Zone)
    """
    lines = ('fib_236', 'fib_382', 'fib_500', 'fib_618', 'signal',)

    params = (
        ('period', 50),
        ('tolerance', 1),
    )

    plotinfo = dict(plot=True, subplot=False, plotname='Auto Fib', overlay=True)
    plotlines = dict(
        fib_236=dict(color='gray', linestyle='--', _name='23.6%'),
        fib_382=dict(color='orange', linestyle='--', _name='38.2%'),
        fib_500=dict(color='blue', _name='50.0%'),
        fib_618=dict(color='red', _name='61.8% (Golden)'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        self.swing_high = bt.indicators.Highest(self.data.high, period=self.params.period)
        self.swing_low = bt.indicators.Lowest(self.data.low, period=self.params.period)
        self.range = self.swing_high - self.swing_low

        self.lines.fib_236 = self.swing_high - (self.range * 0.236)
        self.lines.fib_382 = self.swing_high - (self.range * 0.382)
        self.lines.fib_500 = self.swing_high - (self.range * 0.500)
        self.lines.fib_618 = self.swing_high - (self.range * 0.618)

    def next(self):
        self.lines.signal[0] = 0
        close = self.data.close[0]

        # Condition: Price touches 61.8% level but closes above it
        tolerance = self.params.tolerance
        golden_level = self.lines.fib_618[0]

        # Long bounce setup at 61.8% Golden Ratio
        if self.data.low[0] <= (golden_level + tolerance) and close > golden_level:
            self.lines.signal[0] = 1

        # Breakdown below 61.8% level
        elif close < (golden_level - tolerance):
            self.lines.signal[0] = -1  # Trend Broken -> Short
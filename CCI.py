import backtrader as bt


class AncCCI(bt.Indicator):
    """
    Commodity Channel Index (CCI) Implementation.
    Standard Period: 14 or 20.
    Lines:
      - cci: The CCI value.
      - signal:
          2: Extreme Overbought (> 200)
          1: Strong Uptrend (> 100)
          0: Noise Zone (-100 to 100)
         -1: Strong Downtrend (< -100)
         -2: Extreme Oversold (< -200)
    """
    lines = ('cci', 'signal',)

    params = (
        ('period', 14),
        ('factor', 0.015),
        ('upper_band', 100.0),
        ('lower_band', -100.0),
        ('extreme_band', 200.0),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='CCI System')
    plotlines = dict(
        cci=dict(color='orange', _name='CCI Line'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.cci = bt.indicators.CommodityChannelIndex(
            self.data,
            period=self.params.period,
            factor=self.params.factor
        )

    def next(self):
        val = self.lines.cci[0]

        if val > self.params.extreme_band:
            self.lines.signal[0] = 2  # Extreme Overbought (>200) -> Potential Reversal Short
        elif val > self.params.upper_band:
            self.lines.signal[0] = 1  # Momentum Breakout (>100) -> Trend-following Long
        elif val < -self.params.extreme_band:
            self.lines.signal[0] = -2  # Extreme Oversold (<-200) -> Potential Reversal Long
        elif val < self.params.lower_band:
            self.lines.signal[0] = -1  # Momentum Breakdown (<-100) -> Trend-following Short
        else:
            self.lines.signal[0] = 0  # Neutral Noise Zone -> No Trade
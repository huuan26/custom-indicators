import backtrader as bt


class AncROC(bt.Indicator):
    """
Rate of Change (ROC) Indicator
    Lines:
      - roc: The percentage change value
      - signal:
          1: Bullish Zero Cross (Buy)
         -1: Bearish Zero Cross (Sell)
          2: Overbought Warning
         -2: Oversold Warning
    """
    lines = ('roc', 'signal',)

    params = (
        ('period', 12),
        ('upper_extreme', 5),
        ('lower_extreme', -5),
        ('zero_line', 0),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='VN30 ROC')
    plotlines = dict(
        roc=dict(color='blue', _name='ROC %'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.roc = bt.indicators.ROC(
            self.data,
            period=self.params.period
        )

    def next(self):
        self.lines.signal[0] = 0
        roc = self.lines.roc[0]
        roc_prev = self.lines.roc[-1]

        if roc > self.params.upper_extreme:
            self.lines.signal[0] = 2  # Overbought

        elif roc < self.params.lower_extreme:
            self.lines.signal[0] = -2  # Oversold

        # Bullish Zero Cross
        elif roc_prev < self.params.zero_line and roc > self.params.zero_line:
            self.lines.signal[0] = 1

        # Bearish Zero Cross
        elif roc_prev > self.params.zero_line and roc < self.params.zero_line:
            self.lines.signal[0] = -1  
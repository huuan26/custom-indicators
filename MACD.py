import backtrader as bt


class AncMACD(bt.Indicator):
    """
    MACD Indicator with Histogram analysis.
    Lines:
      - macd: The MACD line (Difference between Fast and Slow EMA)
      - signal: The Signal line (EMA of MACD line)
      - histo: The MACD Histogram (MACD - Signal)
    """
    lines = ('macd', 'signal', 'histo',)

    params = (
        ('period_me1', 12),
        ('period_me2', 26),
        ('period_signal', 9),  # Signal
    )

    plotinfo = dict(plot=True, plotname='MACD & Histo', subplot=True)
    plotlines = dict(
        histo=dict(_method='bar', alpha=0.50, width=1.0)  # histogram
    )

    def __init__(self):
        macd_ind = bt.indicators.MACDHisto(
            self.data.close,
            period_me1=self.params.period_me1,
            period_me2=self.params.period_me2,
            period_signal=self.params.period_signal
        )

        self.lines.macd = macd_ind.macd
        self.lines.signal = macd_ind.signal
        self.lines.histo = macd_ind.histo

    def next(self):
        market_state = 0  # 0: Neutral/Sideway
        # Market regime classification logic
        if self.lines.macd[0] > 0 and self.lines.histo[0] > 0:
            if self.lines.histo[0] > self.lines.histo[-1]:
                market_state = 2  # Strong Uptrend
            else:
                market_state = 1  # Weakening Uptrend

        elif self.lines.macd[0] < 0 and self.lines.histo[0] < 0:
            if self.lines.histo[0] < self.lines.histo[-1]:
                market_state = -2  # Strong Downtrend
            else:
                market_state = -1  # Weakening Downtrend

        # market_state can be used as an entry filter
        # Example: Restrict Long entries to market_state >= 1
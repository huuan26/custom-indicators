import backtrader as bt


class AncMFI(bt.Indicator):
    """
    Money Flow Index (MFI) - Volume Weighted RSI.
    Standard Period: 14.
    Lines:
      - mfi: The MFI value (0-100)
      - signal:
          2: Oversold Reversal Buy (< 20)
          1: Bullish Trend (> 50)
         -1: Bearish Trend (< 50)
         -2: Overbought Reversal Sell (> 80)
    """
    lines = ('mfi', 'signal',)

    params = (
        ('period', 14),
        ('upper_band', 80),
        ('lower_band', 20),
        ('mid_band', 50),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='MFI System')
    plotlines = dict(
        mfi=dict(color='purple', _name='MFI Line'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.mfi = bt.indicators.MFI(
            self.data,
            period=self.params.period
        )

    def next(self):
        mfi = self.lines.mfi[0]
        self.lines.signal[0] = 0

        if mfi > self.params.upper_band:
            self.lines.signal[0] = -2  # Overbought
        elif mfi < self.params.lower_band:
            self.lines.signal[0] = 2  # Oversold
        elif mfi > self.params.mid_band:
            self.lines.signal[0] = 1  # Bullish bias (> 50)
        else:  # mfi < 50
            self.lines.signal[0] = -1  # Bearish bias (< 50)
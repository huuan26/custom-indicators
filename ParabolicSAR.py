import backtrader as bt

class AncParabolicSAR(bt.Indicator):
    """
    Parabolic SAR Indicator with Flip Signals.
    Lines:
      - sar: The SAR value dots.
      - signal:
          1: Bullish Reversal (Flip Up)
         -1: Bearish Reversal (Flip Down)
          0: Continuation
    """
    lines = ('sar', 'signal',)

    params = (
        ('period', 0.02),
        ('afmax', 0.20),
    )

    plotinfo = dict(plot=True, subplot=False, plotname='Parabolic SAR')
    plotlines = dict(
        sar=dict(color='black', _method='point', markersize=4),  # (Dots)
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.sar = bt.indicators.ParabolicSAR(
            self.data,
            period=self.params.period,
            afmax=self.params.afmax
        )

    def next(self):
        self.lines.signal[0] = 0
        is_uptrend = self.data.close[0] > self.lines.sar[0]
        was_uptrend = self.data.close[-1] > self.lines.sar[-1]

        if is_uptrend and not was_uptrend:
            self.lines.signal[0] = 1
            # Bullish continuation signal

        elif not is_uptrend and was_uptrend:
            self.lines.signal[0] = -1
            # Bearish continuation signal
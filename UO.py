import backtrader as bt


class AncUO(bt.Indicator):
    """
    Ultimate Oscillator (UO) - 3 Timeframes (7, 14, 28).
    Lines:
      - uo: Ultimate Oscillator value (0-100)
      - signal:
          2: Potential Long Reversal (Oversold < 30)
          1: Bullish Trend Continuation (> 50)
          0: Neutral
         -1: Bearish Trend Continuation (< 50)
         -2: Potential Short Reversal (Overbought > 70)
    """
    lines = ('uo', 'signal',)

    params = (
        ('p1', 7),
        ('p2', 14),
        ('p3', 28),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Ultimate Osc')
    plotlines = dict(
        uo=dict(color='purple', _name='UO Line'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.uo = bt.indicators.UltimateOscillator(
            self.data,
            p1=self.params.p1,
            p2=self.params.p2,
            p3=self.params.p3
        )

    def next(self):
        self.lines.signal[0] = 0
        uo_val = self.lines.uo[0]

        # Reversal triggers
        if uo_val > 70:
            self.lines.signal[0] = -2  # Overbought Reversal

        elif uo_val < 30:
            self.lines.signal[0] = 2  # Oversold Reversal

        elif uo_val > 50:
            self.lines.signal[0] = 1  # Bullish Trend Bias

        elif uo_val < 50:
            self.lines.signal[0] = -1  # Bearish Trend Bias
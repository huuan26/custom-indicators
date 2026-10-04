import backtrader as bt


class AncEOM(bt.Indicator):
    """
    Ease of Movement (EOM) Indicator.
    Formula: ((H+L)/2 - (Hp+Lp)/2) / ((Vol/Scale) / (H-L))
    Lines:
      - eom: The smoothed EOM line (SMA)
      - zero: The zero baseline
      - signal:
          1: Easy Rise (Positive & Rising)
         -1: Easy Fall (Negative & Falling)
          0: Struggle/Congestion (Near Zero)
    """
    lines = ('eom', 'zero', 'signal',)

    params = (
        ('period', 14),
        ('vol_scale', 1000000),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Ease of Movement')
    plotlines = dict(
        eom=dict(color='blue', _name='EOM (14)'),
        zero=dict(color='gray', linestyle='--', _name='Zero Line'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        # Compute Midpoint Distance (DM)
        midpoint = (self.data.high + self.data.low) / 2.0
        dm = midpoint - midpoint(-1)

        # Box Ratio = (Volume / Scale) / (High - Low)
        high_low = self.data.high - self.data.low
        high_low = bt.If(high_low == 0, 0.0001, high_low)

        box_ratio = (self.data.volume / self.params.vol_scale) / high_low

        # Compute Raw 1-period EOM
        # EOM = DM / BR
        box_ratio = bt.If(box_ratio == 0, 0.0001, box_ratio)
        raw_eom = dm / box_ratio

        # Smooth using SMA
        self.lines.eom = bt.indicators.SMA(raw_eom, period=self.params.period)
        self.lines.zero = bt.Constant(0)

    def next(self):
        self.lines.signal[0] = 0
        val = self.lines.eom[0]
        prev = self.lines.eom[-1]

        if val > 0 and val > prev:
            self.lines.signal[0] = 1

        elif val < 0 and val < prev:
            self.lines.signal[0] = -1

        # Congestion / Low-conviction state
        elif abs(val) < 0.5:  # Threshold depends on vol_scale
            self.lines.signal[0] = 0
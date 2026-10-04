import backtrader as bt


class AncPivotPoints(bt.Indicator):
    """
    Standard Pivot Points Indicator.
    Formula:
      - P = (H + L + C) / 3
      - R1 = 2*P - L
      - S1 = 2*P - H
      - R2 = P + (H - L)
      - S2 = P - (H - L)
    Lines:
      - p: Pivot Point (Main Trend)
      - r1, r2: Resistance Levels
      - s1, s2: Support Levels
    """
    lines = ('p', 'r1', 's1', 'r2', 's2',)

    plotinfo = dict(plot=True, subplot=False, overlay=True)
    plotlines = dict(
        p=dict(color='black', linestyle='-', linewidth=1.5, _name='Pivot (P)'),
        r1=dict(color='red', linestyle='--', _name='R1'),
        s1=dict(color='green', linestyle='--', _name='S1'),
        r2=dict(color='red', _name='R2'),
        s2=dict(color='green', _name='S2'),
    )

    def __init__(self):
        h = self.data.high(-1)
        l = self.data.low(-1)
        c = self.data.close(-1)

        self.lines.p = (h + l + c) / 3.0

        # Resistance 1 & Support 1
        self.lines.r1 = (2 * self.lines.p) - l
        self.lines.s1 = (2 * self.lines.p) - h

        # Resistance 2 & Support 2
        self.lines.r2 = self.lines.p + (h - l)
        self.lines.s2 = self.lines.p - (h - l)

    def next(self):
        close = self.data.close[0]
        p = self.lines.p[0]

        if close > p:
            pass
        elif close < p:
            pass

        # if close > r1: Strong Momentum Up -> Target R2
        # if close < s1: Strong Momentum Down -> Target S2
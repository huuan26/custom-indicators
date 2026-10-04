import backtrader as bt


class AncCMO(bt.Indicator):
    """
    Chande Momentum Oscillator (CMO).
    Formula: (SumUp - SumDown) / (SumUp + SumDown) * 100
    Range: -100 to +100
    Default Period: 9 (Standard for short-term trading)
    """
    lines = ('cmo',)

    params = (
        ('period', 9),
    )

    plotinfo = dict(plotymargin=0.05, plotyhlines=[-50, 0, 50])

    def __init__(self):
        change = self.data.close - self.data.close(-1)

        up_movement = bt.If(change > 0, change, 0)

        # If change < 0, take absolute value
        down_movement = bt.If(change < 0, -change, 0.0)

        # SumN
        sum_up = bt.ind.SumN(up_movement, period=self.p.period)
        sum_down = bt.ind.SumN(down_movement, period=self.p.period)

        total_movement = sum_up + sum_down + 0.000001

        self.lines.cmo = 100.0 * (sum_up - sum_down) / total_movement

    def get_market_state(self):
        """
        Helper for strategy logic specific to VN30F1M
        2: Overbought (> 50)
        1: Bull Trend (10 to 50)
        0: Sideway (-10 to 10)
        -1: Bear Trend (-10 to -50)
        -2: Oversold (< -50)
        """
        val = self.lines.cmo[0]
        if val >= 50: return 2
        if 10 <= val < 50: return 1
        if -10 < val < 10: return 0
        if -50 < val <= -10: return -1
        if val <= -50: return -2
        return 0

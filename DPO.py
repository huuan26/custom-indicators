import backtrader as bt


class AncDPO(bt.Indicator):
    """
    DPO.
    Thresholds: +/- 15 points for Extremes.
    """
    lines = ('dpo', 'signal',)
    params = (
        ('period', 20),
        ('extreme', 15),
        ('trend', 5),
    )

    plotinfo = dict(subplot=True, plotname='VN30 DPO Cycle')
    plotlines = dict(
        dpo=dict(color='blue', _name='DPO Points'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        sma = bt.indicators.SMA(self.data, period=self.params.period)
        shift = int(self.params.period / 2) + 1
        self.lines.dpo = self.data.close - sma(-shift)

    def next(self):
        self.lines.signal[0] = 0
        dpo = self.lines.dpo[0]


        # Overbought (> 15 pts) -> Extended rally (Potential reversal)
        if dpo > self.params.extreme:
            self.lines.signal[0] = 2

            # Oversold (< -15 pts) -> Extended sell-off (Potential reversal)
        elif dpo < -self.params.extreme:
            self.lines.signal[0] = -2

        # Uptrend (+5 to +15 pts)
        elif dpo > self.params.trend:
            self.lines.signal[0] = 1

        # Downtrend (-5 to -15 pts)
        elif dpo < -self.params.trend:
            self.lines.signal[0] = -1

        # Sideways (-5 to +5 pts)
        else:
            self.lines.signal[0] = 0
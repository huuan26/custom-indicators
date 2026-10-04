import backtrader as bt


class AncSuperTrend(bt.Indicator):
    """
    SuperTrend Indicator implementation.
    Params:
      - period: Period for ATR
      - multiplier: Multiplier for ATR
    Lines:
      - supertrend: The main trend line
      - direction: 1 for Uptrend (Green), -1 for Downtrend (Red)
    """
    lines = ('supertrend', 'direction',)
    params = (
        ('period', 10),
        ('multiplier', 3),
    )

    plotinfo = dict(plot=True, subplot=False, plotname='SuperTrend')
    plotlines = dict(
        supertrend=dict(color='green', linewidth=2),  # Default styling
        direction=dict(_plotskip=True)
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.params.period)
        self.hl2 = (self.data.high + self.data.low) / 2

    def next(self):
        basic_upper = self.hl2[0] + (self.params.multiplier * self.atr[0])
        basic_lower = self.hl2[0] - (self.params.multiplier * self.atr[0])

        if len(self) == 1:
            self.lines.supertrend[0] = basic_lower
            self.lines.direction[0] = 1
            return

        prev_final_upper = self.lines.supertrend[-1] if self.lines.direction[-1] == -1 else basic_upper
        prev_final_lower = self.lines.supertrend[-1] if self.lines.direction[-1] == 1 else basic_lower

        # Logic: Final Upper Band
        # If previous close < previous Final Upper -> Upper band cannot rise
        if self.data.close[-1] <= self.lines.supertrend[-1] and self.lines.direction[-1] == -1:
            pass


        # 1. Determine Final Bands based on previous bar
        # If Close[-1] > SuperTrend[-1] (Prior Uptrend): Lower Band cannot decline
        # If Close[-1] < SuperTrend[-1] (Prior Downtrend): Upper Band cannot increase

        trend = self.lines.direction[-1]
        st_prev = self.lines.supertrend[-1]

        if trend == 1:  # Active Uptrend
            if basic_lower > st_prev:
                final_lower = basic_lower
            else:
                final_lower = st_prev

            # Check for trend reversal
            if self.data.close[0] < final_lower:
                trend = -1
                self.lines.supertrend[0] = basic_upper  # Reversal to Downtrend: initialize with Basic Upper
            else:
                self.lines.supertrend[0] = final_lower

        else:  # Active Downtrend (trend == -1)
            if basic_upper < st_prev:
                final_upper = basic_upper
            else:
                final_upper = st_prev

            # Check for trend reversal
            if self.data.close[0] > final_upper:
                trend = 1
                self.lines.supertrend[0] = basic_lower  # Reversal to Uptrend: initialize with Basic Lower
            else:
                self.lines.supertrend[0] = final_upper

        self.lines.direction[0] = trend
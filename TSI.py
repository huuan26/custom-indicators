import backtrader as bt


class AncTSI(bt.Indicator):
    """
    True Strength Index (TSI) - Double Smoothed Momentum.
    Parameters: Long(25), Short(13), Signal(7-13).
    """
    lines = ('tsi', 'signal', 'market_state',)
    params = (
        ('long_period', 25),
        ('short_period', 13),
        ('signal_period', 7),
    )

    plotinfo = dict(subplot=True, plotname='TSI (25,13)')
    plotlines = dict(
        tsi=dict(color='blue', _name='TSI'),
        signal=dict(color='red', linestyle='--', _name='Signal'),
        market_state=dict(_plotskip=True)
    )

    def __init__(self):
        pc = self.data.close - self.data.close(-1)
        abs_pc = abs(pc)

        ema_pc_long = bt.indicators.EMA(pc, period=self.params.long_period)
        ema_abs_pc_long = bt.indicators.EMA(abs_pc, period=self.params.long_period)

        ema_pc_short = bt.indicators.EMA(ema_pc_long, period=self.params.short_period)
        ema_abs_pc_short = bt.indicators.EMA(ema_abs_pc_long, period=self.params.short_period)

        denominator = bt.If(ema_abs_pc_short == 0, 0.0001, ema_abs_pc_short)
        self.lines.tsi = (ema_pc_short / denominator) * 100

        # Signal
        self.lines.signal = bt.indicators.EMA(self.lines.tsi, period=self.params.signal_period)

    def next(self):
        self.lines.market_state[0] = 0
        tsi = self.lines.tsi[0]


        # (+/- 40)
        if tsi > 40:
            self.lines.market_state[0] = 2  # Overbought
        elif tsi < -40:
            self.lines.market_state[0] = -2  # Oversold

        # (+/- 25)
        elif tsi > 25:
            self.lines.market_state[0] = 1  # Strong Bullish Trend (> 25)
        elif tsi < -25:
            self.lines.market_state[0] = -1  # Strong Bearish Trend (< -25)

        # (-10 to 10)
        elif -10 <= tsi <= 10:
            self.lines.market_state[0] = 0  # Sideways Consolidation (-10 to 10)
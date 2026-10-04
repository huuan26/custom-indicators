import backtrader as bt


class AncATR_TrailingStop(bt.Indicator):
    """
    ATR Indicator & Trailing Stop.
    Lines:
      - atr: The ATR value (Volatillity in Points)
      - trail_stop_long: Stoploss level for Long positions
      - trail_stop_short: Stoploss level for Short positions
    """
    lines = ('atr', 'trail_stop_long', 'trail_stop_short',)

    params = (
        ('period', 14),
        ('multiplier', 2.5),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='ATR & Trailing Stop')
    plotlines = dict(
        atr=dict(color='orange', _name='ATR Value'),
        trail_stop_long=dict(_plotskip=True),
        trail_stop_short=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.atr = bt.indicators.ATR(
            self.data,
            period=self.params.period
        )

        # Long Stop = Highest High - (ATR * Multiplier)
        # Short Stop = Lowest Low + (ATR * Multiplier)

        self.highest = bt.ind.Highest(self.data.high, period=self.params.period)
        self.lowest = bt.ind.Lowest(self.data.low, period=self.params.period)

        self.lines.trail_stop_long = self.highest - (self.lines.atr * self.params.multiplier)
        self.lines.trail_stop_short = self.lowest + (self.lines.atr * self.params.multiplier)

    def next(self):
        atr_val = self.lines.atr[0]

        market_state = "Normal"

        if atr_val > 8.0:
            market_state = "Extreme Volatility (Panic/FOMO)"
            # Reduce position size, widen stop loss

        elif atr_val < 2.0:
            market_state = "Squeeze (Accumulation)"
            # Await breakout confirmation, avoid range trading

        else:
            market_state = "Trending/Normal"
            # Follow primary trend direction
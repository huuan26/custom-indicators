import backtrader as bt
import math


class AncVWAP(bt.Indicator):
    """
    Intraday VWAP with Standard Deviation Bands.
    Resets automatically at the start of each new trading session.
    Lines:
      - vwap: Main VWAP line
      - upper: VWAP + 2*StdDev
      - lower: VWAP - 2*StdDev
    """
    lines = ('vwap', 'upper', 'lower',)

    params = (
        ('devfactor', 2),
    )

    plotinfo = dict(plot=True, subplot=False, plotname='Intraday VWAP', overlay=True)
    plotlines = dict(
        vwap=dict(color='orange', linewidth=2),
        upper=dict(color='gray', linestyle='--'),
        lower=dict(color='gray', linestyle='--')
    )

    def __init__(self):
        # Cumulative state trackers
        self.cum_pv = 0
        self.cum_vol = 0
        self.cum_sq_pv = 0

    def next(self):
        dt = self.data.datetime.date(0)  # Detect daily session change
        dt_prev = self.data.datetime.date(-1)

        if dt != dt_prev:
            self.cum_pv = 0
            self.cum_vol = 0
            self.cum_sq_pv = 0

        price = (self.data.high[0] + self.data.low[0] + self.data.close[0]) / 3
        vol = self.data.volume[0]

        self.cum_pv += price * vol
        self.cum_vol += vol

        if self.cum_vol == 0:
            self.lines.vwap[0] = price
            self.lines.upper[0] = price
            self.lines.lower[0] = price
            return

        vwap_val = self.cum_pv / self.cum_vol
        self.lines.vwap[0] = vwap_val

        # Var = (Sum(Vol * Price^2) / Sum(Vol)) - VWAP^2
        self.cum_sq_pv += vol * (price * price)
        weighted_avg_sq_price = self.cum_sq_pv / self.cum_vol

        variance = weighted_avg_sq_price - (vwap_val * vwap_val)
        std_dev = math.sqrt(max(0, variance))

        self.lines.upper[0] = vwap_val + (self.params.devfactor * std_dev)
        self.lines.lower[0] = vwap_val - (self.params.devfactor * std_dev)

        # if price > self.lines.upper[0]: State = "Overbought (Revert likely)"
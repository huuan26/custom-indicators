import backtrader as bt
import math


class AncHV(bt.Indicator):
    """
    Historical Volatility (HV).
    Formula: StdDev(Ln(Close/PrevClose), period) * Sqrt(252) * 100
    Lines:
      - hv: The annualized volatility in percentage
      - signal:
          0: Normal
          1: Squeeze (Low Vol - Prep for Move)
          2: High Vol (Danger Zone)
    """
    lines = ('hv', 'signal',)

    params = (
        ('period', 20),
        ('annualize_factor', 252),  # 252 trading days per year
        ('squeeze_threshold', 15),  # Squeeze threshold (HV < 15%)
        ('danger_threshold', 40),  # High volatility danger zone (HV > 40%)
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Historical Volatility (HV)')
    plotlines = dict(
        hv=dict(color='purple', _name='HV %'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        # ln(Close / Close_prev)
        # bt.indicators.Log(target) computes ln(target)
        log_returns = bt.indicators.Log(self.data.close / self.data.close(-1))

        std_dev = bt.indicators.StdDev(log_returns, period=self.params.period)

        # Annualize
        # HV = StdDev * Sqrt(252) * 100
        sqrt_factor = math.sqrt(self.params.annualize_factor)
        self.lines.hv = std_dev * sqrt_factor * 100

    def next(self):
        self.lines.signal[0] = 0
        hv_val = self.lines.hv[0]

        # Squeeze
        if hv_val < self.params.squeeze_threshold:
            self.lines.signal[0] = 1

        # High Volatility -> Elevated risk environment
        elif hv_val > self.params.danger_threshold:
            self.lines.signal[0] = 2

        # HV is non-directional; it quantifies magnitude, not trend direction.
        # Combine HV with trend filters (e.g. MA, MACD):
        # - Rising HV + Rising Price -> Strong Bullish momentum
        # - Rising HV + Falling Price -> Strong Bearish liquidation
        # - Falling HV -> Market consolidation / Stand aside
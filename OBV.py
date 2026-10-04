import backtrader as bt


class AncOBV(bt.Indicator):
    """
    On-Balance Volume (OBV).
    Lines:
      - obv: The cumulative volume line
      - obv_ma: SMA of OBV (Signal line)
      - divergence:
          1: Bullish Divergence Potential
         -1: Bearish Divergence Potential
    """
    lines = ('obv', 'obv_ma', 'divergence',)

    params = (
        ('ma_period', 20),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='OBV System')
    plotlines = dict(
        obv=dict(color='blue', _name='OBV'),
        obv_ma=dict(color='orange', linestyle='--', _name='Signal MA'),
        divergence=dict(_plotskip=True)
    )

    def __init__(self):
        self.lines.obv = bt.indicators.OnBalanceVolume(self.data)
        self.lines.obv_ma = bt.indicators.SMA(self.lines.obv, period=self.params.ma_period)

    def next(self):
        self.lines.divergence[0] = 0

        # OBV above its MA -> Net institutional accumulation -> Long bias
        # OBV below its MA -> Net institutional distribution -> Short bias
        # Price prints new 20-period high while OBV fails to confirm
        price_high_20 = max(self.data.close.get(ago=0, size=20))
        obv_high_20 = max(self.lines.obv.get(ago=0, size=20))

        is_price_new_high = self.data.close[0] >= price_high_20
        is_obv_new_high = self.lines.obv[0] >= obv_high_20

        if is_price_new_high and not is_obv_new_high:
            self.lines.divergence[0] = -1  # Bearish Divergence

        elif self.data.close[0] <= min(self.data.close.get(ago=0, size=20)) and \
                self.lines.obv[0] > min(self.lines.obv.get(ago=0, size=20)):
            self.lines.divergence[0] = 1  # Bullish Divergence
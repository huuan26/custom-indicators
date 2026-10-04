import backtrader as bt


class VN30_AccumulationDistribution(bt.Indicator):
    """
    Accumulation/Distribution (A/D) Line.
    Measures cumulative money flow based on close location relative to high-low range.

    Lines:
      - ad: The Cumulative A/D Line
      - signal:
          1: Money Flowing IN (A/D Rising)
         -1: Money Flowing OUT (A/D Falling)
          2: Bullish Divergence Warning (Trend Change)
         -2: Bearish Divergence Warning (Trend Change)
    """
    lines = ('ad', 'signal',)
    params = (
        ('slope_period', 5),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Acc/Dist Line')
    plotlines = dict(
        ad=dict(color='orange', _name='A/D Line'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        # MFM = ((C - L) - (H - C)) / (H - L)
        range_hl = self.data.high - self.data.low

        # range = 0, MFM = 0
        mfm = bt.If(range_hl == 0, 0,
                    ((self.data.close - self.data.low) - (self.data.high - self.data.close)) / range_hl)

        mfv = mfm * self.data.volume

        self.lines.ad = bt.indicators.Recursive(lambda ad_prev, mfv_curr: ad_prev + mfv_curr, mfv)

    def next(self):
        self.lines.signal[0] = 0

        ad_curr = self.lines.ad[0]
        ad_prev = self.lines.ad[-self.params.slope_period]

        price_curr = self.data.close[0]
        price_prev = self.data.close[-self.params.slope_period]

        if ad_curr > ad_prev:
            self.lines.signal[0] = 1  # Net Money Flow IN (Rising A/D)
        else:
            self.lines.signal[0] = -1  # Net Money Flow OUT (Falling A/D)

        # Bearish Divergence (Price rising while A/D falling) -> Short Signal
        if price_curr > price_prev and ad_curr < ad_prev:
            self.lines.signal[0] = -2

         # Bullish Divergence (Price falling while A/D rising) -> Long Signal
        elif price_curr < price_prev and ad_curr > ad_prev:
            self.lines.signal[0] = 2
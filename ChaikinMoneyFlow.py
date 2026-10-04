import backtrader as bt

class AncChaikinMoneyFlow(bt.Indicator):
    """
    Chaikin Money Flow (CMF) Indicator.
    Formula: Sum(MFV, n) / Sum(Volume, n)
    Lines:
      - cmf: The CMF value (-1 to 1)
      - signal:
          1: Strong Accumulation (> 0.25)
          0: Neutral
         -1: Strong Distribution (< -0.25)
    """
    lines = ('cmf', 'signal',)

    params = (
        ('period', 20),
        ('upper_band', 0.25),
        ('lower_band', -0.25),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Chaikin Money Flow')
    plotlines = dict(
        cmf=dict(color='green', _name='CMF'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        # MFM = ((Close - Low) - (High - Close)) / (High - Low)
        #     = (2 * Close - Low - High) / (High - Low)
        high_low_range = self.data.high - self.data.low
        mfm = (2 * self.data.close - self.data.low - self.data.high) / (high_low_range + 0.0001)

        mfv = mfm * self.data.volume
        sum_mfv = bt.indicators.SumN(mfv, period=self.params.period)
        sum_vol = bt.indicators.SumN(self.data.volume, period=self.params.period)
        self.lines.cmf = sum_mfv / (sum_vol + 0.0001)

    def next(self):
        cmf_val = self.lines.cmf[0]
        self.lines.signal[0] = 0

        if cmf_val > self.params.upper_band:
            self.lines.signal[0] = 1  # Uptrend strong

        elif cmf_val < self.params.lower_band:
            self.lines.signal[0] = -1  # Downtrend strong

        # Logic Zero Line Cross (Optional)
        # if self.lines.cmf[-1] < 0 and self.lines.cmf[0] > 0: Buy Signal Weak
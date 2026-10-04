import backtrader as bt


class AncVolumeOscillator(bt.Indicator):
    """
    Volume Oscillator (VO) - Percentage Difference.
    Formula: 100 * (ShortSMA - LongSMA) / LongSMA
    Lines:
      - vo: The oscillator value
      - signal:
          1: Trend Confirmation (VO > 0)
          0: Weak/Sideway (VO < 0)
         -1: Divergence Warning (Price Up, VO Down or vice versa - Logic handled in Strategy)
    """
    lines = ('vo', 'signal',)

    params = (
        ('short_period', 5),
        ('long_period', 20),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Volume Osc')
    plotlines = dict(
        vo=dict(color='purple', _name='Vol Osc %'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        sma_short = bt.indicators.SMA(self.data.volume, period=self.params.short_period)
        sma_long = bt.indicators.SMA(self.data.volume, period=self.params.long_period)
        self.lines.vo = 100 * (sma_short - sma_long) / (sma_long + 0.0001)

    def next(self):
        vo_val = self.lines.vo[0]

        if vo_val > 0:
            self.lines.signal[0] = 1
        else:
            self.lines.signal[0] = 0 
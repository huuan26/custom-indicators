import backtrader as bt

class AncWilliamsR(bt.Indicator):
    """
    Williams %R Indicator Implementation.
    Scale: -100 to 0.
    Lines:
      - williamsr: The main line.
    """
    lines = ('williamsr',)

    params = (
        ('period', 14),
        ('upper_band', -20),
        ('lower_band', -80),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Williams %R')
    plotlines = dict(
        williamsr=dict(color='purple', _name='%R Line')
    )

    def __init__(self):
        self.lines.williamsr = bt.indicators.WilliamsR(
            self.data,
            period=self.params.period
        )

    def next(self):
        wr = self.lines.williamsr
        if wr[-1] > self.params.upper_band and wr[0] < self.params.upper_band:
            pass
        elif wr[-1] < self.params.lower_band and wr[0] > self.params.lower_band:
            pass
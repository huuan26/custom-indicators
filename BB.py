import backtrader as bt


class AncBollingerBands(bt.Indicator):
    """
    Bollinger Bands.
    Lines:
      - mid: SMA 20
      - top: Upper Band
      - bot: Lower Band
      - squeeze: 1 if squeezing, 0 otherwise
    """
    lines = ('mid', 'top', 'bot', 'squeeze',)

    params = (
        ('period', 20),
        ('devfactor', 2),
        ('squeeze_threshold', 0.015),
    )

    plotinfo = dict(plot=True, subplot=False, plotname='Bollinger Bands', overlay=True)
    plotlines = dict(
        mid=dict(color='red', linestyle='--'),
        top=dict(color='black'),
        bot=dict(color='black'),
        squeeze=dict(_plotskip=True)
    )

    def __init__(self):
        bb = bt.indicators.BollingerBands(
            self.data.close,
            period=self.params.period,
            devfactor=self.params.devfactor
        )

        self.lines.mid = bb.mid
        self.lines.top = bb.top
        self.lines.bot = bb.bot

        self.bandwidth = (self.lines.top - self.lines.bot) / self.lines.mid

    def next(self):
        if self.bandwidth[0] < self.params.squeeze_threshold:
            self.lines.squeeze[0] = 1
        else:
            self.lines.squeeze[0] = 0

        # If Price > Top: "Trend Run Up"
        # If Price < Bot: "Trend Run Down"
        # If Squeeze == 1: "Sideways/Accumulation"
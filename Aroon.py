import backtrader as bt


class AncAroon(bt.Indicator):
    """
    Aroon Indicator optimized for Trend Strength.
    Lines:
      - up: Aroon Up
      - down: Aroon Down
      - signal:
          2: Strong Trend UP (> 70)
          1: Start Trend UP (Crossover)
          0: Sideway / Weak (< 50)
         -1: Start Trend DOWN (Crossover)
         -2: Strong Trend DOWN (> 70)
    """
    lines = ('up', 'down', 'signal',)

    params = (
        ('period', 25),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Aroon System')
    plotlines = dict(
        up=dict(color='green', _name='Aroon Up'),
        down=dict(color='red', _name='Aroon Down'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        aroon = bt.indicators.Aroon(self.data, period=self.params.period)
        self.lines.up = aroon.aroonup
        self.lines.down = aroon.aroondown

    def next(self):
        up = self.lines.up[0]
        down = self.lines.down[0]
        up_prev = self.lines.up[-1]
        down_prev = self.lines.down[-1]

        self.lines.signal[0] = 0

        if up > 70 and down < 30:
            self.lines.signal[0] = 2  # Strong Bullish -> Hold Long

        elif down > 70 and up < 30:
            self.lines.signal[0] = -2  # Strong Bearish -> Hold Short

        elif up_prev < down_prev and up > down:
            self.lines.signal[0] = 1  # Bullish Cross -> Open Long

        elif down_prev < up_prev and down > up:
            self.lines.signal[0] = -1  # Bearish Cross -> Open Short

        # (Sideway)
        elif up < 50 and down < 50:
            self.lines.signal[0] = 0 
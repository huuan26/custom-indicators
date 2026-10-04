import backtrader as bt


class AncKST(bt.Indicator):
    """
    Know Sure Thing (KST) Indicator.
    Formula: Sum of 4 Weighted Smoothed ROCs.
    Lines:
      - kst: The KST line
      - signal: The Signal line (SMA 9 of KST)
      - crossover:
          1: Golden Cross (Buy Signal)
         -1: Death Cross (Sell Signal)
    """
    lines = ('kst', 'signal', 'crossover',)

    params = (
        ('roc1', 10), ('sma1', 10),
        ('roc2', 15), ('sma2', 10),
        ('roc3', 20), ('sma3', 10),
        ('roc4', 30), ('sma4', 15),
        ('sig_period', 9),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='KST Indicator')
    plotlines = dict(
        kst=dict(color='green', _name='KST Line'),
        signal=dict(color='red', linestyle='--', _name='Signal Line'),
        crossover=dict(_plotskip=True)
    )

    def __init__(self):
        r1 = bt.indicators.ROC(self.data, period=self.params.roc1)
        r2 = bt.indicators.ROC(self.data, period=self.params.roc2)
        r3 = bt.indicators.ROC(self.data, period=self.params.roc3)
        r4 = bt.indicators.ROC(self.data, period=self.params.roc4)

        rc1 = bt.indicators.SMA(r1, period=self.params.sma1)
        rc2 = bt.indicators.SMA(r2, period=self.params.sma2)
        rc3 = bt.indicators.SMA(r3, period=self.params.sma3)
        rc4 = bt.indicators.SMA(r4, period=self.params.sma4)

        # Weight: RC1*1, RC2*2, RC3*3, RC4*4
        self.lines.kst = (rc1 * 1) + (rc2 * 2) + (rc3 * 3) + (rc4 * 4)

        self.lines.signal = bt.indicators.SMA(self.lines.kst, period=self.params.sig_period)

    def next(self):
        self.lines.crossover[0] = 0
        kst = self.lines.kst[0]
        sig = self.lines.signal[0]
        kst_prev = self.lines.kst[-1]
        sig_prev = self.lines.signal[-1]

        # Bullish Crossover (Golden Cross)
        if kst_prev < sig_prev and kst > sig:
            self.lines.crossover[0] = 1  # Bullish Golden Cross

        # Bearish Crossover (Death Cross)
        elif kst_prev > sig_prev and kst < sig:
            self.lines.crossover[0] = -1  # Bearish Death Cross

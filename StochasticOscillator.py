import backtrader as bt


class AncStochasticOscillator(bt.Indicator):
    """
    Stochastic Oscillator Indicator
    Lines:
      - percK: The fast line
      - percD: The slow line (Signal)
      - signal:
          1: Buy Signal (Cross Up in Oversold)
         -1: Sell Signal (Cross Down in Overbought)
    """
    lines = ('percK', 'percD', 'signal',)

    params = (
        ('period', 14),  # %K
        ('period_dfast', 3),  # %K
        ('period_dslow', 3),  # %D
        ('upper_band', 80),
        ('lower_band', 20),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Stochastic')
    plotlines = dict(
        percK=dict(color='blue', _name='%K'),
        percD=dict(color='red', _name='%D', ls='--'),
        signal=dict(_plotskip=True)
    )

    def __init__(self):
        stoch = bt.indicators.Stochastic(
            self.data,
            period=self.params.period,
            period_dfast=self.params.period_dfast,
            period_dslow=self.params.period_dslow
        )

        self.lines.percK = stoch.percK
        self.lines.percD = stoch.percD

    def next(self):
        self.lines.signal[0] = 0

        # Long: Bullish cross in Oversold territory (<20)
        if self.lines.percK[-1] < self.lines.percD[-1] and \
                self.lines.percK[0] > self.lines.percD[0] and \
                self.lines.percK[0] < self.params.lower_band:
            self.lines.signal[0] = 1

        # Short: Bearish cross in Overbought territory (>80)
        elif self.lines.percK[-1] > self.lines.percD[-1] and \
                self.lines.percK[0] < self.lines.percD[0] and \
                self.lines.percK[0] > self.params.upper_band:
            self.lines.signal[0] = -1  
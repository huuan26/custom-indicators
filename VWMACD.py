import backtrader as bt


class AncVWMACD(bt.Indicator):
    """
    Volume Weighted MACD (VW-MACD).
    Formula:
      - VWMA = Sum(Price * Vol, N) / Sum(Vol, N)
      - VW-MACD = VWMA(Fast) - VWMA(Slow)
      - Signal = EMA(VW-MACD, Signal_Period)
    Lines:
      - vwmacd
      - signal
      - histo
    """
    lines = ('vwmacd', 'signal', 'histo',)

    params = (
        ('fast_period', 12),
        ('slow_period', 26),
        ('signal_period', 9),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='VW-MACD')
    plotlines = dict(
        vwmacd=dict(color='blue', _name='VW-MACD'),
        signal=dict(color='red', linestyle='--', _name='Signal'),
        histo=dict(_method='bar', alpha=0.5, _name='Histogram')
    )

    def __init__(self):
        # Price * Volume
        pv = self.data.close * self.data.volume

        # VWMA Fast (12)
        # Numerator: Cumulative Price * Volume over 12 periods
        sum_pv_fast = bt.indicators.SumN(pv, period=self.params.fast_period)
        # Denominator: Cumulative Volume over 12 periods
        sum_vol_fast = bt.indicators.SumN(self.data.volume, period=self.params.fast_period)
        # VWMA Fast
        vwma_fast = sum_pv_fast / (sum_vol_fast + 0.0001)

        # VWMA Slow (26)
        sum_pv_slow = bt.indicators.SumN(pv, period=self.params.slow_period)
        sum_vol_slow = bt.indicators.SumN(self.data.volume, period=self.params.slow_period)
        vwma_slow = sum_pv_slow / (sum_vol_slow + 0.0001)

        # VW-MACD Line
        self.lines.vwmacd = vwma_fast - vwma_slow

        # Signal line: EMA of VW-MACD
        self.lines.signal = bt.indicators.EMA(self.lines.vwmacd, period=self.params.signal_period)

        # Histogram
        self.lines.histo = self.lines.vwmacd - self.lines.signal

    def next(self):
        # 1: Uptrend, -1: Downtrend
        if self.lines.vwmacd[0] > self.lines.signal[0]:
            if self.lines.vwmacd[0] > 0:
                # Bullish volume-momentum alignment
                pass

        # Volume-price divergence detection (concept)
        # if Price is High and VW-MACD is Lower -> Divergence
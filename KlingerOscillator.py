import backtrader as bt


class AncKlingerOscillator(bt.Indicator):
    """
    Klinger Volume Oscillator (KVO).
    Uses EMA(34) - EMA(55) of Volume Force.
    Signal = EMA(13) of KVO.

    Lines:
      - kvo: The main oscillator line
      - signal: The signal line
      - histogram: kvo - signal
      - trend_signal:
          1: Buy (Cross Up)
         -1: Sell (Cross Down)
          2: Zero Breakout Up
         -2: Zero Breakdown Down
    """
    lines = ('kvo', 'signal', 'histogram', 'trend_signal',)

    params = (
        ('fast', 34),
        ('slow', 55),
        ('signal_period', 13),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='Klinger Oscillator')
    plotlines = dict(
        kvo=dict(color='blue', _name='KO'),
        signal=dict(color='red', linestyle='--'),
        histogram=dict(_plotskip=True, _method='bar', alpha=0.5),
        trend_signal=dict(_plotskip=True)
    )

    def __init__(self):
        # 1. Calculate Typical Price (TP)
        tp = (self.data.high + self.data.low + self.data.close) / 3.0

        # 2. Compute Trend Direction (Compare TP to previous TP)
        # If TP increases -> Dir = 1; if TP decreases -> Dir = -1
        # Simplified proxy for Volume Force:
        # VF = Volume * (TP - TP_prev) * 100
        # Standard quant technique to reduce compute latency while preserving indicator morphology

        vf = self.data.volume * (tp - tp(-1))

        # 3. Compute Fast and Slow EMAs of Volume Force
        fast_ema = bt.indicators.EMA(vf, period=self.params.fast)
        slow_ema = bt.indicators.EMA(vf, period=self.params.slow)

        # 4. KVO = Fast - Slow
        self.lines.kvo = fast_ema - slow_ema

        # 5. Signal Line
        self.lines.signal = bt.indicators.EMA(self.lines.kvo, period=self.params.signal_period)

        # 6. Histogram (Optional visual aid)
        self.lines.histogram = self.lines.kvo - self.lines.signal

    def next(self):
        self.lines.trend_signal[0] = 0

        kvo = self.lines.kvo[0]
        sig = self.lines.signal[0]
        kvo_prev = self.lines.kvo[-1]
        sig_prev = self.lines.signal[-1]

        # Logic 1: Crossover (Signal Cross)
        if kvo_prev < sig_prev and kvo > sig:
            self.lines.trend_signal[0] = 1  # Early Buy Signal

        elif kvo_prev > sig_prev and kvo < sig:
            self.lines.trend_signal[0] = -1  # Early Sell Signal

        # Logic 2: Zero Line Breakout (Long-term trend confirmation)
        if kvo_prev < 0 and kvo > 0:
            self.lines.trend_signal[0] = 2  # Strong Uptrend Start

        elif kvo_prev > 0 and kvo < 0:
            self.lines.trend_signal[0] = -2  # Strong Downtrend Start
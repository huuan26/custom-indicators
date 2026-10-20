# Custom Indicators Library for Backtrader

A comprehensive suite of 31 custom technical indicators built for quantitative trading research, technical analysis, and algorithmic strategy execution on the **Backtrader** framework.

---

## 📌 Features

- **31 Custom Indicators**: High-performance implementations across trend, momentum, volatility, volume, and support/resistance categories.
- **Backtrader Native**: Inherits from `bt.Indicator`, fully compatible with Backtrader line series, indicators chaining, and strategy plotting.
- **Quant & Research Ready**: Optimized calculations using NumPy/Pandas compatible logic.

---

## 📂 Included Indicators

### Trend & Moving Averages
- **AncMA**: Flexible moving average with multiple smoothing types (SMA, EMA, WMA, etc.)
- **AncADX**: Average Directional Index with directional movement lines ($+DI$, $-DI$)
- **AncAroon**: Aroon Up, Aroon Down, and Aroon Oscillator
- **AncSuperTrend**: ATR-based trend following stop-and-reverse band
- **AncParabolicSAR**: Parabolic Stop and Reverse price tracking
- **AncKST**: "Know Sure Thing" multi-timeframe momentum oscillator

### Volatility & Channels
- **AncATR_TrailingStop**: Average True Range trailing stop calculation
- **AncBollingerBands**: Dynamic volatility bands with standard deviation channels
- **AncDonchianChannels**: Highest high and lowest low price channels
- **AncKeltnerChannels**: ATR-based envelope bands around an exponential moving average
- **AncHV**: Historical Volatility estimator

### Momentum & Oscillators
- **AncMACD**: Moving Average Convergence Divergence with signal and histogram
- **AncVWMACD**: Volume-Weighted MACD incorporating trade volume into trend conviction
- **AncStochasticOscillator**: Fast and Slow Stochastic $\%K$ and $\%D$
- **AncCCI**: Commodity Channel Index
- **AncCMO**: Chande Momentum Oscillator
- **AncROC**: Rate of Change price momentum
- **AncTSI**: True Strength Index double-smoothed momentum
- **AncUO**: Ultimate Oscillator multi-timeframe weighted momentum
- **AncWilliamsR**: Williams %R overbought/oversold oscillator
- **AncDPO**: Detrended Price Oscillator isolating cyclical components

### Volume & Money Flow
- **AncVWAP**: Volume-Weighted Average Price intraday and period benchmark
- **AncOBV**: On-Balance Volume cumulative volume flow
- **AncMFI**: Money Flow Index volume-weighted RSI
- **AncChaikinMoneyFlow**: Chaikin Money Flow ($CMF$) accumulator
- **AncKlingerOscillator**: Klinger Volume Oscillator for long-term money flow trends
- **AncVolumeOscillator**: Percentage volume oscillator between short and long volume EMAs
- **AncEOM**: Ease of Movement relating price change to volume
- **VN30_AccumulationDistribution**: Tailored accumulation/distribution metric

### Support & Resistance
- **AncPivotPoints**: Standard, Fibonacci, Camarilla, and Woodie pivot points
- **AncFibonacci**: Dynamic retracement and extension levels

---

## 🚀 Installation

Ensure you have Python 3.8+ installed along with dependencies:

```bash
git clone https://github.com/huuan26/custom-indicators.git
cd custom-indicators
pip install -r requirements.txt
```

---

## 💡 Quick Usage Example

```python
import backtrader as bt
from custom_indicators import AncSuperTrend, AncVWAP, AncBollingerBands

class CustomStrategy(bt.Strategy):
    def __init__(self):
        # Initialize custom indicators
        self.supertrend = AncSuperTrend(self.data, period=10, multiplier=3.0)
        self.bb = AncBollingerBands(self.data.close, period=20, devfactor=2.0)
        self.vwap = AncVWAP(self.data)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.supertrend.lines.supertrend[0]:
                self.buy()
        else:
            if self.data.close[0] < self.supertrend.lines.supertrend[0]:
                self.close()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # Add data feed & strategy here...
    cerebro.addstrategy(CustomStrategy)
    # cerebro.run()
```

---

## 📄 License

This project is licensed under the MIT License.

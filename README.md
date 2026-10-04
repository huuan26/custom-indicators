# Custom Indicators for Backtrader (`custom-indicators`)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Backtrader](https://img.shields.io/badge/Engine-Backtrader-orange.svg)](https://www.backtrader.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modular, production-grade library of **31 custom technical indicators** built on the **Backtrader** event-driven framework, designed for quantitative finance, systematic alpha research, and algorithmic trading execution.

---

## 📌 Features & Indicator Catalog

The library organizes 31 custom indicators across 4 core quantitative disciplines:

### 1. Momentum & Oscillators
| File | Class Name | Description |
| :--- | :--- | :--- |
| `WilliamsR.py` | `AncWilliamsR` | Williams %R oscillator bounded between -100 and 0. |
| `StochasticOscillator.py` | `AncStochasticOscillator` | Dual-line Stochastic Oscillator (%K, %D) with oversold/overbought crosses. |
| `CCI.py` | `AncCCI` | Commodity Channel Index with extreme mean-reversion and trend breakout states. |
| `CMO.py` | `AncCMO` | Chande Momentum Oscillator with scale -100 to +100. |
| `ROC.py` | `AncROC` | Rate of Change percentage momentum oscillator with zero-line cross detection. |
| `TSI.py` | `AncTSI` | True Strength Index with double exponential momentum smoothing. |
| `UO.py` | `AncUO` | Ultimate Oscillator aggregating weighted momentum across 3 distinct cycle lengths (7, 14, 28). |
| `KST.py` | `AncKST` | Martin Pring's Know Sure Thing (KST) summing 4 weighted smoothed ROC cycles. |
| `MACD.py` | `AncMACD` | Moving Average Convergence Divergence with 4-state histogram trend regime tracking. |
| `VWMACD.py` | `AncVWMACD` | Volume-Weighted MACD weighting price movements by transaction volume. |

### 2. Trend Identification
| File | Class Name | Description |
| :--- | :--- | :--- |
| `ADX.py` | `AncADX` | Average Directional Movement Index quantifying directional trend strength. |
| `Aroon.py` | `AncAroon` | Aroon Up, Down, and Oscillator tracking elapsed time since periodic highs and lows. |
| `SuperTrend.py` | `AncSuperTrend` | Volatility-adaptive ATR trailing stop trendline with dynamic band clamping. |
| `ParabolicSAR.py` | `AncParabolicSAR` | Parabolic Stop and Reverse tracking trend acceleration and reversal flips. |
| `DPO.py` | `AncDPO` | Detrended Price Oscillator isolating cyclical components by eliminating long-term trends. |
| `MovingAverage.py` | `AncMA` | Dual-mode Moving Average supporting both SMA and EMA with percentage spread tracking. |

### 3. Volatility & Price Envelopes
| File | Class Name | Description |
| :--- | :--- | :--- |
| `ATR.py` | `AncATR_TrailingStop` | Average True Range trailing stop mechanism for adaptive stop-loss and risk management. |
| `BB.py` | `AncBollingerBands` | Bollinger Bands with bandwidth volatility squeeze detection. |
| `DonchianChannel.py` | `AncDonchianChannels` | Donchian Channels plotting periodic high-low bands for breakout identification. |
| `KeltnerChannels.py` | `AncKeltnerChannels` | Keltner Channels combining an EMA centerline with ATR volatility bands. |
| `HV.py` | `AncHV` | Annualized Historical Volatility computed from continuous log returns. |
| `Fibonacci.py` | `AncFibonacci` | Dynamic Fibonacci retracement levels (23.6%, 38.2%, 50.0%, 61.8% Golden Ratio). |
| `PivotPoints.py` | `AncPivotPoints` | Classic technical pivot support and resistance price targets (P, R1, S1, R2, S2). |

### 4. Volume & Order Flow
| File | Class Name | Description |
| :--- | :--- | :--- |
| `ChaikinMoneyFlow.py` | `AncChaikinMoneyFlow` | Chaikin Money Flow (CMF) measuring institutional accumulation over volume. |
| `MFI.py` | `AncMFI` | Money Flow Index (Volume-Weighted RSI) with overbought/oversold boundaries. |
| `OBV.py` | `AncOBV` | On-Balance Volume with moving average trend filter and divergence detection. |
| `AccumulationDistribution.py` | `VN30_AccumulationDistribution` | Cumulative A/D line evaluating money flow location within the candle range. |
| `VolumeOscillator.py` | `AncVolumeOscillator` | Dual-moving average volume difference oscillator. |
| `VWAP.py` | `AncVWAP` | Intraday Volume-Weighted Average Price resetting daily with standard deviation bands. |
| `EOM.py` | `AncEOM` | Ease of Movement evaluating price velocity relative to volume density. |
| `KlingerOscillator.py` | `AncKlingerOscillator` | Klinger Volume Oscillator (KVO) capturing long-term volume flow dynamics. |

---

## 🚀 Quick Start

### Installation

Clone the repository into your strategy directory or Python environment:

```bash
git clone https://github.com/huuan26/custom-indicators.git
```

Ensure dependencies are installed:

```bash
pip install backtrader numpy pandas
```

### Usage Example

```python
import backtrader as bt
from custom_indicators import AncWilliamsR, AncSuperTrend, AncBollingerBands

class MomentumAlphaStrategy(bt.Strategy):
    params = (
        ('wr_period', 14),
        ('atr_period', 10),
        ('atr_multiplier', 3.0),
    )

    def __init__(self):
        # Initialize Custom Indicators
        self.wr = AncWilliamsR(self.data, period=self.params.wr_period)
        self.supertrend = AncSuperTrend(
            self.data, 
            period=self.params.atr_period, 
            multiplier=self.params.atr_multiplier
        )
        self.bb = AncBollingerBands(self.data, period=20, devfactor=2)

    def next(self):
        # Trend continuation rule
        if self.supertrend.lines.direction[0] == 1:
            # Bullish trend active
            if self.wr.lines.williamsr[0] < -80:
                # Oversold dip within uptrend
                if not self.position:
                    self.buy()
        elif self.supertrend.lines.direction[0] == -1:
            # Bearish trend active
            if self.position:
                self.close()
```

---

## 🛠️ Adding New Indicators

1. Create a new module `<IndicatorName>.py`.
2. Inherit from `backtrader.Indicator`.
3. Declare `lines`, `params`, and implement the quantitative logic in `__init__` or `next`.
4. Export the new class in `__init__.py`.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 👤 Author

**huuan26**
- GitHub: [@huuan26](https://github.com/huuan26)

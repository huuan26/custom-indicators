"""
Custom Indicators Library for Backtrader
========================================
A comprehensive suite of 31 custom technical indicators designed for quantitative
trading research and algorithmic strategy execution on the Backtrader framework.
"""

try:
    from .ADX import AncADX
    from .ATR import AncATR_TrailingStop
    from .AccumulationDistribution import VN30_AccumulationDistribution
    from .Aroon import AncAroon
    from .BB import AncBollingerBands
    from .CCI import AncCCI
    from .CMO import AncCMO
    from .ChaikinMoneyFlow import AncChaikinMoneyFlow
    from .DPO import AncDPO
    from .DonchianChannel import AncDonchianChannels
    from .EOM import AncEOM
    from .Fibonacci import AncFibonacci
    from .HV import AncHV
    from .KST import AncKST
    from .KeltnerChannels import AncKeltnerChannels
    from .KlingerOscillator import AncKlingerOscillator
    from .MACD import AncMACD
    from .MFI import AncMFI
    from .MovingAverage import AncMA
    from .OBV import AncOBV
    from .ParabolicSAR import AncParabolicSAR
    from .PivotPoints import AncPivotPoints
    from .ROC import AncROC
    from .StochasticOscillator import AncStochasticOscillator
    from .SuperTrend import AncSuperTrend
    from .TSI import AncTSI
    from .UO import AncUO
    from .VWAP import AncVWAP
    from .VWMACD import AncVWMACD
    from .VolumeOscillator import AncVolumeOscillator
    from .WilliamsR import AncWilliamsR
except ImportError:
    from ADX import AncADX
    from ATR import AncATR_TrailingStop
    from AccumulationDistribution import VN30_AccumulationDistribution
    from Aroon import AncAroon
    from BB import AncBollingerBands
    from CCI import AncCCI
    from CMO import AncCMO
    from ChaikinMoneyFlow import AncChaikinMoneyFlow
    from DPO import AncDPO
    from DonchianChannel import AncDonchianChannels
    from EOM import AncEOM
    from Fibonacci import AncFibonacci
    from HV import AncHV
    from KST import AncKST
    from KeltnerChannels import AncKeltnerChannels
    from KlingerOscillator import AncKlingerOscillator
    from MACD import AncMACD
    from MFI import AncMFI
    from MovingAverage import AncMA
    from OBV import AncOBV
    from ParabolicSAR import AncParabolicSAR
    from PivotPoints import AncPivotPoints
    from ROC import AncROC
    from StochasticOscillator import AncStochasticOscillator
    from SuperTrend import AncSuperTrend
    from TSI import AncTSI
    from UO import AncUO
    from VWAP import AncVWAP
    from VWMACD import AncVWMACD
    from VolumeOscillator import AncVolumeOscillator
    from WilliamsR import AncWilliamsR

__all__ = [
    'AncADX',
    'AncATR_TrailingStop',
    'VN30_AccumulationDistribution',
    'AncAroon',
    'AncBollingerBands',
    'AncCCI',
    'AncCMO',
    'AncChaikinMoneyFlow',
    'AncDPO',
    'AncDonchianChannels',
    'AncEOM',
    'AncFibonacci',
    'AncHV',
    'AncKST',
    'AncKeltnerChannels',
    'AncKlingerOscillator',
    'AncMACD',
    'AncMFI',
    'AncMA',
    'AncOBV',
    'AncParabolicSAR',
    'AncPivotPoints',
    'AncROC',
    'AncStochasticOscillator',
    'AncSuperTrend',
    'AncTSI',
    'AncUO',
    'AncVWAP',
    'AncVWMACD',
    'AncVolumeOscillator',
    'AncWilliamsR',
]

import backtrader as bt


class AncADX(bt.Indicator):
    """
    ADX Indicator with Directional Movement (DMI)
    Lines:
      - adx: Strength of the trend
      - plusDI: Positive Directional Indicator
      - minusDI: Negative Directional Indicator
    Params:
      - period: 14 (Standard)
    """
    lines = ('adx', 'plusDI', 'minusDI',)

    params = (
        ('period', 14),
    )

    plotinfo = dict(plot=True, subplot=True, plotname='ADX & DMI')

    def __init__(self):
        dmi = bt.indicators.DirectionalMovementIndex(
            self.data,
            period=self.params.period
        )

        self.lines.adx = dmi.adx
        self.lines.plusDI = dmi.plusDI
        self.lines.minusDI = dmi.minusDI

    def next(self):
        adx_val = self.lines.adx[0]
        p_di = self.lines.plusDI[0]
        m_di = self.lines.minusDI[0]

        trend_status = "Sideway"

        if adx_val > 25:
            if p_di > m_di:
                trend_status = "Strong Uptrend (15 Up / 5 Down)"
            elif m_di > p_di:
                trend_status = "Strong Downtrend (15 Down / 5 Up)"
        elif adx_val < 20:
            trend_status = "No Trend (10 Up / 10 Down)"

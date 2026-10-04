try:
    from .MovingAverage import AncMA
except ImportError:
    from MovingAverage import AncMA

__all__ = ['AncMA']

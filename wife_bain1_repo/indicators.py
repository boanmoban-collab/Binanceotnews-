"""
Technical Indicators & Market Analysis Module (Pure Python, No external TA-Lib dependency)
Computes RSI, EMA, Volatility, Spread, and Dip-Rebound Signals.
"""

from typing import List, Tuple, Optional


def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculates Relative Strength Index (RSI). Returns 50.0 if not enough data."""
    clean_prices = [p for p in prices if p is not None and isinstance(p, (int, float)) and p > 0]
    if len(clean_prices) < period + 1:
        return 50.0

    gains = []
    losses = []
    for i in range(1, len(clean_prices)):
        change = clean_prices[i] - clean_prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(change))

    # Initial average
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # Smoothed Wilder moving average
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return round(max(0.0, min(100.0, rsi)), 2)


def calculate_ema(prices: List[float], period: int) -> Optional[float]:
    """Calculates Exponential Moving Average (EMA)."""
    clean_prices = [p for p in prices if p is not None and isinstance(p, (int, float)) and p > 0]
    if len(clean_prices) < period or period <= 0:
        return None

    multiplier = 2.0 / (period + 1)
    ema = sum(clean_prices[:period]) / period
    for p in clean_prices[period:]:
        ema = (p - ema) * multiplier + ema
    return round(ema, 4)


def calculate_volatility_pct(highs: List[float], lows: List[float], current_price: float) -> float:
    """Calculates average high-low range percentage over recent bars."""
    if not highs or not lows or current_price <= 0:
        return 0.0

    count = min(len(highs), len(lows), 10)
    if count == 0:
        return 0.0

    ranges = []
    for h, l in zip(highs[-count:], lows[-count:]):
        if h is not None and l is not None and h >= l >= 0:
            ranges.append((h - l) / current_price * 100.0)

    return round(sum(ranges) / len(ranges), 3) if ranges else 0.0


def calculate_dip_and_rebound(
    closes: List[float], current_price: float, lookback: int = 15
) -> Tuple[float, float]:
    """
    Measures:
    1. dip_pct: How much the lowest point in lookback fell from the local swing high (%).
       Chronologically, the swing high must precede the swing low.
    2. rebound_pct: How much current price has bounced from that recent swing low (%).
    """
    clean_closes = [c for c in closes if c is not None and isinstance(c, (int, float)) and c > 0]
    if len(clean_closes) < 5 or current_price <= 0:
        return 0.0, 0.0

    window = clean_closes[-lookback:] if len(clean_closes) >= lookback else clean_closes
    n = len(window)

    # Find the swing high that precedes the lowest trough
    # We look for the peak within the first part of the window (up to n-2)
    peak = max(window)
    peak_idx = window.index(peak)

    if peak_idx >= n - 2:
        # If peak is at the very tip, market might be making new highs without having dipped
        earlier = window[:-2]
        if earlier:
            peak = max(earlier)
            peak_idx = window.index(peak)
        else:
            return 0.0, 0.0

    subsequent = window[peak_idx:]
    if not subsequent:
        return 0.0, 0.0

    trough = min(subsequent)
    if peak <= 0 or trough <= 0:
        return 0.0, 0.0

    dip_pct = ((peak - trough) / peak) * 100.0
    rebound_pct = ((current_price - trough) / trough) * 100.0 if trough > 0 else 0.0

    return round(max(0.0, dip_pct), 3), round(max(0.0, rebound_pct), 3)

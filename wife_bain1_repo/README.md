# ⚡ بوت بينانس سبوت اللحظي 24/7 (Binance Spot 24/7 Scalper Bot) - الكود الكامل والدليل الشامل

بوت تداول فوري آلي مخصص للعمل على منصة **Binance Spot** على مدار الساعة **24/7 دون أي تجميد أو توقف**، متوافق كلياً مع منصة السحاب **Railway** وخوادم Docker، ومجهز بنظام وقف الأرباح المتحرك (Trailing Take-Profit)، وحماية رأس المال، والتعويض التلقائي لرسوم التداول.

---

## 📑 فهرس المحتويات
1. [المميزات والتصحيحات الجوهرية](#-المميزات-والتصحيحات-الجوهرية)
2. [إعداد المتغيرات البيئية (Environment Variables)](#-إعداد-المتغيرات-البيئية)
3. [دليل النشر والتشغيل (Deployment Guide)](#-دليل-النشر-والتشغيل)
4. [جناح الاختبارات الآلية (Unit Tests)](#-جناح-الاختبارات-الآلية)
5. [الأكواد البرمجية الكاملة لجميع ملفات المشروع](#-الأكواد-البرمجية-الكاملة-لجميع-ملفات-المشروع)
- [config.py](#-configpy) : إعدادات البوت والتحقق من المتغيرات وأزواج التداول
- [indicators.py](#-indicatorspy) : مؤشرات التحليل الفني (RSI، الارتداد اللحظي، والتذبذب)
- [spot_engine.py](#-spot_enginepy) : محرك الصفقات الفورية وحساب الكميات والوقف المتحرك (Trailing Stop)
- [main.py](#-mainpy) : حلقة التداول اللحظي 24/7 وخادم لوحة التحكم وفحص الصحة
- [test_engine.py](#-test_enginepy) : جناح الاختبارات الآلية (Unit Tests) لسلامة العمليات الحسابية
- [requirements.txt](#-requirementstxt) : حزم بايثون الأساسية المطلوبة
- [Dockerfile](#-Dockerfile) : ملف بناء حاوية دوكر الجاهزة للتشغيل السحابي
- [Procfile](#-Procfile) : أمر تشغيل الخادم والعملية الرئيسية
- [railway.json](#-railwayjson) : إعدادات النشر على منصة Railway السحابية
- [railway.toml](#-railwaytoml) : تكوين النشر البديل لـ Railway
- [.env.example](#-envexample) : نموذج المتغيرات البيئية ومفاتيح الـ API
- [.github/workflows/ci.yml](#-github-workflows-ciyml) : سير عمل الفحص الآلي المستمر (GitHub Actions CI)

---

## 🎯 المميزات والتصحيحات الجوهرية

1. **التحويل الكامل إلى التداول الفوري (Binance Spot)**:
   - إلغاء الروافع المالية والمخاطر التصفوية نهائياً؛ التداول يتم بشراء العملة الأساسية وبيعها مقابل USDT في السوق الفوري.
2. **منع التجميد والتعافي التلقائي (Zero-Freeze Resilience)**:
   - **تعويض رسوم المنصة (Fee Compensation)**: عند إغلاق الصفقة، يقرأ المحرك رصيد العملة الحر الفعلي لتفادي فشل البيع بسبب خصم عمولة التداول.
   - **معالجة أخطاء 429 و 451**: نظام ذكي للانتظار التلقائي وإعادة المحاولة دون تعليق المعالج.
3. **استراتيجية القنص اللحظي السريع (Dip & Rebound + Trailing Take-Profit)**:
   - **رادار الهبوط والارتداد**: اشتراط حدوث القمة قبل القاع زمنياً لتفادي الدخول الخاطئ أثناء الصعود المتواصل.
   - **تأكيد التشبع (RSI Momentum)**: منع الشراء إذا كان مؤشر القوة النسبية أعلى من الحد المسموح.
   - **وقف الربح المتحرك (Trailing Stop)**: يلاحق السعر عند صعوده ويغلق الصفقة فور ارتداده بنسبة محددة لجني الأرباح.
4. **جلب قيود السوق اللحظية ديناميكياً (Dynamic LOT_SIZE & Precision)**:
   - اشتقاق عدد الخانات العشرية بدقة من مرشحات المنصة عبر مكتبة Decimal لمنع رفض الأوامر.
5. **لوحة تحكم مباشرة متجاوبة (Live Dark Dashboard)**:
   - واجهة ويب باللغتين العربية والإنجليزية مع فحص صحة مستمر (/health و /api/status).

---

## ⚙️ إعداد المتغيرات البيئية

| المتغير | القيمة الافتراضية | الشرح |
|---|---|---|
| `BINANCE_API_KEY` | - | مفتاح API الخاص ببينانس (مع تفعيل Spot Trading) |
| `BINANCE_API_SECRET` | - | الرمز السري لمفتاح الـ API |
| `LIVE_TRADING` | `false` | اجعلها `true` للتداول الحقيقي بالأموال الحقيقية |
| `SYMBOL` | `BTC/USDT` | زوج التداول الفوري (مثال: `BTC/USDT`, `ETH/USDT`, `SOL/USDT`) |
| `TARGET_ORDER_USD` | `11.0` | قيمة الصفقة بالدولار (يجب أن تكون ≥ $10) |
| `LOOP_INTERVAL_SEC` | `5.0` | سرعة دورة الفحص اللحظي بالثواني |
| `BUY_DIP_MIN_PCT` | `0.25` | الحد الأدنى لنسبة الهبوط اللحظي للدخول (%) |
| `BUY_REBOUND_CONFIRM_PCT` | `0.08` | نسبة تأكيد ارتداد السعر للدخول (%) |
| `BUY_RSI_MAX` | `48` | أقصى قيمة لمؤشر RSI للسماح بالشراء |
| `TRAILING_STOP_ENABLED` | `true` | تفعيل وقف الربح المتحرك |
| `TRAILING_ACTIVATION_PCT` | `0.35` | نسبة الصعود المطلوبة لتفعيل وقف الربح المتحرك (%) |
| `TRAILING_CALLBACK_PCT` | `0.15` | نسبة ارتداد السعر لإغلاق الصفقة بالربح المحقق (%) |
| `STOP_LOSS_PCT` | `0.80` | وقف الخسارة الصارم لحماية رأس المال (%) |
| `PORT` | `8080` | منفذ لوحة التحكم وفحص الصحة |

---

## 🚀 دليل النشر والتشغيل

### التشغيل عبر سحاب Railway:
1. ارفع المشروع إلى مستودعك على GitHub.
2. في لوحة **Railway**، اختر **New Project -> Deploy from GitHub repo**.
3. أضف المتغيرات في تبويب **Variables**.
4. سيبدأ البناء تلقائياً وتشغيل الخادم.

### التشغيل عبر Docker:
```bash
docker build -t binance-spot-bot .
docker run -d --name bot -p 8080:8080 --env-file .env binance-spot-bot
```

### التشغيل المحلي:
```bash
pip install -r requirements.txt
python main.py
```

---

## 🧪 جناح الاختبارات الآلية

يحتوي المشروع على ملف اختبارات شامل `test_engine.py` يفحص دقة مؤشر RSI، رادار الارتداد، تقريب الخانات العشرية، ودورة حياة الصفقة:
```bash
python -m unittest test_engine.py
```

---

## 💻 الأكواد البرمجية الكاملة لجميع ملفات المشروع

فيما يلي المحتوى البرمجي الكامل غير المنقوص لكل ملف من ملفات المشروع:

---

### 📄 `config.py`
**الوصف**: إعدادات البوت والتحقق من المتغيرات وأزواج التداول

```python
"""
Binance Spot 24/7 Scalper Bot Configuration
Handles environment variables, validation, and symbol formatting for Spot trading.
"""

import os
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback to standard library .env parser if python-dotenv is not installed
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass


def get_env_bool(key: str, default: bool = False) -> bool:
    val = os.getenv(key, "").strip().lower()
    if val in ("true", "1", "yes", "t", "on"):
        return True
    if val in ("false", "0", "no", "f", "off"):
        return False
    return default


def get_env_float(key: str, default: float) -> float:
    val = os.getenv(key, "").strip()
    if not val:
        return default
    try:
        return float(val)
    except ValueError:
        return default


def get_env_int(key: str, default: int) -> int:
    val = os.getenv(key, "").strip()
    if not val:
        return default
    try:
        return int(val)
    except ValueError:
        return default


def mask_key(key: Optional[str]) -> str:
    """Mask sensitive API key strings for safe diagnostic logging."""
    if not key or key.strip() in ("", "your_binance_api_key_here", "your_api_key"):
        return "NOT_SET"
    k = key.strip()
    if len(k) <= 8:
        return f"{k[:2]}...{k[-2:]} (len: {len(k)})"
    return f"{k[:4]}...{k[-4:]} (len: {len(k)})"


class Config:
    # -------------------------------------------------------------
    # API Credentials & Execution Mode (Binance Spot)
    # -------------------------------------------------------------
    API_KEY: str = os.getenv("BINANCE_API_KEY", "").strip()
    API_SECRET: str = os.getenv("BINANCE_API_SECRET", "").strip()
    LIVE_TRADING: bool = get_env_bool("LIVE_TRADING", False)
    TESTNET: bool = get_env_bool("TESTNET", False)
    BINANCE_PROXY: Optional[str] = os.getenv("BINANCE_PROXY", "").strip() or None

    # -------------------------------------------------------------
    # Spot Trading Pair & Sizing
    # -------------------------------------------------------------
    RAW_SYMBOL: str = os.getenv("SYMBOL", "BTC/USDT").strip().upper()

    @classmethod
    def get_spot_symbol(cls) -> str:
        """
        Normalize symbol to standard CCXT Spot format: 'BTC/USDT'
        Accepts: BTCUSDT, BTC/USDT, BTC_USDT, BTC-USDT
        """
        sym = cls.RAW_SYMBOL.replace("-", "/").replace("_", "/").replace(":", "/")
        if "/" in sym:
            parts = sym.split("/")
            return f"{parts[0]}/{parts[1]}"
        if sym.endswith("USDT"):
            return f"{sym[:-4]}/USDT"
        if sym.endswith("BUSD"):
            return f"{sym[:-4]}/BUSD"
        if sym.endswith("FDUSD"):
            return f"{sym[:-5]}/FDUSD"
        return f"{sym}/USDT"

    @classmethod
    def get_base_quote(cls) -> tuple[str, str]:
        sym = cls.get_spot_symbol()
        base, quote = sym.split("/")
        return base, quote

    @classmethod
    def get_binance_raw_symbol(cls) -> str:
        """Returns raw exchange symbol like BTCUSDT"""
        return cls.get_spot_symbol().replace("/", "")

    # Target order notional in quote currency (USDT) - automatically enforced >= $10.0 for Binance Spot
    _raw_target_usd = get_env_float("TARGET_ORDER_USD", 11.0)
    TARGET_ORDER_USD: float = max(10.5, _raw_target_usd) if _raw_target_usd > 0 else 11.0
    MAX_POSITIONS: int = get_env_int("MAX_POSITIONS", 1)

    # -------------------------------------------------------------
    # Timing & Frequency (Real-time scalping loop)
    # -------------------------------------------------------------
    LOOP_INTERVAL_SEC: float = get_env_float("LOOP_INTERVAL_SEC", 5.0)
    BUY_COOLDOWN_SEC: int = get_env_int("BUY_COOLDOWN_SEC", 60)

    # -------------------------------------------------------------
    # Entry Strategy: Confirmed Dip + Rebound + RSI Momentum
    # -------------------------------------------------------------
    BUY_DIP_MIN_PCT: float = get_env_float("BUY_DIP_MIN_PCT", 0.25)
    BUY_REBOUND_CONFIRM_PCT: float = get_env_float("BUY_REBOUND_CONFIRM_PCT", 0.08)
    BUY_RSI_MAX: float = get_env_float("BUY_RSI_MAX", 48.0)
    MIN_VOLATILITY_PCT: float = get_env_float("MIN_VOLATILITY_PCT", 0.20)
    MAX_SPREAD_PCT: float = get_env_float("MAX_SPREAD_PCT", 0.15)

    # -------------------------------------------------------------
    # Exit Strategy: Trailing Take-Profit & Capital Protection
    # -------------------------------------------------------------
    TRAILING_STOP_ENABLED: bool = get_env_bool("TRAILING_STOP_ENABLED", True)
    TRAILING_ACTIVATION_PCT: float = get_env_float("TRAILING_ACTIVATION_PCT", 0.35)
    TRAILING_CALLBACK_PCT: float = get_env_float("TRAILING_CALLBACK_PCT", 0.15)
    STOP_LOSS_PCT: float = get_env_float("STOP_LOSS_PCT", 0.80)
    MAX_HOLD_TIME_SEC: int = get_env_int("MAX_HOLD_TIME_SEC", 1200)
    STAGNANT_EXIT_PCT: float = get_env_float("STAGNANT_EXIT_PCT", 0.10)

    # -------------------------------------------------------------
    # Network, Dashboard & State
    # -------------------------------------------------------------
    PORT: int = get_env_int("PORT", 8080)
    STATE_FILE: str = os.getenv("STATE_FILE", "spot_state.json")

    @classmethod
    def validate(cls) -> list[str]:
        errors = []
        if cls.TARGET_ORDER_USD < 5.0:
            errors.append(f"TARGET_ORDER_USD ({cls.TARGET_ORDER_USD}) is below Binance Spot minNotional ($5). Recommended >= $10.")
        if cls.LOOP_INTERVAL_SEC < 1.0:
            errors.append("LOOP_INTERVAL_SEC must be >= 1.0 second.")
        if cls.STOP_LOSS_PCT <= 0:
            errors.append("STOP_LOSS_PCT must be > 0.")
        if cls.TRAILING_ACTIVATION_PCT <= cls.TRAILING_CALLBACK_PCT:
            errors.append("TRAILING_ACTIVATION_PCT should be strictly greater than TRAILING_CALLBACK_PCT.")
        if cls.LIVE_TRADING:
            if not cls.API_KEY or cls.API_KEY in ("your_binance_api_key_here", "NOT_SET"):
                errors.append("LIVE_TRADING is True, but BINANCE_API_KEY is missing or invalid.")
            if not cls.API_SECRET or cls.API_SECRET in ("your_binance_api_secret_here", "NOT_SET"):
                errors.append("LIVE_TRADING is True, but BINANCE_API_SECRET is missing or invalid.")
        return errors

```

---

### 📄 `indicators.py`
**الوصف**: مؤشرات التحليل الفني (RSI، الارتداد اللحظي، والتذبذب)

```python
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

```

---

### 📄 `spot_engine.py`
**الوصف**: محرك الصفقات الفورية وحساب الكميات والوقف المتحرك (Trailing Stop)

```python
"""
Binance Spot 24/7 Scalping & Position Execution Engine
Handles precision formatting, dynamic balance fee-compensation, trailing stops,
risk protection, and persistent state management for Binance Spot.
"""

import json
import logging
import os
import time
from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("SpotEngine")


def precision_from_step(step: float, default: int = 5) -> int:
    """Derives decimal precision count from a step/tick size float."""
    if step <= 0:
        return default
    try:
        # Use str formatted without scientific notation
        s = f"{step:.10f}".rstrip("0").rstrip(".")
        if "." in s:
            return len(s.split(".")[1])
        return 0
    except Exception:
        return default


def round_step(val: float, step: float) -> float:
    """Rounds down a value to the nearest step size to satisfy LOT_SIZE filters."""
    if step <= 0 or val <= 0:
        return 0.0
    try:
        prec = precision_from_step(step, 8)
        d_val = Decimal(f"{val:.{prec + 4}f}")
        d_step = Decimal(f"{step:.{prec + 4}f}")
        units = (d_val / d_step).quantize(Decimal("1"), rounding=ROUND_DOWN)
        result = float(units * d_step)
        return float(f"{result:.{prec}f}")
    except Exception:
        return float(int(val / step) * step)


def round_tick(val: float, tick: float) -> float:
    """Rounds a price to the nearest tick size to satisfy PRICE_FILTER."""
    if tick <= 0 or val <= 0:
        return 0.0
    try:
        prec = precision_from_step(tick, 8)
        d_val = Decimal(f"{val:.{prec + 4}f}")
        d_tick = Decimal(f"{tick:.{prec + 4}f}")
        units = (d_val / d_tick).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        result = float(units * d_tick)
        return float(f"{result:.{prec}f}")
    except Exception:
        return float(round(val / tick) * tick)


@dataclass
class SpotPosition:
    symbol: str
    entry_price: float
    qty: float
    entry_time: float
    highest_price: float
    trailing_active: bool = False
    trailing_stop_price: float = 0.0
    order_id: Optional[str] = None
    cost_usd: float = 0.0


@dataclass
class ClosedTrade:
    symbol: str
    entry_price: float
    exit_price: float
    qty: float
    entry_time: float
    exit_time: float
    pnl_usd: float
    pnl_pct: float
    exit_reason: str


class SpotScalperEngine:
    def __init__(
        self,
        symbol: str,
        target_order_usd: float = 11.0,
        trailing_enabled: bool = True,
        trailing_activation_pct: float = 0.35,
        trailing_callback_pct: float = 0.15,
        stop_loss_pct: float = 0.80,
        max_hold_time_sec: int = 1200,
        stagnant_exit_pct: float = 0.10,
        buy_cooldown_sec: int = 60,
        state_file: str = "spot_state.json",
    ):
        self.symbol = symbol
        self.target_order_usd = target_order_usd
        self.trailing_enabled = trailing_enabled
        self.trailing_activation_pct = trailing_activation_pct
        self.trailing_callback_pct = trailing_callback_pct
        self.stop_loss_pct = stop_loss_pct
        self.max_hold_time_sec = max_hold_time_sec
        self.stagnant_exit_pct = stagnant_exit_pct
        self.buy_cooldown_sec = buy_cooldown_sec
        self.state_file = state_file

        # Market filters from exchange
        self.price_precision: int = 2
        self.amount_precision: int = 5
        self.tick_size: float = 0.01
        self.step_size: float = 0.00001
        self.min_qty: float = 0.00001
        self.min_notional: float = 5.0

        # State tracking
        self.active_position: Optional[SpotPosition] = None
        self.last_sell_time: float = 0.0
        self.total_realized_pnl_usd: float = 0.0
        self.total_trades_count: int = 0
        self.winning_trades_count: int = 0
        self.losing_trades_count: int = 0
        self.recent_trades: List[ClosedTrade] = []
        self.start_time: float = time.time()

        self.load_state()

    def set_market_filters(
        self,
        price_precision: int,
        amount_precision: int,
        tick_size: float,
        step_size: float,
        min_qty: float,
        min_notional: float,
    ):
        """Configure precision and exchange limits fetched from Binance Spot."""
        self.tick_size = tick_size if tick_size > 0 else 10 ** (-max(0, price_precision))
        self.step_size = step_size if step_size > 0 else 10 ** (-max(0, amount_precision))

        derived_price_prec = precision_from_step(self.tick_size, price_precision)
        derived_amount_prec = precision_from_step(self.step_size, amount_precision)

        self.price_precision = max(price_precision, derived_price_prec)
        self.amount_precision = max(amount_precision, derived_amount_prec)

        self.min_qty = max(min_qty, self.step_size)
        self.min_notional = max(5.0, min_notional)

        logger.info(
            f"Configured Spot Filters for {self.symbol} -> TickSize: {self.tick_size} (dec: {self.price_precision}), "
            f"StepSize: {self.step_size} (dec: {self.amount_precision}), MinQty: {self.min_qty}, MinNotional: {self.min_notional} USDT"
        )

    def format_price(self, price: float) -> float:
        """Formats price matching exchange tick size."""
        rounded = round_tick(price, self.tick_size)
        return float(f"{rounded:.{self.price_precision}f}")

    def format_qty(self, qty: float) -> float:
        """Formats order quantity matching exchange step size."""
        rounded = round_step(qty, self.step_size)
        return float(f"{rounded:.{self.amount_precision}f}")

    def calculate_buy_qty(self, current_price: float, available_quote_balance: float = 0.0) -> float:
        """
        Calculates optimal base asset quantity for a Spot BUY order.
        Ensures compliance with minNotional ($5-$10) and available wallet balance.
        """
        if current_price <= 0:
            return 0.0

        spend_usd = max(self.target_order_usd, self.min_notional * 1.05)

        if available_quote_balance > 0:
            if available_quote_balance < self.min_notional:
                logger.warning(
                    f"Available quote balance (${available_quote_balance:.2f}) is below Binance Spot minNotional (${self.min_notional:.2f})."
                )
                return 0.0
            if available_quote_balance < spend_usd:
                # Spend 98% of available balance to leave buffer for taker fees
                spend_usd = available_quote_balance * 0.98

        if spend_usd < self.min_notional:
            logger.warning(
                f"Target spend ${spend_usd:.2f} is below Binance Spot minNotional ${self.min_notional:.2f}."
            )
            return 0.0

        raw_qty = spend_usd / current_price
        formatted_qty = self.format_qty(raw_qty)

        # Check notional value after rounding down
        if (formatted_qty * current_price) < self.min_notional:
            # Increment one step to satisfy minNotional
            formatted_qty = self.format_qty(formatted_qty + self.step_size)

        return formatted_qty

    def can_buy(self) -> Tuple[bool, str]:
        """Checks if bot is allowed to enter a new Spot position."""
        if self.active_position is not None:
            return False, "Already in an active Spot position."

        now = time.time()
        elapsed_since_sell = now - self.last_sell_time
        if elapsed_since_sell < self.buy_cooldown_sec:
            rem = int(self.buy_cooldown_sec - elapsed_since_sell)
            return False, f"Buy cooldown active ({rem}s remaining)."

        return True, "Ready to buy."

    def open_position(self, entry_price: float, qty: float, order_id: Optional[str] = None) -> SpotPosition:
        """Registers a newly filled Spot BUY order."""
        pos = SpotPosition(
            symbol=self.symbol,
            entry_price=entry_price,
            qty=qty,
            entry_time=time.time(),
            highest_price=entry_price,
            trailing_active=False,
            trailing_stop_price=0.0,
            order_id=order_id,
            cost_usd=round(entry_price * qty, 4),
        )
        self.active_position = pos
        logger.info(
            f"🚀 [SPOT BUY EXECUTED] Entered {self.symbol} at ${entry_price:,.2f} | "
            f"Qty: {qty} | Total Cost: ${pos.cost_usd:.2f} USDT"
        )
        self.save_state()
        return pos

    def update_position_and_check_exit(self, current_price: float) -> Tuple[bool, str, float]:
        """
        Monitors active Spot position:
        1. Tracks high-water mark (highest price seen).
        2. Activates and trails Trailing Take-Profit.
        3. Checks Hard Stop-Loss.
        4. Checks Max Hold Time stagnant exit.
        Returns: (should_exit, exit_reason, sell_qty)
        """
        if self.active_position is None:
            return False, "NO_POSITION", 0.0

        pos = self.active_position
        now = time.time()
        hold_time = now - pos.entry_time

        # Update high-water mark
        if current_price > pos.highest_price:
            pos.highest_price = current_price

        # Calculate current and peak gains
        pnl_pct = ((current_price - pos.entry_price) / pos.entry_price) * 100.0
        peak_gain_pct = ((pos.highest_price - pos.entry_price) / pos.entry_price) * 100.0

        # 1. Trailing Stop Activation & Trailing
        if self.trailing_enabled and peak_gain_pct >= self.trailing_activation_pct:
            pos.trailing_active = True
            calculated_stop = pos.highest_price * (1.0 - (self.trailing_callback_pct / 100.0))
            if calculated_stop > pos.trailing_stop_price:
                pos.trailing_stop_price = self.format_price(calculated_stop)

            # Trigger exit if current price drops below trailing stop
            if current_price <= pos.trailing_stop_price:
                reason = f"TRAILING_TAKE_PROFIT (Peak: +{peak_gain_pct:.2f}%, Exit: +{pnl_pct:.2f}%)"
                return True, reason, pos.qty

        # 2. Hard Stop-Loss Protection
        if pnl_pct <= -self.stop_loss_pct:
            reason = f"HARD_STOP_LOSS (Current: {pnl_pct:.2f}%, Limit: -{self.stop_loss_pct:.2f}%)"
            return True, reason, pos.qty

        # 3. Stagnant / Max Hold Time Exit
        if hold_time >= self.max_hold_time_sec:
            if pnl_pct >= self.stagnant_exit_pct:
                reason = f"STAGNANT_PROFIT_EXIT (Hold: {int(hold_time)}s, PnL: +{pnl_pct:.2f}%)"
                return True, reason, pos.qty
            elif pnl_pct <= -0.15:
                reason = f"STAGNANT_TIMEOUT_EXIT (Hold: {int(hold_time)}s, PnL: {pnl_pct:.2f}%)"
                return True, reason, pos.qty

        return False, "HOLDING", 0.0

    def close_position(
        self, exit_price: float, filled_qty: float, exit_reason: str
    ) -> Optional[ClosedTrade]:
        """Registers a filled Spot SELL order, calculates realized PnL, and archives trade."""
        if self.active_position is None:
            return None

        pos = self.active_position
        now = time.time()

        # Deduct standard Spot taker fee ~0.075-0.1% from gross PnL
        revenue_usd = exit_price * filled_qty
        cost_usd = pos.entry_price * filled_qty
        gross_pnl = revenue_usd - cost_usd
        est_fees = (cost_usd + revenue_usd) * 0.00075  # 0.075% fee
        net_pnl = gross_pnl - est_fees
        pnl_pct = ((exit_price - pos.entry_price) / pos.entry_price) * 100.0

        trade = ClosedTrade(
            symbol=pos.symbol,
            entry_price=pos.entry_price,
            exit_price=exit_price,
            qty=filled_qty,
            entry_time=pos.entry_time,
            exit_time=now,
            pnl_usd=round(net_pnl, 4),
            pnl_pct=round(pnl_pct, 2),
            exit_reason=exit_reason,
        )

        self.total_realized_pnl_usd += net_pnl
        self.total_trades_count += 1
        if net_pnl >= 0:
            self.winning_trades_count += 1
        else:
            self.losing_trades_count += 1

        self.recent_trades.insert(0, trade)
        if len(self.recent_trades) > 20:
            self.recent_trades = self.recent_trades[:20]

        logger.info(
            f"✅ [SPOT SELL EXECUTED] Closed {self.symbol} at ${exit_price:,.2f} | "
            f"Net PnL: {net_pnl:+.4f} USDT ({pnl_pct:+.2f}%) | Reason: {exit_reason}"
        )

        self.active_position = None
        self.last_sell_time = now
        self.save_state()
        return trade

    def get_status_summary(self, current_price: float = 0.0) -> Dict[str, Any]:
        """Provides status data for HTTP Dashboard and API."""
        pos_data = None
        if self.active_position:
            pos = self.active_position
            pnl_pct = ((current_price - pos.entry_price) / pos.entry_price) * 100.0 if current_price else 0.0
            pnl_usd = (current_price - pos.entry_price) * pos.qty if current_price else 0.0
            hold_sec = int(time.time() - pos.entry_time)
            pos_data = {
                "symbol": pos.symbol,
                "entry_price": pos.entry_price,
                "current_price": current_price,
                "highest_price": pos.highest_price,
                "qty": pos.qty,
                "cost_usd": pos.cost_usd,
                "trailing_active": pos.trailing_active,
                "trailing_stop_price": pos.trailing_stop_price,
                "unrealized_pnl_usd": round(pnl_usd, 4),
                "unrealized_pnl_pct": round(pnl_pct, 2),
                "hold_time_seconds": hold_sec,
            }

        win_rate = (
            round((self.winning_trades_count / self.total_trades_count) * 100.0, 1)
            if self.total_trades_count > 0
            else 0.0
        )

        return {
            "symbol": self.symbol,
            "has_active_position": self.active_position is not None,
            "position": pos_data,
            "total_realized_pnl_usd": round(self.total_realized_pnl_usd, 4),
            "total_trades": self.total_trades_count,
            "winning_trades": self.winning_trades_count,
            "losing_trades": self.losing_trades_count,
            "win_rate_pct": win_rate,
            "recent_trades": [asdict(t) for t in self.recent_trades[:5]],
            "uptime_seconds": int(time.time() - self.start_time),
        }

    def save_state(self):
        """Persists trade history and active position to state file."""
        try:
            state = {
                "total_realized_pnl_usd": self.total_realized_pnl_usd,
                "total_trades_count": self.total_trades_count,
                "winning_trades_count": self.winning_trades_count,
                "losing_trades_count": self.losing_trades_count,
                "last_sell_time": self.last_sell_time,
                "active_position": asdict(self.active_position) if self.active_position else None,
                "recent_trades": [asdict(t) for t in self.recent_trades],
                "saved_at": time.time(),
            }
            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to persist state: {e}")

    def load_state(self):
        """Loads state from disk if exists."""
        if not os.path.exists(self.state_file):
            return
        try:
            with open(self.state_file, "r") as f:
                state = json.load(f)
            self.total_realized_pnl_usd = state.get("total_realized_pnl_usd", 0.0)
            self.total_trades_count = state.get("total_trades_count", 0)
            self.winning_trades_count = state.get("winning_trades_count", 0)
            self.losing_trades_count = state.get("losing_trades_count", 0)
            self.last_sell_time = state.get("last_sell_time", 0.0)
            act_pos = state.get("active_position")
            if act_pos:
                self.active_position = SpotPosition(**act_pos)
            self.recent_trades = []
            for t in state.get("recent_trades", []):
                self.recent_trades.append(ClosedTrade(**t))
            logger.info(
                f"Restored state from {self.state_file} -> {self.total_trades_count} trades, "
                f"Realized PnL: {self.total_realized_pnl_usd:+.4f} USDT"
            )
        except Exception as e:
            logger.warning(f"Could not load state from {self.state_file}: {e}")

```

---

### 📄 `main.py`
**الوصف**: حلقة التداول اللحظي 24/7 وخادم لوحة التحكم وفحص الصحة

```python
"""
Binance Spot 24/7 Scalper Trading Bot - Production Main Runner
Autonomous real-time spot trading with Dip & Rebound Entry, Trailing Stop-Loss,
zero-freeze error recovery, and embedded Railway health check dashboard.
"""

import html
import json
import logging
import os
import signal
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional, Tuple

from config import Config, mask_key
import indicators
from spot_engine import SpotScalperEngine

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("BinanceSpotScalper")

# Global status dictionary for Web Dashboard & Railway Healthchecks
BOT_STATUS: Dict[str, Any] = {
    "status": "INITIALIZING",
    "strategy": "Binance Spot Real-Time Scalper (Dip & Rebound + Trailing TP)",
    "symbol": Config.get_spot_symbol(),
    "raw_symbol": Config.get_binance_raw_symbol(),
    "live_trading": Config.LIVE_TRADING,
    "current_price": 0.0,
    "price_change_24h": 0.0,
    "rsi": 50.0,
    "dip_pct": 0.0,
    "rebound_pct": 0.0,
    "volatility_pct": 0.0,
    "spread_pct": 0.0,
    "entry_signals": {
        "dip_satisfied": False,
        "rebound_satisfied": False,
        "rsi_satisfied": False,
        "spread_satisfied": False,
        "can_buy": False,
        "reason": "Initializing...",
    },
    "has_position": False,
    "position": None,
    "total_realized_pnl_usd": 0.0,
    "total_trades": 0,
    "winning_trades": 0,
    "losing_trades": 0,
    "win_rate_pct": 0.0,
    "recent_trades": [],
    "external_ip": "Detecting...",
    "error_diagnostic": None,
    "last_loop_time": None,
    "base_asset": Config.get_base_quote()[0],
    "quote_asset": Config.get_base_quote()[1],
    "wallet_balances": {"quote_free": 0.0, "base_free": 0.0},
}

shutdown_event = threading.Event()


def get_public_ip() -> str:
    """Detects outbound IP address to verify server region and for Binance API whitelisting."""
    providers = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://checkip.amazonaws.com",
    ]
    for url in providers:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                ip = resp.read().decode("utf-8").strip()
                if ip:
                    return ip
        except Exception:
            continue
    return "UNKNOWN_IP"


class DashboardHealthHandler(BaseHTTPRequestHandler):
    """
    Non-blocking HTTP daemon server providing:
    - /health (Railway healthcheck endpoint returning 200 OK)
    - /api/status (JSON feed for monitoring)
    - / (Modern responsive HTML dashboard in Arabic and English)
    """

    def log_message(self, format, *args):
        # Suppress spammy request logs
        return

    def do_GET(self):
        if self.path in ("/health", "/ping"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            payload = {
                "status": "healthy",
                "bot": BOT_STATUS["status"],
                "live_trading": BOT_STATUS["live_trading"],
                "symbol": BOT_STATUS["symbol"],
                "current_price": BOT_STATUS["current_price"],
                "realized_pnl_usd": BOT_STATUS["total_realized_pnl_usd"],
                "trades": BOT_STATUS["total_trades"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(BOT_STATUS, default=str).encode("utf-8"))
            return

        # Render HTML Dashboard
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html_page = self.render_html_dashboard()
        self.wfile.write(html_page.encode("utf-8"))

    def render_html_dashboard(self) -> str:
        s = BOT_STATUS
        mode_badge = (
            '<span class="badge live">🟢 تداول حقيقي (LIVE SPOT)</span>'
            if s["live_trading"]
            else '<span class="badge sim">🟡 محاكاة (DRY RUN / SIMULATION)</span>'
        )

        diag_box = ""
        if s.get("error_diagnostic"):
            diag_box = f"""
            <div class="alert alert-error">
                <strong>⚠️ تنبيه فني:</strong> {html.escape(str(s['error_diagnostic']))}
            </div>
            """

        pos = s.get("position")
        if pos:
            pnl_cls = "text-green" if pos.get("unrealized_pnl_pct", 0) >= 0 else "text-red"
            trailing_badge = (
                '<span class="tag tag-active">مفعل (Trailing Active)</span>'
                if pos.get("trailing_active")
                else '<span class="tag tag-waiting">قيد الانتظار</span>'
            )
            position_card = f"""
            <div class="card active-pos-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="color:var(--yellow); font-size:1.1rem;">⚡ صفقة فورية نشطة ({pos.get('symbol')})</h3>
                    <div>{trailing_badge}</div>
                </div>
                <div class="grid-stats" style="margin-top:14px; margin-bottom:0;">
                    <div>
                        <div class="card-label">سعر الدخول (Entry Price)</div>
                        <div class="card-value font-mono">${pos.get('entry_price', 0):,.2f}</div>
                    </div>
                    <div>
                        <div class="card-label">الربح غير المحقق (Unrealized PnL)</div>
                        <div class="card-value font-mono {pnl_cls}">{pos.get('unrealized_pnl_pct', 0):+.2f}% (${pos.get('unrealized_pnl_usd', 0):+.4f})</div>
                    </div>
                    <div>
                        <div class="card-label">أعلى سعر تم بلوغه (Peak High)</div>
                        <div class="card-value font-mono text-blue">${pos.get('highest_price', 0):,.2f}</div>
                    </div>
                    <div>
                        <div class="card-label">وقف الربح المتحرك (Trailing Stop)</div>
                        <div class="card-value font-mono text-yellow">${pos.get('trailing_stop_price', 0):,.2f}</div>
                    </div>
                </div>
                <div style="margin-top:12px; font-size:0.85rem; color:var(--muted);">
                    الكمية: <strong>{pos.get('qty')} {s.get('base_asset')}</strong> | القيمة: <strong>${pos.get('cost_usd', 0):,.2f} USDT</strong> | مدة الاحتفاظ: <strong>{pos.get('hold_time_seconds', 0)} ثانية</strong>
                </div>
            </div>
            """
        else:
            sig = s.get("entry_signals", {})
            position_card = f"""
            <div class="card" style="border-left: 4px solid var(--blue);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 style="font-size:1rem; color:var(--text);">🎯 حالة رادار الدخول الفوري اللحظي (Entry Signals)</h3>
                    <span style="font-size:0.8rem; color:var(--muted);">{sig.get('reason', 'Searching')}</span>
                </div>
                <div style="display:flex; gap:12px; flex-wrap:wrap; font-size:0.85rem;">
                    <span class="signal-tag {'tag-ok' if sig.get('dip_satisfied') else 'tag-wait'}">
                        الهبوط: {s.get('dip_pct', 0):.2f}% (الهدف: ≥{Config.BUY_DIP_MIN_PCT}%)
                    </span>
                    <span class="signal-tag {'tag-ok' if sig.get('rebound_satisfied') else 'tag-wait'}">
                        الارتداد: {s.get('rebound_pct', 0):.2f}% (الهدف: ≥{Config.BUY_REBOUND_CONFIRM_PCT}%)
                    </span>
                    <span class="signal-tag {'tag-ok' if sig.get('rsi_satisfied') else 'tag-wait'}">
                        مؤشر RSI: {s.get('rsi', 0):.1f} (الهدف: ≤{Config.BUY_RSI_MAX})
                    </span>
                    <span class="signal-tag {'tag-ok' if sig.get('spread_satisfied') else 'tag-wait'}">
                        الفارق: {s.get('spread_pct', 0):.3f}%
                    </span>
                </div>
            </div>
            """

        trades_rows = ""
        for t in s.get("recent_trades", []):
            pnl_val = t.get("pnl_usd", 0.0)
            pnl_cls = "text-green" if pnl_val >= 0 else "text-red"
            trades_rows += f"""
            <tr>
                <td class="font-mono">${t.get('entry_price', 0):,.2f}</td>
                <td class="font-mono">${t.get('exit_price', 0):,.2f}</td>
                <td class="font-mono">{t.get('qty')}</td>
                <td class="font-mono font-bold {pnl_cls}">{t.get('pnl_pct', 0):+.2f}% (${pnl_val:+.4f})</td>
                <td style="font-size:0.8rem; color:var(--muted);">{html.escape(t.get('exit_reason', ''))}</td>
            </tr>
            """

        return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بينانس سبوت - بوت التداول الفوري اللحظي 24/7</title>
    <meta http-equiv="refresh" content="4">
    <style>
        :root {{
            --bg: #0b0e14;
            --surface: #141923;
            --border: #232c3d;
            --text: #f0f3f8;
            --muted: #8b99ad;
            --green: #0ecb81;
            --red: #f6465d;
            --yellow: #f0b90b;
            --blue: #2979ff;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        body {{ background: var(--bg); color: var(--text); padding: 18px; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid var(--border); }}
        .title-group h1 {{ font-size: 1.4rem; display: flex; align-items: center; gap: 8px; }}
        .badge {{ font-size: 0.8rem; padding: 4px 10px; border-radius: 999px; font-weight: 700; }}
        .badge.live {{ background: rgba(14, 203, 129, 0.15); color: var(--green); border: 1px solid var(--green); }}
        .badge.sim {{ background: rgba(240, 185, 11, 0.15); color: var(--yellow); border: 1px solid var(--yellow); }}
        .grid-stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin-bottom: 20px; }}
        .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }}
        .active-pos-card {{ border: 1px solid var(--yellow); background: rgba(240, 185, 11, 0.04); }}
        .card-label {{ font-size: 0.8rem; color: var(--muted); margin-bottom: 5px; }}
        .card-value {{ font-size: 1.5rem; font-weight: 700; }}
        .text-green {{ color: var(--green); }}
        .text-red {{ color: var(--red); }}
        .text-yellow {{ color: var(--yellow); }}
        .text-blue {{ color: var(--blue); }}
        .font-mono {{ font-family: 'SFMono-Regular', Consolas, monospace; direction: ltr; display: inline-block; }}
        .alert {{ padding: 12px 16px; border-radius: 8px; margin-bottom: 18px; font-size: 0.9rem; }}
        .alert-error {{ background: rgba(246, 70, 93, 0.15); border: 1px solid var(--red); color: #ff8b99; }}
        .signal-tag {{ padding: 5px 10px; border-radius: 6px; font-size: 0.82rem; }}
        .signal-tag.tag-ok {{ background: rgba(14, 203, 129, 0.18); color: var(--green); border: 1px solid var(--green); }}
        .signal-tag.tag-wait {{ background: rgba(139, 153, 173, 0.12); color: var(--muted); border: 1px solid var(--border); }}
        .tag {{ padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }}
        .tag.tag-active {{ background: rgba(14, 203, 129, 0.2); color: var(--green); }}
        .tag.tag-waiting {{ background: rgba(139, 153, 173, 0.15); color: var(--muted); }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 10px 12px; text-align: right; border-bottom: 1px solid var(--border); font-size: 0.88rem; }}
        th {{ color: var(--muted); font-size: 0.75rem; font-weight: 600; }}
        footer {{ margin-top: 25px; text-align: center; color: var(--muted); font-size: 0.8rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="title-group">
                <h1>⚡ بوت التداول الفوري اللحظي (Binance Spot Scalper)</h1>
                <p style="color: var(--muted); font-size: 0.85rem; margin-top: 3px;">تداول العقود الفورية لحظياً دون تجميد أو توقف 24/7 على Railway</p>
            </div>
            <div>{mode_badge}</div>
        </header>

        {diag_box}

        <div class="grid-stats">
            <div class="card">
                <div class="card-label">سعر السوق الفوري ({s.get('symbol')})</div>
                <div class="card-value font-mono text-yellow">${s.get('current_price', 0.0):,.2f}</div>
                <div style="font-size: 0.78rem; margin-top: 4px; color: var(--muted);">تغير 24 ساعة: {s.get('price_change_24h', 0.0):+.2f}%</div>
            </div>
            <div class="card">
                <div class="card-label">صافي الربح المحقق (Realized PnL)</div>
                <div class="card-value font-mono text-green">{s.get('total_realized_pnl_usd', 0.0):+.4f} USDT</div>
                <div style="font-size: 0.78rem; margin-top: 4px; color: var(--muted);">عدد الصفقات: {s.get('total_trades', 0)} (نسبة النجاح: {s.get('win_rate_pct', 0.0)}%)</div>
            </div>
            <div class="card">
                <div class="card-label">حجم الصفقة المستهدف (Order Size)</div>
                <div class="card-value font-mono text-blue">${Config.TARGET_ORDER_USD:,.2f} USDT</div>
                <div style="font-size: 0.78rem; margin-top: 4px; color: var(--muted);">تحديث كل {Config.LOOP_INTERVAL_SEC} ثواني</div>
            </div>
            <div class="card">
                <div class="card-label">حالة المحرك (Engine Status)</div>
                <div class="card-value font-mono" style="font-size: 1.25rem;">{s.get('status')}</div>
                <div style="font-size: 0.78rem; margin-top: 4px; color: var(--muted);">IP السيرفر: {s.get('external_ip')}</div>
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            {position_card}
        </div>

        <div class="card">
            <h3 style="font-size: 1rem; margin-bottom: 10px;">📜 سجل الصفقات المغلقة مؤخراً (Recent Executions)</h3>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>سعر الدخول</th>
                            <th>سعر الخروج</th>
                            <th>الكمية</th>
                            <th>صافي الربح</th>
                            <th>سبب الإغلاق</th>
                        </tr>
                    </thead>
                    <tbody>
                        {trades_rows or '<tr><td colspan="5" style="text-align: center; color: var(--muted);">لا توجد صفقات منفذة حتى الآن. الرادار يراقب الفرص اللحظية...</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>

        <footer>
            Binance Spot Engine v2.0 | المنفذ: <code>{Config.PORT}</code> | رابط الفحص: <code>/health</code> | متصل ومستقر على مدار الساعة 24/7
        </footer>
    </div>
</body>
</html>
"""


def start_health_server(port: int):
    """Starts the background HTTP daemon for Railway."""
    try:
        server = HTTPServer(("0.0.0.0", port), DashboardHealthHandler)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        logger.info(f"🌐 Web Dashboard & Railway health endpoint live on http://0.0.0.0:{port}")
    except Exception as e:
        logger.error(f"Failed to start HTTP server on port {port}: {e}")


class PublicBinanceFallback:
    """
    Fallback public API client used when CCXT is absent or during dry-run simulation.
    Fetches real-time Binance Spot tickers, orderbook depth, and klines directly via REST.
    """

    def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        raw = symbol.replace("/", "").replace("-", "").replace("_", "")
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={raw}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "last": float(data.get("lastPrice", 0.0)),
                "bid": float(data.get("bidPrice", 0.0)),
                "ask": float(data.get("askPrice", 0.0)),
                "percentage": float(data.get("priceChangePercent", 0.0)),
            }

    def fetch_ohlcv(self, symbol: str, timeframe="1m", limit=30) -> List[List[float]]:
        raw = symbol.replace("/", "").replace("-", "").replace("_", "")
        url = f"https://api.binance.com/api/v3/klines?symbol={raw}&interval={timeframe}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # Format: [open_time, open, high, low, close, volume]
            return [[d[0], float(d[1]), float(d[2]), float(d[3]), float(d[4]), float(d[5])] for d in data]


    def fetch_exchange_info(self, symbol: str) -> Dict[str, Any]:
        raw = symbol.replace('/', '').replace('-', '').replace('_', '')
        url = f'https://api.binance.com/api/v3/exchangeInfo?symbol={raw}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode('utf-8'))


def init_exchange():
    """Initializes CCXT Binance Spot instance with robust options."""
    try:
        import ccxt
    except ImportError:
        logger.warning("CCXT not installed locally. Using Binance REST Client for market data.")
        return PublicBinanceFallback()

    exchange_config = {
        "apiKey": Config.API_KEY,
        "secret": Config.API_SECRET,
        "enableRateLimit": True,
        "timeout": 10000,
        "options": {
            "defaultType": "spot",  # Strictly Binance Spot (api.binance.com)
            "adjustForTimeDifference": True,
            "recvWindow": 10000,
        },
    }

    if Config.BINANCE_PROXY:
        exchange_config["proxies"] = {
            "http": Config.BINANCE_PROXY,
            "https": Config.BINANCE_PROXY,
        }
        logger.info(f"Using outbound proxy for Binance API: {Config.BINANCE_PROXY}")

    exchange = ccxt.binance(exchange_config)

    if Config.TESTNET:
        exchange.set_sandbox_mode(True)
        logger.info("Connecting to Binance Spot Testnet.")

    return exchange


def configure_spot_filters(exchange, symbol: str, engine: SpotScalperEngine):
    """Queries exchange markets and sets precision, LOT_SIZE, and MIN_NOTIONAL limits."""
    if isinstance(exchange, PublicBinanceFallback):
        try:
            info = exchange.fetch_exchange_info(symbol)
            sym_list = info.get('symbols', [])
            if sym_list:
                s_info = sym_list[0]
                tick = 0.01
                step = 0.00001
                min_q = 0.00001
                min_n = 5.0
                for f in s_info.get('filters', []):
                    f_type = f.get('filterType')
                    if f_type == 'PRICE_FILTER':
                        tick = float(f.get('tickSize', 0.01))
                    elif f_type == 'LOT_SIZE':
                        step = float(f.get('stepSize', 0.00001))
                        min_q = float(f.get('minQty', 0.00001))
                    elif f_type in ('NOTIONAL', 'MIN_NOTIONAL'):
                        min_n = float(f.get('minNotional', 5.0))
                engine.set_market_filters(2, 5, tick, step, min_q, min_n)
                return
        except Exception as e:
            logger.warning(f'Could not fetch REST exchangeInfo: {e}')
        engine.set_market_filters(2, 5, 0.01, 0.00001, 0.00001, 5.0)
        return

    logger.info(f"Fetching Binance Spot market filters for {symbol}...")
    markets = exchange.load_markets()

    target_market = None
    for s, m in markets.items():
        if s == symbol or m.get("id") == Config.get_binance_raw_symbol():
            target_market = m
            break

    if not target_market:
        available = [k for k in markets.keys() if "USDT" in k][:6]
        raise ValueError(f"Spot pair '{symbol}' not found on Binance! Examples: {available}")

    price_precision = target_market.get("precision", {}).get("price", 2)
    amount_precision = target_market.get("precision", {}).get("amount", 5)

    limits = target_market.get("limits", {})
    min_qty = limits.get("amount", {}).get("min", 0.00001)
    min_notional = limits.get("cost", {}).get("min", 5.0)

    tick_size = 0.0
    step_size = 0.0
    for f in target_market.get("info", {}).get("filters", []):
        f_type = f.get("filterType")
        if f_type == "PRICE_FILTER":
            tick_size = float(f.get("tickSize", 0.0))
        elif f_type == "LOT_SIZE":
            step_size = float(f.get("stepSize", 0.0))
            min_qty = max(min_qty, float(f.get("minQty", min_qty)))
        elif f_type == "NOTIONAL":
            min_notional = max(min_notional, float(f.get("minNotional", min_notional)))
        elif f_type == "MIN_NOTIONAL":
            min_notional = max(min_notional, float(f.get("minNotional", min_notional)))

    engine.set_market_filters(
        price_precision=int(price_precision) if price_precision is not None else 2,
        amount_precision=int(amount_precision) if amount_precision is not None else 5,
        tick_size=tick_size,
        step_size=step_size,
        min_qty=float(min_qty),
        min_notional=float(min_notional),
    )


def execute_spot_buy(exchange, symbol: str, qty: float, price: float, engine: Optional[SpotScalperEngine] = None) -> Tuple[bool, Optional[str]]:
    """Executes a real Spot BUY order on Binance."""
    try:
        order_qty = engine.format_qty(qty) if engine else qty
        if engine and order_qty < engine.min_qty:
            logger.error(f"Cannot buy: calculated qty ({order_qty}) is below minQty ({engine.min_qty}).")
            return False, None
        order = exchange.create_market_buy_order(symbol, order_qty)
        order_id = str(order.get("id", "N/A"))
        logger.info(f"Successfully placed Spot Market BUY: {symbol} Qty: {order_qty} (ID: {order_id})")
        return True, order_id
    except Exception as e:
        logger.error(f"Failed to execute Spot BUY: {e}")
        BOT_STATUS["error_diagnostic"] = f"Failed BUY order: {e}"
        return False, None


def execute_spot_sell(exchange, symbol: str, qty: float, price: float) -> Tuple[bool, float]:
    """
    Executes a real Spot SELL order on Binance.
    Queries actual wallet balance to prevent insufficient balance failures.
    """
    try:
        base, _ = Config.get_base_quote()
        # Query free balance to guarantee sufficient coins after fees
        balance = exchange.fetch_balance()
        free_base = float(balance.get(base, {}).get("free", 0.0))

        actual_qty = min(qty, free_base)
        # Apply step size
        actual_qty = float(f"{actual_qty:.5f}")

        if actual_qty <= 0:
            logger.error(f"Cannot sell: free balance of {base} is 0 or less than step size.")
            return False, 0.0

        order = exchange.create_market_sell_order(symbol, actual_qty)
        logger.info(f"Successfully placed Spot Market SELL: {symbol} Qty: {actual_qty}")
        return True, actual_qty
    except Exception as e:
        logger.error(f"Failed to execute Spot SELL: {e}")
        BOT_STATUS["error_diagnostic"] = f"Failed SELL order: {e}"
        return False, 0.0


def run_spot_bot():
    """Main continuous execution loop for the 24/7 Binance Spot Scalper."""
    logger.info("=" * 65)
    logger.info("🚀 Starting Binance Spot 24/7 Scalper Trading Bot")
    logger.info(f"Symbol: {Config.get_spot_symbol()} (Raw: {Config.get_binance_raw_symbol()})")
    logger.info(f"Execution Mode: {'🔴 LIVE TRADING (REAL FUNDS)' if Config.LIVE_TRADING else '🟡 SIMULATION (DRY RUN)'}")
    logger.info(f"Target Order Size: ${Config.TARGET_ORDER_USD:.2f} USDT")
    logger.info(f"Trailing TP: {Config.TRAILING_ACTIVATION_PCT}% activation, {Config.TRAILING_CALLBACK_PCT}% callback")
    logger.info(f"Hard Stop-Loss: -{Config.STOP_LOSS_PCT}% | Loop Interval: {Config.LOOP_INTERVAL_SEC}s")
    logger.info("=" * 65)

    # 1. Start HTTP server immediately
    start_health_server(Config.PORT)

    # 2. Detect external IP
    ext_ip = get_public_ip()
    BOT_STATUS["external_ip"] = ext_ip
    logger.info(f"Outbound Server IP: {ext_ip}")

    # 3. Instantiate Spot Scalper Engine
    engine = SpotScalperEngine(
        symbol=Config.get_spot_symbol(),
        target_order_usd=Config.TARGET_ORDER_USD,
        trailing_enabled=Config.TRAILING_STOP_ENABLED,
        trailing_activation_pct=Config.TRAILING_ACTIVATION_PCT,
        trailing_callback_pct=Config.TRAILING_CALLBACK_PCT,
        stop_loss_pct=Config.STOP_LOSS_PCT,
        max_hold_time_sec=Config.MAX_HOLD_TIME_SEC,
        stagnant_exit_pct=Config.STAGNANT_EXIT_PCT,
        buy_cooldown_sec=Config.BUY_COOLDOWN_SEC,
        state_file=Config.STATE_FILE,
    )

    symbol = Config.get_spot_symbol()
    exchange = None

    # 4. Connect to Exchange with auto-reconnect
    while not shutdown_event.is_set():
        try:
            exchange = init_exchange()
            configure_spot_filters(exchange, symbol, engine)
            BOT_STATUS["status"] = "RUNNING (24/7)"
            BOT_STATUS["error_diagnostic"] = None
            break
        except Exception as e:
            err_str = str(e)
            logger.error(f"Error connecting to Binance: {err_str}")
            BOT_STATUS["status"] = "RETRYING_CONNECTION"

            if "-2008" in err_str or "Invalid Api-Key" in err_str:
                diag = (
                    "Binance Spot API Key rejected (-2008). "
                    "1) Ensure BINANCE_API_KEY and BINANCE_API_SECRET in Railway Variables are correct. "
                    "2) Check 'Enable Reading' and 'Enable Spot & Margin Trading' in Binance API Management. "
                    f"3) If IP restriction is active, whitelist server IP: {ext_ip}"
                )
                BOT_STATUS["error_diagnostic"] = diag
            elif "451" in err_str:
                diag = "Binance Geo-restriction (451). Deploy your Railway service in EU West (Amsterdam) or set BINANCE_PROXY."
                BOT_STATUS["error_diagnostic"] = diag
            else:
                BOT_STATUS["error_diagnostic"] = err_str

            time.sleep(10)

    # 5. Continuous 24/7 Real-Time Loop
    logger.info("Entering 24/7 real-time Spot scalping loop...")
    while not shutdown_event.is_set():
        try:
            loop_start = time.time()

            # A. Fetch Real-time Market Data (Ticker & Orderbook)
            ticker = exchange.fetch_ticker(symbol)
            current_price = float(ticker.get("last") or 0.0)
            bid_price = float(ticker.get("bid") or current_price)
            ask_price = float(ticker.get("ask") or current_price)
            price_change = float(ticker.get("percentage") or 0.0)

            if current_price <= 0:
                time.sleep(Config.LOOP_INTERVAL_SEC)
                continue

            spread_pct = ((ask_price - bid_price) / current_price) * 100.0 if current_price else 0.0

            BOT_STATUS["current_price"] = current_price
            BOT_STATUS["price_change_24h"] = price_change
            BOT_STATUS["spread_pct"] = round(spread_pct, 4)
            BOT_STATUS["last_loop_time"] = datetime.now(timezone.utc).isoformat()

            # B. Fetch Recent Candles for Technical Indicators
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=30)
                closes = [c[4] for c in ohlcv]
                highs = [c[2] for c in ohlcv]
                lows = [c[3] for c in ohlcv]

                rsi = indicators.calculate_rsi(closes, period=14)
                dip_pct, rebound_pct = indicators.calculate_dip_and_rebound(closes, current_price, lookback=15)
                volatility_pct = indicators.calculate_volatility_pct(highs, lows, current_price)

                BOT_STATUS["rsi"] = rsi
                BOT_STATUS["dip_pct"] = dip_pct
                BOT_STATUS["rebound_pct"] = rebound_pct
                BOT_STATUS["volatility_pct"] = volatility_pct
            except Exception as e:
                logger.debug(f"Could not calculate full indicators this cycle: {e}")
                rsi = 50.0
                dip_pct = 0.0
                rebound_pct = 0.0

            # C. Monitor Active Position (Exit Logic)
            if engine.active_position is not None:
                should_exit, exit_reason, sell_qty = engine.update_position_and_check_exit(current_price)
                if should_exit:
                    logger.info(f"⚡ EXIT SIGNAL TRIGGERED: {exit_reason} | Selling {sell_qty} {symbol}...")
                    if Config.LIVE_TRADING and not isinstance(exchange, PublicBinanceFallback):
                        success, actual_sold = execute_spot_sell(exchange, symbol, sell_qty, current_price, engine)
                        if success:
                            engine.close_position(current_price, actual_sold, exit_reason)
                    else:
                        # Simulated Exit
                        engine.close_position(current_price, sell_qty, exit_reason)

            # D. Evaluate Entry Conditions (Buy Logic)
            else:
                can_buy, buy_check_msg = engine.can_buy()

                dip_satisfied = dip_pct >= Config.BUY_DIP_MIN_PCT
                rebound_satisfied = rebound_pct >= Config.BUY_REBOUND_CONFIRM_PCT
                rsi_satisfied = rsi <= Config.BUY_RSI_MAX
                spread_satisfied = spread_pct <= Config.MAX_SPREAD_PCT

                BOT_STATUS["entry_signals"] = {
                    "dip_satisfied": dip_satisfied,
                    "rebound_satisfied": rebound_satisfied,
                    "rsi_satisfied": rsi_satisfied,
                    "spread_satisfied": spread_satisfied,
                    "can_buy": can_buy,
                    "reason": buy_check_msg,
                }

                if can_buy and dip_satisfied and rebound_satisfied and rsi_satisfied and spread_satisfied:
                    logger.info(
                        f"🎯 ENTRY CONDITIONS CONFIRMED for {symbol}! "
                        f"Dip: {dip_pct:.2f}%, Rebound: {rebound_pct:.2f}%, RSI: {rsi:.1f}"
                    )
                    quote_balance = 0.0
                    if Config.LIVE_TRADING and not isinstance(exchange, PublicBinanceFallback):
                        try:
                            bal = exchange.fetch_balance()
                            _, quote = Config.get_base_quote()
                            quote_balance = float(
                                (bal.get(quote, {}) or {}).get("free", 0.0)
                                or (bal.get("free", {}) or {}).get(quote, 0.0)
                                or 0.0
                            )
                            BOT_STATUS["wallet_balances"]["quote_free"] = quote_balance
                        except Exception as e:
                            logger.warning(f"Could not fetch wallet balance: {e}")

                    # Calculate quantity with balance validation
                    buy_qty = engine.calculate_buy_qty(current_price, available_quote_balance=quote_balance)
                    if buy_qty > 0:
                        if Config.LIVE_TRADING and not isinstance(exchange, PublicBinanceFallback):
                            success, order_id = execute_spot_buy(exchange, symbol, buy_qty, current_price, engine)
                            if success:
                                engine.open_position(current_price, buy_qty, order_id)
                        else:
                            # Simulated Buy
                            sim_order_id = f"SIM_{int(time.time())}"
                            engine.open_position(current_price, buy_qty, sim_order_id)

            # E. Update Dashboard Summary
            summary = engine.get_status_summary(current_price)
            BOT_STATUS.update(
                {
                    "has_position": summary["has_active_position"],
                    "position": summary["position"],
                    "total_realized_pnl_usd": summary["total_realized_pnl_usd"],
                    "total_trades": summary["total_trades"],
                    "winning_trades": summary["winning_trades"],
                    "losing_trades": summary["losing_trades"],
                    "win_rate_pct": summary["win_rate_pct"],
                    "recent_trades": summary["recent_trades"],
                }
            )

        except urllib.error.HTTPError as e:
            if e.code == 429:
                logger.warning("Binance rate limit (429). Backing off for 30s...")
                time.sleep(30)
            else:
                logger.error(f"HTTP error in loop: {e}")
                time.sleep(Config.LOOP_INTERVAL_SEC)
        except Exception as e:
            logger.error(f"Unexpected error in trading loop: {e}")
            BOT_STATUS["error_diagnostic"] = str(e)
            time.sleep(Config.LOOP_INTERVAL_SEC)

        # Sleep remaining time to maintain consistent loop frequency
        elapsed = time.time() - loop_start
        sleep_time = max(0.5, Config.LOOP_INTERVAL_SEC - elapsed)
        time.sleep(sleep_time)

    logger.info("Bot execution loop exited cleanly.")


def handle_signals(signum, frame):
    logger.info(f"Received shutdown signal ({signum}). Gracefully closing...")
    shutdown_event.set()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_signals)
    signal.signal(signal.SIGTERM, handle_signals)
    run_spot_bot()

```

---

### 📄 `test_engine.py`
**الوصف**: جناح الاختبارات الآلية (Unit Tests) لسلامة العمليات الحسابية

```python
"""
Automated Unit Test Suite for Binance Spot 24/7 Scalper Bot
Validates indicators, precision calculations, and scalper engine execution logic.
"""

import unittest
import os
import shutil
import tempfile
import indicators
import spot_engine
from config import Config


class TestIndicators(unittest.TestCase):
    def test_calculate_rsi_flat(self):
        prices = [100.0] * 20
        self.assertEqual(indicators.calculate_rsi(prices, 14), 50.0)

    def test_calculate_rsi_uptrend(self):
        prices = [100.0 + i for i in range(25)]
        rsi = indicators.calculate_rsi(prices, 14)
        self.assertGreater(rsi, 80.0)

    def test_calculate_rsi_downtrend(self):
        prices = [100.0 - i for i in range(25)]
        rsi = indicators.calculate_rsi(prices, 14)
        self.assertLess(rsi, 20.0)

    def test_calculate_dip_and_rebound(self):
        # Peak at 110, drops to 100 (9.09% dip), bounces to 102 (+2% rebound)
        closes = [100.0, 105.0, 110.0, 108.0, 104.0, 100.0, 101.5]
        dip, rebound = indicators.calculate_dip_and_rebound(closes, 102.0)
        self.assertGreater(dip, 8.0)
        self.assertGreater(rebound, 1.5)

    def test_calculate_dip_and_rebound_pure_uptrend(self):
        # Continual uptrend: should not register a dip
        closes = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0]
        dip, rebound = indicators.calculate_dip_and_rebound(closes, 110.0)
        self.assertEqual(dip, 0.0)


class TestPrecisionAndEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.temp_dir, "test_state.json")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_precision_from_step(self):
        self.assertEqual(spot_engine.precision_from_step(0.01), 2)
        self.assertEqual(spot_engine.precision_from_step(0.0001), 4)
        self.assertEqual(spot_engine.precision_from_step(0.00001), 5)
        self.assertEqual(spot_engine.precision_from_step(1.0), 0)

    def test_round_step(self):
        self.assertEqual(spot_engine.round_step(0.123456, 0.001), 0.123)
        self.assertEqual(spot_engine.round_step(0.000199, 0.0001), 0.0001)

    def test_round_tick(self):
        self.assertEqual(spot_engine.round_tick(65123.456, 0.01), 65123.46)
        self.assertEqual(spot_engine.round_tick(65123.454, 0.01), 65123.45)

    def test_scalper_engine_lifecycle(self):
        engine = spot_engine.SpotScalperEngine(
            symbol="BTC/USDT",
            target_order_usd=15.0,
            trailing_enabled=True,
            trailing_activation_pct=0.35,
            trailing_callback_pct=0.15,
            stop_loss_pct=0.80,
            buy_cooldown_sec=5,
            state_file=self.state_file,
        )
        engine.set_market_filters(2, 5, 0.01, 0.00001, 0.00001, 5.0)

        # 1. Test Buy Qty calculation
        price = 60000.0
        qty = engine.calculate_buy_qty(price)
        self.assertGreaterEqual(qty * price, 5.0)

        # 2. Open Position
        pos = engine.open_position(entry_price=60000.0, qty=qty)
        self.assertIsNotNone(engine.active_position)
        self.assertEqual(pos.entry_price, 60000.0)

        # 3. Can't buy when already in position
        can_buy, msg = engine.can_buy()
        self.assertFalse(can_buy)

        # 4. Trailing TP test: price rises by +0.50% (triggers activation at +0.35%)
        peak_price = 60000.0 * 1.0050
        exit_needed, reason, _ = engine.update_position_and_check_exit(peak_price)
        self.assertFalse(exit_needed)
        self.assertTrue(engine.active_position.trailing_active)

        # Price drops below trailing stop
        exit_price = 60000.0 * 1.0030
        exit_needed, reason, sell_qty = engine.update_position_and_check_exit(exit_price)
        self.assertTrue(exit_needed)
        self.assertIn("TRAILING_TAKE_PROFIT", reason)

        # 5. Close position
        trade = engine.close_position(exit_price, sell_qty, reason)
        self.assertIsNotNone(trade)
        self.assertGreater(trade.pnl_usd, 0)
        self.assertIsNone(engine.active_position)

        # 6. Verify state file was saved
        self.assertTrue(os.path.exists(self.state_file))


if __name__ == "__main__":
    unittest.main()

```

---

### 📄 `requirements.txt`
**الوصف**: حزم بايثون الأساسية المطلوبة

```text
ccxt>=4.1.0
python-dotenv>=1.0.0
requests>=2.31.0
urllib3>=2.0.0

```

---

### 📄 `Dockerfile`
**الوصف**: ملف بناء حاوية دوكر الجاهزة للتشغيل السحابي

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Environment defaults
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["python", "main.py"]

```

---

### 📄 `Procfile`
**الوصف**: أمر تشغيل الخادم والعملية الرئيسية

```text
web: python main.py

```

---

### 📄 `railway.json`
**الوصف**: إعدادات النشر على منصة Railway السحابية

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}

```

---

### 📄 `railway.toml`
**الوصف**: تكوين النشر البديل لـ Railway

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python main.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

```

---

### 📄 `.env.example`
**الوصف**: نموذج المتغيرات البيئية ومفاتيح الـ API

```bash
# ==========================================
# Binance Spot API credentials (Configure in Railway Variables)
# Never commit your real API keys to GitHub!
# ==========================================
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here
LIVE_TRADING=true

# Trading pair and position sizing
SYMBOL=BTC/USDT
TARGET_ORDER_USD=11.0
MAX_POSITIONS=1
LOOP_INTERVAL_SEC=10
BUY_COOLDOWN_SEC=60
BUY_DIP_MIN_PCT=0.25
BUY_REBOUND_CONFIRM_PCT=0.08
BUY_RSI_MAX=48
MIN_VOLATILITY_PCT=0.20
MAX_SPREAD_PCT=0.15
TRAILING_STOP_ENABLED=true
TRAILING_ACTIVATION_PCT=0.35
TRAILING_CALLBACK_PCT=0.15
STOP_LOSS_PCT=0.80
MAX_HOLD_TIME_SEC=1200
STAGNANT_EXIT_PCT=0.10
PORT=8080

# Entry Strategy: Buy confirmed dip + rebound
BUY_DIP_MIN_PCT=0.25
BUY_REBOUND_CONFIRM_PCT=0.08
BUY_RSI_MAX=48
MIN_VOLATILITY_PCT=0.20
MAX_SPREAD_PCT=0.15

# Exit Strategy: High-water trailing take profit + capital protection
TRAILING_STOP_ENABLED=true
TRAILING_ACTIVATION_PCT=0.35
TRAILING_CALLBACK_PCT=0.15
STOP_LOSS_PCT=0.80
MAX_HOLD_TIME_SEC=1200
STAGNANT_EXIT_PCT=0.10

# Optional proxy if Railway service is not in Europe (e.g. if in US)
# BINANCE_PROXY=http://user:pass@proxy-ip:port

```

---

### 📄 `.github/workflows/ci.yml`
**الوصف**: سير عمل الفحص الآلي المستمر (GitHub Actions CI)

```yaml
name: Python CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: python -m pip install -r requirements.txt

      - name: Compile Python files
        run: python -m py_compile config.py indicators.py spot_engine.py main.py

      - name: Run Unit Tests
        run: python -m unittest test_engine.py

```

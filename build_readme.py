import os

repo_dir = '/app/applet/wife_bain1_repo'

def read_file(filename):
    p = os.path.join(repo_dir, filename)
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

files_to_embed = [
    ('config.py', 'python', 'إعدادات البوت والتحقق من المتغيرات وأزواج التداول'),
    ('indicators.py', 'python', 'مؤشرات التحليل الفني (RSI، الارتداد اللحظي، والتذبذب)'),
    ('spot_engine.py', 'python', 'محرك الصفقات الفورية وحساب الكميات والوقف المتحرك (Trailing Stop)'),
    ('main.py', 'python', 'حلقة التداول اللحظي 24/7 وخادم لوحة التحكم وفحص الصحة'),
    ('test_engine.py', 'python', 'جناح الاختبارات الآلية (Unit Tests) لسلامة العمليات الحسابية'),
    ('requirements.txt', 'text', 'حزم بايثون الأساسية المطلوبة'),
    ('Dockerfile', 'dockerfile', 'ملف بناء حاوية دوكر الجاهزة للتشغيل السحابي'),
    ('Procfile', 'text', 'أمر تشغيل الخادم والعملية الرئيسية'),
    ('railway.json', 'json', 'إعدادات النشر على منصة Railway السحابية'),
    ('railway.toml', 'toml', 'تكوين النشر البديل لـ Railway'),
    ('.env.example', 'bash', 'نموذج المتغيرات البيئية ومفاتيح الـ API'),
    ('.github/workflows/ci.yml', 'yaml', 'سير عمل الفحص الآلي المستمر (GitHub Actions CI)'),
]

header = """# ⚡ بوت بينانس سبوت اللحظي 24/7 (Binance Spot 24/7 Scalper Bot) - الكود الكامل والدليل الشامل

بوت تداول فوري آلي مخصص للعمل على منصة **Binance Spot** على مدار الساعة **24/7 دون أي تجميد أو توقف**، متوافق كلياً مع منصة السحاب **Railway** وخوادم Docker، ومجهز بنظام وقف الأرباح المتحرك (Trailing Take-Profit)، وحماية رأس المال، والتعويض التلقائي لرسوم التداول.

---

## 📑 فهرس المحتويات
1. [المميزات والتصحيحات الجوهرية](#-المميزات-والتصحيحات-الجوهرية)
2. [إعداد المتغيرات البيئية (Environment Variables)](#-إعداد-المتغيرات-البيئية)
3. [دليل النشر والتشغيل (Deployment Guide)](#-دليل-النشر-والتشغيل)
4. [جناح الاختبارات الآلية (Unit Tests)](#-جناح-الاختبارات-الآلية)
5. [الأكواد البرمجية الكاملة لجميع ملفات المشروع](#-الأكواد-البرمجية-الكاملة-لجميع-ملفات-المشروع)
"""

for fname, lang, desc in files_to_embed:
    anchor = fname.replace('.', '').replace('/', '-')
    header += f"- [{fname}](#-{anchor}) : {desc}\n"

body = """
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
"""

output_parts = [header, body]

for fname, lang, desc in files_to_embed:
    code = read_file(fname)
    block = f"\n---\n\n### 📄 `{fname}`\n**الوصف**: {desc}\n\n```{lang}\n{code}\n```\n"
    output_parts.append(block)

full_readme = "".join(output_parts)

with open(os.path.join(repo_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(full_readme)

print("Generated full README.md successfully, length:", len(full_readme))

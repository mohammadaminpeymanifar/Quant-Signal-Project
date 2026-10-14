import requests

# آدرس MarketWatch که تو مستندات tsetmc بود
MARKET_URL = "https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch"


def get_market_overview(min_volume=100_000):
    """
    کل بازار رو با یه درخواست می‌گیره.
    فقط نمادهای فعال (با معامله امروز) رو برمی‌گردونه.
    """
    resp = requests.get(
        MARKET_URL,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    out = []
    for item in data.get("marketWatch", []):
        symbol = item.get("lva") or ""
        last = item.get("pdv") or 0      # آخرین معامله
        close = item.get("pcl") or 0     # پایانی
        yday = item.get("py") or 0       # پایانی دیروز
        volume = item.get("qtj") or 0    # حجم

        # فیلتر ساده: نماد باید معامله شده باشه
        if not symbol or last == 0 or volume < min_volume:
            continue

        out.append({
            "symbol": symbol,
            "last": int(last),
            "close": int(close),
            "yday": int(yday),
            "volume": int(volume),
        })

    return out
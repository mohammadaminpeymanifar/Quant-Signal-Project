from market import get_market_overview

m = get_market_overview()
print("تعداد کل:", len(m))
print("۵ تای اول:")
for item in m[:5]:
    print(item["symbol"], item["last"], item["volume"])
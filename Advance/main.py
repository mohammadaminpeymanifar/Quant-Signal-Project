from market import get_market_overview
from shortlist import shortlist
from load_data import load
from signal import evaluate
from table import print_table


def main():
    # ---- مرحله ۱: کل بازار ----
    print("در حال دریافت لیست بازار از tsetmc...")
    market = get_market_overview()
    print(f"✅ تعداد نمادهای فعال: {len(market)}")

    # ---- مرحله ۲: فیلتر درشت ----
    short = shortlist(market, top_n=15)
    print(f"✅ کاندیداها برای بررسی عمیق: {len(short)}")
    print(f"   {[c['symbol'] for c in short]}\n")

    # ---- مرحله ۳: امتیازدهی عمیق ----
    print("در حال محاسبه فیچرها...")
    rows = []
    for i, c in enumerate(short, 1):
        try:
            data = load(c["symbol"])
            feats, score, sig = evaluate(data)
            rows.append((c["symbol"], feats, score, sig))
            print(f"   [{i}/{len(short)}] {c['symbol']}: {score}/4")
        except Exception as e:
            print(f"   [{i}/{len(short)}] {c['symbol']}: خطا — {e}")

    # ---- مرحله ۴: مرتب و top 5 ----
    rows.sort(key=lambda x: x[2], reverse=True)
    top5 = rows[:5]

    print(f"\n🏆 ۵ نماد برتر:")
    print_table(top5)


if __name__ == "__main__":
    main()
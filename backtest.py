from load_data import load


def backtest(symbol, hold_days=5):
    """هر BUY فرضی رو ۵ روز نگه می‌داره و بازدهش رو حساب می‌کنه."""
    data = load(symbol)
    h = data["history"]
    trades = []

    for i in range(6, len(h) - hold_days):
        f1 = (h[i]["last"] - h[i - 1]["last"]) / h[i - 1]["last"] > 0
        f2 = h[i]["adj"] > h[i - 5]["adj"]
        avg5 = sum(h[j]["volume"] for j in range(i - 5, i)) / 5
        f4 = avg5 > 0 and h[i]["volume"] > avg5 * 1.5

        score = int(f1) + int(f2) + int(f4)
        if score < 3:
            continue

        buy = h[i]["adj"]
        sell = h[i + hold_days]["adj"]
        ret = (sell - buy) / buy * 100
        trades.append({"date": h[i]["date"], "return": ret})

    return trades


def report(trades, label):
    if not trades:
        print(f"{label}: هیچ معامله‌ای نبود")
        return
    returns = [t["return"] for t in trades]
    wins = sum(1 for r in returns if r > 0)
    print(f"\n{'=' * 40}")
    print(f"بک‌تست {label}")
    print(f"{'=' * 40}")
    print(f"تعداد: {len(trades)}")
    print(f"میانگین بازده: {sum(returns) / len(returns):.2f}%")
    print(f"نرخ برد: {wins / len(returns) * 100:.1f}%")
    print(f"مجموع: {sum(returns):.2f}%")


if __name__ == "__main__":
    for symbol, label in [("فولاد", "FOOLAD"), ("فملی", "FAMELI"), ("خودرو", "KHODRO")]:
        trades = backtest(symbol)
        report(trades, label)
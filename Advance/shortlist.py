def shortlist(candidates, top_n=15):
    """
    فیلتر درشت: از کل بازار، یه لیست کوچیک انتخاب کن.
    معیار: نمادهایی که امروز مثبتن، مرتب بر اساس حجم.
    """
    positive = []
    for c in candidates:
        if c["yday"] > 0 and c["last"] > c["yday"]:
            positive.append(c)

    # مرتب بر اساس حجم (شلوغ‌ترین اول)
    positive.sort(key=lambda c: c["volume"], reverse=True)

    return positive[:top_n]
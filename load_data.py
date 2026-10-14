import pytse_client as tse

_cache = {}


def _num(value, kind=float, default=0):
    """تبدیل امن به عدد. اگه None بود، default برمی‌گردونه."""
    if value is None:
        return default
    try:
        return kind(value)
    except (TypeError, ValueError):
        return default


def _str(value, default="—"):
    """تبدیل امن به متن."""
    if value is None:
        return default
    return str(value).strip()


def _day(value):
    text = str(value).split(".")[0]
    return text[:10] if len(text) >= 10 and text[4] == "-" else text


def load(symbol):
    """داده یک نماد رو از tsetmc می‌گیره و دیکشنری برمی‌گردونه."""
    if symbol in _cache:
        return _cache[symbol]

    t = tse.Ticker(symbol)

    history = [
        {
            "date": _day(r["date"]),
            "adj": _num(r["adjClose"], int),
            "last": _num(r["close"], int),
            "volume": _num(r["volume"], int),
        }
        for r in t.history.to_dict("records")
    ]

    clients = [
        {
            "date": _day(r["date"]),
            "real": _num(r["individual_buy_vol"], int),
            "legal": _num(r["corporate_buy_vol"], int),
        }
        for r in t.client_types.to_dict("records")
    ]
    clients.reverse()

    data = {
        "title": _str(t.title),
        "group": _str(t.group_name),
        "market": _str(t.flow),
        "last": _num(t.last_price, int),
        "yday": _num(t.yesterday_price, int),
        "pe": _num(t.p_e_ratio, float),
        "history": history,
        "clients": clients,
    }
    _cache[symbol] = data
    return data
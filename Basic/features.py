def feature_return_1d(data):
    """آیا بازده امروز مثبته؟"""
    if data["yday"] == 0:
        return False
    return (data["last"] - data["yday"]) / data["yday"] > 0


def feature_return_5d(data):
    """آیا بازده ۵ روزه مثبته؟"""
    h = data["history"]
    if len(h) < 6 or h[-6]["adj"] == 0:
        return False
    return h[-1]["adj"] > h[-6]["adj"]


def feature_real_buyer(data):
    """آیا حقیقی بیشتر از حقوقی خریده؟"""
    if not data["clients"]:
        return False
    last = data["clients"][-1]
    return last["real"] > last["legal"]


def feature_volume_spike(data, factor=1.5):
    """آیا حجم امروز از میانگین ۵ روز قبل بیشتره؟"""
    h = data["history"]
    if len(h) < 6:
        return False
    avg5 = sum(d["volume"] for d in h[-6:-1]) / 5
    if avg5 == 0:
        return False
    return h[-1]["volume"] > avg5 * factor
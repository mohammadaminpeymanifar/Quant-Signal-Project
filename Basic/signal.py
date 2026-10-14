from features import (
    feature_return_1d,
    feature_return_5d,
    feature_real_buyer,
    feature_volume_spike,
)


def evaluate(data):
    """چهار فیچر رو حساب می‌کنه و سیگنال برمی‌گردونه."""
    feats = {
        "R1": feature_return_1d(data),
        "R5": feature_return_5d(data),
        "RB": feature_real_buyer(data),
        "V": feature_volume_spike(data),
    }
    score = sum(feats.values())

    if score == 4:
        sig = "BUY"
    elif score == 3:
        sig = "WATCH"
    elif score == 2:
        sig = "WAIT"
    else:
        sig = "SELL"

    return feats, score, sig
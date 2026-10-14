from load_data import load
from signal import evaluate
from table import print_table


symbols = [
    ("فولاد", "FOOLAD"),
    ("فملی", "FAMELI"),
    ("خودرو", "KHODRO"),
    ("وبملت", "WEBMELAT"),
    ("شستا", "SHESTA"),
]


def main():
    rows = []
    for symbol, label in symbols:
        try:
            data = load(symbol)
            feats, score, sig = evaluate(data)
            rows.append((label, feats, score, sig))
        except Exception as e:
            print(f"خطا در {label}: {e}")
            rows.append((label, {"R1": False, "R5": False, "RB": False, "V": False}, 0, "ERR"))

    print_table(rows)


if __name__ == "__main__":
    main()
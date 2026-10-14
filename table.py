import sys
import re


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    GRAY = "\033[90m"


# اگه تو ترمینال نیستیم، رنگ‌ها رو خالی کن
if not sys.stdout.isatty():
    C.RESET = C.BOLD = C.RED = C.GREEN = C.YELLOW = ""
    C.CYAN = C.MAGENTA = C.GRAY = ""


SIGNAL_COLOR = {
    "BUY": C.GREEN,
    "WATCH": C.CYAN,
    "WAIT": C.YELLOW,
    "SELL": C.RED,
    "ERR": C.MAGENTA,
}

ANSI_RE = re.compile(r"\033\[[0-9;]*m")
visible_len = lambda s: len(ANSI_RE.sub("", s))


def print_table(rows):
    """
    rows: لیستی از (label, feats_dict, score, signal)
    """
    headers = ["Symbol", "R1", "R5", "RB", "V", "Score", "Signal"]
    mark = lambda v: f"{C.GREEN}✓{C.RESET}" if v else f"{C.GRAY}✗{C.RESET}"

    table = []
    for label, feats, score, sig in rows:
        color = SIGNAL_COLOR.get(sig, C.RESET)
        table.append([
            f"{C.BOLD}{label}{C.RESET}",
            mark(feats["R1"]),
            mark(feats["R5"]),
            mark(feats["RB"]),
            mark(feats["V"]),
            f"{score}/4",
            f"{color}{C.BOLD}{sig}{C.RESET}",
        ])

    widths = [visible_len(h) for h in headers]
    for row in table:
        for i, c in enumerate(row):
            widths[i] = max(widths[i], visible_len(c))

    def line(l, m, r):
        return l + m.join("─" * (w + 2) for w in widths) + r

    def row_str(cells, header=False):
        parts = []
        for i, cell in enumerate(cells):
            pad = widths[i] - visible_len(cell)
            s = f" {cell}{' ' * pad} "
            if header:
                s = f"{C.BOLD}{s}{C.RESET}"
            parts.append(s)
        return "│" + "│".join(parts) + "│"

    print(line("╭", "┬", "╮"))
    print(row_str(headers, header=True))
    print(line("├", "┼", "┤"))
    for row in table:
        print(row_str(row))
    print(line("╰", "┴", "╯"))
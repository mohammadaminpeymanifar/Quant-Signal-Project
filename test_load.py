from load_data import load

d = load("فولاد")
print("title:", d["title"])
print("group:", d["group"])
print("last:", d["last"])
print("history days:", len(d["history"]))
print("clients days:", len(d["clients"]))
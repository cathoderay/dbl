from dbl import DBL


N = 100000
dbl = DBL()


for i in range(N + 1):
    dbl.set(f"key-{i}", f"value-{i}")


# duplicates to test compaction
for j in range(N + 1):
    dbl.set(f"key-{0}", f"value-{j}")

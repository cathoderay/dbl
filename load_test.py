import sys

from dbl import DBL


N = 100 if not sys.argv[-1][-1].isdigit() else int(sys.argv[-1])
dbl = DBL()


for i in range(N + 1):
    dbl.set(f"key-{i}", f"value-{i}")


# duplicates to test compaction
for j in range(N + 1):
    dbl.set(f"key-{0}", f"value-{j}")

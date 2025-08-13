import sys

from dbl import DBL


N = 1000 if not sys.argv[-1][-1].isdigit() else int(sys.argv[-1])
dbl = DBL()

dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(N + 1)))

# duplicates to test compaction
dbl.set_bulk(tuple((f"key-{0}", f"value-{i}") for i in range(N + 1)))

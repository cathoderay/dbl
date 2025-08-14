import os
import sys


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL


N = 10 if not sys.argv[-1][-1].isdigit() else int(sys.argv[-1])
dbl = DBL()

dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(N + 1)), update_index=False)

# duplicates to test compaction
dbl.set_bulk(tuple((f"key-{0}", f"value-{i}") for i in range(N + 1)), update_index=False)

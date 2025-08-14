import os
import random
import sys


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL


N = 10 if not sys.argv[-1][-1].isdigit() else int(sys.argv[-1])
dbl = DBL()

dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(1, N + 1)), update_index=False)
print(f"Set {N} distinct keys in bulk.")

# duplicates to test compaction
random_key = f"key-{random.randint(1, N)}"
dbl.set_bulk(tuple((f"{random_key}", f"value-{i}") for i in range(1, N + 1)), update_index=False)
print(f"Set {N} new entries for key={random_key} in bulk.")
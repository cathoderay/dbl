import os
import random
import sys


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL


N = 10 if not sys.argv[-1][-1].isdigit() else int(sys.argv[-1])
dbl = DBL()

dbl.clean_all()
print("Starting clean.")
print("-"* 50)

print(f"Setting {N} distinct keys in bulk without updating the index...")
dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(1, N + 1)), update_index=False)
print("✅ Done.")
print("-"* 50)

# duplicates to test compaction
random_key = f"key-{random.randint(1, N)}"
print(f"Setting {N} new entries with the same key={random_key} in bulk without updating the index...")
dbl.set_bulk(tuple((f"{random_key}", f"value-{i}") for i in range(1, N + 1)), update_index=False)
print("✅ Done.")
print("-"* 50)

print("Cleaned database.")
dbl.clean_all()
print("✅ Done.")
print("-"* 50)

print(f"Setting {N} distinct keys in bulk updating the index...")
dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(1, N + 1)), update_index=True)
print("✅ Done.")
print("-"* 50)

# duplicates to test compaction
random_key = f"key-{random.randint(1, N)}"
print(f"Setting {N} new entries for key={random_key} in bulk updating the index...")
dbl.set_bulk(tuple((f"{random_key}", f"value-{i}") for i in range(1, N + 1)), update_index=True)
print("✅ Done.")
print("-"* 50)
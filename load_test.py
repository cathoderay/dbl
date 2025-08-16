import os
import random
import sys


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL

print(f"\n 🏁 LOAD TEST REPORT 🏁 {'-'*50}\n")
N = 10 if not sys.argv[-1][-1].isdigit() else int(sys.argv[-1])
dbl = DBL()

print("-"* 50)

dbl.clean_all()
print("Starting clean.")
print(dbl.get_index_metadata())

print(f"🏃‍➡️ Setting {N} distinct keys in bulk without updating the index...")
dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(1, N + 1)), update_index=False)
print("✅ Done.")
print(dbl.get_index_metadata())

# duplicates to test compaction
random_key = f"key-{random.randint(1, N)}"
print(f"🏃‍➡️ Setting {N} new entries with the same key={random_key} in bulk without updating the index...")
dbl.set_bulk(tuple((f"{random_key}", f"value-{i}") for i in range(1, N + 1)), update_index=False)
print("✅ Done.")
print(dbl.get_index_metadata())

print("Cleaned database.")
dbl.clean_all()
print("✅ Done.")
print(dbl.get_index_metadata())

# duplicates to test compaction
random_key = f"key-{random.randint(1, N)}"
print(f"🏃‍➡️ Setting {N} new entries for key={random_key} in bulk updating the index...")
dbl.set_bulk(tuple((f"{random_key}", f"value-{i}") for i in range(1, N + 1)), update_index=True)
print("✅ Done.")
print(dbl.get_index_metadata())

print("Cleaned database.")
dbl.clean_all()
print("✅ Done.")
print(dbl.get_index_metadata())

print(f"🏃‍➡️ Setting {N} distinct keys in bulk updating the index...")
dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(1, N + 1)), update_index=True)
print("✅ Done.")
print(dbl.get_index_metadata())
dbl.clean_all()


print(f"\n 🏁 LOAD TEST REPORT (CPP experiment) 🏁 {'-'*50}\n")

for _ in range(1): # change it to 50 to generate dataset of 1GB
    print(f"🏃‍➡️ Setting {N} distinct keys in bulk without updating the index...")
    dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(1, N + 1)), update_index=False)
    print("✅ Done.")

print("Performing a get with index being built in-memory via Python")
print(dbl.get("key-42", use_experiment=False))

print("Performing a get using index being built in-memory via C++ shared object")
print(dbl.get("key-42", use_experiment=True))

dbl.clean_all()

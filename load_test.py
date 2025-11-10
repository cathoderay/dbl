import os
import random


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL


class LoadTest:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"\n⏩ Load Test: {self.name}")
        self.dbl = DBL()
        self.dbl.clean_all()
        print("DB clean.")
        return self.dbl

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(dbl.get_index_metadata())
        self.dbl.clean_all()
        print("✅ Done.\n")


print(f"\n 🏁 LOAD TEST REPORT 🏁 {'-'*50}\n")


with LoadTest("distinct-keys") as dbl:
    n = 100_000
    print(f"🏃‍➡️ Setting {n} distinct keys with values of the same length in bulk...")
    for i in range(1, n + 1):
        dbl.set(f"key-{i}", f"value-{i}")
    print("Getting one inexistent key...")
    assert dbl.get("key-0") == None, "Value is not correct."
    print("Getting one existent key...")
    assert dbl.get("key-1") == "value-1", "Value is not correct."


with LoadTest("same-key") as dbl:
    n = 100_000
    random_key = f"{random.randint(1, n)}"
    print(f"🏃‍➡️ Setting {n} new entries with the same key={random_key} in bulk...")
    for i in range(1, n + 1):
        dbl.set(f"key-{random_key}", f"value-{i}")
    print("Getting one existent key...")
    assert dbl.get(f"key-{random_key}") == f"value-{n}", "Value is not correct."


with LoadTest("larger-values") as dbl:
    n = 100_000
    length = 500
    print(f"🏃‍➡️ Setting {n} distinct keys with values of length={length} in bulk...")
    for i in range(1, n + 1):
        dbl.set(f"key-{i}", f"{i}-" + "b"*length)
    random_key = f"{random.randint(1, n)}"
    print(f"Getting one existent key ({random_key})...")
    assert dbl.get(f"key-{random_key}") == f"{random_key}-" + "b"*length, "Value is not correct."

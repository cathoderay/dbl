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
        print()
        print(f"⏩ LoadTestName: {self.name}")
        self.dbl = DBL()
        self.dbl.clean_all()
        print("DB clean.")
        return self.dbl

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(dbl.get_index_metadata())
        self.dbl.clean_all()
        print("✅")
        print()


print(f"\n 🏁 LOAD TEST REPORT 🏁 {'-'*50}\n")


# distinct keys
with LoadTest("distinct-keys") as dbl:
    n = 100_000
    print(f"🏃‍➡️ Setting {n} distinct keys with values of the same length in bulk...")
    dbl.set_bulk(tuple((f"key-{i}", f"value-{i}") for i in range(1, n + 1)))
    print("Getting one inexistent key...")
    print(dbl.get("key-0"))
    print("Getting one existent key...")
    print(dbl.get("key-1"))


# same key
with LoadTest("same-key") as dbl:
    n = 100_000
    random_key = f"key-{random.randint(1, n)}"
    print(f"🏃‍➡️ Setting {n} new entries with the same key={random_key} in bulk...")
    dbl.set_bulk(tuple((f"{random_key}", f"value-{i}") for i in range(1, n + 1)))
    print("Getting one existent key...")
    print(dbl.get(random_key))


# distinct keys and larger values
with LoadTest("larger-values") as dbl:
    n = 100_000
    length = 500
    print(f"🏃‍➡️ Setting {n} distinct keys with values of length={length} in bulk...")
    dbl.set_bulk(tuple((f"key-{i}", f"{i}-" + "b"*length) for i in range(1, n + 1)))
    random_key = f"key-{random.randint(1, n)}"
    print(f"Getting one existent key ({random_key})...")
    print(dbl.get(random_key))

import os
import random


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL
from helper import dbl_profile


class BenchmarkTest:
    def __init__(self, internal):
        self.internal = internal 

    def __enter__(self):
        print(f"\n⏩ Benchmark: {self.internal}")
        self.dbl = DBL(internal=self.internal)
        self.dbl.clean_all()
        print("DB clean.")
        return self.dbl

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.dbl.get_index_metadata())
        self.dbl.clean_all()
        print("✅ Done.\n")


print(f"\n 🏁 BENCHMARK TEST REPORT 🏁 {'-'*50}\n")


@dbl_profile
def cpp():
    with BenchmarkTest("cpp") as dbl:
        n = 100_000
        print(f"🏃‍➡️ Setting {n} distinct keys with values of the same length...")
        for i in range(1, n + 1):
            dbl.set(f"key-{i}", f"value-{i}")
        print("Getting one inexistent key...")
        assert dbl.get("key-0") == None, "Value is not correct."
        print("Getting one existent key...")
        assert dbl.get("key-324") == "value-324", "Value is not correct."


@dbl_profile
def rust():
    with BenchmarkTest("rust") as dbl:
        n = 100_000
        print(f"🏃‍➡️ Setting {n} distinct keys with values of the same length...")
        for i in range(1, n + 1):
            dbl.set(f"key-{i}", f"value-{i}")
        print("Getting one inexistent key...")
        assert dbl.get("key-0") == None, "Value is not correct."
        print("Getting one existent key...")
        assert dbl.get("key-324") == "value-324", "Value is not correct."

rust()
cpp()
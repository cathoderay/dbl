import os
import random
from time import time


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL


class BenchmarkTest:
    def __init__(self, internal, type):
        self.internal = internal
        self.type = type

    def __enter__(self):
        print(f"\n⏩ Benchmark: {self.internal} | Type: {self.type}")
        self.dbl = DBL(internal=self.internal)
        self.dbl.clean_all()
        print("DB clean.")
        return self.dbl

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.dbl.get_index_metadata())
        self.dbl.clean_all()
        print("✅ Done.\n")


print(f"\n 🏁 BENCHMARK TEST REPORT 🏁 {'-'*50}\n")


n = 10_000
result = []
def write():
    for internal in ["cpp", "rust"]:
        with BenchmarkTest(internal, "write") as dbl:
            def write():
                print(f"🏃‍➡️ Setting {n} distinct keys with values of the same length...")
                for i in range(1, n + 1):
                    dbl.set(f"key-{i}", f"value-{i}")
            start = time()
            write()
            duration = time() - start
            assert dbl.get("key-0") == None
            assert dbl.get("key-324") == "value-324"
        result.append([f"{internal}-write", duration])



def read():
    for internal in ["cpp", "rust"]:
        with BenchmarkTest(internal, "read") as dbl:
            def write():
                print(f"🏃‍➡️ Setting {n} distinct keys with values of the same length...")
                for i in range(1, n + 1):
                    dbl.set(f"key-{i}", f"value-{i}")
            write()

            def read():
                print(f"🏃‍➡️ Gettting {n} distinct keys with values of the same length...")
                for i in range(1, n + 1):
                    assert dbl.get(f"key-{i}") == f"value-{i}"
            start = time()
            read()
            duration = time() - start
        result.append([f"{internal}-read", duration])


def print_results():
    width = 20
    header = " | ".join(f"{item:<{width}}" for item in [f"type (n = {n})", "time (in seconds)"])
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    for row in result:
        print(" | ".join(f"{item:<{width}}" for item in row))
    print("-" * len(header))


write()
read()
print_results()
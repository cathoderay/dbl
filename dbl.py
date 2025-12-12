#!/usr/bin/env python3

"""
    This is a naive implementation of a key-value log structured database
    inspired by the book "Designing Data-Intensive Applications: The Big Ideas
    Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann.
"""

__author__ = "Ronald Kaiser"


from datetime import datetime
import functools
import os
import pprint
import readline
import sys
import time


if os.getenv("DBL_TEST_ENV") == "1":
    import conf_test as conf
else:
    import conf
print(f"[{__name__}] conf file loaded: [{conf.__name__}]")

import dbl_internal # type: ignore


def print_debug(data):
    if not conf.DEBUG:
        return

    if isinstance(data, str):
        _print_debug(data)

    if isinstance(data, list):
        for datum in data:
            _print_debug(datum)


def print_profile(data):
    if not conf.PROFILE:
        return

    if isinstance(data, str):
        _print_profile(data)

    if isinstance(data, list):
        for datum in data:
            _print_profile(datum)


def _print_debug(line):
    print(f"\033[37m[DEBUG ({datetime.now()})]", line, "\033[0m")


def _print_profile(line):
    print(f"\033[37m[PROFILE ({datetime.now()})]", line, "\033[0m")


def encode(data):
    return data.encode(conf.ENCODING, errors="strict")


def decode(data):
    return data.decode(conf.ENCODING, errors="strict")


def dbl_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print_debug(f" ▶️ Entering {str(func.__name__)} {args} {kwargs}")
        result = func(*args, **kwargs)
        print_debug(f" ⬅️ Exiting {str(func.__name__)}")
        return result
    return wrapper


def dbl_profile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print_profile(f"Spent {end - start} in {str(func.__name__)}")
        return result
    return wrapper


@dbl_log
def validate(key, value):
    assert conf.KEY_VALUE_SEPARATOR not in key, \
    f"Key cannot contain separator ({conf.KEY_VALUE_SEPARATOR})"

    assert conf.END_RECORD not in value, \
    f"Value cannot contain character ({conf.END_RECORD})"


def print_ascii_logo():
    print(r"""
    Welcome to:

       ▐▌▗▖   █
       ▐▌▐▌   █
    ▗▞▀▜▌▐▛▀▚▖█
    ▝▚▄▟▌▐▙▄▞▘█

    version 0.1
    by Ronald Kaiser
    """)


class DBL:
    @dbl_log
    def __init__(self, database_path=conf.DATABASE_PATH):
        self.internal = dbl_internal 
        self.DATABASE_PATH = database_path
        self.initialize_internal()
        print(f"DBL initialized. Database opened at {database_path}.")

    def initialize_internal(self):
        dbl_internal.initialize(
            self.DATABASE_PATH,
            conf.KEY_VALUE_SEPARATOR,
            conf.END_RECORD,
            conf.DELETE_VALUE
        )

    @dbl_log
    @dbl_profile
    def set(self, key, value):
        validate(key, value)

        self.internal.set(encode(key), encode(value))
        return f"{key} => {value}"

    @dbl_profile
    @dbl_log
    def build_index(self):
        self.internal.build_index()
        return True

    @dbl_log
    def compact(self):
        self.internal.compact(conf.COMPACT_PATH)
        return f"{conf.COMPACT_PATH} written."

    @dbl_log
    def replace_from_compact(self):
        os.rename(conf.COMPACT_PATH, self.DATABASE_PATH)
        return f"{self.DATABASE_PATH} replaced from compact."

    @dbl_log
    @dbl_profile
    def get(self, key):
        value = decode(self.internal.get(encode(key)))
        return value if len(value) > 0 else None

    @dbl_profile
    @dbl_log
    def delete(self, key):
        self.internal.set(encode(key), encode(conf.DELETE_VALUE))
        assert self.get(key) == None
        return True

    @dbl_log
    @dbl_profile
    def find_tail(self, key):
        DEPTH_LIMIT = 42
        depth = DEPTH_LIMIT
        last = key
        cur = None
        seen = set([last])
        while depth and (cur:= self.get(last)):
            print(f"{last} => {cur}")
            if cur in seen: raise Exception("Cycle detected")
            seen.add(cur)
            depth -= 1
            last = cur
        return last

    @dbl_log
    def compact_and_replace(self):
        self.compact()
        self.replace_from_compact()
        return True

    @dbl_log
    def _remove_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
        assert os.path.exists(filename) == False, \
        f"It seems file {filename} was not removed correctly. Please, double check it."

    @dbl_log
    def clean_database(self):
        self._remove_file(conf.DATABASE_PATH)
        self._clean_index()
        return True

    @dbl_log
    def _clean_index(self):
        self.internal.clean_index()
        assert self.internal.get_index_size() == 0, \
        "It seems index still contains some keys."

    @dbl_log
    def clean_index(self):
        self._clean_index()
        return True

    @dbl_log
    def clean_compact(self):
        os.remove(conf.COMPACT_PATH)
        return f"{conf.COMPACT_PATH} removed."

    @dbl_log
    def clean_all(self):
        self.clean_index()
        self.clean_database()
        return True

    @dbl_log
    def _print_index_metadata(self):
        pprint.pprint({
            "number of keys": self.internal.get_index_size(),
            "bytes indexed": self.internal.get_bytes_read(),
            "keys": self.internal.get_index_keys()
        })

    @dbl_log
    def print_index_metadata(self):
        self.build_index()
        self._print_index_metadata()
        return True


class REPL:
    @dbl_log
    def __init__(self, database_path=conf.DATABASE_PATH):
        self.dbl = DBL(database_path)
        self.operations = {
            "build_index": lambda operands: self.dbl.build_index(),
            "check_debug_flag": lambda operands: str(conf.DEBUG),
            "clean_all": lambda operands: self.dbl.clean_all(),
            "clean_compact": lambda operands: self.dbl.clean_compact(),
            "clean_database": lambda operands: self.dbl.clean_database(),
            "clean_index": lambda operands: self.dbl.clean_index(),
            "compact": lambda operands: self.dbl.compact(),
            "compact_and_replace": lambda operands: self.dbl.compact_and_replace(),
            "del": lambda operands: self.dbl.delete(*operands),
            "exit": lambda operands: self.exit(),
            "find_tail": lambda operands: self.dbl.find_tail(*operands),
            "get": lambda operands: self.dbl.get(*operands),
            "help": lambda operands: self.help(),
            "index": lambda operands: self.dbl.print_index_metadata(),
            "replace_from_compact": lambda operands: self.dbl.replace_from_compact(),
            "set": lambda operands: self.dbl.set(*operands),
            "toggle_debug": lambda operands: self.toggle_debug(),
        }

    @dbl_log
    def start(self):
        print_ascii_logo()
        print(self.get_instructions())
        self.loop()

    @dbl_log
    def _loop(self):
        readline.parse_and_bind("tab: complete")
        while True:
            print()
            try:
                inp = input()
                if not inp: continue
                operator, *operands = inp.split()
                result = self.run(operator, operands)
                if result is None: print("☑️ None"); continue
                print("✅ " + (result if isinstance(result, str) else "Done."))
            except Exception as e:
                print("⚠️ " + str(e))

    @dbl_log
    def loop(self):
        try:
            self._loop()
        except KeyboardInterrupt:
            self.print_goodbye_message()

    def print_goodbye_message(self):
        print("\nThanks for using dbl!")
        print("Don't forget to eat your veggies! 🥦")

    def get_instructions(self):
        return "Type 'help' to list available operations."

    @dbl_log
    def help(self):
        operations = self.operations.keys()
        return "Operations available:\n" + "\n".join(map(lambda item: " * " + item, operations))

    @dbl_log
    def toggle_debug(self):
        conf.DEBUG ^= True
        return conf.DEBUG

    @dbl_log
    def run(self, operator, operands):
        if operator not in self.operations:
            raise Exception(f"🤷🏻‍♂️ Unknown operation. {self.get_instructions()}")

        return self.operations[operator](operands)

    @dbl_log
    def exit(self):
        self.print_goodbye_message()
        exit()


if __name__ == "__main__":
    if "--debug" in sys.argv: conf.DEBUG = True
    if "--profile" in sys.argv: conf.PROFILE = True
    database_path = sys.argv[1] if len(sys.argv) > 1 else conf.DATABASE_PATH
    repl = REPL(database_path)
    repl.start()
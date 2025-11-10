#!/usr/bin/env python3

"""
    This is a naive implementation of a key-value log structured database
    inspired by the book "Designing Data-Intensive Applications: The Big Ideas
    Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann.
"""

__author__ = "Ronald Kaiser"


import os
import readline
import sys


if os.getenv("DBL_TEST_ENV") == "1":
    import conf_test as conf
else:
    import conf
print(f"[{__name__}] conf file loaded: [{conf.__name__}]")


from helper import encode, decode, print_ascii_logo, dbl_log, dbl_profile, validate


# Rust integration --------------------------------------------------------------------------

import rust_internal # type: ignore

rust_internal = rust_internal
rust_internal.initialize(conf.DATABASE_PATH, conf.KEY_VALUE_SEPARATOR, conf.END_RECORD, conf.DELETE_VALUE)

# -------------------------------------------------------------------------------------------------


class DBL:
    @dbl_log
    def __init__(self, internal=None):
        self.internal = rust_internal
        print("Internal:", internal)
        print(f"Using {conf.DATABASE_PATH}")

    @dbl_log
    @dbl_profile
    def set(self, key, value):
        validate(key, value)

        self.internal.set(encode(key), encode(value))
        # TODO: check return code
        return f"{key} => {value}"

    @dbl_profile
    def validate_bulk(self, items):
        for key, value in items:
            validate(key, value)

    @dbl_profile
    @dbl_log
    def set_bulk(self, items):
        pass
        # self.validate_bulk(items)

        # pairs_type = KeyValueItem * len(items)
        # pairs = pairs_type()

        # for i, (key, value) in enumerate(items):
        #     pairs[i].key = encode(key)
        #     pairs[i].value = encode(value)

        # self.internal.set_bulk(pairs, len(items))

    @dbl_profile
    @dbl_log
    def build_index(self):
        return self.internal.build_index()

    @dbl_log
    def compact(self):
        self.internal.compact(conf.COMPACT_PATH)
        return f"{conf.COMPACT_PATH} written."

    @dbl_log
    def replace_from_compact(self):
        os.rename(conf.COMPACT_PATH, conf.DATABASE_PATH)
        return f"{conf.DATABASE_PATH} replaced from compact."

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
    def _get_index_metadata(self):
        return {
            "number of keys": self.internal.get_index_size(),
            "bytes indexed": self.internal.get_bytes_read()
        }

    @dbl_log
    def get_index_metadata(self):
        return str(self._get_index_metadata())


class REPL:
    @dbl_log
    def __init__(self):
        self.dbl = DBL()
        self.operations = {
            "help": lambda operands: self.help(),
            "set": lambda operands: self.dbl.set(*operands),
            "get": lambda operands: self.dbl.get(*operands),
            "del": lambda operands: self.dbl.delete(*operands),
            "compact": lambda operands: self.dbl.compact(),
            "compact_and_replace": lambda operands: self.dbl.compact_and_replace(),
            "replace_from_compact": lambda operands: self.dbl.replace_from_compact(),
            "build_index": lambda operands: self.dbl.build_index(),
            "toggle_debug": lambda operands: self.toggle_debug(),
            "check_debug_flag": lambda operands: str(conf.DEBUG),
            "clean_database": lambda operands: self.dbl.clean_database(),
            "clean_compact": lambda operands: self.dbl.clean_compact(),
            "clean_index": lambda operands: self.dbl.clean_index(),
            "clean_all": lambda operands: self.dbl.clean_all(),
            "index": lambda operands: self.dbl.get_index_metadata(),
            "find_tail": lambda operands: self.dbl.find_tail(*operands),
            "exit": lambda operands: self.exit()
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
                operator, *operands = input().split()
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
    repl = REPL()
    repl.start()

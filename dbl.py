#!/usr/bin/env python3

"""
    This is a naive implementation of a key-value log structured database
    inspired by the book "Designing Data-Intensive Applications: The Big Ideas
    Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann.
"""

__author__ = "Ronald Kaiser"


from collections import namedtuple
import os
import sys
import shutil
from typing import Dict


if os.getenv("DBL_TEST_ENV") == "1":
    import conf_test as conf
else:
    import conf
print(f"[{__name__}] conf file loaded: [{conf.__name__}]")


from helper import print_debug, encode, decode, print_ascii_logo, dbl_log, dbl_profile, validate


IndexValue = namedtuple("IndexValue", "start size")

# CPP integration -------------------------------------------------------------------------------------------------

import ctypes
import os

dbl_internal = None

if os.name != 'posix':
    print("Incompatible OS")
    exit(-1)

internal = 'internal.so'

try:
    dbl_internal = ctypes.CDLL(os.path.join(os.path.dirname(__file__), internal))
except OSError as e:
    print(f"Error loading library: {e}")
    print("Ensure {internal} is available (Linux/macOS)")
    exit(-1)

class KeyValueItem(ctypes.Structure):
    _fields_ = [
        ("key", ctypes.c_char_p),
        ("value", ctypes.c_char_p),
    ]

dbl_internal.initialize.argtypes = [ctypes.c_char_p]*3
dbl_internal.get.argtypes = [ctypes.c_char_p]
dbl_internal.get.restype = ctypes.c_char_p
dbl_internal.set.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
dbl_internal.get_bytes_read.restype = ctypes.c_longlong
dbl_internal.set_bulk.argtypes = [ctypes.POINTER(KeyValueItem), ctypes.c_int]
dbl_internal.initialize(encode(conf.DATABASE_PATH), encode(conf.KEY_VALUE_SEPARATOR), encode(conf.END_RECORD))

# -------------------------------------------------------------------------------------------------


class DBL:
    @dbl_log
    def __init__(self):
        print(f"Using {conf.DATABASE_PATH}")

    @dbl_log
    def get_filename(self, is_compact):
        if is_compact:
            return conf.COMPACT_PATH
        return conf.DATABASE_PATH

    @dbl_profile
    @dbl_log
    def set(self, key, value):
        validate(key, value)

        dbl_internal.set(encode(key), encode(value))
        # TODO: check return code
        return f"{key} => {value}"

    @dbl_profile
    def validate_bulk(self, items):
        for key, value in items:
            validate(key, value)

    @dbl_profile
    @dbl_log
    def set_bulk(self, items):
        self.validate_bulk(items)

        pairs_type = KeyValueItem * len(items)
        pairs = pairs_type()

        for i, (key, value) in enumerate(items):
            pairs[i].key = encode(key)
            pairs[i].value = encode(value)

        dbl_internal.set_bulk(pairs, len(items))

    @dbl_log
    def build_index(self):
        return dbl_internal.build_index()

    @dbl_log
    def compact(self):
        raise NotImplementedError("Not implemented")

    @dbl_log
    def compact_and_replace(self):
        raise NotImplementedError("Not implemented")

    @dbl_log
    def replace_from_compact(self):
        raise NotImplementedError("Not implemented")

    @dbl_log
    @dbl_profile
    def get(self, key):
        value = decode(dbl_internal.get(encode(key)))
        return value if len(value) > 0 else None

    @dbl_log
    def compact_and_replace(self):
        self.compact()
        self.replace_from_compact()

    @dbl_log
    def _remove_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

    @dbl_log
    def clean_database(self):
        self._remove_file(conf.DATABASE_PATH)
        self._clean_index()

    @dbl_log
    def _clean_index(self):
        dbl_internal.clean_index()

    @dbl_log
    def clean_index(self):
        self._clean_index()

    @dbl_log
    def clean_compact(self):
        raise NotImplementedError("Not implemented")

    @dbl_log
    def clean_all(self):
        self.clean_index()
        self.clean_database()

    @dbl_log
    def _get_index_metadata(self):
        metadata = []
        metadata.append(f"  Number of keys: {dbl_internal.get_index_size()}")
        metadata.append(f"  Bytes indexed: {dbl_internal.get_bytes_read()}")
        return metadata

    @dbl_log
    def get_index_metadata(self):
        return "\n".join(["Index: " + "-"*50] + self._get_index_metadata() + ["-"*50])


class REPL:
    @dbl_log
    def __init__(self):
        self.dbl = DBL()
        self.operations = {
            "help": lambda operands: self.help(),
            "set": lambda operands: self.dbl.set(*operands),
            "get": lambda operands: self.dbl.get(*operands),
            "compact": lambda operands: self.dbl.compact(),
            "compact_and_replace": lambda operands: self.dbl.compact_and_replace(),
            "replace_from_compact": lambda operands: self.dbl.replace_from_compact(),
            "build_index": lambda operands: self.dbl.build_index(),
            "toggle_debug_flag": lambda operands: self.toggle_debug(),
            "check_debug_flag": lambda operands: str(conf.DEBUG),
            "clean_database": lambda operands: self.dbl.clean_database(),
            "clean_compact": lambda operands: self.dbl.clean_compact(),
            "clean_index": lambda operands: self.dbl.clean_index(),
            "clean_all": lambda operands: self.dbl.clean_all(),
            "index": lambda operands: self.dbl.get_index_metadata(),
        }

    @dbl_log
    def start(self):
        print_ascii_logo()
        self.print_instructions()
        self.loop()

    @dbl_log
    def _loop(self):
        while True:
            print("\n=>", end=" ")
            try:
                operator, *operands = input().split()
                result = self.run(operator, operands)
                if result is None: print("☑️ None"); continue
                print("✅ " + (result if isinstance(result, str) else "Done."))
            except Exception as e:
                print(str(e))

    @dbl_log
    def loop(self):
        try:
            self._loop()
        except KeyboardInterrupt:
            self.print_goodbye_message()

    def print_goodbye_message(self):
        print("\nThanks for using dbl!")
        print("Don't forget to eat your veggies! 🥦")

    def print_instructions(self):
        print("Type help to list available operations.")

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
        try:
            self.operations[operator]
        except KeyError:
            raise KeyError("Unknown operation.")

        try:
            return self.operations[operator](operands)
        except KeyError:
            print("Unknown operation.")


if __name__ == "__main__":
    if "--debug" in sys.argv: conf.DEBUG = True
    if "--profile" in sys.argv: conf.PROFILE = True
    if "--db" in sys.argv: conf.DATABASE_PATH = sys.argv[-1] # todo: do proper parsing
    repl = REPL()
    repl.start()

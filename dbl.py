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


class DBL:
    @dbl_log
    def __init__(self):
        self.index: Dict[str, IndexValue] = {}
        self.bytes_indexed = 0
        print(f"Using {conf.DATABASE_PATH}")

    @dbl_log
    def get_encoded_data(self, key, value):
        return (
            encode(key),
            encode(conf.KEY_VALUE_SEPARATOR),
            encode(value),
            encode(conf.END_RECORD)
        )

    @dbl_log
    def _set(self, key, value, is_compact=False):
        validate(key, value)

        filename = self.get_filename(is_compact)
        key_b, sep_b, value_b, end_b = self.get_encoded_data(key, value)
        content = key_b + sep_b + value_b + end_b

        with open(filename, "ab") as file:
            file.seek(0, os.SEEK_END)
            value_start = file.tell() + len(key_b) + len(sep_b)
            file.write(content)
            if not is_compact:
                self._update_index(key, IndexValue(value_start, len(value_b)))
                self.bytes_indexed = file.tell()

    @dbl_log
    def get_filename(self, is_compact):
        if is_compact:
            return conf.COMPACT_PATH
        return conf.DATABASE_PATH

    @dbl_profile
    @dbl_log
    def _set_bulk(self, items, filename):
        for key, value in items:
            validate(key, value)

        content = b"".join(
            (b"".join(self.get_encoded_data(key, value))
            for key, value in items)
        )

        with open(filename, "ab") as file:
            file.seek(0, os.SEEK_END)
            file.write(content)

    @dbl_log
    def set(self, key, value, is_compact=False):
        self._set(key, value, is_compact)
        return f"{key} => {value}"

    @dbl_log
    def set_bulk(self, items, update_index, is_compact=False):
        filename = self.get_filename(is_compact)
        self._set_bulk(items, filename)

        if not update_index: return
        if not is_compact: self._build_index()

    @dbl_log
    def _update_index(self, index_key, index_value):
        self.index[index_key] = index_value

    @dbl_profile
    def _build_index(self, filename=None):
        if not filename:
            filename = self.get_filename(is_compact=False)

        with open(filename, 'rb') as file:
            file_size = os.path.getsize(filename)
            if self.index:
                if self.bytes_indexed == file_size:
                    print_debug("Index already built. Skipping.")
                    return self.bytes_indexed
                elif self.bytes_indexed < file_size:
                    print_debug("Resuming from last point...")
                    file.seek(self.bytes_indexed, os.SEEK_SET)
            start = file.tell()
            bytes_read = file.read()
        self._update_index_bulk(bytes_read, start)
        return self.bytes_indexed

    @dbl_profile
    @dbl_log
    def _update_index_bulk(self, bytes_read, start):
        END_RECORD_N = ord(conf.END_RECORD)
        KEY_VALUE_SEPARATOR_N = ord(conf.KEY_VALUE_SEPARATOR)

        key = current = []
        new_entries = 0
        for i, b in enumerate(bytes_read):
            if b == KEY_VALUE_SEPARATOR_N:
                key = current
                current = []
                start = i + 1
            elif b == END_RECORD_N:
                current = []
                end = i + 1
                self._update_index(decode(bytes(key)), IndexValue(start, end - start - 1))
                new_entries += 1
                start = end
            else:
                current.append(b)
        self.bytes_indexed = end
        print_debug(f"Found {new_entries} new entries.")

    @dbl_log
    def build_index(self, filename=None):
        if not filename:
            filename = self.get_filename(is_compact=False)
        return self._build_index(filename)

    @dbl_log
    @dbl_profile
    def get(self, key):
        filename = self.get_filename(is_compact=False)
        if not os.path.exists(filename):
            print("Empty db. Use operation 'set' to insert a new entry.")
            return
        self._build_index(filename)

        try:
            offset, size = self.index[key]
        except KeyError:
            raise ValueError("Key not found")

        try:
            with open(filename, 'rb') as file:
                file.seek(offset, 0)
                value = decode(file.read(size))
                return value
        except Exception as e:
            print(str(e))

    @dbl_log
    def _cleanup_compact(self):
        print_debug(f"Cleaning up {conf.COMPACT_PATH}...")
        file = open(conf.COMPACT_PATH, "w")
        file.close()

    @dbl_log
    def _compact(self):
        items = []
        for key in self.index:
            value = self.get(key)
            items.append((key, value))
        filename = self.get_filename(is_compact=True)
        self._set_bulk(items, filename)

    @dbl_log
    def compact(self):
        self._build_index()
        self._cleanup_compact()
        self._compact()

    @dbl_log
    def _copy_from_compact(self):
        shutil.copyfile(conf.COMPACT_PATH, conf.DATABASE_PATH)

    @dbl_log
    def _remove_compact(self):
        if os.path.exists(conf.COMPACT_PATH):
            os.remove(conf.COMPACT_PATH)

    @dbl_log
    def replace_from_compact(self):
        self._copy_from_compact()
        self._remove_compact()
        self._build_index()

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
    def clean_compact(self):
        self._remove_file(conf.COMPACT_PATH)

    @dbl_log
    def _clean_index(self):
        self.index = {}
        self.bytes_indexed = 0

    @dbl_log
    def clean_index(self):
        self._clean_index()

    @dbl_log
    def clean_all(self):
        self.clean_index()
        self.clean_database()
        self.clean_compact()

    @dbl_log
    def _get_index_metadata(self):
        metadata = []
        metadata.append(f"Number of keys: {len(self.index)}")
        metadata.append(f"Bytes indexed: {self.bytes_indexed}")
        metadata.append(f"Size of index object in bytes: {sys.getsizeof(self.index)}")
        return metadata

    @dbl_log
    def get_index_metadata(self):
        return "\n".join(["-"*50] + self._get_index_metadata() + ["-"*50])

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
            "index_metadata": lambda operands: self.dbl.get_index_metadata(),
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
                self.run(operator, operands)
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
            result = self.operations[operator](operands)
            print("✅ " + (result if isinstance(result, str) else "Done."))
        except KeyError:
            print("Unknown operation.")


if __name__ == "__main__":
    if "--debug" in sys.argv: conf.DEBUG = True
    if "--profile" in sys.argv: conf.PROFILE = True
    if "--db" in sys.argv: conf.DATABASE_PATH = sys.argv[-1] # todo: do proper parsing
    repl = REPL()
    repl.start()

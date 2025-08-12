#!/usr/bin/env python3

# Goal: naive experiment to study log-structured database
# Author: Ronald Kaiser


# Log of problems / solutions:
    # Problem 1: search is slow, have to go through the whole file to find last key/value.
    # Solution: build index in memory pointing to byte position of value. [done]

    # Problem 2: the client looses its index once the command is run.
    # Solution 1: have an index loaded in a instance always available.
    # Solution 2: add repl to interact with the db. [done]

    # Problem 3: many lines for the same key can make the file size greater than it should be
    # Solution 1: offer an operation to compact it [done]

    # Problem 4: compact operation is slow
    # Solution 1: offer a compact operation that writes bytes in bulk [todo]

    # Problem 5: compaction does not replace current data
    # Solution 1: offer an option to update it [done]

    # Problem 6: is it really faster with index? how much?
    # Solution 1: benchmark it [todo]

    # Problem 7: when new key/value is added by another process, local index is not updated
    # Solution 1: add how many bytes were read, and build index from there [done]

    # Problem 8: multiple processes can write at the same time and mess with data in disk
    # Solution 1: add lock for writes (allow many to read) [todo]


import os
import sys
import shutil

import conf
from helper import print_debug, encode, decode, print_ascii_logo, print_operations, dbl_log, validate


class DBL:
    @dbl_log
    def __init__(self):
        self.index = {}
        self.bytes_indexed = 0

    @dbl_log
    def set(self, key, value, filename=conf.DATABASE_FILENAME):
        validate(key, value)

        key_b = encode(key)
        separator_b = encode(conf.KEY_VALUE_SEPARATOR)
        value_b = encode(value)
        end_b = encode(conf.END_RECORD)

        content = key_b + separator_b + value_b + end_b

        with open(filename, "ab") as file:
            END = os.path.getsize(filename)
            value_start = END + len(key_b) + len(separator_b)
            self.index[key] = (value_start, len(value_b))
            file.seek(END, 0)
            file.write(content)
            self.bytes_indexed = file.tell()

        print_debug("Record written.")

    @dbl_log
    def build_index(self, filename=conf.DATABASE_FILENAME):
        with open(filename, 'rb') as file:
            filename_size = os.path.getsize(filename)
            if self.index:
                if self.bytes_indexed == filename_size:
                    print_debug("Index already built.")
                    return
                elif self.bytes_indexed < filename_size:
                    print_debug("Resuming from last point...")
                    file.seek(self.bytes_indexed, 0)
            key = current = b""
            start, end = file.tell(), file.tell()
            while (c:= file.read(1)):
                if decode(c) == conf.KEY_VALUE_SEPARATOR:
                    key = current
                    current = b""
                    start = file.tell()
                elif decode(c) == conf.END_RECORD:
                    current = b""
                    end = file.tell()
                    self.index[decode(key)] = (start, end - start - 1)
                    start, end = end, end
                else:
                    current += c
            self.bytes_indexed = file.tell()

        return self.index

    @dbl_log
    def get(self, key, filename=conf.DATABASE_FILENAME):
        self.build_index()

        try:
            offset, size = self.index[key]
        except KeyError:
            return None

        try:
            with open(filename, 'rb') as file:
                file.seek(offset, 0)
                value = decode(file.read(size))
                return value
        except Exception as e:
            print(str(e))

    @dbl_log
    def _cleanup_compact(self):
        print_debug(f"Cleaning up {conf.COMPACT_TEMP_FILENAME}...")
        file = open(conf.COMPACT_TEMP_FILENAME, "w")
        file.close()

    @dbl_log
    def _compact(self):
        for key in self.index.copy():
            value = self.get(key)
            self.set(key, value, filename=conf.COMPACT_TEMP_FILENAME)

    @dbl_log
    def compact(self):
        if not self.index: self.build_index()
        self._cleanup_compact()
        self._compact()

    @dbl_log
    def _copy_from_compact(self):
        shutil.copyfile(conf.COMPACT_TEMP_FILENAME, conf.DATABASE_FILENAME)

    @dbl_log
    def _remove_compact(self):
        if os.path.exists(conf.COMPACT_TEMP_FILENAME):
            os.remove(conf.COMPACT_TEMP_FILENAME)

    @dbl_log
    def replace_from_compact(self):
        self._copy_from_compact()
        self._remove_compact()
        self.build_index()

    @dbl_log
    def _remove_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

    @dbl_log
    def clean_database(self):
        self._remove_file(conf.DATABASE_FILENAME)
        self._clean_index()

    @dbl_log
    def clean_compact(self):
        self._remove_file(conf.COMPACT_TEMP_FILENAME)

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


if __name__ == "__main__":
    dbl = DBL()
    if "--debug" in sys.argv: conf.DEBUG = True
    if "--prebuild-index" in sys.argv: dbl.build_index()
    print_ascii_logo()
    while True:
        print("=>", end=" ")
        try:
            operator, *operands = input().split()
            if operator == "help":
                print_operations()
            elif operator == "set":
                dbl.set(*operands)
            elif operator == "get":
                print(dbl.get(*operands))
            elif operator == "compact":
                dbl.compact()
            elif operator == "compact_and_replace":
                dbl.compact()
                dbl.replace_from_compact()
            elif operator == "replace_from_compact":
                dbl.replace_from_compact()
            elif operator == "build_index":
                print(dbl.build_index())
            elif operator == "toggle_debug":
                conf.DEBUG ^= True
            elif operator == "clean_database":
                dbl.clean_database()
            elif operator == "clean_compact":
                dbl.clean_compact()
            elif operator == "clean_index":
                dbl.clean_index()
            elif operator == "clean_all":
                dbl.clean_all()
            elif operator == "check_debug":
                print(conf.DEBUG)
            elif operator == "bytes_indexed":
                print(dbl.bytes_indexed)
            else:
                print("Unknown command.")
        except Exception as e:
            print(str(e))

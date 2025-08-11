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

    # Problem 6: how fast is search with index vs not using index
    # Solution 1: benchmark it [todo]

    # Problem 7: check if index is updated before get a new key
    # Solution 1: add how many bytes were read [done]


import os
import sys
import shutil

from helper import print_debug, encode, decode


DATABASE_FILENAME = "dbl.data"
COMPACT_TEMP_FILENAME = "dbl.compact"
END_RECORD = "\n"
KEY_VALUE_SEPARATOR = ","
DEBUG = False


class DBL:
    def __init__(self):
        self.index = {}
        self.bytes_read = 0

    def validate(self, key, value):
        assert KEY_VALUE_SEPARATOR not in key, \
        f"Key cannot contain separator ({KEY_VALUE_SEPARATOR})"

        assert END_RECORD not in value, \
        f"Value cannot contain character ({END_RECORD})"

    def set(self, key, value, filename=DATABASE_FILENAME):
        if DEBUG: print_debug("Inside set", key, value)

        self.validate(key, value)

        key_b = encode(key)
        separator_b = encode(KEY_VALUE_SEPARATOR)
        value_b = encode(value)
        end_b = encode(END_RECORD)

        content = key_b + separator_b + value_b + end_b

        with open(filename, "ab") as file:
            END = os.path.getsize(filename) if os.path.exists(filename) else 0
            value_start = END + len(key_b) + len(separator_b)
            self.index[key] = (value_start, len(value_b))
            file.seek(END, 0)
            file.write(content)

        if DEBUG: print_debug("Record written.")

    def build_index(self):
        if DEBUG: print_debug("Bulding index...")

        with open(DATABASE_FILENAME, 'rb') as file:
            if self.index:
                file.seek(self.bytes_read + 1, 0)
            key = b""
            current = b""
            start, end = 0, 0
            while (c:= file.read(1)):
                if decode(c) == KEY_VALUE_SEPARATOR:
                    key = current
                    current = b""
                    start = file.tell()
                elif decode(c) == END_RECORD:
                    current = b""
                    end = file.tell()
                    self.index[decode(key)] = (start, end - start - 1)
                    start, end = end, end
                else:
                    current += c
            self.bytes_read = file.tell()

        if DEBUG: print_debug("Index built.")

    def get(self, key):
        if DEBUG: print_debug("Inside get", key)

        self.build_index()

        try:
            offset, size = self.index[key]
        except KeyError:
            return None

        with open(DATABASE_FILENAME, 'rb') as file:
            try:
                file.seek(offset, 0)
                value = decode(file.read(size))
            except KeyError:
                value = None

        return value

    def _cleanup_compact(self):
        if DEBUG: print_debug("Inside cleanup compact")
        if DEBUG: print_debug(f"Cleaning up {COMPACT_TEMP_FILENAME}...")
        file = open(COMPACT_TEMP_FILENAME, "w")
        file.close()
        if DEBUG: print_debug(f"Done.")

    def _compact(self):
        if DEBUG: print_debug(f"Compacting...")
        for key in self.index:
            value = self.get(key)
            self.set(key, value, filename=COMPACT_TEMP_FILENAME)
        if DEBUG: print_debug(f"Done.")

    def compact(self):
        if DEBUG: print_debug("Inside compact")
        if not self.index: self.build_index()
        self._cleanup_compact()
        self._compact()
        print(f"Compact version generated at: {COMPACT_TEMP_FILENAME}")

    def _copy_from_compact(self):
        if DEBUG: print_debug(f"Copying from {COMPACT_TEMP_FILENAME} to {DATABASE_FILENAME}...")
        shutil.copyfile(COMPACT_TEMP_FILENAME, DATABASE_FILENAME)
        if DEBUG: print_debug(f"Done.")

    def _remove_compact(self):
        if DEBUG: print_debug(f"Removing {COMPACT_TEMP_FILENAME}...")
        if os.path.exists(COMPACT_TEMP_FILENAME):
            os.remove(COMPACT_TEMP_FILENAME)
        if DEBUG: print_debug(f"Done.")

    def replace_from_compact(self):
        if DEBUG: print_debug("Inside replace from compact")

        self._copy_from_compact()
        self._remove_compact()
        self.build_index()

    def _remove_file(self, filename):
        if DEBUG: print_debug(f"Removing {filename}...")
        if os.path.exists(filename):
            os.remove(filename)
        if DEBUG: print_debug("Done.")

    def clean_database(self):
        if DEBUG: print_debug(f"Inside clean database")
        self._remove_file(DATABASE_FILENAME)
        self.index = {}
        self.bytes_read = 0
        if DEBUG: print_debug("Done.")

    def clean_compact(self):
        if DEBUG: print_debug(f"Inside clean compact")
        self._remove_file(COMPACT_TEMP_FILENAME)
        if DEBUG: print_debug("Done.")


if __name__ == "__main__":
    dbl = DBL()
    if "--debug" in sys.argv:
        DEBUG = True
    if "--prebuild-index" in sys.argv:
        dbl.build_index()
    operations = "help,set,get,compact,compact_and_replace,replace_from_compact,build_index,toggle_debug,check_debug,clean_database,clean_compact,bytes_read"
    while True:
        print("=>", end=" ")
        try:
            operator, *operands = input().split()

            if operator == "help":
                print("Operations available:", operations)
            elif operator == "set":
                dbl.set(*operands)
            elif operator == "get":
                value = dbl.get(*operands)
                print(value)
            elif operator == "compact":
                dbl.compact()
            elif operator == "compact_and_replace":
                dbl.compact()
                dbl.replace_from_compact()
            elif operator == "replace_from_compact":
                dbl.replace_from_compact()
            elif operator == "build_index":
                dbl.build_index()
                print(dbl.index)
            elif operator == "toggle_debug":
                DEBUG ^= True
                print(DEBUG)
            elif operator == "clean_database":
                dbl.clean_database()
            elif operator == "clean_compact":
                dbl.clean_compact()
            elif operator == "check_debug":
                print(DEBUG)
            elif operator == "bytes_read":
                print(dbl.bytes_read)
            else:
                print("Unknown command.")

        except Exception as e:
            print(str(e))

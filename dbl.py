#!/usr/bin/env python3

# Goal: naive experiment to study log-structured database
# Author: Ronald Kaiser


import os
import sys
import shutil

import conf
from helper import print_debug, encode, decode, print_ascii_logo, dbl_log, validate


class DBL:
    @dbl_log
    def __init__(self):
        self.index = {}
        self.bytes_indexed = 0

    @dbl_log
    def set(self, key, value, is_compact=False):
        if is_compact:
            filename = conf.COMPACT_TEMP_FILENAME
        else:
            filename = conf.DATABASE_FILENAME

        validate(key, value)

        key_b = encode(key)
        separator_b = encode(conf.KEY_VALUE_SEPARATOR)
        value_b = encode(value)
        end_b = encode(conf.END_RECORD)

        content = key_b + separator_b + value_b + end_b

        with open(filename, "ab") as file:
            END = os.path.getsize(filename)
            value_start = END + len(key_b) + len(separator_b)
            file.seek(END, 0)
            file.write(content)
            self.bytes_indexed = file.tell()
            if not is_compact:
                self.index[key] = (value_start, len(value_b))
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
        print_debug("Index built.")
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
            self.set(key, value, is_compact=True)

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
    def compact_and_replace(self):
        self.compact()
        self.replace_from_compact()

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

    @dbl_log
    def _get_index_metadata(self):
        metadata = []
        metadata.append(f"Number of keys: {len(self.index)}")
        metadata.append(f"Bytes indexed: {self.bytes_indexed}")
        metadata.append(f"Size of index object in bytes: {sys.getsizeof(self.index)}")
        return metadata

    @dbl_log
    def get_index_metadata(self):
        for line in self._get_index_metadata():
            print(line)

class REPL:
    @dbl_log
    def __init__(self, dbl=None):
        self.dbl = dbl
        self.operations = {
            "help": lambda operands: self.help(),
            "set": lambda operands: self.dbl.set(*operands),
            "get": lambda operands: self.dbl.get(*operands),
            "compact": lambda operands: self.dbl.compact(),
            "compact_and_replace": lambda operands: self.dbl.compact_and_replace(),
            "replace_from_compact": lambda operands: self.dbl.replace_from_compact(),
            "build_index": lambda operands: self.dbl.build_index(),
            "toggle_debug_flag": lambda operands: self.toggle_debug(),
            "check_debug_flag": lambda operands: conf.DEBUG,
            "clean_database": lambda operands: self.dbl.clean_database(),
            "clean_compact": lambda operands: self.dbl.clean_compact(),
            "clean_index": lambda operands: self.dbl.clean_index(),
            "clean_all": lambda operands: self.dbl.clean_all(),
            "index_metadata": lambda operands: self.dbl.get_index_metadata(),
        }

        print_ascii_logo()

        self.dbl = DBL()
        while True:
            print("=>", end=" ")
            try:
                operator, *operands = input().split()
                self.run(operator, operands)
            except Exception as e:
                print(str(e))

    @dbl_log
    def help(self):
        operations = self.operations.keys()
        print("Operations available:")
        print("\n".join(map(lambda item: " * " + item, operations)))

    @dbl_log
    def toggle_debug(self):
        conf.DEBUG ^= True
        return conf.DEBUG

    @dbl_log
    def run(self, operator, operands):
        to_print = "get check_debug_flag bytes_indexed toggle_debug_flag".split()
        try:
            if operator in to_print:
                print(self.operations[operator](operands))
            else:
                self.operations[operator](operands)
        except KeyError:
            print("Unknown command.")


if __name__ == "__main__":
    if "--debug" in sys.argv: conf.DEBUG = True
    repl = REPL()

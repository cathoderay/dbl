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

import conf
from helper import print_debug, encode, decode, print_ascii_logo, dbl_log, validate


IndexValue = namedtuple("IndexValue", "start size")


class DBL:
    @dbl_log
    def __init__(self):
        self.index: Dict[str, IndexValue] = {}
        self.bytes_indexed = 0

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
                self.bytes_indexed = file.tell()
                self._update_index(key, IndexValue(value_start, len(value_b)))

    @dbl_log
    def get_filename(self, is_compact):
        if is_compact:
            return conf.COMPACT_FILENAME
        return conf.DATABASE_FILENAME

    @dbl_log
    def _set_bulk(self, items, is_compact=False):
        for key, value in items:
            validate(key, value)

        filename = self.get_filename(is_compact)

        with open(filename, "ab") as file:
            file.seek(0, os.SEEK_END)
            for key, value in items:
                key_b, sep_b, value_b, end_b = self.get_encoded_data(key, value)
                content = key_b + sep_b + value_b + end_b

                value_start = file.tell() + len(key_b) + len(sep_b)
                file.write(content)

                if not is_compact:
                    self.bytes_indexed = file.tell()
                    self._update_index(key, IndexValue(value_start, len(value_b)))

    @dbl_log
    def set(self, key, value, is_compact=False):
        self._set(key, value, is_compact)
        return f"{key} => {value}"

    @dbl_log
    def set_bulk(self, items):
        self._set_bulk(items)

    @dbl_log
    def _update_index(self, index_key, index_value):
        self.index[index_key] = index_value

    @dbl_log
    def _build_index(self, filename=conf.DATABASE_FILENAME):
        with open(filename, 'rb') as file:
            filename_size = os.path.getsize(filename)
            if self.index:
                if self.bytes_indexed == filename_size:
                    print_debug("Index already built. Skipping.")
                    return self.bytes_indexed
                elif self.bytes_indexed < filename_size:
                    print_debug("Resuming from last point...")
                    file.seek(self.bytes_indexed, os.SEEK_SET)
                    return self.bytes_indexed
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
                    self._update_index(decode(key), IndexValue(start, end - start - 1))
                    start, end = end, end
                else:
                    current += c
            self.bytes_indexed = file.tell()
        return self.bytes_indexed

    @dbl_log
    def build_index(self, filename=conf.DATABASE_FILENAME):
        return self._build_index(filename)

    @dbl_log
    def get(self, key, filename=conf.DATABASE_FILENAME):
        if not os.path.exists(filename):
            print("Empty db. Use operation 'set' to insert a new entry.")
            return
        self._build_index()

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
        print_debug(f"Cleaning up {conf.COMPACT_FILENAME}...")
        file = open(conf.COMPACT_FILENAME, "w")
        file.close()

    @dbl_log
    def _compact(self):
        items = []
        for key in self.index:
            value = self.get(key)
            items.append((key, value))
        self._set_bulk(items, is_compact=True)

    @dbl_log
    def compact(self):
        self._build_index()
        self._cleanup_compact()
        self._compact()

    @dbl_log
    def _copy_from_compact(self):
        shutil.copyfile(conf.COMPACT_FILENAME, conf.DATABASE_FILENAME)

    @dbl_log
    def _remove_compact(self):
        if os.path.exists(conf.COMPACT_FILENAME):
            os.remove(conf.COMPACT_FILENAME)

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
        self._remove_file(conf.DATABASE_FILENAME)
        self._clean_index()

    @dbl_log
    def clean_compact(self):
        self._remove_file(conf.COMPACT_FILENAME)

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
            "check_debug_flag": lambda operands: conf.DEBUG,
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
    repl = REPL()
    repl.start()

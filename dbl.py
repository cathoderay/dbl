#!/usr/bin/env python3

# Experiment on log-structured database
# Author: Ronald Kaiser


# Problem 1: search is slow, have to go through the whole file to find last key/value.
# Solution: build index in memory pointing to byte position of value. [chosen]

# Problem 2: the client looses it's index once the command is run.
# Solution 1: have an index loaded in a instance always available.
# Solution 2: add repl to interact with the db. [chosen]

# Problem 3: many lines for the same key can make the file size greater than it should be
# Solution 1: offer an operation to compact it [chosen]


import os
import sys

from helper import print_debug, encode, decode


DATABASE_FILENAME = "dbl.data"
COMPACT_TEMP_FILENAME = "dbl.compact"
END_RECORD = "\n"
KEY_VALUE_SEPARATOR = ","
DEBUG = False

index = {}


def validate(key, value):
    assert KEY_VALUE_SEPARATOR not in key, \
    f"Key cannot contain separator ({KEY_VALUE_SEPARATOR})"

    assert END_RECORD not in value, \
    f"Value cannot contain new line character ({END_RECORD})"


def set(key, value, filename=DATABASE_FILENAME):
    if DEBUG: print_debug("Inside set", key, value)

    validate(key, value)

    key_b = encode(key)
    separator_b = encode(KEY_VALUE_SEPARATOR)
    value_b = encode(value)
    end_b = encode(END_RECORD)

    content = key_b + separator_b + value_b + end_b

    END = os.path.getsize(filename) if os.path.isfile(filename) else 0

    value_start = END + len(key_b) + len(separator_b)
    index[key] = (value_start, len(value_b))

    with open(filename, "ab") as file:
        file.seek(END, 0)
        file.write(content)

    if DEBUG: print_debug("Record written.")


def build_index():
    if DEBUG: print_debug("Bulding index...")

    with open(DATABASE_FILENAME, 'rb') as file:
        key = ""
        current = ""
        start, end = 0, 0
        while (c:= file.read(1)):
            c = decode(c)
            if c == KEY_VALUE_SEPARATOR:
                key = current
                current = ""
                start = file.tell()
            elif c == END_RECORD:
                current = ""
                end = file.tell()
                index[key] = (start, end - start - 1)
                start, end = end, end
            else:
                current += c

    if DEBUG: print_debug("Index built.")


def get(key):
    if DEBUG: print_debug("Inside get", key)

    if not index:
        build_index()

    try:
        offset, size = index[key]
    except KeyError:
        return None

    with open(DATABASE_FILENAME, 'rb') as file:
        try:
            file.seek(offset, 0)
            value = decode(file.read(size))
        except KeyError:
            value = None

    return value


def compact():
    if DEBUG: print_debug("Inside compact")

    if not index:
        build_index()

    file = open(COMPACT_TEMP_FILENAME, "w")
    file.close()

    for key in index:
        value = get(key)
        set(key, value, filename=COMPACT_TEMP_FILENAME)

    print(f"Compact version generated at: {COMPACT_TEMP_FILENAME}")


if __name__ == "__main__":
    if "--debug" in sys.argv:
        DEBUG = True
    while True:
        print("=>", end=" ")
        try:
            operator, *operands = input().split()

            if operator == "set":
                set(*operands)
            elif operator == "get":
                value = get(*operands)
                print(value)
            elif operator == "compact":
                compact()
            elif operator == "build_index":
                build_index()
                print(index)
        except Exception as e:
            print(str(e))

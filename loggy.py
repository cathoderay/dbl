#!/usr/bin/env python3

# Experiment on log-structured database
# Author: Ronald Kaiser
# Date: 2025-08-08


# Problem 1: search is slow, have to go through the whole file to find last key/value.
# Solution: build index in memory pointing to byte position of value.

# Problem 2: the client looses it's index once the command is run.
# Solution: have an index loaded in a instance always available.


import os
import sys


DATABASE_FILENAME = "/tmp/db.loggy"
END_RECORD = "\n"
KEY_VALUE_SEPARATOR = ","
ENCODING = "utf-8"
DEBUG = True


index = {}


def set(key, value):
	if DEBUG:
		print("Inside set", key, value)

	key_b = key.encode(ENCODING)
	separator_b = KEY_VALUE_SEPARATOR.encode(ENCODING)
	value_b = value.encode(ENCODING)
	end_b = END_RECORD.encode(ENCODING)
	content = key_b + separator_b + value_b + end_b
	END = os.path.getsize(DATABASE_FILENAME)
	value_start = END + len(key_b) + len(separator_b)
	index[key] = (value_start, len(value_b))

	with open(DATABASE_FILENAME, 'ab+') as file:
		file.seek(END, 0)
		file.write(content)


def build_index():
	if DEBUG:
		print("Bulding index...")

	with open(DATABASE_FILENAME, 'rb') as file:
		key = ""
		current = ""
		start, end = 0, 0
		while (c:= file.read(1)):
			c = c.decode(ENCODING)
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


def get(key):
	if DEBUG:
		print("Inside get", key)

	if not index:
		build_index()

	try:
		offset, size = index[key]
	except KeyError:
		return None

	with open(DATABASE_FILENAME, 'rb') as file:
		try:
			file.seek(offset, 0)
			value = file.read(size).decode(ENCODING)
		except KeyError:
			value = None

	return value


if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("Two operations available: get and set")
		exit(-1)
	elif len(sys.argv) == 3 and sys.argv[1] == 'get':
		print(get(sys.argv[2]))
	elif len(sys.argv) == 4 and sys.argv[1] == 'set':
		set(sys.argv[2], sys.argv[3])
		print("Record written.")
	else:
		print("Invalid command. No operation performed.")

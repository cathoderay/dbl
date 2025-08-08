#!/usr/bin/env python3

# Experiment on log-structured database
# Author: Ronald Kaiser
# Date: 2025-08-08


import sys


DATABASE_FILENAME = "/tmp/db.loggy"


def set(key, value):
	with open(DATABASE_FILENAME, 'a+') as file:
		file.write(f"{key},{value}\n")


def get(key):
	with open(DATABASE_FILENAME, 'r') as file:
		value = None
		for line in file.readlines():
			k, *v = line.split(",")
			if k == key:
				value = v[0][:-1] # remove \n
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
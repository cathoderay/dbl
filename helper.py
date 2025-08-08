ENCODING = "utf-8"

def print_debug(*args):
    print("DEBUG: ", *args)


def encode(data):
	return data.encode(ENCODING)


def decode(data):
	return data.decode(ENCODING)
ENCODING = "utf-8"


def print_debug(*args):
    print("DEBUG: ", *args)


def encode(data):
    return data.encode(ENCODING, errors="ignore")


def decode(data):
    return data.decode(ENCODING, errors="ignore")
import conf


def print_debug(*args):
    if conf.DEBUG: print("DEBUG: ", *args)


def encode(data):
    return data.encode(conf.ENCODING, errors="ignore")


def decode(data):
    return data.decode(conf.ENCODING, errors="ignore")


def dbl_log(func):
    def wrapper(*args, **kwargs):
        if conf.DEBUG: print("DEBUG: ", "Entering", str(func.__name__), f"{args}", f"{kwargs}")
        result = func(*args, **kwargs)
        if conf.DEBUG: print("DEBUG: ", "Exiting", str(func.__name__))
        return result
    return wrapper


@dbl_log
def validate(key, value):
    assert conf.KEY_VALUE_SEPARATOR not in key, \
    f"Key cannot contain separator ({conf.KEY_VALUE_SEPARATOR})"

    assert conf.END_RECORD not in value, \
    f"Value cannot contain character ({conf.END_RECORD})"



def print_ascii_logo():
    print(r"""
    Welcome to
          _____                    _____                    _____
         /\    \                  /\    \                  /\    \
        /::\    \                /::\    \                /::\____\
       /::::\    \              /::::\    \              /:::/    /
      /::::::\    \            /::::::\    \            /:::/    /
     /:::/\:::\    \          /:::/\:::\    \          /:::/    /
    /:::/  \:::\    \        /:::/__\:::\    \        /:::/    /
   /:::/    \:::\    \      /::::\   \:::\    \      /:::/    /
  /:::/    / \:::\    \    /::::::\   \:::\    \    /:::/    /
 /:::/    /   \:::\ ___\  /:::/\:::\   \:::\ ___\  /:::/    /
/:::/____/     \:::|    |/:::/__\:::\   \:::|    |/:::/____/
\:::\    \     /:::|____|\:::\   \:::\  /:::|____|\:::\    \
 \:::\    \   /:::/    /  \:::\   \:::\/:::/    /  \:::\    \
  \:::\    \ /:::/    /    \:::\   \::::::/    /    \:::\    \
   \:::\    /:::/    /      \:::\   \::::/    /      \:::\    \
    \:::\  /:::/    /        \:::\  /:::/    /        \:::\    \
     \:::\/:::/    /          \:::\/:::/    /          \:::\    \
      \::::::/    /            \::::::/    /            \:::\    \
       \::::/    /              \::::/    /              \:::\____\
        \::/____/                \::/____/                \::/    /
         ~~                       ~~                       \/____/

    version 0.1
    by Ronald Kaiser
    """)


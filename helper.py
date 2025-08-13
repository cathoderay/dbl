import conf
from datetime import datetime


def print_debug(data):
    if not conf.DEBUG:
        return

    if isinstance(data, str):
        _print_debug(data)

    if isinstance(data, list):
        for datum in data:
            _print_debug(datum)


def _print_debug(line):
    print(f"\033[37m[DEBUG [{datetime.now()}]", line, "\033[0m")


def encode(data):
    return data.encode(conf.ENCODING, errors="ignore")


def decode(data):
    return data.decode(conf.ENCODING, errors="ignore")


def dbl_log(func):
    def wrapper(*args, **kwargs):
        print_debug(f" ▶️ Entering {str(func.__name__)} {args} {kwargs}")
        result = func(*args, **kwargs)
        print_debug(f" ⬅️ Exiting {str(func.__name__)}")
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


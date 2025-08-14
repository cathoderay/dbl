import os

from datetime import datetime
import functools
import time


if os.getenv("DBL_TEST_ENV") == "1":
    import conf_test as conf
else:
    import conf
print(f"[{__name__}] conf file loaded: [{conf.__name__}]")


def print_debug(data):
    if not conf.DEBUG:
        return

    if isinstance(data, str):
        _print_debug(data)

    if isinstance(data, list):
        for datum in data:
            _print_debug(datum)


def print_profile(data):
    if not conf.PROFILE:
        return

    if isinstance(data, str):
        _print_profile(data)

    if isinstance(data, list):
        for datum in data:
            _print_profile(datum)


def _print_debug(line):
    print(f"\033[37m[DEBUG ({datetime.now()})]", line, "\033[0m")


def _print_profile(line):
    print(f"\033[37m[PROFILE ({datetime.now()})]", line, "\033[0m")


def encode(data):
    return data.encode(conf.ENCODING, errors="ignore")


def decode(data):
    return data.decode(conf.ENCODING, errors="ignore")


def dbl_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print_debug(f" ▶️ Entering {str(func.__name__)} {args} {kwargs}")
        result = func(*args, **kwargs)
        print_debug(f" ⬅️ Exiting {str(func.__name__)}")
        return result
    return wrapper


def dbl_profile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print_profile(f"Spent {end - start} in {str(func.__name__)}")
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


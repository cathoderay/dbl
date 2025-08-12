from conf import ENCODING, DEBUG


def print_debug(*args):
    if DEBUG: print("DEBUG: ", *args)


def encode(data):
    return data.encode(ENCODING, errors="ignore")


def decode(data):
    return data.decode(ENCODING, errors="ignore")


def dbl_log(func):
    def wrapper(*args, **kwargs):
        if DEBUG: print("DEBUG: ", "Inside", str(func.__name__), *args[1:], f"{kwargs}")
        result = func(*args, **kwargs)
        if DEBUG: print("DEBUG: ", "Exiting", str(func.__name__))
        return result
    return wrapper



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


def print_operations():
    operations = "help,set,get,compact,compact_and_replace,replace_from_compact,build_index,toggle_debug,check_debug,clean_database,clean_compact,clean_index,clean_all,bytes_indexed"
    print("Operations available:")
    print("\n".join(map(lambda item: " * " + item, operations.split(","))))

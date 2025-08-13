dbl
===
Naive implementation of a key-value log structured database inspired by the book "Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann.

Features
--------

- Written in pure Python
- No third-party dependency
- Suited for key-value data
- 2 main operations:
  - set(key, value)
  - get(key)
- Keys and values are utf-8 strings
- Designed for high write throughput
  - It simply appends to a log file
  - Compaction of old and duplicate entries is available to shrink file size in disk
- Search is done with an in memory hashmap
- REPL (Read Eval Print Loop) available
  - See usage example below
- You can try it out via Python source code
  - See usage example below
- It's open source
- It's a work in progress
- It's not suited for production environment yet

How to run
----------

You can run it like:
```
    $ python3 dbl.py
```
or alternatively you can add an alias to your .zshrc or .bashrc to the dbl.py, like 
```
export PATH=$HOME/code/dbl:$PATH
alias dbl="dbl.py"
```
and then run it like:
```
  $ dbl
```

Usage example (REPL)
--------------------

```
➜  dbl git:(main) dbl

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

Type help to list available commands.

=> help
✅ Operations available:
 * help
 * set
 * get
 * compact
 * compact_and_replace
 * replace_from_compact
 * build_index
 * toggle_debug_flag
 * check_debug_flag
 * clean_database
 * clean_compact
 * clean_index
 * clean_all
 * index_metadata

=> set
DBL.set() missing 2 required positional arguments: 'key' and 'value'

=> set food broccoli
✅ food => broccoli

=> get
DBL.get() missing 1 required positional argument: 'key'

=> get food
✅ broccoli

=> index_metadata
✅ --------------------------------------------------
Number of keys: 1
Bytes indexed: 14
Size of index object in bytes: 184
--------------------------------------------------

=> get drink
Key not found

=> set drink water
✅ drink => water

=> index_metadata
✅ --------------------------------------------------
Number of keys: 2
Bytes indexed: 26
Size of index object in bytes: 184
--------------------------------------------------

=> get drink
✅ water

=> ^C
Thanks for using dbl!
Don't forget to eat your veggies! 🥦
```

Usage example (REPL in debug mode)
----------------------------------

Start your REPL with --debug flag
```
➜  dbl git:(main) dbl --debug
[DEBUG [2025-08-12 16:44:33.043721  ▶️ Entering __init__ (<__main__.REPL object at 0x106bdfb60>,) {}
[DEBUG [2025-08-12 16:44:33.043783  ▶️ Entering __init__ (<__main__.DBL object at 0x106bdfcb0>,) {}
[DEBUG [2025-08-12 16:44:33.043797  ⬅️ Exiting __init__
[DEBUG [2025-08-12 16:44:33.043810  ⬅️ Exiting __init__
[DEBUG [2025-08-12 16:44:33.043823  ▶️ Entering start (<__main__.REPL object at 0x106bdfb60>,) {}

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

Type help to list available commands.
[DEBUG [2025-08-12 16:44:33.043955  ▶️ Entering loop (<__main__.REPL object at 0x106bdfb60>,) {}
[DEBUG [2025-08-12 16:44:33.043973  ▶️ Entering _loop (<__main__.REPL object at 0x106bdfb60>,) {}

=> get food
[DEBUG [2025-08-12 16:44:37.028291  ▶️ Entering run (<__main__.REPL object at 0x106bdfb60>, 'get', ['food']) {}
[DEBUG [2025-08-12 16:44:37.028334  ▶️ Entering get (<__main__.DBL object at 0x106bdfcb0>, 'food') {}
[DEBUG [2025-08-12 16:44:37.028378  ▶️ Entering _build_index (<__main__.DBL object at 0x106bdfcb0>,) {}
[DEBUG [2025-08-12 16:44:37.028532  ▶️ Entering update_index (<__main__.DBL object at 0x106bdfcb0>, 'food', IndexValue(start=5, size=8)) {}
[DEBUG [2025-08-12 16:44:37.028554  ⬅️ Exiting update_index
[DEBUG [2025-08-12 16:44:37.028583  ▶️ Entering update_index (<__main__.DBL object at 0x106bdfcb0>, 'drink', IndexValue(start=20, size=5)) {}
[DEBUG [2025-08-12 16:44:37.028594  ⬅️ Exiting update_index
[DEBUG [2025-08-12 16:44:37.028621  ⬅️ Exiting _build_index
[DEBUG [2025-08-12 16:44:37.028680  ⬅️ Exiting get
✅ broccoli
[DEBUG [2025-08-12 16:44:37.028700  ⬅️ Exiting run
```

Usage example (Python)
----------------------

```
    >>> from dbl import DBL
    >>> dbl = DBL()
    >>> dbl.set("food", "broccoli")
    'food => broccoli'
    >>> dbl.get("food")
    'broccoli'
    >>> dbl.set("happy-emoji", "😊")
    'happy-emoji => 😊'
```

Where is the data stored?
-------------------------

The data is stored and retrieved from the path described in `DATABASE_PATH` located at `conf.py`.


Running tests
-------------

```
➜  dbl git:(main) python3 test.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.003s

OK
```

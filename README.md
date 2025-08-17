dbl
===
```
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
```
This is a naive implementation of a key-value database (log structured).

This is inspired by the book "Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann.

Features
--------

- Written in pure Python (and a bit of C++)
- No third-party dependency
- Suited for key-value data
- 2 main operations:
  - set(key, value)
  - get(key)
- Keys and values are utf-8 strings
- Designed for high write throughput
  - It simply appends to a log file
  - Compaction of entries (old and duplicates) is available to shrink file size in disk
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

1. You can run it like:
  ```
      $ python3 dbl.py
  ```
2. or alternatively you can add an alias to your .zshrc or .bashrc to the dbl.py, like
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
[__main__] conf file loaded: [conf]
[helper] conf file loaded: [conf]
Using /tmp/dbl.data

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

Type 'help' to list available operations.

=> help
✅ Operations available:
 * help
 * set
 * get
 * build_index
 * toggle_debug
 * check_debug_flag
 * clean_database
 * clean_index
 * clean_all
 * index
 * find_tail
 * exit

=> set food broccoli
✅ food => broccoli

=> get food
✅ broccoli

=> index
✅ Index metadata: ------------------------------
- Number of keys: 1
- Bytes indexed: 14
--------------------------------------------------

=> get drink
☑️ None

=> set drink water
✅ drink => water

=> index
✅ Index metadata: ------------------------------
- Number of keys: 2
- Bytes indexed: 26
--------------------------------------------------

=> get drink
✅ water

=> exit

Thanks for using dbl!
Don't forget to eat your veggies! 🥦
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


Usage example (REPL in debug mode)
----------------------------------

Start your REPL with --debug flag
```
➜  dbl git:(main) dbl --debug
[__main__] conf file loaded: [conf]
[helper] conf file loaded: [conf]
[DEBUG (2025-08-14 09:34:48.283236)]  ▶️ Entering __init__ (<__main__.REPL object at 0x1035a7cb0>,) {}
[DEBUG (2025-08-14 09:34:48.283483)]  ▶️ Entering __init__ (<__main__.DBL object at 0x1035a7e00>,) {}
[DEBUG (2025-08-14 09:34:48.283497)] Using /tmp/dbl.data
[DEBUG (2025-08-14 09:34:48.283506)]  ⬅️ Exiting __init__
[DEBUG (2025-08-14 09:34:48.283521)]  ⬅️ Exiting __init__
[DEBUG (2025-08-14 09:34:48.283533)]  ▶️ Entering start (<__main__.REPL object at 0x1035a7cb0>,) {}

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

Type help to list available operations.
[DEBUG (2025-08-14 09:34:48.283648)]  ▶️ Entering loop (<__main__.REPL object at 0x1035a7cb0>,) {}
[DEBUG (2025-08-14 09:34:48.283665)]  ▶️ Entering _loop (<__main__.REPL object at 0x1035a7cb0>,) {}

=> get food
[DEBUG (2025-08-14 09:34:55.819046)]  ▶️ Entering run (<__main__.REPL object at 0x1035a7cb0>, 'get', ['food']) {}
[DEBUG (2025-08-14 09:34:55.819118)]  ▶️ Entering get (<__main__.DBL object at 0x1035a7e00>, 'food') {}
[DEBUG (2025-08-14 09:34:55.820164)]  ▶️ Entering _update_index (<__main__.DBL object at 0x1035a7e00>, 'food', IndexValue(start=5, size=8)) {}
[DEBUG (2025-08-14 09:34:55.820196)]  ⬅️ Exiting _update_index
[DEBUG (2025-08-14 09:34:55.820234)]  ▶️ Entering _update_index (<__main__.DBL object at 0x1035a7e00>, 'drink', IndexValue(start=20, size=5)) {}
[DEBUG (2025-08-14 09:34:55.820248)]  ⬅️ Exiting _update_index
[DEBUG (2025-08-14 09:34:55.820267)] Found 2 new entries.
[DEBUG (2025-08-14 09:34:55.820405)]  ⬅️ Exiting get
✅ broccoli
[DEBUG (2025-08-14 09:34:55.820431)]  ⬅️ Exiting run
```

REPL in test environment
------------------------

You can also use the REPL in test environment, so it will point to a new db defined in `conf_test.py`.
To start it, you just need to prepend `dbl` command with the env variable `DBL_TEST_ENV` as below:
```
   ➜  dbl git:(main) DBL_TEST_ENV=1 dbl
```

Where is the data stored?
-------------------------

The data is stored and retrieved from the path described in `DATABASE_PATH` located at `conf.py`.

Configuration files
-------------------

There are two main configuration files available. One for real usage (`conf.py`) and another one for tests (`conf_test.py`).

Running unit tests
------------------

```
➜  dbl git:(main) ./run_tests.sh
[dbl] conf file loaded: [conf_test]
[helper] conf file loaded: [conf_test]
........
----------------------------------------------------------------------
Ran 8 tests in 0.003s

OK
```

Running load tests
------------------
```
➜  dbl git:(main) ./run_load_test.sh 100000
--------------------------------------------------
Starting clean.
Index: --------------------------------------------------
  Number of keys: 0
  Bytes indexed: 0
--------------------------------------------------
🏃‍➡️ Setting 100000 distinct keys in bulk...
[PROFILE (2025-08-16 17:16:22.764527)] Spent 0.1226658821105957 in validate_bulk
[PROFILE (2025-08-16 17:16:23.175269)] Spent 0.5881552696228027 in set_bulk
✅ Done.
Index: --------------------------------------------------
  Number of keys: 100000
  Bytes indexed: 2177790
--------------------------------------------------
Getting one inexistent key...
[PROFILE (2025-08-16 17:16:23.180219)] Spent 8.702278137207031e-05 in get
None
Getting one existent key...
[PROFILE (2025-08-16 17:16:23.180323)] Spent 7.390975952148438e-05 in get
value-1
Index: --------------------------------------------------
  Number of keys: 100000
  Bytes indexed: 2177790
--------------------------------------------------
Cleaning again...
Index: --------------------------------------------------
  Number of keys: 0
  Bytes indexed: 0
--------------------------------------------------
🏃‍➡️ Setting 100000 new entries with the same key=key-22979 in bulk...
[PROFILE (2025-08-16 17:16:23.425952)] Spent 0.12819409370422363 in validate_bulk
[PROFILE (2025-08-16 17:16:23.778431)] Spent 0.5332779884338379 in set_bulk
✅ Done.
Index: --------------------------------------------------
  Number of keys: 1
  Bytes indexed: 2188895
--------------------------------------------------
Cleaned database.
✅ Done.
Index: --------------------------------------------------
  Number of keys: 0
  Bytes indexed: 0
--------------------------------------------------
✅ Done.
```

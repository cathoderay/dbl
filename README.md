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

- Written in pure Python
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
[dbl] conf file loaded: [conf_test]
[helper] conf file loaded: [conf_test]

 🏁 LOAD TEST REPORT 🏁 --------------------------------------------------

Using /tmp/dbl.data-test-session-1755195104.2882009
--------------------------------------------------
Starting clean.
--------------------------------------------------
Number of keys: 0
Bytes indexed: 0
Size of index object in bytes: 64
--------------------------------------------------
🏃‍➡️ Setting 100000 distinct keys in bulk without updating the index...
[PROFILE (2025-08-14 15:11:44.844838)] Spent 0.4193539619445801 in _set_bulk
✅ Done.
--------------------------------------------------
Number of keys: 0
Bytes indexed: 0
Size of index object in bytes: 64
--------------------------------------------------
🏃‍➡️ Setting 100000 new entries with the same key=key-45932 in bulk without updating the index...
[PROFILE (2025-08-14 15:11:45.354383)] Spent 0.40894007682800293 in _set_bulk
✅ Done.
--------------------------------------------------
Number of keys: 0
Bytes indexed: 0
Size of index object in bytes: 64
--------------------------------------------------
Cleaned database.
✅ Done.
--------------------------------------------------
Number of keys: 0
Bytes indexed: 0
Size of index object in bytes: 64
--------------------------------------------------
🏃‍➡️ Setting 100000 distinct keys in bulk updating the index...
[PROFILE (2025-08-14 15:11:45.904282)] Spent 0.42287683486938477 in _set_bulk
[PROFILE (2025-08-14 15:11:45.905312)] Spent 0.0009801387786865234 in _read_file
[PROFILE (2025-08-14 15:11:46.420145)] Spent 0.5148029327392578 in _update_index_bulk
[PROFILE (2025-08-14 15:11:46.420177)] Spent 0.515861988067627 in _build_index
✅ Done.
--------------------------------------------------
Number of keys: 100000
Bytes indexed: 2177790
Size of index object in bytes: 3844864
--------------------------------------------------
Cleaned database.
✅ Done.
--------------------------------------------------
Number of keys: 0
Bytes indexed: 0
Size of index object in bytes: 64
--------------------------------------------------
🏃‍➡️ Setting 100000 new entries for key=key-38917 in bulk updating the index...
[PROFILE (2025-08-14 15:11:46.936656)] Spent 0.4108619689941406 in _set_bulk
[PROFILE (2025-08-14 15:11:46.937648)] Spent 0.0009479522705078125 in _read_file
[PROFILE (2025-08-14 15:11:47.395052)] Spent 0.45737695693969727 in _update_index_bulk
[PROFILE (2025-08-14 15:11:47.395290)] Spent 0.4586029052734375 in _build_index
✅ Done.
--------------------------------------------------
Number of keys: 1
Bytes indexed: 2188895
Size of index object in bytes: 184
--------------------------------------------------
```
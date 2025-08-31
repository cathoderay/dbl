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
  - and currently experimenting with a bit of C++ and Rust for the most performance-critical internals
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
Note: This instructions will be easier to follow once I decide which language I'm going to use for the internals.

0. First, you need to build internal modules, like:
  ```
      $ ./build_internals.sh
  ```
  This step will generate a `cpp_internal.so` as well as `rust_internal.so` file that will be used from the Python source code.
  
1. Then, you can run it like:
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

help
✅ Operations available:
 * help
 * set
 * get
 * del
 * build_index
 * toggle_debug
 * check_debug_flag
 * clean_database
 * clean_index
 * clean_all
 * index
 * find_tail
 * exit

set food broccoli
✅ food => broccoli

get food
✅ broccoli

index
✅ Index metadata: ------------------------------
- Number of keys: 1
- Bytes indexed: 14
--------------------------------------------------

get drink
☑️ None

set drink water
✅ drink => water

index
✅ Index metadata: ------------------------------
- Number of keys: 2
- Bytes indexed: 26
--------------------------------------------------

get drink
✅ water

exit

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
[DEBUG (2025-08-19 07:43:24.124656)]  ▶️ Entering __init__ (<__main__.REPL object at 0x101939fd0>,) {}
[DEBUG (2025-08-19 07:43:24.124697)]  ▶️ Entering __init__ (<__main__.DBL object at 0x10193a3c0>,) {}
Using /tmp/dbl.data
[DEBUG (2025-08-19 07:43:24.124714)]  ⬅️ Exiting __init__
[DEBUG (2025-08-19 07:43:24.124728)]  ⬅️ Exiting __init__
[DEBUG (2025-08-19 07:43:24.124739)]  ▶️ Entering start (<__main__.REPL object at 0x101939fd0>,) {}

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
[DEBUG (2025-08-19 07:43:24.124851)]  ▶️ Entering loop (<__main__.REPL object at 0x101939fd0>,) {}
[DEBUG (2025-08-19 07:43:24.124870)]  ▶️ Entering _loop (<__main__.REPL object at 0x101939fd0>,) {}

get food
[DEBUG (2025-08-19 07:43:32.499620)]  ▶️ Entering run (<__main__.REPL object at 0x101939fd0>, 'get', ['food']) {}
[DEBUG (2025-08-19 07:43:32.499669)]  ▶️ Entering get (<__main__.DBL object at 0x10193a3c0>, 'food') {}
[DEBUG (2025-08-19 07:43:32.499896)]  ⬅️ Exiting get
[DEBUG (2025-08-19 07:43:32.499918)]  ⬅️ Exiting run
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
....
...........
----------------------------------------------------------------------
Ran 15 tests in 0.189s

OK
```

Running load tests
------------------
```
➜  dbl git:(main) ./run_load_test.sh
[dbl] conf file loaded: [conf_test]
[helper] conf file loaded: [conf_test]

 🏁 LOAD TEST REPORT 🏁 --------------------------------------------------


⏩ LoadTestName: distinct-keys
Using /tmp/dbl.data-test-session-1755623055.884661
DB clean.
🏃‍➡️ Setting 100000 distinct keys with values of the same length in bulk...
[PROFILE (2025-08-19 14:04:16.155197)] Spent 0.1405041217803955 in validate_bulk
[PROFILE (2025-08-19 14:04:16.548607)] Spent 0.5851309299468994 in set_bulk
Getting one inexistent key...
[PROFILE (2025-08-19 14:04:16.553362)] Spent 7.700920104980469e-05 in get
None
Getting one existent key...
[PROFILE (2025-08-19 14:04:16.553567)] Spent 0.00015878677368164062 in get
value-1
Index metadata: ------------------------------
- Number of keys: 100000
- Bytes indexed: 2177790
--------------------------------------------------
✅ Done.


⏩ LoadTestName: same-key
Using /tmp/dbl.data-test-session-1755623055.884661
DB clean.
🏃‍➡️ Setting 100000 new entries with the same key=key-69021 in bulk...
[PROFILE (2025-08-19 14:04:16.794832)] Spent 0.12517714500427246 in validate_bulk
[PROFILE (2025-08-19 14:04:17.132563)] Spent 0.5110280513763428 in set_bulk
Getting one existent key...
[PROFILE (2025-08-19 14:04:17.136216)] Spent 0.00012683868408203125 in get
value-100000
Index metadata: ------------------------------
- Number of keys: 1
- Bytes indexed: 2188895
--------------------------------------------------
✅ Done.


⏩ LoadTestName: larger-values
Using /tmp/dbl.data-test-session-1755623055.884661
DB clean.
🏃‍➡️ Setting 100000 distinct keys with values of length=500 in bulk...
[PROFILE (2025-08-19 14:04:17.879013)] Spent 0.2985498905181885 in validate_bulk
[PROFILE (2025-08-19 14:04:20.493158)] Spent 3.2417349815368652 in set_bulk
Getting one existent key (key-3860)...
[PROFILE (2025-08-19 14:04:20.513601)] Spent 0.00014519691467285156 in get
3860-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
Index metadata: ------------------------------
- Number of keys: 100000
- Bytes indexed: 51677790
--------------------------------------------------
✅ Done.

```

Running benchmark tests
------------------
```
➜  dbl git:(main) ✗ ./run_benchmark.sh
[dbl] conf file loaded: [conf_test]
[helper] conf file loaded: [conf_test]

 🏁 BENCHMARK TEST REPORT 🏁 --------------------------------------------------


⏩ Benchmark: cpp
Internal: cpp
Using /tmp/dbl.data-test-session-1756659949.724519
DB clean.
{'number of keys': 10000, 'bytes indexed': 197788}
✅ Done.


⏩ Benchmark: rust
Internal: rust
Using /tmp/dbl.data-test-session-1756659949.724519
DB clean.
{'number of keys': 10000, 'bytes indexed': 197788}
✅ Done.

------------------------------------------------------------------
type (n = 10000)     | write (in seconds)   | read (in seconds)
------------------------------------------------------------------
cpp                  | 0.6830160617828369   | 0.5692169666290283
rust                 | 0.4856441020965576   | 0.3923947811126709
------------------------------------------------------------------
```

Contributions
-------------
Collaborations are welcome!
Feel free to send me a message, so we can chat!

```
       ▐▌▗▖   █
       ▐▌▐▌   █
    ▗▞▀▜▌▐▛▀▚▖█
    ▝▚▄▟▌▐▙▄▞▘█
```
This is a naive implementation of a key-value database (log structured).

This is inspired by the book "Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann.

Features
--------

- Written in pure Python + Rust
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

0. Just run: 
  ```
      $ ./scripts/install.sh
  ```
  This step will compile and move necessary files to your `$HOME/.dbl` folder.
  Also, a new alias is added to your `.bashrc` and `.zshrc`.
  
1. Restart your terminal, so the new alias take effect. Then you can run:
  ```
    $ dbl
  ```

Usage example (REPL)
--------------------

```
➜  dbl git:(main) ✗ dbl
[__main__] conf file loaded: [conf]
DBL initialized. Database opened at /tmp/dbl.data.

    Welcome to:

       ▐▌▗▖   █
       ▐▌▐▌   █
    ▗▞▀▜▌▐▛▀▚▖█
    ▝▚▄▟▌▐▙▄▞▘█

    version 0.1
    by Ronald Kaiser

Type 'help' to list available operations.

help
✅ Operations available:
 * build_index
 * check_debug_flag
 * clean_all
 * clean_compact
 * clean_database
 * clean_index
 * compact
 * compact_and_replace
 * del
 * exit
 * find_tail
 * get
 * help
 * index
 * replace_from_compact
 * set
 * toggle_debug

set food broccoli
✅ food => broccoli

get food
✅ broccoli

index
{'bytes indexed': 14, 'keys': ['food'], 'number of keys': 1}
✅ None

get drink
☑️ None

set drink water
✅ drink => water

index
{'bytes indexed': 26, 'keys': ['drink', 'food'], 'number of keys': 2}
✅ None

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
    [dbl] conf file loaded: [conf]
    >>> dbl = DBL()
    DBL initialized. Database opened at /tmp/dbl.data.
    >>> dbl.set("food", "broccoli")
    'food => broccoli'
    >>> dbl.get("food")
    'broccoli'
    >>> dbl.set("happy-emoji", "😊")
    'happy-emoji => 😊'
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
➜  dbl git:(main) ./scripts/run_tests.sh
[dbl] conf file loaded: [conf_test]
[helper] conf file loaded: [conf_test]
....
...........
----------------------------------------------------------------------
Ran 15 tests in 0.189s

OK
```

Contributions
-------------
Collaborations are welcome!
Feel free to send me a message, so we can chat!

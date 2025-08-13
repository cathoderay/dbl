# dbl

Naive implementation of a key-value log structured database inspired by the book "Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems" by Martin Kleppmann.

## Features
- Written in pure Python
- No third-party dependency
- Suited for key-value data
- 2 main operations:
  - set(key, value)
  - get(key)
- Keys and values are utf-8 strings
- Designed for high write throughput
  - It simply appends to a log file
  - Compaction is available to shrink file size in disk
- Search is done with an in memory hashmap
- REPL (Read Eval Print Loop) available
  - See usage example below
- You can try it out via Python source code
  - See usage example below
- It's open source
- It's a work in progress
- It's not suited for production environment yet

## How to run
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

## Usage example (REPL)

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

## Usage example (REPL in debug mode)
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

## Usage example (Python)
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

## Where is the data stored?
The data is stored and retrieved from `DATABASE_FILENAME` variable located at `conf.py`.


## Running tests
```
➜  dbl git:(main) python3 test.py
[DEBUG [2025-08-13 08:23:05.537701  ▶️ Entering __init__ (<dbl.DBL object at 0x10f3d7b60>,) {}
[DEBUG [2025-08-13 08:23:05.537760  ⬅️ Exiting __init__
[DEBUG [2025-08-13 08:23:05.537781  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f3d7b60>, 'key', 'value✅') {}
[DEBUG [2025-08-13 08:23:05.537797  ⬅️ Exiting get_encoded_data
.[DEBUG [2025-08-13 08:23:05.537874  ▶️ Entering __init__ (<dbl.DBL object at 0x10f459bd0>,) {}
[DEBUG [2025-08-13 08:23:05.537888  ⬅️ Exiting __init__
[DEBUG [2025-08-13 08:23:05.537900  ▶️ Entering set (<dbl.DBL object at 0x10f459bd0>, '42', 'Douglas Adams') {}
[DEBUG [2025-08-13 08:23:05.537912  ▶️ Entering _set (<dbl.DBL object at 0x10f459bd0>, '42', 'Douglas Adams', False) {}
[DEBUG [2025-08-13 08:23:05.537925  ▶️ Entering validate ('42', 'Douglas Adams') {}
[DEBUG [2025-08-13 08:23:05.537934  ⬅️ Exiting validate
[DEBUG [2025-08-13 08:23:05.537944  ▶️ Entering get_filename (<dbl.DBL object at 0x10f459bd0>, False) {}
[DEBUG [2025-08-13 08:23:05.537954  ⬅️ Exiting get_filename
[DEBUG [2025-08-13 08:23:05.537964  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f459bd0>, '42', 'Douglas Adams') {}
[DEBUG [2025-08-13 08:23:05.537975  ⬅️ Exiting get_encoded_data
[DEBUG [2025-08-13 08:23:05.538083  ▶️ Entering _update_index (<dbl.DBL object at 0x10f459bd0>, '42', IndexValue(start=96, size=13)) {}
[DEBUG [2025-08-13 08:23:05.538100  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.538471  ⬅️ Exiting _set
[DEBUG [2025-08-13 08:23:05.538496  ⬅️ Exiting set
[DEBUG [2025-08-13 08:23:05.538513  ▶️ Entering get (<dbl.DBL object at 0x10f459bd0>, '42') {}
[DEBUG [2025-08-13 08:23:05.538551  ▶️ Entering _build_index (<dbl.DBL object at 0x10f459bd0>,) {}
[DEBUG [2025-08-13 08:23:05.538615 Index already built. Skipping.
[DEBUG [2025-08-13 08:23:05.538636  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.538696  ⬅️ Exiting get
.[DEBUG [2025-08-13 08:23:05.538769  ▶️ Entering __init__ (<dbl.DBL object at 0x10f459a90>,) {}
[DEBUG [2025-08-13 08:23:05.538783  ⬅️ Exiting __init__
[DEBUG [2025-08-13 08:23:05.538800  ▶️ Entering set (<dbl.DBL object at 0x10f459a90>, 'emoji', '😀') {}
[DEBUG [2025-08-13 08:23:05.538815  ▶️ Entering _set (<dbl.DBL object at 0x10f459a90>, 'emoji', '😀', False) {}
[DEBUG [2025-08-13 08:23:05.538826  ▶️ Entering validate ('emoji', '😀') {}
[DEBUG [2025-08-13 08:23:05.538835  ⬅️ Exiting validate
[DEBUG [2025-08-13 08:23:05.538845  ▶️ Entering get_filename (<dbl.DBL object at 0x10f459a90>, False) {}
[DEBUG [2025-08-13 08:23:05.538854  ⬅️ Exiting get_filename
[DEBUG [2025-08-13 08:23:05.538864  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f459a90>, 'emoji', '😀') {}
[DEBUG [2025-08-13 08:23:05.538875  ⬅️ Exiting get_encoded_data
[DEBUG [2025-08-13 08:23:05.538948  ▶️ Entering _update_index (<dbl.DBL object at 0x10f459a90>, 'emoji', IndexValue(start=116, size=4)) {}
[DEBUG [2025-08-13 08:23:05.538962  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.539016  ⬅️ Exiting _set
[DEBUG [2025-08-13 08:23:05.539031  ⬅️ Exiting set
[DEBUG [2025-08-13 08:23:05.539043  ▶️ Entering get (<dbl.DBL object at 0x10f459a90>, 'emoji') {}
[DEBUG [2025-08-13 08:23:05.539068  ▶️ Entering _build_index (<dbl.DBL object at 0x10f459a90>,) {}
[DEBUG [2025-08-13 08:23:05.539127 Index already built. Skipping.
[DEBUG [2025-08-13 08:23:05.539147  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.539203  ⬅️ Exiting get
.[DEBUG [2025-08-13 08:23:05.539265  ▶️ Entering __init__ (<dbl.DBL object at 0x10f4ac2b0>,) {}
[DEBUG [2025-08-13 08:23:05.539277  ⬅️ Exiting __init__
[DEBUG [2025-08-13 08:23:05.539292  ▶️ Entering set_bulk (<dbl.DBL object at 0x10f4ac2b0>, [('name1', 'Paul'), ('name2', 'John'), ('name3', 'Ringo'), ('name4', 'George')]) {}
[DEBUG [2025-08-13 08:23:05.539306  ▶️ Entering _set_bulk (<dbl.DBL object at 0x10f4ac2b0>, [('name1', 'Paul'), ('name2', 'John'), ('name3', 'Ringo'), ('name4', 'George')]) {}
[DEBUG [2025-08-13 08:23:05.539318  ▶️ Entering validate ('name1', 'Paul') {}
[DEBUG [2025-08-13 08:23:05.539326  ⬅️ Exiting validate
[DEBUG [2025-08-13 08:23:05.539336  ▶️ Entering validate ('name2', 'John') {}
[DEBUG [2025-08-13 08:23:05.539343  ⬅️ Exiting validate
[DEBUG [2025-08-13 08:23:05.539476  ▶️ Entering validate ('name3', 'Ringo') {}
[DEBUG [2025-08-13 08:23:05.539498  ⬅️ Exiting validate
[DEBUG [2025-08-13 08:23:05.539512  ▶️ Entering validate ('name4', 'George') {}
[DEBUG [2025-08-13 08:23:05.539522  ⬅️ Exiting validate
[DEBUG [2025-08-13 08:23:05.539533  ▶️ Entering get_filename (<dbl.DBL object at 0x10f4ac2b0>, False) {}
[DEBUG [2025-08-13 08:23:05.539542  ⬅️ Exiting get_filename
[DEBUG [2025-08-13 08:23:05.539554  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f4ac2b0>, 'name1', 'Paul') {}
[DEBUG [2025-08-13 08:23:05.539565  ⬅️ Exiting get_encoded_data
[DEBUG [2025-08-13 08:23:05.539577  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f4ac2b0>, 'name2', 'John') {}
[DEBUG [2025-08-13 08:23:05.539587  ⬅️ Exiting get_encoded_data
[DEBUG [2025-08-13 08:23:05.539598  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f4ac2b0>, 'name3', 'Ringo') {}
[DEBUG [2025-08-13 08:23:05.539608  ⬅️ Exiting get_encoded_data
[DEBUG [2025-08-13 08:23:05.539619  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f4ac2b0>, 'name4', 'George') {}
[DEBUG [2025-08-13 08:23:05.539628  ⬅️ Exiting get_encoded_data
[DEBUG [2025-08-13 08:23:05.539748  ▶️ Entering _build_index (<dbl.DBL object at 0x10f4ac2b0>,) {}
[DEBUG [2025-08-13 08:23:05.539883  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'asdf', IndexValue(start=5, size=4)) {}
[DEBUG [2025-08-13 08:23:05.539906  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.539939  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, '42', IndexValue(start=13, size=13)) {}
[DEBUG [2025-08-13 08:23:05.539950  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.539976  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'emoji', IndexValue(start=33, size=4)) {}
[DEBUG [2025-08-13 08:23:05.539985  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540006  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name1', IndexValue(start=44, size=4)) {}
[DEBUG [2025-08-13 08:23:05.540015  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540049  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name2', IndexValue(start=55, size=4)) {}
[DEBUG [2025-08-13 08:23:05.540058  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540078  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name3', IndexValue(start=66, size=5)) {}
[DEBUG [2025-08-13 08:23:05.540087  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540107  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name4', IndexValue(start=78, size=6)) {}
[DEBUG [2025-08-13 08:23:05.540299  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540321  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, '42', IndexValue(start=88, size=4)) {}
[DEBUG [2025-08-13 08:23:05.540331  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540353  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, '42', IndexValue(start=96, size=13)) {}
[DEBUG [2025-08-13 08:23:05.540363  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540383  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'emoji', IndexValue(start=116, size=4)) {}
[DEBUG [2025-08-13 08:23:05.540392  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540411  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name1', IndexValue(start=127, size=4)) {}
[DEBUG [2025-08-13 08:23:05.540420  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540439  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name2', IndexValue(start=138, size=4)) {}
[DEBUG [2025-08-13 08:23:05.540447  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540466  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name3', IndexValue(start=149, size=5)) {}
[DEBUG [2025-08-13 08:23:05.540476  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540495  ▶️ Entering _update_index (<dbl.DBL object at 0x10f4ac2b0>, 'name4', IndexValue(start=161, size=6)) {}
[DEBUG [2025-08-13 08:23:05.540504  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.540518 Found 14 new entries.
[DEBUG [2025-08-13 08:23:05.540537  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.540547  ⬅️ Exiting _set_bulk
[DEBUG [2025-08-13 08:23:05.540554  ⬅️ Exiting set_bulk
[DEBUG [2025-08-13 08:23:05.540564  ▶️ Entering get (<dbl.DBL object at 0x10f4ac2b0>, 'name1') {}
[DEBUG [2025-08-13 08:23:05.540593  ▶️ Entering _build_index (<dbl.DBL object at 0x10f4ac2b0>,) {}
[DEBUG [2025-08-13 08:23:05.540657 Index already built. Skipping.
[DEBUG [2025-08-13 08:23:05.540677  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.540732  ⬅️ Exiting get
[DEBUG [2025-08-13 08:23:05.540747  ▶️ Entering get (<dbl.DBL object at 0x10f4ac2b0>, 'name2') {}
[DEBUG [2025-08-13 08:23:05.540769  ▶️ Entering _build_index (<dbl.DBL object at 0x10f4ac2b0>,) {}
[DEBUG [2025-08-13 08:23:05.540814 Index already built. Skipping.
[DEBUG [2025-08-13 08:23:05.540831  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.540879  ⬅️ Exiting get
[DEBUG [2025-08-13 08:23:05.540893  ▶️ Entering get (<dbl.DBL object at 0x10f4ac2b0>, 'name3') {}
[DEBUG [2025-08-13 08:23:05.540914  ▶️ Entering _build_index (<dbl.DBL object at 0x10f4ac2b0>,) {}
[DEBUG [2025-08-13 08:23:05.540960 Index already built. Skipping.
[DEBUG [2025-08-13 08:23:05.540977  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.541025  ⬅️ Exiting get
[DEBUG [2025-08-13 08:23:05.541039  ▶️ Entering get (<dbl.DBL object at 0x10f4ac2b0>, 'name4') {}
[DEBUG [2025-08-13 08:23:05.541058  ▶️ Entering _build_index (<dbl.DBL object at 0x10f4ac2b0>,) {}
[DEBUG [2025-08-13 08:23:05.541101 Index already built. Skipping.
[DEBUG [2025-08-13 08:23:05.541117  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.541165  ⬅️ Exiting get
.[DEBUG [2025-08-13 08:23:05.541232  ▶️ Entering __init__ (<dbl.DBL object at 0x10f4ac180>,) {}
[DEBUG [2025-08-13 08:23:05.541244  ⬅️ Exiting __init__
[DEBUG [2025-08-13 08:23:05.541267  ▶️ Entering set (<dbl.DBL object at 0x10f4ac180>, 'key,key', 'value') {}
[DEBUG [2025-08-13 08:23:05.541279  ▶️ Entering _set (<dbl.DBL object at 0x10f4ac180>, 'key,key', 'value', False) {}
[DEBUG [2025-08-13 08:23:05.541289  ▶️ Entering validate ('key,key', 'value') {}
.[DEBUG [2025-08-13 08:23:05.541359  ▶️ Entering __init__ (<dbl.DBL object at 0x10f45d7f0>,) {}
[DEBUG [2025-08-13 08:23:05.541371  ⬅️ Exiting __init__
[DEBUG [2025-08-13 08:23:05.541383  ▶️ Entering get (<dbl.DBL object at 0x10f45d7f0>, '42') {}
[DEBUG [2025-08-13 08:23:05.541406  ▶️ Entering _build_index (<dbl.DBL object at 0x10f45d7f0>,) {}
[DEBUG [2025-08-13 08:23:05.541478  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'asdf', IndexValue(start=5, size=4)) {}
[DEBUG [2025-08-13 08:23:05.541491  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.541516  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, '42', IndexValue(start=13, size=13)) {}
[DEBUG [2025-08-13 08:23:05.541525  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.541548  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'emoji', IndexValue(start=33, size=4)) {}
[DEBUG [2025-08-13 08:23:05.541557  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.541578  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name1', IndexValue(start=44, size=4)) {}
[DEBUG [2025-08-13 08:23:05.541587  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.541606  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name2', IndexValue(start=55, size=4)) {}
[DEBUG [2025-08-13 08:23:05.541614  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.541634  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name3', IndexValue(start=66, size=5)) {}
[DEBUG [2025-08-13 08:23:05.541642  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.541662  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name4', IndexValue(start=78, size=6)) {}
[DEBUG [2025-08-13 08:23:05.542303  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542345  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, '42', IndexValue(start=88, size=4)) {}
[DEBUG [2025-08-13 08:23:05.542359  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542384  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, '42', IndexValue(start=96, size=13)) {}
[DEBUG [2025-08-13 08:23:05.542394  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542417  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'emoji', IndexValue(start=116, size=4)) {}
[DEBUG [2025-08-13 08:23:05.542427  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542447  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name1', IndexValue(start=127, size=4)) {}
[DEBUG [2025-08-13 08:23:05.542456  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542475  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name2', IndexValue(start=138, size=4)) {}
[DEBUG [2025-08-13 08:23:05.542494  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542515  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name3', IndexValue(start=149, size=5)) {}
[DEBUG [2025-08-13 08:23:05.542525  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542545  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, 'name4', IndexValue(start=161, size=6)) {}
[DEBUG [2025-08-13 08:23:05.542553  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.542569 Found 14 new entries.
[DEBUG [2025-08-13 08:23:05.542587  ⬅️ Exiting _build_index
[DEBUG [2025-08-13 08:23:05.542653  ⬅️ Exiting get
[DEBUG [2025-08-13 08:23:05.542671  ▶️ Entering set (<dbl.DBL object at 0x10f45d7f0>, '42', 'Test') {}
[DEBUG [2025-08-13 08:23:05.542682  ▶️ Entering _set (<dbl.DBL object at 0x10f45d7f0>, '42', 'Test', False) {}
[DEBUG [2025-08-13 08:23:05.542753  ▶️ Entering validate ('42', 'Test') {}
[DEBUG [2025-08-13 08:23:05.542776  ⬅️ Exiting validate
[DEBUG [2025-08-13 08:23:05.542790  ▶️ Entering get_filename (<dbl.DBL object at 0x10f45d7f0>, False) {}
[DEBUG [2025-08-13 08:23:05.542799  ⬅️ Exiting get_filename
[DEBUG [2025-08-13 08:23:05.542810  ▶️ Entering get_encoded_data (<dbl.DBL object at 0x10f45d7f0>, '42', 'Test') {}
[DEBUG [2025-08-13 08:23:05.542822  ⬅️ Exiting get_encoded_data
[DEBUG [2025-08-13 08:23:05.542902  ▶️ Entering _update_index (<dbl.DBL object at 0x10f45d7f0>, '42', IndexValue(start=171, size=4)) {}
[DEBUG [2025-08-13 08:23:05.542916  ⬅️ Exiting _update_index
[DEBUG [2025-08-13 08:23:05.543017  ⬅️ Exiting _set
[DEBUG [2025-08-13 08:23:05.543039  ⬅️ Exiting set
.[DEBUG [2025-08-13 08:23:05.543105  ▶️ Entering __init__ (<dbl.DBL object at 0x10f3cf8a0>,) {}
[DEBUG [2025-08-13 08:23:05.543118  ⬅️ Exiting __init__
[DEBUG [2025-08-13 08:23:05.543140  ▶️ Entering set (<dbl.DBL object at 0x10f3cf8a0>, 'key', 'value\n') {}
[DEBUG [2025-08-13 08:23:05.543152  ▶️ Entering _set (<dbl.DBL object at 0x10f3cf8a0>, 'key', 'value\n', False) {}
[DEBUG [2025-08-13 08:23:05.543163  ▶️ Entering validate ('key', 'value\n') {}
.
----------------------------------------------------------------------
Ran 7 tests in 0.006s

OK
```

import os
import threading
import unittest


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL, dbl_internal


class DBLTest(unittest.TestCase):
    def setUp(self):
        dbl_internal.clean_index()
        DBL().clean_all()

    def tearDown(self):
        dbl_internal.clean_index()
        DBL().clean_all()

    def test_set_value_cannot_contain_end_record_character(self):
        dbl = DBL()
        assert dbl_internal.get_bytes_read() == 0
        with self.assertRaises(AssertionError):
            dbl.set("key", "value\n")

    def test_set_key_cannot_contain_key_value_separator(self):
        dbl = DBL()
        assert dbl_internal.get_bytes_read() == 0
        with self.assertRaises(AssertionError):
            dbl.set("key,key", "value")

    def test_set_and_get(self):
        dbl = DBL()
        assert dbl_internal.get_bytes_read() == 0
        dbl.set("42", "Douglas Adams")
        assert(dbl.get("42") == "Douglas Adams")

    def test_set_updates_local_index(self):
        dbl = DBL()
        assert dbl_internal.get_bytes_read() == 0
        bytes_indexed_before = dbl_internal.get_bytes_read()
        dbl.set("42", "Test")
        dbl.get("42")
        bytes_indexed_after = dbl_internal.get_bytes_read()
        assert(bytes_indexed_before < bytes_indexed_after)

    def test_set_emoji(self):
        dbl = DBL()
        assert dbl_internal.get_bytes_read() == 0
        dbl.set("emoji", "😀")
        assert(dbl.get("emoji") == "😀")

    def test_set_bulk(self):
        dbl = DBL()
        assert dbl_internal.get_bytes_read() == 0
        bytes_indexed_before = dbl_internal.get_bytes_read()
        data = [
            ("name1", "Paul"),
            ("name2", "John"),
            ("name3", "Ringo"),
            ("name4", "George")
        ]
        dbl.set_bulk(data)
        bytes_indexed_after = dbl_internal.get_bytes_read()
        assert(bytes_indexed_before < bytes_indexed_after)
        assert(dbl.get("name1") == "Paul")
        assert(dbl.get("name2") == "John")
        assert(dbl.get("name3") == "Ringo")
        assert(dbl.get("name4") == "George")

    def test_get_non_existent_key(self):
        dbl = DBL()
        assert dbl_internal.get_bytes_read() == 0
        assert dbl.get("ooops") == None

    def test_concurrency(self):
        def thread_one():
            dbl = DBL()
            for _ in range(1000):
                dbl.set("food", "lettuce")

        def thread_two():
            dbl = DBL()
            for _ in range(1000):
                dbl.set("food", "broccoli")

        thread1 = threading.Thread(target=thread_one)
        thread2 = threading.Thread(target=thread_two)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        dbl = DBL()
        assert dbl.get("food") in ["lettuce", "broccoli"]
        dbl.set("food", "tomato")
        assert dbl.get("food") == "tomato"

    def test_bytes_read(self):
        dbl = DBL()
        dbl.set("food", "broccoli")
        dbl.set("drink", "water")
        assert dbl_internal.get_bytes_read() == 26

    def test_find_tail(self):
        dbl = DBL()
        dbl.set("a", "b")
        dbl.set("b", "c")
        dbl.set("c", "d")
        assert dbl.find_tail("a") == "d"

    def test_find_tail_with_cycle(self):
        dbl = DBL()
        dbl.set("a", "b")
        dbl.set("b", "c")
        dbl.set("c", "a")
        with self.assertRaises(Exception):
            dbl.find_tail("a")

    def test_set_and_get_japanese(self):
        dbl = DBL()
        dbl.set("hello:japanese", "こんにちは")
        assert dbl.get("hello:japanese") == "こんにちは"

    def test_to_reproduce_fixed_bug_and_prevent_it_from_regress(self):
        dbl = DBL()
        key, value = "encoding-issue", "https://en.wikipedia.or"
        dbl.set(key, value)
        assert dbl.get(key) == value

    def test_multiple_sets_and_gets(self):
        dbl = DBL()
        for i in range(100):
            key, value = f"key-{i}", f"value-{i}"
            dbl.set(key, value)
            dbl.get(key)

    def test_remove_key(self):
        dbl = DBL()
        dbl.delete("key")
        assert dbl.get("key") == None


if __name__ == "__main__":
    unittest.main()
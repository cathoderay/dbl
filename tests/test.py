import os
import threading
import unittest


if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL, decode, encode


class DBLTest(unittest.TestCase):
    def setUp(self):
        DBL().clean_all()

    def tearDown(self):
        DBL().clean_all()

    def test_set_value_cannot_contain_end_record_character(self):
        dbl = DBL()
        assert dbl.internal.get_bytes_read() == 0
        with self.assertRaises(AssertionError):
            dbl.set("key", "value\x1E")

    def test_set_key_cannot_contain_key_value_separator(self):
        dbl = DBL()
        assert dbl.internal.get_bytes_read() == 0
        with self.assertRaises(AssertionError):
            dbl.set("key\x1Dkey", "value")

    def test_set_and_get(self):
        dbl = DBL()
        assert dbl.internal.get_bytes_read() == 0
        dbl.set("42", "Douglas Adams")
        assert(dbl.get("42") == "Douglas Adams")

    def test_set_updates_local_index(self):
        dbl = DBL()
        assert dbl.internal.get_bytes_read() == 0
        bytes_indexed_before = dbl.internal.get_bytes_read()
        dbl.set("42", "Test")
        dbl.get("42")
        bytes_indexed_after = dbl.internal.get_bytes_read()
        assert(bytes_indexed_before < bytes_indexed_after)

    def test_set_emoji(self):
        dbl = DBL()
        assert dbl.internal.get_bytes_read() == 0
        dbl.set("emoji", "😀")
        assert(dbl.get("emoji") == "😀")

    @unittest.skip("not implemented in rust yet")
    def test_set_bulk(self):
        dbl = DBL()
        assert dbl.internal.get_bytes_read() == 0
        bytes_indexed_before = dbl.internal.get_bytes_read()
        data = [
            ("name1", "Paul"),
            ("name2", "John"),
            ("name3", "Ringo"),
            ("name4", "George")
        ]
        dbl.set_bulk(data)
        bytes_indexed_after = dbl.internal.get_bytes_read()
        assert(bytes_indexed_before < bytes_indexed_after)
        assert(dbl.get("name1") == "Paul")
        assert(dbl.get("name2") == "John")
        assert(dbl.get("name3") == "Ringo")
        assert(dbl.get("name4") == "George")

    def test_get_non_existent_key(self):
        dbl = DBL()
        assert dbl.internal.get_bytes_read() == 0
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
        assert dbl.internal.get_bytes_read() == 0
        dbl.get("foo")
        assert dbl.internal.get_bytes_read() == 26

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
            assert dbl.get(key) == value

    def test_remove_key(self):
        dbl = DBL()
        dbl.delete("key")
        assert dbl.get("key") == None
    
    def test_allow_commas_in_values(self):
        dbl = DBL()
        value = "value, with, commas"
        dbl.set("key-with-commas", value)
        assert dbl.get("key-with-commas") == value

    def test_allow_newlines_in_values(self):
        dbl = DBL()
        value = "value\nwith\nnewlines"
        dbl.set("key-with-newlines", value)
        assert dbl.get("key-with-newlines") == value

    def test_compact(self):
        from conf_test import COMPACT_PATH

        dbl = DBL()
        for i in range(10):
            dbl.set("key-0", f"value-{i}")

        bytes_before = os.path.getsize(dbl.DATABASE_PATH)

        dbl.compact()

        bytes_after = os.path.getsize(COMPACT_PATH)

        assert bytes_before == 140
        assert bytes_after == 14
        assert dbl.get("key-0") == "value-9"


class DBLHelperTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_encode_and_decode(self):
        original = "https://en.wikipedia.or"
        assert decode(encode(original)) == original



if __name__ == "__main__":
    unittest.main()
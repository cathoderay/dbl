import os
import unittest

if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from dbl import DBL, dbl_internal
from helper import decode


class DBLTest(unittest.TestCase):
    def setUp(self):
        DBL().clean_all()

    def test_set_value_cannot_contain_end_record_character(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        with self.assertRaises(AssertionError):
            dbl.set("key", "value\n")

    def test_set_key_cannot_contain_key_value_separator(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        with self.assertRaises(AssertionError):
            dbl.set("key,key", "value")

    def test_set_and_get(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        dbl.set("42", "Douglas Adams")
        assert(dbl.get("42") == "Douglas Adams")

    def test_set_updates_local_index(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        bytes_indexed_before = dbl.bytes_indexed
        assert(len(dbl.index) == 0)
        dbl.get("42")
        assert(len(dbl.index) >= 0)
        dbl.set("42", "Test")
        bytes_indexed_after = dbl.bytes_indexed
        assert(bytes_indexed_before < bytes_indexed_after)

    def test_set_emoji(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        dbl.set("emoji", "😀")
        assert(dbl.get("emoji") == "😀")

    def test_get_encoded_data(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        encoded = dbl.get_encoded_data("key", "value✅")
        assert((b'key', b',', b'value\xe2\x9c\x85', b'\n') == encoded)

    def test_set_bulk(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        bytes_indexed_before = dbl.bytes_indexed
        data = [
            ("name1", "Paul"),
            ("name2", "John"),
            ("name3", "Ringo"),
            ("name4", "George")
        ]
        dbl.set_bulk(data, update_index=True)
        bytes_indexed_after = dbl.bytes_indexed
        assert(bytes_indexed_before < bytes_indexed_after)
        assert(dbl.get("name1") == "Paul")
        assert(dbl.get("name2") == "John")
        assert(dbl.get("name3") == "Ringo")
        assert(dbl.get("name4") == "George")

    def test_set_bulk_without_updating_index(self):
        dbl = DBL()
        assert dbl.bytes_indexed == 0
        bytes_indexed_before = dbl.bytes_indexed
        data = [
            ("name1", "Paul"),
            ("name2", "John"),
            ("name3", "Ringo"),
            ("name4", "George")
        ]
        dbl.set_bulk(data, update_index=False)
        bytes_indexed_after = dbl.bytes_indexed
        assert(bytes_indexed_before == bytes_indexed_after)


if os.getenv("DBL_CPP_EXPERIMENT") == "1":
    class DBLTestCPPExperiment(unittest.TestCase):
        def setUp(self):
            dbl_internal.clean_index()
            DBL().clean_all()

        def test_verify_outputs_are_the_same(self):
            dbl = DBL()
            dbl.set("food", "lettuce")
            dbl.set("drink", "water")
            assert dbl.get("food") == decode(dbl_internal.get(b"food"))
            assert dbl.get("drink") == decode(dbl_internal.get(b"drink"))
            dbl_internal.clean_index()

        def test_set_and_get(self):
            dbl_internal.set(b"food", b"broccoli")
            assert decode(dbl_internal.get(b"food")) == "broccoli"

        def test_set_and_get_2(self):
            dbl_internal.set(b"drink", b"water")
            dbl_internal.set(b"food", b"broccoli")
            assert decode(dbl_internal.get(b"food")) == "broccoli"

            dbl_internal.set(b"food", b"lettuce")
            assert decode(dbl_internal.get(b"drink")) == "water"
            assert decode(dbl_internal.get(b"food")) == "lettuce"


if __name__ == "__main__":
    unittest.main()
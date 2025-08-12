import unittest


from dbl import DBL


class LoggyTest(unittest.TestCase):
    def test_set_value_cannot_contain_end_record_character(self):
        dbl = DBL()
        with self.assertRaises(AssertionError):
            dbl.set("key", "value\n")

    def test_set_key_cannot_contain_key_value_separator(self):
        dbl = DBL()
        with self.assertRaises(AssertionError):
            dbl.set("key,key", "value")

    def test_set_and_get(self):
        dbl = DBL()
        dbl.set("42", "Douglas Adams")
        assert(dbl.get("42") == "Douglas Adams")

    def test_set_updates_local_index(self):
        dbl = DBL()
        bytes_indexed_before = dbl.bytes_indexed
        assert(len(dbl.index) == 0)
        dbl.get("42")
        assert(len(dbl.index) >= 0)
        dbl.set("42", "Test")
        bytes_indexed_after = dbl.bytes_indexed
        assert(bytes_indexed_before < bytes_indexed_after)

    def test_set_emoji(self):
        dbl = DBL()
        dbl.set("emoji", "😀")
        assert(dbl.get("emoji") == "😀")


if __name__ == "__main__":
    unittest.main()
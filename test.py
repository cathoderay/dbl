import unittest


import dbl


class LoggyTest(unittest.TestCase):
    def test_set_value_cannot_contain_end_record_character(self):
        with self.assertRaises(AssertionError):
            dbl.set("key", "value\n")

    def test_set_key_cannot_contain_key_value_separator(self):
        with self.assertRaises(AssertionError):
            dbl.set("key,key", "value")

    def test_set_and_get(self):
        dbl.set("42", "Douglas Adams")
        assert(dbl.get("42") == "Douglas Adams")

    def test_set_updates_local_index(self):
        previous_index = dbl.index.get("42", None)
        dbl.set("42", "Test")
        new_index = dbl.index.get("42", None)
        assert(previous_index != new_index)


if __name__ == "__main__":
    unittest.main()
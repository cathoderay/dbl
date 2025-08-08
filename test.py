import unittest


import loggy 


class LoggyTest(unittest.TestCase):
    def test_set_and_get(self):
        loggy.set("42", "Douglas Adams")
        assert(loggy.get("42") == "Douglas Adams")
    
    def test_set_updates_local_index(self):
        key = 42
        previous_index = loggy.index.get(42, None)
        loggy.set("42", "Test")
        new_index = loggy.index.get(42, None)
        assert(previous_index != new_index)


if __name__ == "__main__":
    unittest.main()
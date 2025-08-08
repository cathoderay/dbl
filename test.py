import unittest


import loggy 


class LoggyTest(unittest.TestCase):
    def test_set_and_get(self):
        loggy.set("42", "Douglas Adams")
        assert(loggy.get("42") == "Douglas Adams")
    



if __name__ == "__main__":
    unittest.main()
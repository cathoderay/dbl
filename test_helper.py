import os
import unittest



if not os.getenv("DBL_TEST_ENV", 0) == "1":
    print("You should set DBL_TEST_ENV to run tests.")
    exit(-1)


from helper import encode, decode


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
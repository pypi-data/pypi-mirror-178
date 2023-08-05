import unittest


class TestCompile(unittest.TestCase):
    def test_str(self):
        result = ""
        self.assertIsInstance(result, str, "result is not str")

    def test_list(self):
        result = ""
        self.assertIsInstance(result, list, "result is not list")


if __name__ == '__main__':
    unittest.main()

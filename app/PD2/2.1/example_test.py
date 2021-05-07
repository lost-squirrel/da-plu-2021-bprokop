import unittest

from file import greetings


class ExampleTest(unittest.TestCase):
    @greetings
    def show_greetings(self):
        return "joe doe"

    @greetings
    def param_greetings(self, name):
        return name

    def test_multiple_names(self):
        self.assertEqual(self.param_greetings(
            "bartosz mikolaj prokop"), "Hello Bartosz Mikolaj Prokop")
        self.assertEqual(self.param_greetings(
            "bartosz mikolaj stefan prokop"), "Hello Bartosz Mikolaj Stefan Prokop")

    def test_proper_capitalization(self):
        self.assertEqual(self.param_greetings(
            "BArTosz mIkolaJ prokOp"), "Hello Bartosz Mikolaj Prokop")

    def test_single_name(self):
        self.assertEqual(self.param_greetings(
            "bartosz"), "Hello Bartosz")

    def test_result(self):
        self.assertEqual(self.show_greetings(), "Hello Joe Doe")


if __name__ == "__main__":
    unittest.main()

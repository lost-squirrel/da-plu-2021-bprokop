import unittest

from file import format_output


class ExampleTest(unittest.TestCase):
    @format_output("first_name")
    def show_dict(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
        }

    def test_result(self):
        self.assertEqual(self.show_dict(), {"first_name": "Jan"})


if __name__ == "__main__":
    unittest.main()

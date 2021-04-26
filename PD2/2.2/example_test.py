import unittest

from file import is_palindrome


class ExampleTest(unittest.TestCase):
    @is_palindrome
    def show_sentence(self):
        return "annA"

    @is_palindrome
    def show_sentence_param(self, sentence):
        return sentence

    def test_result(self):
        self.assertEqual(self.show_sentence(), "annA - is palindrome")

    def test_not_palindrome(self):
        self.assertEqual(self.show_sentence_param('bartosz'),
                         'bartosz - is not palindrome')

    def test_not_palindrome_special(self):
        self.assertEqual(self.show_sentence_param('2!!Łapał za kran, a kanarka złapał.#!21'),
                         '2!!Łapał za kran, a kanarka złapał.#!21 - is not palindrome')

    def test_numeric_palindrome(self):
        self.assertEqual(self.show_sentence_param('111222111'),
                         '111222111 - is palindrome')

    def test_numeric_special_palindrome(self):
        self.assertEqual(self.show_sentence_param('1,1.1.2!@22#$%%111!@#$%^&*()'),
                         '1,1.1.2!@22#$%%111!@#$%^&*() - is palindrome')

    def test_empty_string(self):
        self.assertEqual(self.show_sentence_param(''),
                         ' - is palindrome')

    def test_polish_chars(self):
        self.assertEqual(self.show_sentence_param('Łapał za kran, a kanarka złapał.'),
                         'Łapał za kran, a kanarka złapał. - is palindrome')


if __name__ == "__main__":
    unittest.main()

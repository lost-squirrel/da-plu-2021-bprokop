from file import add_class_method, add_instance_method
import unittest


class ExampleClass:
    pass


@add_class_method(ExampleClass)
def cls_method():
    return "Hello!"


@add_instance_method(ExampleClass)
def inst_method():
    return "Hello!"


class ExampleTest(unittest.TestCase):
    def test_result(self):
        self.assertEqual(ExampleClass.cls_method(), cls_method())
        self.assertEqual(ExampleClass().inst_method(), inst_method())


if __name__ == "__main__":
    unittest.main()

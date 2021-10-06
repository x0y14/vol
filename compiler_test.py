import unittest

class A:
    def __init__(self):
        self.mem = []
        self.mp = len(self.mem) - 1


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # self.assertEqual(True, False)  # add assertion here
        a = A()
        self.assertEqual(-1, a.mp)
        a.mem.append(1)
        self.assertEqual(0, a.mp)


if __name__ == '__main__':
    unittest.main()

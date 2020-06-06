import unittest
from myfunc import is_prime, add, divide


class TestMyFunc(unittest.TestCase):
    def setUp(self):
        print('每个测试用例执行前都会调用setUp方法准备环境')

    def tearDown(self):
        print('每个测试用例执行后都会调用tearDown方法进行环境清理')

    def test_is_prime(self):
        print('is_prime')
        self.assertTrue(is_prime(5))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(-1))
        self.assertFalse(is_prime(-3))

    def test_add(self):
        print('add')
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_divide(self):
        print('divide')
        self.assertEqual(2, divide(6, 3))
        self.assertNotEqual(2, divide(5, 2))


if __name__ == '__main__':
    unittest.main()

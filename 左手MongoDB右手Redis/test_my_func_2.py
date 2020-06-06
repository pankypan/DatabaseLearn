import unittest
import sys

from myfunc import is_prime, add, divide
from HtmlTestRunner


class TestMyFunc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('在所有测试用例执行前会调用setUpClass方法准备环境')

    @classmethod
    def tearDownClass(cls):
        print('在所有测试用例执行完毕后会调用tearDownClass方法进行环境清理')

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

    @unittest.skipUnless(sys.platform.startswith('linux'), 'requires Linux')
    def test_divide(self):
        print('divide')
        self.assertEqual(2, divide(6, 3))
        self.assertNotEqual(2, divide(5, 2))


if __name__ == '__main__':
    # 1 使用TestSuite控制用例顺序，用例的执行顺序是由添加到TestSuite的顺序决定的
    tests = [TestMyFunc('test_is_prime'), TestMyFunc('test_add'), TestMyFunc('test_divide')]

    suite = unittest.TestSuite()
    suite.addTests(tests)  # 将测试用例增加到测试套件

    runner = unittest.TextTestRunner()
    runner.run(suite)

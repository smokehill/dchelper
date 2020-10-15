import os
import unittest

from cache import Cache

cache = Cache('.cache_test')

class TestCacheMethods(unittest.TestCase):

    def test_01_remember(self):
        cache.remember(100)
        cache.remember(200)

        self.assertEqual(cache.proc_list, ['100','200'])

    def test_02_forget(self):
        cache.forget(100)
        cache.forget(200)

        self.assertEqual(cache.proc_list, [])

    def test_03_forget(self):
        cache.forget()
        is_file = os.path.isfile(cache.file_path)

        self.assertFalse(is_file)


if __name__ == '__main__':
    unittest.main()
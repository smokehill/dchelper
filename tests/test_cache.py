import os
import unittest

from dchelp.cache import Cache


class TestCache(unittest.TestCase):

    cache = None

    def __init__(self, *args, **kwargs):
        self.cache = Cache('proc_test')
        super(TestCacheMethods, self).__init__(*args, **kwargs)

    def test_01_remember(self):
        self.cache.remember(100)
        self.cache.remember(200)

        self.assertEqual(self.cache.proc_list, ['100','200'])

    def test_02_forget(self):
        self.cache.forget(100)
        self.cache.forget(200)

        self.assertEqual(self.cache.proc_list, [])

    def test_03_forget(self):
        self.cache.forget()
        is_file = os.path.isfile(self.cache.proc_file)

        self.assertFalse(is_file)
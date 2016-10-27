# -*- coding: utf-8 -*-

import unittest

import os
from .mock_ssg import *


class TestSSGBasic(unittest.TestCase):
    """\
    - The basic functionality:
        + clean
        + load_templates
        + render
        + send_static
    """
    def setUp(self):
        self.valid_empty_markdown_file = 'foo.md'
        self.invalid_empty_markdown_file = 'bar.mdx'
        open(self.valid_empty_markdown_file, 'a').close()
        open(self.invalid_empty_markdown_file, 'a').close()

    @classmethod
    def setUpClass(cls):
        cls.ssg = MockSSG()

    def test_filepath_doesnt_exists(self):
        with self.assertRaises(OSError):
            self.ssg.load_templates('foo')

    def test_load_valid_markdown_file(self):
        tmpls = self.ssg.load_templates(self.valid_empty_markdown_file)
        self.assertTrue(tmpls)

    def test_load_invalid_markdown_file(self):
        tmpls = self.ssg.load_templates(self.invalid_empty_markdown_file)
        self.assertFalse(tmpls)

    def tearDown(self):
        try:
            os.remove(self.valid_empty_markdown_file)
            os.remove(self.invalid_empty_markdown_file)
        except OSError as e:
            raise e


if __name__ == '__main__':
    unittest.main()

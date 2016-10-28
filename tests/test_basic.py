# -*- coding: utf-8 -*-

import unittest

import os
from .mock_ssg import *
from .data import md


class TestSSGBasic(unittest.TestCase):
    """\
    - The basic functionality:
        + clean
        + load_templates
        + render
        + publish
        + send_static
    """
    def setUp(self):
        self.invalid_empty_markdown_file = 'foo.mdx'
        self.valid_markdown_file = 'foo.md'
        self.pymd_exts = ['extra', 'meta']
        open(self.invalid_empty_markdown_file, 'w').close()
        with open(self.valid_markdown_file, 'w') as f:
            f.write(md.markdown_text)

    @classmethod
    def setUpClass(cls):
        cls.ssg = MockSSG()

    def test_add_python_markdown_extensions(self):
        self.ssg.add_pymd_exts(self.pymd_exts)
        self.assertEqual(self.ssg.pymd_exts,
            ['markdown.extensions.extra', 'markdown.extensions.meta'])

    def test_filepath_doesnt_exists(self):
        with self.assertRaises(OSError):
            self.ssg.ifpath = 'foo'
            self.ssg.load_templates(self.ssg.ifpath)

    def test_load_invalid_markdown_file(self):
        self.ssg.ifpath = self.invalid_empty_markdown_file
        tmpls = self.ssg.load_templates(self.ssg.ifpath)
        self.assertFalse(tmpls)

    def test_load_valid_markdown_file(self):
        self.ssg.ifpath = self.valid_markdown_file
        tmpls = self.ssg.load_templates(self.ssg.ifpath)
        self.assertTrue(tmpls)

    def tearDown(self):
        try:
            os.remove(self.valid_markdown_file)
            os.remove(self.invalid_empty_markdown_file)
        except OSError as e:
            raise e


if __name__ == '__main__':
    unittest.main()

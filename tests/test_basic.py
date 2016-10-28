# -*- coding: utf-8 -*-

import unittest

from shutil import rmtree
from os import path, mkdir, remove

from .mock_ssg import *
from .data import md


class TestSSGBasic(unittest.TestCase):
    """\
    - The basic functionality:
        + add_pymd_exts
        + clean
        + load_templates
        + render
        + publish
        + send_static
    """
    def setUp(self):
        self.invalid_empty_markdown_file = 'foo.mdx'
        self.valid_markdown_file0 = 'foo.md'
        self.valid_markdown_file1 = 'bar.md'
        self.tmpdir = 'temp'
        self.pymd_exts = ['extra', 'meta']

        mkdir(self.tmpdir)
        open(self.invalid_empty_markdown_file, 'w').close()
        open(path.join(self.tmpdir, self.invalid_empty_markdown_file), 'w').close()
        with open(self.valid_markdown_file0, 'w') as f:
            f.write(md.markdown_text0)

    @classmethod
    def setUpClass(cls):
        cls.ssg = MockSSG()

    def test_add_python_markdown_extensions(self):
        self.ssg.add_pymd_exts(self.pymd_exts)
        self.assertEqual(self.ssg.pymd_exts,
            ['markdown.extensions.extra', 'markdown.extensions.meta'])

    def test_filepath_doesnt_exists(self):
        with self.assertRaises(OSError):
            self.ssg.ifpath = 'foo' # assume it doesn't exist
            self.ssg.load_templates(self.ssg.ifpath)

    def test_load_invalid_markdown_file(self):
        self.ssg.ifpath = self.invalid_empty_markdown_file
        self.assertFalse(self.ssg.load_templates(self.ssg.ifpath))

    def test_load_valid_markdown_file(self):
        self.ssg.ifpath = self.valid_markdown_file0
        self.assertTrue(self.ssg.load_templates(self.ssg.ifpath))

    def test_filepath_nothing_to_publish(self):
        self.ssg.ifpath = self.tmpdir
        self.assertFalse(self.ssg.load_templates(self.ssg.ifpath))

    def test_generated_page_content(self):
        with open(path.join(self.tmpdir, self.valid_markdown_file0), 'w') as f:
            f.write(md.markdown_text0)
        self.ssg.ifpath = self.tmpdir
        tmpls = self.ssg.load_templates(self.ssg.ifpath)
        self.assertTrue(tmpls)
        
        posts = self.ssg.render(tmpls)     
        self.assertTrue(posts[0]['meta'])
        self.assertTrue(posts[0]['html'])
        self.assertEqual(posts[0]['fname'], 'foo.html')

    def test_publish(self):
        with open(path.join(self.tmpdir, self.valid_markdown_file0), 'w') as f:
            f.write(md.markdown_text1)
        

    def tearDown(self):
        try:
            remove(self.valid_markdown_file0)
            remove(self.invalid_empty_markdown_file)
            rmtree(self.tmpdir)
        except OSError as e:
            raise e


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-

import unittest

from shutil import rmtree
from os import path, makedirs, remove
from jinja2 import Environment, exceptions

from .mock_ssg import *
from .data import md


class TestSSGBasic(unittest.TestCase):
    """Test the basic functionality"""
    def setUp(self):
        self.invalid_empty_markdown_file = 'foo.mdx'
        self.valid_markdown_file0 = 'foo.md'
        self.valid_markdown_file1 = 'bar.md'
        self.output_html_file = 'foo.index'
        self.tmpdir = 'temp' # assume it doesn't exist
        self.pymd_exts = ['extra', 'meta']

        # TODO: Replace it with tempfile.mkdtemp()
        makedirs(self.tmpdir, exist_ok=True)
        open(self.invalid_empty_markdown_file, 'w').close()
        open(path.join(self.tmpdir, self.invalid_empty_markdown_file), 'w').close()
        with open(self.valid_markdown_file0, 'w') as f:
            f.write(md.markdown_text0)

    @classmethod
    def setUpClass(cls):
        cls.ssg = MockSSG()

    def test_add_python_markdown_extensions(self):
        self.ssg.pymd_exts = self.pymd_exts
        self.assertEqual(self.ssg.pymd_exts,
            ['markdown.extensions.extra', 'markdown.extensions.meta'])

    def test_filepath_doesnt_exists(self):
        with self.assertRaises(OSError):
            self.ssg.ifpath = 'foo' # assume it doesn't exist
            self.ssg.load_posts(self.ssg.ifpath)

    def test_load_templates(self):
        self.assertIn('index', self.ssg.load_templates(self.ssg.tmplpath))

    def test_load_invalid_markdown_file(self):
        self.ssg.ifpath = self.invalid_empty_markdown_file
        self.assertFalse(self.ssg.load_posts(self.ssg.ifpath))

    def test_load_valid_markdown_file(self):
        self.ssg.ifpath = self.valid_markdown_file0
        self.assertTrue(self.ssg.load_posts(self.ssg.ifpath))

    def test_filepath_nothing_to_publish(self):
        self.ssg.ifpath = self.tmpdir
        self.assertFalse(self.ssg.load_posts(self.ssg.ifpath))

    def test_generated_page_content(self):
        with open(path.join(self.tmpdir, self.valid_markdown_file0), 'w') as f:
            f.write(md.markdown_text0)
        posts = self.ssg.load_posts(self.ssg.ifpath)
        self.assertTrue(posts)
        
        pages = self.ssg.render(posts)     
        self.assertTrue(pages[0]['meta'])
        self.assertTrue(pages[0]['html'])
        self.assertEqual(pages[0]['fname'], 'foo.html')

    def test_publish_invalid_page_dict(self):
        with self.assertRaises(TypeError):
            self.ssg.publish([{'foo': 'bar'}])

    def test_publish_single_page(self):
        self.ssg.ofpath = path.join(self.tmpdir, self.output_html_file)
        post = self.ssg.load_posts(self.valid_markdown_file0)
        self.assertTrue(post)

        tmpl = self.ssg.load_templates(self.ssg.tmplpath)
        self.assertTrue(tmpl)

        page = self.ssg.render(post)
        self.ssg.publish(page, tmpl)
        self.assertTrue(path.exists(self.ssg.ofpath))

    def test_publish_all(self):
        with open(path.join(self.tmpdir, self.valid_markdown_file0), 'w') as f:
            f.write(md.markdown_text1)

    def tearDown(self):
        try:
            remove(self.valid_markdown_file0)
            remove(self.invalid_empty_markdown_file)
            rmtree(self.tmpdir)
        except OSError as e:
            raise e

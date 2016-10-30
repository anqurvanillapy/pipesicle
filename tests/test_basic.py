# -*- coding: utf-8 -*-

import unittest

from os import remove
from pathlib import Path
from tempfile import \
    NamedTemporaryFile as tmpfile, \
    TemporaryDirectory as tmpdir

from .mock_ssg import *
from .data import md


class TestSSGBasic(unittest.TestCase):
    """Test the basic functionality"""
    def setUp(self):
        self.valid_markdown_file = 'foo.md'
        self.invalide_markdown_file = 'foo.mdx'

    @classmethod
    def setUpClass(cls):
        cls.ssg = MockSSG()

    def test_add_python_markdown_extensions(self):
        pymd_exts = ['extra', 'meta']
        self.ssg.pymd_exts = pymd_exts
        self.assertEqual(self.ssg.pymd_exts,
                         ['markdown.extensions.extra',
                          'markdown.extensions.meta'])

    def test_filepath_doesnt_exists(self):
        with self.assertRaises(OSError):
            self.ssg.ifpath = 'foo' # assume it doesn't exist
            self.ssg.load_posts(self.ssg.ifpath)

    def test_load_templates(self):
        self.assertIn('index', self.ssg.load_templates(self.ssg.tmplpath))

    def test_load_invalid_markdown_file(self):
        with tmpfile(suffix='.mdx') as tmp:
            self.ssg.ifpath = tmp.name
            self.assertFalse(self.ssg.load_posts(self.ssg.ifpath))

    def test_load_valid_markdown_file(self):
        with tmpfile(suffix='.md') as tmp:
            self.ssg.ifpath = tmp.name
            self.assertTrue(self.ssg.load_posts(self.ssg.ifpath))

    def test_filepath_nothing_to_publish(self):
        with tmpdir() as tmp:
            tmp_path = Path(tmp)
            invalid_md = tmp_path / self.invalide_markdown_file
            invalid_md.write_text(md.markdown_text0)
            self.ssg.ifpath = str(tmp_path)
            self.assertFalse(self.ssg.load_posts(self.ssg.ifpath))

    def test_generated_page_content(self):
        with tmpdir() as tmp:
            tmp_path = Path(tmp)
            valid_md = tmp_path / self.valid_markdown_file
            valid_md.write_text(md.markdown_text0)
            self.ssg.ifpath = str(tmp_path)
            posts = self.ssg.load_posts(self.ssg.ifpath)
            self.assertTrue(posts)
            
            pages = self.ssg.render(posts)     
            self.assertTrue(pages[0]['meta'])
            self.assertTrue(pages[0]['content'])
            self.assertEqual(pages[0]['fname'], 'foo.html')

    def test_publish_invalid_page_dict(self):
        with self.assertRaises(TypeError):
            self.ssg.publish([{'foo': 'bar'}])

    def test_publish_single_page(self):
        output_html_file = 'index.html'

        with tmpdir() as tmp:
            tmp_path = Path(tmp)
            valid_md = tmp_path / self.valid_markdown_file
            valid_md.write_text(md.markdown_text1)

            self.ssg.ofpath = output_html_file
            post = self.ssg.load_posts(str(valid_md))
            self.assertTrue(post)

            tmpl = self.ssg.load_templates(self.ssg.tmplpath)
            self.assertTrue(tmpl)

            page = self.ssg.render(post)
            self.ssg.publish(page, tmpl)
            self.assertTrue(Path(self.ssg.ofpath).exists())
            
            # individual test case tearDown
            try:
                remove(output_html_file)
            except OSError as e:
                raise e

    def test_publish_all(self):
        pass

# -*- coding: utf-8 -*-

import unittest

from os import remove
from shutil import rmtree
from pathlib import Path
from tempfile import \
    NamedTemporaryFile as tmpfile, \
    TemporaryDirectory as tmpdir

from .mock_ssg import *
from .data import md


class TestSSGBasic(unittest.TestCase):
    """Test the basic functionality"""
    @classmethod
    def setUpClass(cls):
        cls.ssg = MockSSG()

    def test_add_python_markdown_extensions(self):
        pymd_exts = ['extra', 'tables']
        self.ssg.pymd_exts = pymd_exts
        # 'meta' is the default extension
        self.assertEqual(self.ssg.pymd_exts,
                         ['markdown.extensions.meta',
                          'markdown.extensions.extra',
                          'markdown.extensions.tables'])

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
            invalid_md = tmp_path / 'foo.mdx'
            invalid_md.write_text(md.markdown_text['content'][0])
            self.ssg.ifpath = str(tmp_path)
            self.assertFalse(self.ssg.load_posts(self.ssg.ifpath))

    def test_generated_page_content(self):
        with tmpdir() as tmp:
            tmp_path = Path(tmp)
            valid_md = tmp_path / md.markdown_text['fname'][0]
            valid_md.write_text(md.markdown_text['content'][0])
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
            valid_md = tmp_path / md.markdown_text['fname'][0]
            valid_md.write_text(md.markdown_text['content'][1])

            self.ssg.ofpath = output_html_file
            post = self.ssg.load_posts(str(valid_md))
            self.assertTrue(post)

            tmpl = self.ssg.load_templates(self.ssg.tmplpath)
            self.assertTrue(tmpl)

            page = self.ssg.render(post)
            self.assertTrue(page)

            self.ssg.publish(page, tmpl)
            self.assertTrue(Path(self.ssg.ofpath).exists())
            
            # private test case tearDown: remove `index.html`
            try:
                remove(output_html_file)
            except OSError as e:
                raise e

    def test_create_invalid_manual_page_dict(self):
        with self.assertRaises(TypeError):
            self.ssg.create_page_dict([], 'foo', 'bar')

    def test_create_manual_page_dict(self):
        page = self.ssg.create_page_dict([], 'index', 'bar')
        self.assertTrue('index' in page['meta']['type'])

    def test_publish_all(self):
        with tmpdir() as tmp:
            tmp_path = Path(tmp)
            post_text = md.markdown_text['content']
            fnames = md.markdown_text['fname']

            touch_md = lambda x: tmp_path / x
            for i in range(len(post_text)):
                touch_md(fnames[i]).write_text(post_text[i])

            posts = self.ssg.load_posts(str(tmp_path))
            self.assertTrue(posts)

            tmpls = self.ssg.load_templates(self.ssg.tmplpath)
            self.assertTrue(tmpls)

            pages = self.ssg.render(posts)
            self.assertTrue(pages)

            self.ssg.publish(pages, tmpls)
            self.assertTrue(Path(self.ssg.ofpath).exists)
            
            # private test case tearDown: remove `site`
            try:
                rmtree(self.ssg.ofpath)
            except OSError as e:
                raise e

    def test_send_static_assets(self):
        dest = 'static'
        self.ssg.send_static(dest)

        asset = Path(dest) / 'style.css'
        self.assertTrue(asset.exists())

        # private test case tearDown: remove `static`
        try:
            rmtree(dest)
        except OSError as e:
            raise e

    def test_clean_generated_pages(self):
        with tmpdir() as tmp:
            tmp_path = Path(tmp)
            file_to_clean = tmp_path / 'foo.html'
            file_to_clean.write_text('')
            file_not_to_clean = tmp_path / 'foo.txt'
            file_not_to_clean.write_text('')

            self.ssg.ofpath = str(tmp_path)
            self.ssg.clean()
            self.assertFalse(file_to_clean.exists())
            self.assertTrue(file_not_to_clean.exists())

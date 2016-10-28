# -*- coding: utf-8 -*-

from metassg import MetaSSG

import codecs
from os.path import basename, splitext
from markdown import Markdown
from bs4 import BeautifulSoup
from jinja2 import *


class MockSSG(MetaSSG):
    """\
    - Mock SSG for multiple usage, e.g.
        + slideshow generator (without `clean()` method)
        + blog, wiki (with `clean()` method)
    """
    def __init__(self):
        super().__init__(None, None)

    def render(self, tmpls):
        """Render Jinja2 templates"""
        posts = []

        for t in tmpls:
            try:
                with codecs.open(t, 'r', encoding='utf-8') as f:
                    md = Markdown(extensions=self.pymd_exts)
                    html = BeautifulSoup(md.convert(f.read()), 'lxml')
                    meta = md.Meta
                    fname = lambda x: '{}.html'.format(splitext(basename(x))[0])
                    posts.append({'html': html, 'meta': meta, 'fname': fname(t)})
            except Exception as e:
                raise e

        return posts

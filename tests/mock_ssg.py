# -*- coding: utf-8 -*-
"""
    MockSSG
    =======

    Incomplete SSG for unit testing.
"""

from postocol import Postocol

import codecs
from os.path import basename, splitext
from markdown import Markdown
from bs4 import BeautifulSoup


class MockSSG(Postocol):
    tmplpath = 'tests/data'
    staticpath = 'tests/data/static'

    def render(self, posts):
        """Render pages with Jinja2 templates"""
        pages = []

        for p in posts:
            with codecs.open(p, 'r', encoding='utf-8') as f:
                md = Markdown(extensions=self.pymd_exts)
                html = BeautifulSoup(md.convert(f.read()), 'lxml')
                html.html.hidden = True
                html.body.hidden = True # remove html and body tags
                meta = md.Meta
                fname = lambda x: '{}.html'.format(splitext(basename(x))[0])
                pages.append({'content': html,
                              'meta': meta,
                              'fname': fname(p)})

        return pages

# -*- coding: utf-8 -*-

from postocol import Postocol

import codecs
from os.path import basename, splitext
from markdown import Markdown
from bs4 import BeautifulSoup


class MockSSG(Postocol):
    """\
        - Mock SSG for multiple usage, e.g.
            + slideshow generator (without `clean()` method)
            + blog, wiki (with `clean()` method)
    """
    tmplpath = 'tests/data'
    staticpath = 'tests/data/static'
    ifpath = '' # abstract property, but replaced with temp file/dir

    def render(self, posts):
        """Render Jinja2 templates"""
        pages = []

        for p in posts:
            try:
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
            except Exception as e:
                raise e

        return pages

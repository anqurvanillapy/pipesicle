# -*- coding: utf-8 -*-
"""
    MockSSG
    =======

    Incomplete SSG for unit testing.
"""

from postocol import Postocol
from os.path import basename, splitext


class MockSSG(Postocol):
    tmplpath = 'tests/data'
    staticpath = 'tests/data/static'

    def render(self, posts):
        """Render pages with Jinja2 templates"""
        pages = []
        chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

        for h, m, p in posts:
            pages.append({'content': h, 'meta': m, 'fname': chfn(p)})

        return pages

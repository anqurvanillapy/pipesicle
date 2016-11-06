#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Example SSG
    ===========

    Similar to the `MockSSG` in test suite, but using full functionality and
    workflow.
"""


from postocol import Postocol

import codecs
from os.path import join, basename, splitext
from collections import defaultdict

from markdown import Markdown
from bs4 import BeautifulSoup


class SSG(Postocol):
    """SSG Example"""
    def __init__(self):
        self.pymd_exts = ['fenced_code', 'codehilite']

    def run(self):
        """Control flow goes here"""
        self.clean()
        self.tmpls = self.load_templates()
        self.posts = self.load_posts()
        self.pages = self.render(self.posts)
        self.publish(self.pages, self.tmpls)
        self.send_codehilite_style()
        self.send_static(join(self.ofpath, self.staticpath))

    def render(self, posts):
        """Render pages"""
        pages = []
        chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

        pgroup = ['states', 'properties']
        pgdict = {pg:defaultdict(list) for pg in pgroup}
        index = []

        for c, m, f in posts:
            pages.append({'content': c,
                          'meta': m,
                          'fname': chfn(f)})

            if 'misc' not in m.get('type'):
                index.append({'title': m['title'][0], 'fname': chfn(f)})

            for pg in pgroup:
                for mname in m.get(pg, []):
                    pgdict[pg][mname].append({'title': m['title'][0],
                                              'fname': chfn(f)}) 

        pages += [self.create_page_dict(c, n) for c, n in \
                  list(zip([index, *pgdict.values()], ['index', *pgdict.keys()]))]
        return pages


if __name__ == '__main__':
    ssg = SSG()
    ssg.run()

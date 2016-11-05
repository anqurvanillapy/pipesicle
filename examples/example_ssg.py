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
    def run(self):
        """Control flow goes here"""
        self.clean()
        self.tmpls = self.load_templates()
        self.posts = self.load_posts()
        self.pages = self.render(self.posts)
        self.publish(self.pages, self.tmpls)
        self.send_static(join(self.ofpath, self.staticpath))

    def render(self, posts):
        """Render pages"""
        pages = []
        chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

        pgroup = ['states', 'properties']
        pgdict = {pg:defaultdict(list) for pg in pgroup}
        index = []

        for p in posts:
            with codecs.open(p, 'r', encoding='utf-8') as f:
                md = Markdown(extensions=self.pymd_exts)
                html = BeautifulSoup(md.convert(f.read()), 'lxml')
                html.html.hidden = True
                html.body.hidden = True # remove html and body tags
                meta = md.Meta
                pages.append({'content': html,
                              'meta': meta,
                              'fname': chfn(p)})

                if 'misc' not in meta.get('type'):
                    index.append({'title': meta['title'][0], 'fname': chfn(p)})

                for pg in pgroup:
                    if meta.get(pg):
                        for m in meta[pg]:
                            pgdict[pg][m].append({'title': meta['title'][0],
                                                  'fname': chfn(p)}) 

        pages += [self.create_page_dict(c, n) for c, n in \
                  list(zip([index, *pgdict.values()], ['index', *pgdict.keys()]))]
        return pages


if __name__ == '__main__':
    ssg = SSG()
    ssg.run()

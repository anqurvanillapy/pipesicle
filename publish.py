# -*- coding: utf-8 -*-
"""
    Project Site
    ============

    Generate project site's index on `gh-page` branch.
"""


from postocol import Postocol

import codecs
from os.path import join, basename, splitext
from collections import defaultdict

from markdown import Markdown
from bs4 import BeautifulSoup


class ProjectSite(Postocol):
    """ProjectSite Example"""
    ifpath = 'index.md'
    ofpath = 'index.html'

    def run(self):
        self.tmpls = self.load_templates(self.tmplpath)
        self.posts = self.load_posts(self.ifpath)
        self.pages = self.render(self.posts)
        self.publish(self.pages, self.tmpls)

    def render(self, posts):
        pages = []
        chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

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

        return pages


if __name__ == '__main__':
    projsite = ProjectSite()
    projsite.run()

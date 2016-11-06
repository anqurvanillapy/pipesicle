#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Project Site
    ============

    Generate project site's index on `gh-page` branch.
"""


from postocol import Postocol
from os.path import basename, splitext


class ProjectSite(Postocol):
    """ProjectSite Example"""
    ifpath = 'preface.md'
    ofpath = 'index.html'
    default_post_type = 'index'

    def __init__(self):
        self.pymd_exts = ['fenced_code', 'codehilite']

    def run(self):
        self.tmpls = self.load_templates()
        self.posts = self.load_posts()
        self.pages = self.render(self.posts)
        self.publish(self.pages, self.tmpls)
        self.send_codehilite_style('trac')

    def render(self, posts):
        pages = []
        chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])
        for c, m, f in posts:
            pages.append({'content': c, 'meta': m, 'fname': chfn(f)})
        return pages


if __name__ == '__main__':
    projsite = ProjectSite()
    projsite.run()

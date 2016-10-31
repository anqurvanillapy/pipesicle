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
        self.tmpls = self.load_templates(self.tmplpath)
        self.posts = self.load_posts(self.ifpath)
        self.pages = self.render(self.posts)
        self.publish(self.pages, self.tmpls)
        self.send_static(join(self.ofpath, self.staticpath))

    def render(self, posts):
        """Render pages"""
        pages = []
        chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

        autogen_pages = ['index', 'states', 'properties']
        states = defaultdict(list)
        props = defaultdict(list)
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
                if 'misc' not in meta['type']:
                    index.append({'title': meta['title'][0], 'fname': chfn(p)})
                try:
                    for state in meta['states']:
                        states[state].append({'title': meta['title'][0],
                                              'fname': chfn(p)})
                    for prop in meta['properties']:
                        props[prop].append({'title': meta['title'][0],
                                            'fname': chfn(p)})
                except KeyError as e:
                    pass # `p` may not have any states/properties, e.g. misc

        pages += [self.create_page_dict(c, n) for c, n in \
                  list(zip([index, states, props], autogen_pages))]
        return pages


if __name__ == '__main__':
    ssg = SSG()
    ssg.run()

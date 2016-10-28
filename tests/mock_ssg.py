# -*- coding: utf-8 -*-

from metassg import MetaSSG

import codecs
from markdown import markdown
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
                    html = BeautifulSoup(markdown(f.read(),
                        extensions=self.pymd_exts), 'lxml')
            except Exception as e:
                raise e

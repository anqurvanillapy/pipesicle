# -*- coding: utf-8 -*-

import os
from abc import abstractmethod, ABCMeta


class MetaSSG(metaclass=ABCMeta):
    """SSG base class"""
    def __init__(self, ifpath, ofpath):
        self.ifpath = ifpath
        self.ofpath = ofpath

    def clean(self):
        """Clean all legacy generated pages"""
        if os.path.isdir(self.ofpath):
            for f in os.listdir(self.ofpath):
                if os.path.splitext(f)[1] in {'.html', '.htm'}:
                    try:
                        os.remove(os.path.join(self.ofpath, f))
                    except OSError as e:
                        print('warning: unable to delete {}'.format(f))

    def load_templates(self, fpath):
        """\
        - Load templates using Jinja2 Environment
            + `fpath` can be filename and directory
            + FileSystemLoader is specified
        """
        pass

    @abstractmethod
    def render(self, posts):
        """\
        - Render the posts
            + Using Jinja2 render the templates
            + Publish pages into the destination directory
        """
        pass

    def send_static(self):
        """Send static assets to destination directory"""
        pass

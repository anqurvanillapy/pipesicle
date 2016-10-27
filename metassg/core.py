# -*- coding: utf-8 -*-

import os, errno
from abc import abstractmethod, ABCMeta


class MetaSSG(metaclass=ABCMeta):
    """SSG base class"""
    def __init__(self, ifpath, ofpath):
        self.ifpath = ifpath
        self.ofpath = ofpath
        self.mdexts =  {'.markdown', '.mdown', '.mkdn', '.md', '.mkd', '.mdwn',
        '.mdtxt', '.mdtext', '.text', '.txt'}

    def clean(self):
        """Clean all legacy generated pages"""
        if os.path.isdir(self.ofpath):
            for f in os.listdir(self.ofpath):
                if os.path.splitext(f)[1] in {'.html', '.htm'}:
                    try:
                        os.remove(os.path.join(self.ofpath, f))
                    except OSError as e: # no propagation
                        if e.errno != errno.ENOENT: # silent removal
                            print('warning: Unable to delete {}'.format(f))

    def load_templates(self, fpath):
        """\
        - Load templates using Jinja2 Environment
            + `fpath` can be filename and directory
            + FileSystemLoader is specified
        """
        if os.path.exists(fpath):
            tmpls = []

            for f in [fpath] if os.path.isfile(fpath) else os.listdir(fpath):
                if os.path.splitext(f)[1] in self.mdexts:
                    tmpls.append(f)

            return tmpls
        else:
            raise OSError(errno.ENOENT)

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

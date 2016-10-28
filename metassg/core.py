# -*- coding: utf-8 -*-

import os, errno
from abc import abstractmethod, ABCMeta


class MetaSSG(metaclass=ABCMeta):
    """SSG base class"""
    def __init__(self, ifpath, ofpath):
        self.ifpath = ifpath
        self.ofpath = ofpath
        self.md_exts =  {'.markdown', '.mdown', '.mkdn', '.md', '.mkd', '.mdwn',
        '.mdtxt', '.mdtext', '.text', '.txt'}
        self.pymd_exts = []

    def add_pymd_exts(self, exts):
        prefix = 'markdown.extensions.{}'
        self.pymd_exts += list(map(lambda x: prefix.format(x), exts))

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
                if os.path.splitext(f)[1] in self.md_exts:
                    tmpls.append(f)

            if not tmpls:
                print('warning: Nothing to publish')
            return tmpls
        else:
            raise OSError(errno.ENOENT)

    @abstractmethod
    def render(self, tmpls):
        """Render the posts (Jinja2 templates)"""
        pass

    def publish(self, posts):
        """Publish rendered posts"""
        pass

    def send_static(self, fpath):
        """Send static assets to destination directory"""
        pass

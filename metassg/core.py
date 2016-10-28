# -*- coding: utf-8 -*-
"""
    MetaSSG
    =======

    Abstract class for creating homemade static site generator

    - Abstract methods:
        + `render()`: Render pages
    - Abstract properties:
        + `tmplpath`: Template path for Jinja2 Environment
        + `ifpath`: input path (output path is `site` by default)
    - Notice:
        + The page dict should have 3 keys: `html`, `meta`, and `fname`
"""


import errno, codecs
from os import makedirs, remove, path, listdir, strerror
from abc import abstractmethod, ABCMeta

from jinja2 import Environment, FileSystemLoader, exceptions


class MetaSSG(metaclass=ABCMeta):
    """SSG base class"""
    _ofpath = 'site'
    _pymd_exts = []
    md_exts =  {'.markdown', '.mdown', '.mkdn', '.md', '.mkd', '.mdwn', '.mdtxt',
        '.mdtext', '.text', '.txt'}
    tmpl_types = {'layout', 'index', 'post', 'states', 'properties', 'misc'}

    @property
    @abstractmethod
    def tmplpath(self): pass

    @property
    @abstractmethod
    def ifpath(self): pass

    @property
    def ofpath(self):
        return self._ofpath

    @ofpath.setter
    def ofpath(self, val):
        self._ofpath = val

    @property
    def pymd_exts(self):
        return self._pymd_exts

    @pymd_exts.setter
    def pymd_exts(self, exts):
        prefix = 'markdown.extensions.{}'
        self._pymd_exts += list(map(lambda x: prefix.format(x), exts))

    def clean(self):
        """Clean all legacy generated pages"""
        if path.isdir(self.ofpath):
            for f in listdir(self.ofpath):
                if path.splitext(f)[1] in {'.html', '.htm'}:
                    try:
                        remove(path.join(self.ofpath, f))
                    except OSError as e: # no propagation
                        if e.errno != errno.ENOENT: # silent removal
                            print('warning: Unable to delete {}'.format(f))

    def load_templates(self, fpath):
        """\
            - Load templates using Jinja2 Environment
                + `fpath` should be directory
                + FileSystemLoader is specified
            - Template extensions should be only `.html`
            - Template names should be one of the following
                + layout, index, post, states, properties, misc
        """
        env = Environment(loader=FileSystemLoader(fpath))
        tmpls = {}

        for t in self.tmpl_types:
            try:
                tmpls[t] = env.get_template('{}.html'.format(t))
            except exceptions.TemplateNotFound as e:
                print('warning: no template named {}.html'.format(t))

        return tmpls

    def load_posts(self, fpath):
        """Load valid posts from source directory"""
        if path.exists(fpath):
            posts = []

            for f in [fpath] if path.isfile(fpath) else \
                list(map(lambda x: path.join(fpath, x), listdir(fpath))):
                if path.splitext(f)[1] in self.md_exts:
                    posts.append(f)

            if not posts:
                print('warning: Nothing to publish')
            return posts
        else:
            raise OSError(errno.ENOENT, strerror(errno.ENOENT), fpath)

    @abstractmethod
    def render(self, posts):
        """Render the posts (Jinja2 templates)"""
        pass

    def publish(self, pages, tmpls):
        """Publish rendered posts"""
        is_single = len(pages) == 1
        dest = lambda x: self.ofpath if is_single else path.join(self.ofpath, x)

        if not is_single:
            makedirs(self.ofpath, exist_ok=True)

        for p in pages:
            if all(k in p for k in {'html', 'meta', 'fname'}):
                with codecs.open(dest(p['fname']), 'w', encoding='utf-8',
                    errors='xmlcharrefreplace') as f:
                    f.write(tmpls.get(*p['meta']['type']).render(**p))
            else:
                raise TypeError('Invalid page dict')

    def send_static(self, fpath):
        """Send static assets to destination directory"""
        pass

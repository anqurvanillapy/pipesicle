# -*- coding: utf-8 -*-

import errno, codecs
from os import remove, path, listdir
from abc import abstractmethod, ABCMeta

from jinja2 import Environment, FileSystemLoader, exceptions


class MetaSSG(metaclass=ABCMeta):
    """SSG base class"""
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
    @abstractmethod
    def ofpath(self): pass

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
                print('warning: no template named {}'.format(t))

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
            raise OSError(errno.ENOENT)

    @abstractmethod
    def render(self, posts):
        """Render the posts (Jinja2 templates)"""
        pass

    def publish_page(self, page):
        """Publish single page"""
        # try:
        #     with codec.open(self.ofpath, encoding='utf-8',
        #         errors='xmlcharrefreplace', 'w') as f:
        #         f.write()
        # except Exception as e:
        #     raise e
        pass

    def publish_posts(self, posts):
        """Publish rendered posts"""
        # for p in posts:
        #     try:
                
        #     except Exception as e:
        #         raise e
        pass

    def publish_index(self, posts):
        """Publish index for rendered posts"""
        pass

    def publish_properties(self, posts):
        """Publish list of properties"""
        pass

    def publish_states(self, posts):
        """Publish list of states"""
        pass

    def send_static(self, fpath):
        """Send static assets to destination directory"""
        pass

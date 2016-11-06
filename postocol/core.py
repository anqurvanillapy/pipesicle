# -*- coding: utf-8 -*-
"""
    Postocol
    ========

    Posting Protocol: Abstract class for creating homemade static site generator
"""


import codecs, errno
from shutil import copytree, rmtree
from os import makedirs, remove, path, listdir, strerror
from abc import abstractmethod, ABCMeta

from jinja2 import Environment, FileSystemLoader, exceptions
from markdown import Markdown
from bs4 import BeautifulSoup
from pygments.formatters import HtmlFormatter


class Postocol(metaclass=ABCMeta):
    """SSG base class"""
    ifpath = 'content'
    ofpath = 'site'
    tmplpath = 'templates'
    staticpath = 'static'
    default_post_type = 'post'
    _pymd_exts = ['markdown.extensions.meta']
    _md_exts =  {'.markdown', '.mdown', '.mkdn', '.md', '.mkd', '.mdwn', '.mdtxt',
                '.mdtext', '.text', '.txt'}
    _tmpl_types = {'layout', 'index', 'post', 'states', 'properties', 'misc'}

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

    def load_templates(self, fpath=None):
        """\
            - Load templates using Jinja2 Environment
                + `fpath` should be directory
                + FileSystemLoader is specified
            - Template extensions should be only `.html`
            - Template names should be one of the following
                + layout, index, post, states, properties, misc
        """
        if fpath == None:
            fpath = self.tmplpath

        env = Environment(loader=FileSystemLoader(fpath))
        tmpls = {}

        for t in self._tmpl_types:
            try:
                tmpls[t] = env.get_template('{}.html'.format(t))
            except exceptions.TemplateNotFound as e:
                print('warning: No template named {}.html'.format(t))

        return tmpls

    def load_posts(self, fpath=None):
        """\
            - Load valid posts from source directory
            - Convert the text to extract the HTML data, metas and filenames
            - Returns a list of tuples that store the above information
        """
        if fpath == None:
            fpath = self.ifpath

        if path.exists(fpath):
            posts = []

            for f in [fpath] if path.isfile(fpath) \
                             else list(map(lambda x: path.join(fpath, x),
                                           listdir(fpath))):
                if path.splitext(f)[1] in self._md_exts:
                    with codecs.open(f, 'r', encoding='utf-8') as fh:
                        md = Markdown(extensions=self.pymd_exts)
                        html = BeautifulSoup(md.convert(fh.read()), 'lxml')

                        if html.html:
                            # Remove html and body tags
                            html.html.hidden = True
                            html.body.hidden = True
                            meta = md.Meta

                            if not meta.get('type'):
                                meta['type'] = [self.default_post_type]

                            posts.append((html, meta, f))

            if not posts:
                print('warning: Nothing to publish')
            return posts
        else:
            raise OSError(errno.ENOENT, strerror(errno.ENOENT), fpath)

    @abstractmethod
    def render(self, posts):
        """Render the posts (Jinja2 templates), shall be implemented"""
        pass

    def publish(self, pages, tmpls):
        """Publish rendered posts"""
        try:
            is_single = len(pages) == 1 and 'index' in pages[0]['meta']['type']
        except KeyError as e:
            raise e

        if not is_single: makedirs(self.ofpath, exist_ok=True)
        dest = lambda x: self.ofpath if is_single else path.join(self.ofpath, x)

        for p in pages:
            if all(k in p for k in {'content', 'meta', 'fname'}):
                with codecs.open(dest(p['fname']), 'w', encoding='utf-8',
                                 errors='xmlcharrefreplace') as f:
                    f.write(tmpls.get(*p['meta']['type']).render(**p))
            else:
                raise KeyError('Invalid page dict to publish')

    def send_static(self, dest):
        """Send static assets directory to dest directory"""
        try:
            if path.exists(dest): rmtree(dest)
            copytree(self.staticpath, dest)
        except Exception as e:
            raise e

    def create_page_dict(self, content, tmpl_type):
        """\
            Create page dictionary manually, especially for `index`, `states` or
            `properties`.
        """
        if tmpl_type in self._tmpl_types:
            return {'content': content,
                    'meta': {'type': [tmpl_type]},
                    'fname': '{}.html'.format(tmpl_type)}
        else:
            raise TypeError('Invalid manual page dict')

    def send_codehilite_style(self, theme='default', dest=None):
        """Send Pygments stylesheet to dest directory"""
        if dest == None:
            dest = self.staticpath

        hl = HtmlFormatter(style=theme).get_style_defs('.codehilite')
        fname = path.join(dest, 'codehilite.css')

        with open(fname, 'w') as f:
            f.write(hl)

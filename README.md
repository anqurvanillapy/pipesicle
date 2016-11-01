postocol
========

**Posting Protocol**, SSG (Static site generator) abstract class for extensible
use. Only supported Python 3.5+, for the compatibility of 3.4, 2.7 or other
versions not tested and guaranteed.

Requirements
------------

- [Jinja2](http://jinja.pocoo.org/) `>=2.8`

- Additional (for creating a page generator):
    + [Markdown](https://pythonhosted.org/Markdown/) `>=2.6.7`
    + [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) `>=4.5.1`

Installation
------------

Not on PyPI yet. Please clone and manually run the setup script.

```bash
$ git clone git@github.com:anqurvanillapy/postocol.git
$ cd postocol
$ python3 setup.py install # or use `-r` to specify requirements
```

API Reference
-------------

### Properties

#### `ifpath`

|Type|Default|
|:-:|:-:|
|`str`|`'content'`|

Input file/directory.

#### `ofpath`

|Type|Default|
|:-:|:-:|
|`str`|`'site'`|

Output file/directory.

#### `tmplpath`

|Type|Default|
|:-:|:-:|
|`str`|`'templates'`|

Template directory, mainly used by `jinja2.Environment` with the loader
`jinja2.FileSystemLoader` for better flexibility.

#### `staticpath`

|Type|Default|
|:-:|:-:|
|`str`|`'static'`|

Static assets directory.

#### `pymd_exts`

|Type|Default|
|:-:|:-:|
|`list`|`['markdown.extensions.meta']`|

List of needed
[python-markdown extensions](https://pythonhosted.org/Markdown/extensions/index.html),
where the "Name" suffixes should be given and will be completed, e.g. pass a
`['extra']` and it will be extended to `['markdown.extensions.extra']` in the
background.

### `Postocol.clean()`

|Argument|Return|
|:-:|:-:|
|Void|Void|

Clean all the files with extensions `.html` or `.htm` in the directory `ofpath`,
and it will not remove anything if `ofpath` is a file.

### `Postocol.load_templates(fpath=None)`

|`fpath` Type|Return Type|
|:-:|:-:|
|`str`, `'self.tmplpath'` if not given|`dict`|

Load all [valid templates](#implementation-workflow) from `fpath`, and return a
dict with the valid template types as keys, and the Jinja2 template paths as
values. **Attention, the template file extension should only be `.html`.**

### `Postocol.load_posts(fpath=None)`

|`fpath` Type|Return Type|
|:-:|:-:|
|`str`, `'self.ifpath'` if not given|`list`|

Load all valid Markdown posts from `fpath`, and return a list of their paths.
These extensions are only readable for this method: `.markdown`, `.mdown`,
`.mkdn`, `.md`, `.mkd`, `.mdwn`, `.mdtxt`, `.mdtext`, `.text` and `.txt`.

### `Postocol.render(posts)` (**abstract**)

|`posts` Type|Return Type|
|:-:|:-:|
|`list`|`list`|

Abstract method for rendering the loaded Markdown posts. You can use
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and
[python-markdown](https://pythonhosted.org/Markdown/) to implement the
rendering, but **most importantly, returned list of pages (a page is a dict)
should have at least 3 keys,** which are `content` (Markdown-generated stuff),
`meta` (metadata of a post) and `fname` (outpuf filename).

For example, a valid returned `pages` dict looks like this:

```python
pages = [{'content': '<p>Rendered paragraph</p>',
          'meta': {'title': ['Hello, Postocol!'],
                   'type': ['post']},
          'fname': 'foo.html'}]
```

### `Postocol.publish(pages, tmpls)`

|`pages` Type|`tmpls` Type|Return|
|:-:|:-:|:-:|
|`list`|`dict`|Void|

Render the templates `tmpls` with the generated HTML `pages`, and write them
to `ofpath`. If `ofpath` is a file, the `fname` value in a page dict will be
overridden, and the method brings out the file `ofpath`.

Implementation Workflow
-----------------------

- There are **3** document types that Postocol mainly serves, which are:
    + Single page (e.g. slideshow)
    + Blog
    + Wiki
- Therefore, Postocol will by default trace **6** types of templates as follows:
    + `index`, for blog or wiki, or even the slideshow (because it can be stored
    in one static HTML file, hence assuming that it is an index page)
    + `post`, for blog or wiki, e.g. an article
    + `states`, mainly for wiki, a list containing the current states of a post,
    e.g. *unfinished*, *not proofread*, *stub*, etc., similar to
    [Wikipedia:Tags](https://en.wikipedia.org/wiki/Wikipedia:Tags)
    + `properties`, for wiki or blog, a list of the properties of a post, e.g.
    *howto*, *daily*, *compsci*, *PoC*, etc., similarly the categories or tags
    + `misc`, something you want to provide independently, instead of listing in
    `index`, `states` or `properties`, e.g. *about*, *contact*, *resume*, etc.
    + `layout`, serving something above
- **Additionally**, `index`, `states` and `properties` could be automatically
generated from self-implemented `Postocol.render()` method.

### For single-page (slideshow) generator

There is no need to `clean()` anything and `send_static()` for a single-page
generator, so the workflow is simple. For instance, a slideshow generator might
act like this.

```
                    load_templates()     publish()
                          |                  |
                          v                  v
(slides.md) --+------- template ---+--> (index.html)
              |                    |
              +-- post ---> page --+
                   ^          ^
                   |          |
            load_posts()   render()
```

### For blog/wiki generator

Wiki uses the whole functionality to update all the posts, whereas the workflow
of a blog generator is similar:

```
(foo.md) --+
(bar.md) --+   clean(site/) load_templates() publish()  send_static()
           |         |            |              |             |
           v         v            v              v             v
       (content/) ---+----- templates ---+--> (site/) --+-> (site/static/)
                     |                   |              +-> (index.html)
                     +-- posts -> pages -+              +-> (states.html)
                          ^         ^                   +-> (properties.html)
                          |         |                   +-- (foo.html)
                   load_posts()  render()               +-- (bar.html)
```

Example
-------

### Starter

The project site hosted on
[gh-pages branch](https://github.com/anqurvanillapy/postocol/tree/gh-pages)
contains a minimalist webpage generator that ignores two unnecessary methods
`clean()` and `send_static()`, which can be your first sight under the hood.

> Off we go!

First, import everything we need to implement our own `render()` method, and
some built-in tools for coping with encoding/decoding and path manipulation.
In the meantime, create a class inheriting `Postocol` with some key constants.

```python
from postocol import Postocol

import codecs
from os.path import basename, splitext

from markdown import Markdown
from bs4 import BeautifulSoup


class Starter(Postocol):
    ifpath = 'preface.md'
    ofpath = 'index.html'
```

Second, we add a `run()` method for the control flow, which goes like

> Load templates from `templates` folder, and load `preface.md` to a list called
`posts`. Render the Markdown file and bring the `pages` out. Finally, publish it
to the file `index.html`, which is combined with our `templates` and `pages`.

```python
def run(self):
    self.tmpls = self.load_templates()
    self.posts = self.load_posts()
    self.pages = self.render(self.posts)
    self.publish(self.pages, self.tmpls)
```

Eventually, here comes the boss! Now implement the abstract method `render()` to
translate our Markdown page into HTML, collecting **3** kinds of the page
information: `content` (the generated HTML content), `meta` (title, type, date,
etc., right at the beginning of a Markdown post) and `fname` (filename). Notice
that `BeautifulSoup` brings the HTML with nodes like
`<html><body></body></html>`, which are not wanted in our content because later
it will be rendered into the templates. Since `lxml` will help us conveniently
eliminate those tags, we use it as the parser.

```python
def render(self, posts):
    pages = []
    # Tiny function to add `.html` extension
    chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

    for p in posts:
        with codecs.open(p, 'r', encoding='utf-8') as f:
            # Create an instance with loading the extensions, because we need
            # `meta` of the post, which won't be parsed by default.
            md = Markdown(extensions=self.pymd_exts)
            html = BeautifulSoup(md.convert(f.read()), 'lxml')
            # Remove `html` and `body` tags
            html.html.hidden = True
            html.body.hidden = True
            # Attention, `meta` is quite like a `defaultdict(list)` that all
            # metadata are stored in the list as `meta`'s value, even its length
            # is just 1. E.g. {'title': ['Foo'], 'date': ['Nov 1, 2016']}.
            meta = md.Meta
            pages.append({'content': html,
                          'meta': meta,
                          'fname': chfn(p)})

    return pages
```

What is inside the `preface.md` and the index template are not gonna be
displayed right here. Check out the
[branch](https://github.com/anqurvanillapy/postocol/tree/gh-pages) and run it to
see what kinds of magic will just happen!

### Main Course

See [examples](https://github.com/anqurvanillapy/postocol/tree/master/examples)
directory that offers a fully implemented **wiki** generator demo, which may
help you fast-prototyping your own generator.

Test
----

Postocol doesn't use any third-party testing libraries, for the built-in
`unittest` is decent for testing its basic functionality, which is able to be
used from the command line.

```bash
$ python3 -m unittest # use `-v` to show verbose of the test suite
```

License
-------

MIT
